from django.contrib import admin
from home.models import Setting, Menu, ContactFormMessage, FAQ
from user.models import Channel
from django.contrib.auth.models import User
from django.utils.html import format_html

# Özelleştirilmiş admin paneli görünüm sınıfları

class SettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'image_tag', 'status']
    readonly_fields = ['image_tag', 'created_at', 'updated_at']  # Add read-only fields here
    search_fields = ['title', 'company']
    list_filter = ['status']
    fieldsets = (
        (None, {
            'fields': ('title', 'keywords', 'description', 'company', 'address', 'phone', 'email', 'icon', 'instagram', 'youtube', 'linkedin', 'aboutus', 'contact', 'references', 'status')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at', 'updated_at']

class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'ordernumber', 'answer', 'status']
    list_filter = ['status']
    search_fields = ['question']
    ordering = ['ordernumber']
    readonly_fields = ['created_at', 'updated_at']

class ContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'status', 'image_tag', 'created_at']
    list_filter = ['type', 'status']
    search_fields = ['title', 'keywords', 'description']
    readonly_fields = ['image_tag']
    prepopulated_fields = {'slug': ('title',)}

class MenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'parent', 'image_tag', 'created_at']
    list_filter = ['status']
    search_fields = ['title', 'keywords', 'description']
    readonly_fields = ['image_tag']
    prepopulated_fields = {'slug': ('title',)}

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="50"/>', obj.image.url)
        return ''

# Admin paneline modelleri ekle
admin.site.register(Setting, SettingAdmin)
admin.site.register(ContactFormMessage, ContactFormMessageAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Channel)
