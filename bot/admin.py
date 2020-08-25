from django.contrib import admin
from .models import Textupload, Inquiry

#admin.site.register(Imageupload)
#admin.site.register(Keyword)

@admin.register(Textupload)
class TextuploadAdmin(admin.ModelAdmin):
    list_display = ('pk', 'company', 'product', 'date_of_upload', 'usertext', 'result')
    #ordering = ['-date_of_upload']

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'date_of_inquiry', 'usertext', 'message', 'company', 'product', 'contact', 'phone', 'fax')
