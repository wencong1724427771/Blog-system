from django.contrib import admin

# Register your models here.
from .models import Link,SideBar
from typeidea.custom_site import custome_site


@admin.register(Link,site=custome_site)
class LinkAdmin(admin.ModelAdmin,):
    list_display = ('title','href','status','weight','created_time')
    fields = ('title','href','status','weight')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(LinkAdmin, self).save_model(request, obj, form, change)


@admin.register(SideBar,site=custome_site)
class SiderBarAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_type', 'content', 'created_time')
    fields = ('title', 'display_type', 'content')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(SiderBarAdmin, self).save_model(request, obj, form, change)



    