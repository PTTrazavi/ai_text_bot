from django.contrib import admin
from .models import Textupload

#admin.site.register(Imageupload)
#admin.site.register(Keyword)

@admin.register(Textupload)
class TextuploadAdmin(admin.ModelAdmin):
    list_display = ('date_of_upload', 'usertext', 'result')
