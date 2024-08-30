from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from user.models import Post  # Post modelini buraya ekleyin

class PostSitemap(Sitemap):
    changefreq = "daily"  # Günlük olarak değiştirildi
    priority = 0.8

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.date  # Post modelinizdeki güncellenme tarihi alanı

    def location(self, obj):
        link = "/post/" + obj.image.path.replace("/srv/media/", "")
        return link  # Image alanının URL'sini kullanın
