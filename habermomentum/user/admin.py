from django.contrib import admin

# Register your models here.
from user.models import UserProfile, Post


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_name', 'city', 'image_tag']

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Post)