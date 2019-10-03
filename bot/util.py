import sys
from .models import Textupload
#add frame to the image
def texttool(text_by_user):
    if len(text_by_user) > 10:
        result = "ok"
    else:
        result = "no"
    return result
