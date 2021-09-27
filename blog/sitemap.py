from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Post


class PostSitemap(Sitemap):
    changefreq = "daily"    # 可选,指定每个对象的更新频率  "daily"
    priority = 1.0           # 可选,指定每个对象的优先级,默认0.5
    protocol = 'https'       # 协议

    def items(self):         # 返回一个列表,必须有
        return Post.objects.filter(status=Post.STATUS_NORMAL)

    def lastmod(self,obj):    # 该方法返回一个datetime,表示每个对象的最后修改时间
        return obj.created_time

    def location(self, obj): # 返回每篇文章的URL
        return reverse('post_detail',args=[obj.pk])

