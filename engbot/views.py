from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (
    TextSendMessage,
)
import os
import time, datetime
from .util import texttool, jieba_validation, trans
from django.views.generic import ListView
#LINE setting
YOUR_CHANNEL_ACCESS_TOKEN = settings.LINE_CHANNEL_ACCESS_TOKEN
YOUR_CHANNEL_SECRET = settings.LINE_CHANNEL_SECRET

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# upload text
from .models import Textuploadeng
from .forms import UploadtextForm
def textvalidationEng(request):
    form = UploadtextForm()
    content = {
        'form': form,
    }
    return render(request, 'engbot/textvalidationEng.html',content)

#validation result
def resultEng(request):
    if request.method == 'POST':
        form = UploadtextForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            text_by_user = form.cleaned_data['usertext']
            date_of_upload = str(datetime.datetime.today())
            #process the text to judge if it is legal
            #result = texttool(text_by_user)
            text_by_user_eng = text_by_user
            text_by_user = trans(text_by_user) # become chinese
            result, rate, keywords = jieba_validation(text_by_user)
            #add red keywords
            #text_by_user_nc = text_by_user
            #r_b = '<span style="color:red;">'
            #r_a = '</span>'
            #for word in keywords:
            #    text_by_user = text_by_user.replace(word, r_b + word + r_a)

            txt = Textuploadeng(usertext=text_by_user, usertext_eng=text_by_user_eng, result=str(result), date_of_upload = date_of_upload)
            txt.save()

            content = {
                'original': txt.usertext_eng,
                'result': txt.result,
                'rate': round(rate * 100, 2),
                'original_nc': text_by_user_eng,
                'keywords': str(keywords).replace("'","").replace(" ",""), #temp string for keywords
            }
            return render(request, 'engbot/resultEng.html', content)

#validation result
from .models import Inquiryeng
from .forms import InquiryForm
from django.utils.safestring import SafeString
def inquiryEng(request):
    if request.method == 'POST':
        result = request.POST.get('result')
        keywords = request.POST.get('keywords')

        form = InquiryForm(initial={'usertext':result, 'keywords': keywords})

        content = {
            'form': form,
        }
        return render(request, 'engbot/inquiryEng.html', content)

#line
def lineEng(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            company = form.cleaned_data['company']
            contact = form.cleaned_data['contact']
            phone = form.cleaned_data['phone']
            fax= form.cleaned_data['fax']
            usertext = form.cleaned_data['usertext']
            message = form.cleaned_data['message']

            #red words process
            usertext_nc = usertext
            keywords = form.cleaned_data['keywords']
            #keywords = keywords[1:-1].split(',')
            #r_b = '<span style="color:red;">'
            #r_a = '</span>'
            #for word in keywords:
            #    usertext = usertext.replace(word, r_b + word + r_a)
            #red words process end here

            date_of_inquiry = str(datetime.datetime.today())

            inquiry = Inquiryeng(company = company, contact = contact, phone = phone,
                                fax = fax, usertext = usertext, message = message,
                                date_of_inquiry = date_of_inquiry)
            inquiry.save()
            #make message to send by LINE
            LINE = str(contact + " of " + company + " has asked a question.\n\nContent:" + usertext_nc + "\n\nMessage:" + message)
            line_bot_api.broadcast([TextSendMessage(text=LINE)])

        return render(request, 'engbot/lineEng.html')

#pdf generator
from .util import render_to_pdf
def pdfEng(request):
    original = request.POST.get('original')
    result = request.POST.get('result')
    rate = request.POST.get('rate')
    keywords = request.POST.get('keywords')
    #split original
    original = [original[i:i+80] for i in range(0,len(original), 80)]
    #red words process

    if len(keywords) > 2:
        keywords = keywords[1:-1].split(',')
        r_b = '<span style="color:red;">'
        r_a = '</span>'
        for word in keywords:
            for key, value in enumerate(original):
                original[key] = value.replace(word, r_b + word + r_a)

    data = {
        'today': datetime.date.today(),
        'original': original,
        'result': result,
        'rate': rate,
    }
    pdf = render_to_pdf('engbot/pdfEng.html', data)
    return HttpResponse(pdf, content_type='application/pdf')

#####backend site views from here #####
#all_list
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

class textupload_listEng(LoginRequiredMixin, generic.ListView):
    model = Textuploadeng
    paginate_by = 10
    ordering='-date_of_upload'
    template_name = 'engbot/textupload_listEng.html'

#all_detail
class textupload_detailEng(LoginRequiredMixin, generic.DetailView):
    model = Textuploadeng
    template_name = 'engbot/textupload_detailEng.html'

#inquiry_list
class inquiry_listEng(LoginRequiredMixin, generic.ListView):
    model = Inquiryeng
    paginate_by = 10
    ordering='-date_of_inquiry'
    template_name = 'engbot/inquiry_listEng.html'

#inquiry_detail
class inquiry_detailEng(LoginRequiredMixin, generic.DetailView):
    model = Inquiryeng
    template_name = 'engbot/inquiry_detailEng.html'
