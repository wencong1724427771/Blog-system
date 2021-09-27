from django.contrib import admin

# Register your models here.
from .models import Comment
from typeidea.custom_site import custome_site


@admin.register(Comment,site=custome_site)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target','nickname','content','website','created_time')
