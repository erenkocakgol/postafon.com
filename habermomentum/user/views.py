from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from user.models import UserProfile, UserProfileForm, Profile, Post, Channel, ChannelRole
from home.models import Setting, Menu
from django.contrib.auth.models import User
from django.forms import ModelForm
from home.forms import CaptchaForm, ContactFormu
from django.views.decorators.http import require_POST



# Kullanıcı profilini görüntüleme ve güncelleme
@login_required(login_url='/login')
def index(request):
    menu = Menu.objects.filter(status="True")
    menusearch = Menu.objects.all()
    setting = Setting.objects.first()

    # Kullanıcının profilini al veya oluştur
    try:
        user_profile, created = UserProfile.objects.update_or_create(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None
        messages.warning(request, "Kullanıcı profili bulunamadı.")
    
    context = { 
        'menu': menu,
        'setting': setting,
        'captcha': CaptchaForm(),
        'menusearch': menusearch,
        'page': 'user',
        'pagename': 'Kullanıcı Bilgileri',
        'profile': user_profile
    }
    return render(request, "user_pages/user_profile.html", context)


@login_required(login_url='/login')
def updateuserprofile(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil Bilgileriniz başarı ile güncellenmiştir.")
            return HttpResponseRedirect(url)
        else:
            messages.warning(request, "Profil Bilgilerinizi güncellerken bir sorun oluştu.")
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    
    context = {'form': form}
    return render(request, 'user_pages/user_profile_update.html', context)


@login_required(login_url='/login')
def updateuserpassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Şifreniz değiştirilmiştir.')
            return redirect('/user')
        else:
            messages.warning(request, 'Lütfen hataları düzelterek, tekrar deneyiniz.<br>' + str(form.errors))
            return redirect('/user/updateuserpassword')
    else:
        menu = Menu.objects.filter(status="True")
        menusearch = Menu.objects.all()
        setting = Setting.objects.first()
        
        form = PasswordChangeForm(request.user)
        
        context = { 
            'menu': menu,
            'setting': setting,
            'captcha': CaptchaForm(),
            'menusearch': menusearch,
            'page': 'user',
            'form': form,
            'pagename': 'Kullanıcı Bilgileri'
        }
        
        return render(request, 'user_pages/updateuserpassword.html', context)


# Gönderi oluşturma ve listeleme
@login_required(login_url='/login')
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        channel_id = request.POST.get('channel')
        image = request.FILES.get('image')
        channel = get_object_or_404(Channel, id=channel_id)

        post = Post.objects.create(
            title=title,
            content=content,
            author=request.user,
            channel=channel,
            image=image
        )
        messages.success(request, 'Gönderiniz başarıyla oluşturuldu.')
        return redirect('index')

    channels = Channel.objects.filter(members=request.user)
    return render(request, 'user_pages/create_post.html', {'channels': channels})


@login_required(login_url='/login')
def list_posts(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'user_pages/list_posts.html', {'posts': posts})


# Kanal oluşturma
@login_required(login_url='/login')
def create_channel(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        channel = Channel.objects.create(name=name, owner=request.user)
        channel.members.add(request.user)
        messages.success(request, 'Kanal başarıyla oluşturuldu.')
        return redirect('index')
    return render(request, 'user_pages/create_channel.html')


# Kanal detayları ve yönetimi
@login_required(login_url='/login')
def channel_detail(request, channel_id):
    channel = get_object_or_404(Channel, id=channel_id)
    if request.user in channel.members.all():
        return render(request, 'user_pages/channel_detail.html', {'channel': channel})
    else:
        messages.warning(request, 'Bu kanala erişim izniniz yok.')
        return redirect('index')

@login_required(login_url='/login')
def assign_channel_role(request, channel_id, user_id):
    channel = get_object_or_404(Channel, id=channel_id)
    user = get_object_or_404(User, id=user_id)
    role = request.POST.get('role')

    ChannelRole.objects.update_or_create(user=user, channel=channel, defaults={'role': role})
    messages.success(request, f'{user.username} için {role} rolü başarıyla atandı.')
    return redirect('channel_detail', channel_id=channel_id)

@login_required
@require_POST
def like_post(request, post_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Lütfen önce giriş yapınız.")
        return HttpResponseRedirect(reverse('index'))  # Anasayfaya yönlendir

    post = get_object_or_404(Post, id=post_id)

    # Beğenme durumunu kontrol et
    if request.user in post.likes.all():
        # Kullanıcı beğenmişse, beğenmesini kaldır
        post.likes.remove(request.user)
        liked = False
    else:
        # Kullanıcı beğenmemişse, beğen
        post.likes.add(request.user)
        liked = True

    # Beğeni sayısını güncelle
    like_count = post.likes.count()

    return JsonResponse({'liked': liked, 'like_count': like_count})

def get_like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)  # post nesnesini burada tanımlıyoruz

    if request.user.is_authenticated:
        # Beğenme durumunu kontrol et
        if request.user in post.likes.all():
            # Kullanıcı beğenmişse, liked=True
            liked = True
        else:
            # Kullanıcı beğenmemişse, liked=False
            liked = False
    else:
        liked = False
    
    like_count = post.likes.count()  # Beğeni sayısını al
    return JsonResponse({'liked': liked, 'like_count': like_count})
    