from datetime import date
from django.shortcuts import render
from blog.models import Tag,Post,Category
from config.models import SideBar
from comment.models import Comment
from comment.forms import CommentForm
# Create your views here.
from django.views.generic import DetailView,ListView
from django.shortcuts import get_object_or_404
from django.db.models import Q,F
from django.core.cache import cache


def post_list(request,category_id=None,tag_id=None):
    tag = None
    category = None
    if tag_id:
        '''如果tag_id存在,获取tag名,显示tag标签下的文章；'''
        post_list,tag = Post.get_by_tag(tag_id)
    elif category_id:
        '''如果category存在,获取category名,显示该分类下的文章'''
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()
    context = {
        'category':category,
        'tag':tag,
        'post_list':post_list,
        'sidebars':SideBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request, 'post/list.html', context=context)


def post_detail(request,post_id):
    post = Post.detail_post(post_id)
    context = {
        "post":post,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request, 'post/detail.html', context=context)


class CommeonViewMixin:
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
        })
        context.update(Category.get_navs())
        return context


class IndexView(CommeonViewMixin,ListView):
    queryset = Post.latest_posts()
    paginate_by = 3
    context_object_name = 'post_list'
    template_name = 'post/list.html'


class CategoryView(IndexView):
    def get_context_data(self,**kwargs):
        # print(self.kwargs)    # {'category_id': '1'}
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        # print(self.kwargs)    # {'category_id': '1'}
        category = get_object_or_404(Category,pk=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        """重写get_queryset根据分类过滤"""
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_date(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        """重写get_queryset根据标签过滤"""
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)


class PostDetailView(CommeonViewMixin,DetailView):
    queryset = Post.latest_posts()
    template_name = 'post/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self,**kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        post_id = self.kwargs.get('post_id')
        context.update({
            'comment_form':CommentForm,
            'target':self.request.path,    # /post/1.html/
            'target_name':Post.objects.get(pk=post_id)     # 得到当前文章名
        })
        return context

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request,*args,**kwargs)
        # Post.objects.filter(pk=self.object.id).update(pv=F('pv')+1,uv=F('uv')+1)


        # 使用pv和uv统计
        self.handle_visited()
        # 视图必须返回一个 HttpResponse 对象
        return response

    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = 'pv:%s:%s'%(uid,self.request.path)
        uv_key = 'pv:%s:%s:%s'%(uid,str(date.today()),self.request.path)
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key,1,1*60)     # 1分钟有效
        if not cache.get(uv_key):
            increase_uv = True
            cache.set(pv_key,1,24*60*60)    # 24小时有效
        if increase_pv and increase_uv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv')+1,uv=F('uv')+1)
        elif increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv')+1)
        elif increase_uv:
            Post.objects.filter(pk=self.object.id).update(uv=F('uv') + 1)


class SearchView(IndexView):
    '''self ---> <blog.views.SearchView object at 0x04A526E8>'''
    def get_context_data(self,**kwargs):
        context = super(SearchView, self).get_context_data()
        context.update({
            'keyword':self.request.GET.get('keyword',''),
        })
        return context

    def get_queryset(self):
        queryset = super(SearchView, self).get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))


class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super(AuthorView, self).get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id = author_id)


