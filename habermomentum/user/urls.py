from django.urls import path
from user import views as user_views
from home import views as home_views

urlpatterns = [
    path('', user_views.index, name='user_index'),  # Kullanıcı ana sayfası
    path('home/', home_views.index, name='home_index'),  # Ana sayfa
    path('updateuserprofile/', user_views.updateuserprofile, name="updateuserprofile"),
    path('updateuserpassword/', user_views.updateuserpassword, name="updateuserpassword"),
    path('logout/', home_views.logoutview, name="logout"),

    # Gönderi yönetimi
    path('create_post/', user_views.create_post, name="create_post"),  # Gönderi oluşturma
    path('list_posts/', user_views.list_posts, name="list_posts"),  # Kullanıcının gönderilerini listeleme

    # Kanal yönetimi
    path('create_channel/', user_views.create_channel, name="create_channel"),  # Kanal oluşturma
    path('channel/<int:channel_id>/', user_views.channel_detail, name="channel_detail"),  # Kanal detayları
    path('channel/<int:channel_id>/assign_role/<int:user_id>/', user_views.assign_channel_role, name="assign_channel_role"),  # Kanal rol atama
]
