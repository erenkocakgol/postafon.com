from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from home.models import Setting, Menu, ContactFormu, ContactFormMessage, FAQ
from home.forms import CaptchaForm, ContactFormu
import configparser
import requests
import json
import os
from pathlib import Path
from home.data import read_from_db

BASE_DIR = Path(__file__).resolve().parent.parent

config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, "KEYS.CONFIG"))

RECAPTCHA_PUBLIC_KEY = config.get('DJANGO', 'RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = config.get('DJANGO', 'RECAPTCHA_PRIVATE_KEY')

def index(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "Giriş yaptınız. Hoş geldiniz.")
                return HttpResponseRedirect(reverse('index'))
            else:
                messages.warning(request, "Kullanıcı adı veya şifre yanlış. Lütfen tekrar deneyin.")
        
        elif 'register' in request.POST:
            reg_username = request.POST['reg_username']
            reg_email = request.POST['reg_email']
            reg_password = request.POST['reg_password']
            reg_password_again = request.POST['reg_password_again']
            if reg_password != reg_password_again:
                messages.warning(request, "Şifreler eşleşmiyor.")
            else:
                recaptcha_response = request.POST.get('g-recaptcha-response')
                recaptcha_secret_key = RECAPTCHA_PRIVATE_KEY
                recaptcha_public_key = RECAPTCHA_PUBLIC_KEY
                recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'
                payload = {'sitekey': recaptcha_public_key, 'secret': recaptcha_secret_key, 'response': recaptcha_response}
                response = requests.post(recaptcha_url, data=payload)
                result = json.loads(response.content)
                is_registered1 = User.objects.filter(username=reg_username).exists()
                is_registered2 = User.objects.filter(email=reg_email).exists()
                
                if result['success'] and not is_registered1 and not is_registered2:
                    user = User.objects.create_user(username=reg_username, email=reg_email, password=reg_password)
                    login(request, user)
                    messages.success(request, 'Kayıt başarılı! Hoş geldiniz.')
                    return HttpResponseRedirect(reverse('index'))
                elif is_registered1 or is_registered2:
                    messages.error(request, 'Kullanıcı adı veya e-posta zaten kayıtlı.')
                else:
                    messages.error(request, 'reCAPTCHA doğrulaması başarısız oldu.')
    all_news = read_from_db()
    setting = Setting.objects.first()
    menu = Menu.objects.filter(status="True")
    context = {
        'menu': menu,
        'setting': setting,
        'page': 'home',
        'captcha': CaptchaForm(),
        'articles': all_news,
    }
    return render(request, 'index.html', context)

def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def faqs(request):
    menu = Menu.objects.filter(status="True")
    faqs = FAQ.objects.filter(status="True").order_by('ordernumber')
    context = {
        'menu': menu,
        'page': 'faqs',
        'pagename': 'Sıkça Sorulan Sorular',
        'faqs': faqs
    }
    return render(request, 'faqs.html', context)

