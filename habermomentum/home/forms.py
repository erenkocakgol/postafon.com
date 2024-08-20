from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from home.models import ContactFormMessage
from pathlib import Path
import configparser
import os

BASE_DIR = Path(__file__).resolve().parent.parent

config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, "KEYS.CONFIG"))

RECAPTCHA_PUBLIC_KEY = config.get('DJANGO', 'RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = config.get('DJANGO', 'RECAPTCHA_PRIVATE_KEY')

class SearchForm(forms.Form):
    query = forms.CharField(
        label='Search',
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Search...'})
    )
    menuid = forms.IntegerField(
        label='Searchsel',
        widget=forms.HiddenInput()
    )

class CaptchaForm(forms.Form):
    captcha = ReCaptchaField(public_key=RECAPTCHA_PUBLIC_KEY, private_key=RECAPTCHA_PRIVATE_KEY)

class ContactFormu(forms.ModelForm):
    class Meta:
        model = ContactFormMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adınız', 'required': 'required'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Konu', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Adresiniz', 'required': 'required'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Mesaj', 'required': 'required'}),
        }
