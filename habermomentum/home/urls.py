from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.index, name='home'),
    path('logout/', views.logoutview, name='logout'),
    path('faqs/', views.faqs, name='faqs'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('user/', include('user.urls')),
]
