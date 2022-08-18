from django import template
from datetime import datetime
from dateutil import parser
from django.utils import timezone
register = template.Library()


@register.simple_tag()
def modifaidtime(post_time):
    post_time = post_time
    current_time = datetime.now(timezone.utc)
    post_time = current_time - post_time
    post_time = str(post_time).split(",")
    return post_time[0]
