from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from home import views as views_home
from user import views as views_user

urlpatterns = [
    path('', include('home.urls')),
    path('faq/', include('home.urls')),
    path('admin/', admin.site.urls),
    

    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('user/', include('user.urls')),
]
# Görselin admin panelinde görüntülenmesine ve görsel yoluna adres satırı ile ulaşışmasına sağlıyor.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

