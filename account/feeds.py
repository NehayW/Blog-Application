from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import User
from django.urls import reverse

 
class blogFeed(Feed):
    title = "geeksforgeeks"
    link = ""
    description = "RSS feed of GeeksForGeeks"
 
    def items(self):
        return User.objects.all()
 
    def item_title(self, item):
        return item.email
       
    def item_description(self, item):
        return item.first_name
 
    # def item_link(self, item):
    #    return reverse('post_detail', args =[item.id])