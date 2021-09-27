from django.shortcuts import render
from django.http import HttpResponse
from blog.views import CommeonViewMixin
from django.views.generic import ListView
from .models import Link
# Create your views here.



class LinkListView(CommeonViewMixin,ListView):
        queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
        template_name = 'config/links.html'
        context_object_name = 'link_list'






