from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    ImageMessage,
    ImageSendMessage,
)
import os
import time, datetime
from .util import texttool
from django.views.generic import ListView
#parameter for global count
count = 0

YOUR_CHANNEL_ACCESS_TOKEN = settings.LINE_CHANNEL_ACCESS_TOKEN
YOUR_CHANNEL_SECRET = settings.LINE_CHANNEL_SECRET

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    signature = request.META["HTTP_X_LINE_SIGNATURE"]
    body = request.body.decode('utf-8')
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        HttpResponseForbidden()
    return HttpResponse('OK', status=200)

# オウム返し
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))

# upload text
from .models import Textupload
from .forms import UploadtextForm
def textvalidation(request):
    if request.method == 'POST':
        form = UploadtextForm(request.POST) #remember to add request.FILES!
        # Check if the form is valid:
        if form.is_valid():
            text_by_user = form.cleaned_data['usertext']
            date_of_upload = str(datetime.datetime.today())
            #process the text to judge is it is legal
            result = texttool(text_by_user)
            txt = Textupload(usertext=text_by_user, result=result, date_of_upload = date_of_upload)
            txt.save()

            content = {
                'form': form,
                'original': txt.usertext,
                'result': txt.result,
            }
            return render(request, 'bot/textvalidation.html', content)
    # If this is a GET (or any other method) create the default form.
    else:
        form = UploadtextForm()
    # default or not valid comes here
    content = {
        'form': form,
    }
    return render(request, 'bot/textvalidation.html',content)
