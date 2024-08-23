from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from home.models import Setting, Menu, ContactFormu, ContactFormMessage, FAQ
from home.forms import CaptchaForm, ContactFormu
from user.models import Post, Channel
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
    if request.path == "login/":
        messages.warning(request, "Lütfen önce giriş yapınız.")
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
    
    admin_user = User.objects.get(username='admin')

    #Post.objects.filter(author=admin_user).delete()
    
    for news in all_news:
        admin_channel = Channel.objects.first()

        # news[7] değerini almak
        author_username = news[7]

        # Kullanıcıyı seçmek
        if author_username == "Sistem Akışı":
            author = admin_user
            channel = admin_channel
        else:
            try:
                author = User.objects.get(username=author_username)
            except User.DoesNotExist:
                # Eğer kullanıcı bulunamazsa, bir varsayılan kullanıcı belirleyebilir veya hatayı yönetebilirsiniz
                author = admin_user
            try:
                # Burada kanalın uygun bir özelliğini kullanmanız gerekebilir
                channel = Channel.objects.get(owner=author)
            except Channel.DoesNotExist:
                channel = admin_channel
        
        # Önce Post nesnesini arayın
        post = Post.objects.filter(title=news[2]).first()

        if post:
            # Eğer Post nesnesi varsa, alanları güncelleyin
            post.kategori = news[1]
            post.content = news[3]
            post.image = news[4]
            post.keywords = news[5]
            post.pp_img = news[6]
            post.author = author
            post.channel = channel
            post.date = news[10]
            post.status = "published"
            post.save()
        else:
            # Eğer Post nesnesi yoksa, yenisini oluşturun
            post = Post.objects.create(
                kategori=news[1],
                title=news[2],
                content=news[3],
                image=news[4],
                keywords=news[5],
                pp_img=news[6],
                author=author,
                channel=channel,
                date=news[10],
                status="published",
            )

        # `likes` ve `reposts` kullanıcılarını eklemek
        # Burada `liked_users_list` ve `reposted_users_list` örneğin user username listeleri olmalı
        if isinstance(news[7], list):
            # Eğer `news[7]` ve `news[8]` listeler ise, topluca kullanıcı ekle
            for username in news[7]:
                try:
                    user = User.objects.get(username=username)
                    post.likes.add(user)
                except User.DoesNotExist:
                    pass  # Kullanıcı bulunamazsa, bu durumda yapılacak işlem
        else:
            # Tekil kullanıcı eklemek için (Eğer bir liste değilse)
            try:
                user = User.objects.get(username=news[7])
                post.likes.add(user)
            except User.DoesNotExist:
                pass  # Kullanıcı bulunamazsa, bu durumda yapılacak işlem

        if isinstance(news[8], list):
            # Eğer `news[8]` bir liste ise, topluca kullanıcı ekle
            for username in news[8]:
                try:
                    user = User.objects.get(username=username)
                    post.reposts.add(user)
                except User.DoesNotExist:
                    pass  # Kullanıcı bulunamazsa, bu durumda yapılacak işlem
        else:
            # Tekil kullanıcı eklemek için (Eğer bir liste değilse)
            try:
                user = User.objects.get(username=news[8])
                post.reposts.add(user)
            except User.DoesNotExist:
                pass  # Kullanıcı bulunamazsa, bu durumda yapılacak işlem

        # `Post` nesnesini kaydet
        post.save()

    
    
    setting = Setting.objects.first()
    menu = Menu.objects.filter(status="True")
    post = Post.objects.all()
    context = {
        'menu': menu,
        'setting': setting,
        'page': 'home',
        'captcha': CaptchaForm(),
        'articles': all_news,
        'post': post,
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

