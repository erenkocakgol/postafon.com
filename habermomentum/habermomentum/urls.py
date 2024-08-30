from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from home import views as views_home
from user import views as views_user

from django.contrib.sitemaps.views import sitemap
from .sitemaps import PostSitemap

sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    

    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('user/', include('user.urls')),
    path('accounts/', include('user.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
# Görselin admin panelinde görüntülenmesine ve görsel yoluna adres satırı ile ulaşışmasına sağlıyor.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

