from django.urls import path, include
from home import views
from user import views as user_views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.index, name='home'),
    path('logout/', views.logoutview, name='logout'),
    path('login/', views.index, name='login'),
    path('faqs/', views.faqs, name='faqs'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('user/', include('user.urls')),
    


]
