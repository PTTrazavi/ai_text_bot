from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
import csv

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
@login_required
def textvalidation(request):
    form = UploadtextForm()
    content = {
        'form': form,
    }
    return render(request, 'bot/textvalidation.html',content)

#validation result
@login_required
def result(request):
    if request.method == 'POST':
        form = UploadtextForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            text_by_user = form.cleaned_data['usertext']
            company_name = form.cleaned_data['company']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            product_name = form.cleaned_data['product']
            date_of_upload = str(datetime.datetime.today())
            #process the text to judge if it is legal
            #result = texttool(text_by_user)
            result, rate, keywords = jieba_validation(text_by_user)
            #add red keywords
            text_by_user_nc = text_by_user
            r_b = '<span style="color:red;">'
            r_a = '</span>'
            for word in keywords:
                text_by_user = text_by_user.replace(word, r_b + word + r_a)

            txt = Textupload(company=str(company_name), email=str(email), phone=str(phone),
                            product=str(product_name), usertext=text_by_user, result=str(result),
                            date_of_upload = date_of_upload)
            txt.save()

            content = {
                'company': txt.company,
                'product': txt.product,
                'original': txt.usertext,
                'result': txt.result,
                'rate': round(rate * 100, 2),
                'original_nc': text_by_user_nc,
                'keywords': str(keywords).replace("'","").replace(" ",""), #temp string for keywords
            }
            return render(request, 'bot/result.html', content)

#inquiry
from .models import Inquiry
from .forms import InquiryForm
from django.utils.safestring import SafeString
@login_required
def inquiry(request):
    if request.method == 'POST':
        company = request.POST.get('company')
        product = request.POST.get('product')
        original = request.POST.get('original')
        result = request.POST.get('result')
        keywords = request.POST.get('keywords')

        form = InquiryForm(initial={'company':company, 'product':product,
                        'usertext':original, 'keywords': keywords})

        #add red keywords
        original_c = original
        if len(keywords) > 2:
            keywords = keywords[1:-1].split(',')
        r_b = '<span style="color:red;">'
        r_a = '</span>'
        for word in keywords:
            original_c = original_c.replace(word, r_b + word + r_a)

        content = {
            'form': form,
            'result': result,
            'original_c': original_c
        }
        return render(request, 'bot/inquiry.html', content)

#line
@login_required
def line(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            company = form.cleaned_data['company']
            product = form.cleaned_data['product']
            contact = form.cleaned_data['contact']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            fax= form.cleaned_data['fax']
            usertext = form.cleaned_data['usertext']
            message = form.cleaned_data['message']

            #red words process
            usertext_nc = usertext
            keywords = form.cleaned_data['keywords']
            if len(keywords) > 2:
                keywords = keywords[1:-1].split(',')
                r_b = '<span style="color:red;">'
                r_a = '</span>'
                for word in keywords:
                    usertext = usertext.replace(word, r_b + word + r_a)
            #red words process end here

            date_of_inquiry = str(datetime.datetime.today())

            inquiry = Inquiry(company = company, product = product, contact = contact, email = email,
                                phone = phone, fax = fax, usertext = usertext, message = message,
                                date_of_inquiry = date_of_inquiry)
            inquiry.save()
            #make message to send by LINE
            LINE = str(company + "的" + contact + "在網站上詢問了問題。\n\n內容：" + usertext_nc + "\n\n訊息：" + message)
            line_bot_api.broadcast([TextSendMessage(text=LINE)])

        return render(request, 'bot/line.html')

#pdf generator
from .util import render_to_pdf
@login_required
def pdf(request):
    company = request.POST.get('company')
    product = request.POST.get('product')
    original = request.POST.get('original')
    result = request.POST.get('result')
    rate = request.POST.get('rate')
    keywords = request.POST.get('keywords')
    #split original
    original = [original[i:i+40] for i in range(0,len(original), 40)]
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
        'company': company,
        'product': product,
        'original': original,
        'result': result,
        'rate': rate,
    }
    pdf = render_to_pdf('bot/pdf.html', data)
    return HttpResponse(pdf, content_type='application/pdf')

#download Textupload csv
@login_required
@permission_required('bot.can_check_backend')
def textupload_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="textupload.csv"'

    writer = csv.writer(response)
    # writer.writerow("\xEF\xBB\xBF") #prevent from messed up chinese
    writer.writerow(['公司', 'email', '電話', '產品', '廣告內容', '判斷結果', '日期'])
    # for row in Textupload.objects.all().values_list('company', 'email', 'phone', 'product', 'usertext', 'result', 'date_of_upload'):
    for row in Textupload.objects.all():
        row_item = [row.company, row.email, row.phone, row.product, row.usertext, "合格" if row.result=="0" else "違規", row.date_of_upload]
        writer.writerow(row_item)

    return response

#download Inquiry csv
@login_required
@permission_required('bot.can_check_backend')
def inquiry_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="inquiry.csv"'

    writer = csv.writer(response)
    writer.writerow(['公司', '產品', '聯絡人', 'email', '電話', '傳真', '廣告內容', '訊息', '日期'])
    for row in Inquiry.objects.all().values_list('company', 'product', 'contact', 'email', 'phone', 'fax', 'usertext', 'message', 'date_of_inquiry'):
        writer.writerow(row)

    return response


#####backend site views from here #####
#all_list
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class textupload_list(PermissionRequiredMixin, generic.ListView):
    permission_required = 'bot.can_check_backend'
    model = Textupload
    paginate_by = 10
    ordering='-date_of_upload'

#all_detail
class textupload_detail(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'bot.can_check_backend'
    model = Textupload

#inquiry_list
class inquiry_list(PermissionRequiredMixin, generic.ListView):
    permission_required = 'bot.can_check_backend'
    model = Inquiry
    paginate_by = 10
    ordering='-date_of_inquiry'

#inquiry_detail
class inquiry_detail(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'bot.can_check_backend'
    model = Inquiry
