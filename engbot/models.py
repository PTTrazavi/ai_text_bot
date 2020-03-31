from django.db import models
from django.urls import reverse
#from django.core.files import File
#import os

class Textuploadeng(models.Model):
    usertext = models.TextField()
    usertext_eng = models.TextField()
    result = models.CharField(max_length=8)
    date_of_upload = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.usertext

    def get_absolute_url(self):
        return reverse('textupload_detailEng', args=[str(self.id)])

class Inquiryeng(models.Model):
    company = models.CharField(max_length=64)
    contact = models.CharField(max_length=16)
    phone = models.CharField(max_length=16)
    fax = models.CharField(max_length=16)
    usertext = models.TextField()
    message = models.TextField()
    date_of_inquiry = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.usertext

    def get_absolute_url(self):
        return reverse('inquiry_detailEng', args=[str(self.id)])
