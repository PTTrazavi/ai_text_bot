from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class UploadtextForm(forms.Form):
    usertext = forms.CharField(label="", label_suffix="", initial="",
                                strip=True, min_length=1,
                                widget=forms.Textarea(attrs={'class':'form-control transparent','rows':8, 'cols':10}))

    def clean_image(self):
        data = self.cleaned_data['usertext']
        # Check if there is no data.
        if len(data) < 1 :
            raise ValidationError(_("Keyword can't be empty!"))

        # Remember to always return the cleaned data.
        return data
