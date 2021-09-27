"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path

from .custom_site import custome_site
# from blog.views import post_list,post_detail
from blog.views import PostDetailView,IndexView,CategoryView,TagView,SearchView,AuthorView
from config.views import LinkListView
from comment.views import CommentView

from django.contrib.sitemaps import views as sitemap_view
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap

urlpatterns = [
    # # 博客首页
    # re_path('^$',post_list,name='index'),
    # # 分类列表页
    # re_path('^category/(?P<category_id>\d+)/$',post_list,name='category_list'),
    # # 标签列表页
    # re_path('^tag/(?P<tag_id>\d+)/$',post_list,name='tag_list'),
    # # 博客详情页
    # re_path('^post/(?P<post_id>\d+).html/$',post_detail,name='post_detail'),
    # 友链展示页
    # re_path('^links/$',links,name='links'),

    re_path('^index/$', IndexView.as_view(), name='index'),  # 使用ListView
    re_path('^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category_list'),  # 使用ListView
    re_path('^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag_list'),  # 使用ListView
    re_path('^post/(?P<post_id>\d+).html/$', PostDetailView.as_view(), name='post_detail'),  # 使用DetailView
    re_path('^links/$',LinkListView.as_view(),name='links'),

    # 搜索
    re_path('^search/$',SearchView.as_view(),name='search'),
    # 作者页面
    re_path('^author/(?P<owner_id>\d+)/$',AuthorView.as_view(),name='author'),
    # 友链展示页
    re_path('^links/$', LinkListView.as_view(), name='links'),
    # 评论功能
    re_path('^comment/$', CommentView.as_view(), name='comment'),

    # 订阅器
    re_path('^rss|feed/$', LatestPostFeed(), name='rss'),
    re_path('^sitemap\.xml$', sitemap_view.sitemap, {'sitemaps':{'posts':PostSitemap}}),


    re_path('^super_admin/', admin.site.urls),
    re_path('^admin/', custome_site.urls),
]
