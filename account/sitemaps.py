from django.contrib.sitemaps import Sitemap
from .models import User
 
# siemap class
class blogSitemap(Sitemap):
# change frequency and priority
    changefreq = "daily"
    priority = 1.0
 
    def items(self):
        return User.objects.all()
 
    # def lastmod(self, obj):
    #     return obj.updated_on