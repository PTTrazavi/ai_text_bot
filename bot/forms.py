from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class UploadtextForm(forms.Form):
    usertext = forms.CharField(label="", label_suffix="", initial="",
                                strip=True, min_length=1,
                                widget=forms.Textarea(attrs={'class':'form-control transparent','rows':12, 'cols':14}))

    def clean_usertext(self):
        data = self.cleaned_data['usertext']
        # Check if there is no data.
        if len(data) < 1 :
            raise ValidationError(_("Keyword can't be empty!"))

        # Remember to always return the cleaned data.
        return data

class InquiryForm(forms.Form):
    company = forms.CharField(label="公司名稱", label_suffix="：", initial="",
                                strip=True, min_length=1,
                                widget=forms.Textarea(attrs={'class':'form-control transparent','rows':1, 'cols':8}))
    contact = forms.CharField(label="聯絡人", label_suffix="：", initial="",
                                strip=True, min_length=1,
                                widget=forms.Textarea(attrs={'class':'form-control transparent','rows':1, 'cols':8}))
    phone = forms.CharField(label="電話", label_suffix="：", initial="",
                                strip=True, min_length=1,
                                widget=forms.Textarea(attrs={'class':'form-control transparent','rows':1, 'cols':8}))
    fax = forms.CharField(label="傳真", label_suffix="：", initial="",
                                strip=True, min_length=1,
                                widget=forms.Textarea(attrs={'class':'form-control transparent','rows':1, 'cols':8}))
    usertext = forms.CharField(label="辨識結果", label_suffix="：", initial="",
                                strip=True, min_length=1,
                                widget=forms.Textarea(attrs={'class':'form-control transparent','rows':6, 'cols':10}))
    message = forms.CharField(label="訊息內容", label_suffix="：", initial="",
                                strip=True, min_length=1,
                                widget=forms.Textarea(attrs={'class':'form-control transparent','rows':6, 'cols':10}))

    def clean_company(self):
        data = self.cleaned_data['company']
        return data
    def clean_contact(self):
        data = self.cleaned_data['contact']
        return data
    def clean_phone(self):
        data = self.cleaned_data['phone']
        return data
    def clean_fax(self):
        data = self.cleaned_data['fax']
        return data
    def clean_usertext(self):
        data = self.cleaned_data['usertext']
        return data
    def clean_message(self):
        data = self.cleaned_data['message']
        return data
