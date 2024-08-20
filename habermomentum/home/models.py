from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.forms import ModelForm, TextInput, Textarea
from django.utils.safestring import mark_safe
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from django.urls import reverse

from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=100)
    content = models.TextField()
    author_name = models.CharField(max_length=100)
    author_position = models.CharField(max_length=100)
    background_image = models.ImageField(upload_to='backgrounds/')
    author_image = models.ImageField(upload_to='authors/')

    def __str__(self):
        return self.title


# Menü modeli için MPTT (Multi Parent Tree Table) model kullanımı
class Menu(MPTTModel):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(max_length=100)  # Menü başlığı
    keywords = models.CharField(max_length=255)  # Anahtar kelimeler
    description = models.CharField(max_length=255)  # Açıklama
    image = models.ImageField(blank=True, upload_to='images/')  # Menüye ait resim
    status = models.CharField(max_length=10, choices=STATUS)  # Aktif/pasif durumu
    slug = models.SlugField(null=True, unique=True)  # URL dostu slug
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)  # Üst menü
    created_at = models.DateTimeField(auto_now_add=True, editable=False)  # Oluşturulma tarihi
    updated_at = models.DateTimeField(auto_now=True, editable=False)  # Güncellenme tarihi

    class MPTTMeta:
        order_insertion_by = ['title']  # Ağaç yapısında sıralama

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' -> '.join(full_path[::-1])

    def get_absolute_url(self):
        return reverse('menu_detail', kwargs={'slug': self.slug})


# Ayarlar için model, site genelinde kullanılacak genel bilgileri içerir
class Setting(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(max_length=150)  # Site başlığı
    keywords = models.CharField(max_length=255)  # Anahtar kelimeler
    description = models.CharField(max_length=255)  # Açıklama
    company = models.CharField(max_length=50)  # Şirket adı
    address = models.CharField(blank=True, max_length=100)  # Şirket adresi
    phone = models.CharField(blank=True, max_length=15)  # Telefon numarası
    email = models.CharField(blank=True, max_length=50)  # E-posta adresi
    icon = models.ImageField(blank=True, upload_to='images/')  # Site ikon resmi
    instagram = models.CharField(blank=True, max_length=50)  # Instagram bağlantısı
    youtube = models.CharField(blank=True, max_length=50)  # Instagram bağlantısı
    linkedin = models.CharField(blank=True, max_length=50)  # Instagram bağlantısı
    aboutus = RichTextUploadingField(blank=True)  # Hakkımızda sayfası için zengin metin
    contact = RichTextUploadingField(blank=True)  # İletişim sayfası için zengin metin
    references = RichTextUploadingField(blank=True)  # Referanslar sayfası için zengin metin
    status = models.CharField(max_length=10, choices=STATUS)  # Aktif/pasif durumu
    created_at = models.DateTimeField(auto_now_add=True)  # Oluşturulma tarihi
    updated_at = models.DateTimeField(auto_now=True)  # Güncellenme tarihi

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.icon.url))

    image_tag.short_description = 'Icon'

# İletişim formu mesajlarını kaydeden model
class ContactFormMessage(models.Model):
    STATUS = (
        ('New', 'Yeni'),
        ('Read', 'Okundu'),
        ('Closed', 'Kapalı'),
    )
    name = models.CharField(blank=True, max_length=20)  # Gönderen adı
    email = models.CharField(blank=True, max_length=50)  # Gönderen e-posta adresi
    subject = models.CharField(blank=True, max_length=50)  # Mesaj konusu
    message = models.CharField(blank=True, max_length=255)  # Mesaj içeriği
    status = models.CharField(max_length=10, choices=STATUS, default='New')  # Mesaj durumu
    ip = models.CharField(blank=True, max_length=20)  # Mesaj gönderildiği IP adresi
    note = models.CharField(blank=True, max_length=100)  # Yönetici notları
    created_at = models.DateTimeField(auto_now_add=True)  # Oluşturulma tarihi
    updated_at = models.DateTimeField(auto_now=True)  # Güncellenme tarihi

    def __str__(self):
        return self.name

# İletişim formu için form modeli
class ContactFormu(ModelForm):
    class Meta:
        model = ContactFormMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Adınız', 'required': 'required'}),
            'subject': TextInput(attrs={'class': 'form-control', 'placeholder': 'Konu', 'required': 'required'}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Adresiniz', 'required': 'required'}),
            'message': Textarea(attrs={'class': 'form-control', 'placeholder': 'Mesaj', 'required': 'required'}),
        }

# Sıkça Sorulan Sorular (FAQ) modeli
class FAQ(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    ordernumber = models.IntegerField()  # Sıra numarası
    question = models.CharField(max_length=150)  # Soru
    answer = models.TextField(max_length=255)  # Cevap
    status = models.CharField(max_length=10, choices=STATUS)  # Aktif/pasif durumu
    created_at = models.DateTimeField(auto_now_add=True)  # Oluşturulma tarihi
    updated_at = models.DateTimeField(auto_now=True)  # Güncellenme tarihi

    def __str__(self):
        return self.question
