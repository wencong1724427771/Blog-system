from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed

# RSS简易消息聚合,提供订阅接口
from .models import Post


class ExtendedRSSFees(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super(ExtendedRSSFees, self).add_item_elements(handler,item)
        handler.addQuickElement('content:html',item['content_html'])


class LatestPostFeed(Feed):
    feed_type = Rss201rev2Feed   # 可以不写,默认值
    title = "Bon Blog System"
    link = '/res/'
    description = "A Blog System  By Django"

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.desc

    def item_link(self, item):
        return reverse('post_detail',args=[item.pk])

    def item_extra_kwargs(self, item):
        return {'content_html':self.item_content_html(item)}

    def item_content_html(self,item):
        return item.content_html