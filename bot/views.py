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
from .util import texttool, jieba_validation
from django.views.generic import ListView
#LINE setting
YOUR_CHANNEL_ACCESS_TOKEN = settings.LINE_CHANNEL_ACCESS_TOKEN
YOUR_CHANNEL_SECRET = settings.LINE_CHANNEL_SECRET

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# upload text
from .models import Textupload
from .forms import UploadtextForm
def textvalidation(request):
    form = UploadtextForm()
    content = {
        'form': form,
    }
    return render(request, 'bot/textvalidation.html',content)

#validation result
def result(request):
    if request.method == 'POST':
        form = UploadtextForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            text_by_user = form.cleaned_data['usertext']
            date_of_upload = str(datetime.datetime.today())
            #process the text to judge if it is legal
            #result = texttool(text_by_user)
            result = jieba_validation(text_by_user)
            txt = Textupload(usertext=text_by_user, result=str(result), date_of_upload = date_of_upload)
            txt.save()

            content = {
                'original': txt.usertext,
                'result': txt.result,
                'rate': '80',
            }
            return render(request, 'bot/result.html', content)

#validation result
from .models import Inquiry
from .forms import InquiryForm
def inquiry(request):
    if request.method == 'POST':
        result = request.POST.get('result')
        form = InquiryForm(initial={'usertext':result})

        content = {
            'form': form,
        }
        return render(request, 'bot/inquiry.html', content)

#line
def line(request):
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

            date_of_inquiry = str(datetime.datetime.today())

            inquiry = Inquiry(company = company, contact = contact, phone = phone,
                                fax = fax, usertext = usertext, message = message,
                                date_of_inquiry = date_of_inquiry)
            inquiry.save()
            #make message to send by LINE
            LINE = str(company + "的" + contact + "在網站上詢問了問題。內容：" + usertext + " 訊息：" + message)
            line_bot_api.broadcast([TextSendMessage(text=LINE)])

        return render(request, 'bot/line.html')

#####backend site views from here #####
#all_list
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

class textupload_list(LoginRequiredMixin, generic.ListView):
    model = Textupload
    paginate_by = 10
    ordering='-date_of_upload'

#all_detail
class textupload_detail(LoginRequiredMixin, generic.DetailView):
    model = Textupload

#inquiry_list
class inquiry_list(LoginRequiredMixin, generic.ListView):
    model = Inquiry
    paginate_by = 10
    ordering='-date_of_inquiry'

#inquiry_detail
class inquiry_detail(LoginRequiredMixin, generic.DetailView):
    model = Inquiry
