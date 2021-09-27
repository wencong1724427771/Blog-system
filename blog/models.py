from django.contrib.auth.models import User   # 身份认证系统auth模块
from django.db import models
import mistune
# Create your models here.


class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE= 0
    STATUS_ITEMS = (
        (STATUS_NORMAL,'正常'),
        (STATUS_DELETE,'删除')
    )

    name = models.CharField(max_length=50,verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                        choices=STATUS_ITEMS,verbose_name="状态")
    is_nav = models.BooleanField(default=False,verbose_name="是否为导航")
    owner = models.ForeignKey(User,verbose_name="作者",on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    @classmethod
    def get_navs(cls):
        categories = cls.objects.filter(status=cls.STATUS_NORMAL) # 查一次数据库取出所有数据
        nav_categories = []
        normal_categories = []
        for category in categories:
            if category.is_nav:
                nav_categories.append(category)
            else:
                normal_categories.append(category)
        return {
            "navs":nav_categories,
            "categories":normal_categories,
        }


class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除')
    )
    name = models.CharField(max_length=10,verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS,verbose_name="状态")
    owner = models.ForeignKey(User,verbose_name="作者",on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "标签"


class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DELETE, '草稿'),
    )

    title = models.CharField(max_length=255, verbose_name="标题")
    desc = models.CharField(max_length=1024,blank=True,verbose_name="摘要")
    content = models.TextField(verbose_name="正文",help_text="正文必须是MarkDown格式")
    content_html = models.TextField(verbose_name="正文html代码",blank=True,editable=False)
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS, verbose_name="状态")
    category = models.ForeignKey(Category,verbose_name="分类",on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag,verbose_name="标签")
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE,blank=True,null=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']     # 根据id进行降序排序

    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)         # object对象；get取不到对象会报错
        except Tag.DoesNotExist:
            post_list = []
            tag = None
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)\
                .select_related('owner','category')
        return post_list,tag

    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            post_list = []
        else:
            post_list = category.post_set.filter(status=Category.STATUS_NORMAL)\
                .select_related('owner','category')
        return post_list, category

    @classmethod
    def latest_posts(cls):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-created_time')
        return queryset

    # @classmethod
    # def detail_post(cls,post_id):
    #     try:
    #         post = cls.objects.get(id=post_id)
    #     except Post.DoesNotExist:
    #         post = []
    #     return post

    @classmethod
    def hot_posts(cls):                                     # only 优化
        return cls.objects.filter(status=cls.STATUS_NORMAL).only('title').order_by('-pv')
    
    def save(self, *args,**kwargs):
        ''''''
        self.content_html = mistune.markdown(self.content)
        # print(self.content_html,'Postxxxxxxx')
        super(Post, self).save(*args,**kwargs)

    from django.utils.functional import cached_property
    # sitemap：因为Post存在tag字段，影响到了url.item.tags。
    # 所以在模型中增加一个属性来输出配置好的tags
    @cached_property
    def tags(self):
        return ','.join(self.tag.values_list('name',flat=True))