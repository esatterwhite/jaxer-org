from django.contrib.syndication.feeds import Feed
from jaxerlog.models import UserLogEntry
from django.utils.feedgenerator import Atom1Feed
from django.contrib.syndication.feeds import FeedDoesNotExist
from djang

class SiteActivityFeed(Feed):
    feed_type = Atom1Feed
    title_template = 'feeds/activity/title.html'
    link = '/activity/'
    description_template = 'feeds/activity/description.html'
    description = ""
    title = "" 
    def items(self):
        return UserLogEntry.objects.order_by('-action_time')