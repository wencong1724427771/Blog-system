from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
# Register your models here.

from .models import Post,Category,Tag
from .adminforms import PostAdminForm
from typeidea.custom_site import custome_site
from typeidea.base_admin import BaseOwnerAdmin
from django.contrib.admin.models import LogEntry   # 日志


class PostInline(admin.StackedInline):              # StackedInline样式不同
    fields = ('title','desc')
    extra = 0                # 控制额外的
    model = Post


@admin.register(Category,site=custome_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline,]
    list_display = ('name','status','is_nav','created_time','post_count')
    fields = ('name','status','is_nav')

    def post_count(self,obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'

    def save_model(self, request, obj, form, change):   # 自动保存owner
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request,obj,form,change)


@admin.register(Tag,site=custome_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name','status','created_time')
    fields = ('name','status')        # fileds字段控制“修改添加字段”时显示的条目

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器,展示当前用户分类"""
    title = "分类过滤器"
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id','name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post,site=custome_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm       # 自定义form

    list_display = [
        'title','category','status',
        'created_time','owner','operator'
    ]
    list_display_links = []
    # list_filter = ['category']
    list_filter = [CategoryOwnerFilter]
    search_fields = ['title','category__name']

    actions_on_top = True
    # actions_on_bottom = True

    # 编辑页面
    # save_on_top = True

    # fields = (
    #     ('category','title'),   # 第一行显示分类和标题
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )

    fieldsets = (      # 替换fields
        ('基础配置',{
            'description':'基础配置描述',
            'fields':(
                ('title','category'),
                'status',
            ),
        }),
        ('内容',{
            'fields':(
                'desc',
                'content',
                'tag',
            ),
        }),
        ('额外信息',{
            'classes':('collapse',),
            'fields':('pv','uv'),
        })
    )

    def operator(self,obj):
        return format_html(
            '<a herf="{}">编辑</a>',
            reverse('cus_admin:blog_post_change',args=(obj.id,))
        )
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        # print(request,1111111)        # <WSGIRequest: GET '/admin/blog/post/1/change/'> 1111111
        qs = super(PostAdmin, self).get_queryset(request)
        # print(qs,222222)             # <QuerySet [<Post: admin之定义过滤器>, <Post: 金瓶梅>]> 222222
        return qs.filter(owner=request.user)

    # class Media:
    #     css = {
    #         'all':("https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/5.0.2/css/bootstrap.min.css",),
    #     }
    #     js = ("https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/5.0.2/js/bootstrap.bundle.js",)


@admin.register(LogEntry,site=custome_site)
class LoginEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr','object_id','action_flag','user','change_message']


