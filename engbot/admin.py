from django.contrib import admin
from .models import Textuploadeng, Inquiryeng

#admin.site.register(Imageupload)
#admin.site.register(Keyword)

@admin.register(Textuploadeng)
class TextuploadengAdmin(admin.ModelAdmin):
    list_display = ('pk', 'date_of_upload', 'usertext', 'usertext_eng', 'result')
    #ordering = ['-date_of_upload']

@admin.register(Inquiryeng)
class InquiryengAdmin(admin.ModelAdmin):
    list_display = ('pk', 'date_of_inquiry', 'usertext', 'message', 'company', 'contact', 'phone', 'fax')
