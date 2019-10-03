from django.db import models
#from django.core.files import File
#import os

class Textupload(models.Model):
    usertext = models.TextField()
    result = models.CharField(max_length=8)
    date_of_upload = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.usertext
