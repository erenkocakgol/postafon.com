from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm
from django.utils.safestring import mark_safe

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    image = models.ImageField(blank=True, upload_to='images/users/')

    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name

    def image_tag(self):
        if self.image == "":
            return ""
        else:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'country', 'image']

# Kullanıcı profili için model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', default='uploads/images/users/defaultuser.jpg', blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    biography = models.TextField(blank=True)  # Biyografi alanı eklendi

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Post modeli
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    channel = models.ForeignKey('Channel', on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Kanal modeli
class Channel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_channels')
    members = models.ManyToManyField(User, related_name='joined_channels', blank=True)
    points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Kanal yöneticileri ve rütbeleri için model
class ChannelRole(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Yönetici'),
        ('moderator', 'Moderatör'),
        ('elder', 'Büyük'),
        ('member', 'Üye')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('user', 'channel', 'role')

    def __str__(self):
        return f"{self.user.username} - {self.role} in {self.channel.name}"
