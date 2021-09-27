from django import template

from blog.models import Post

register = template.Library()


@register.inclusion_tag('config/sidebar_content_type.html')
def content_html(sidebars):
    from comment.models import Comment
    if sidebars.display_type == sidebars.DISPLAY_HTML:
        result = sidebars.content
        date = {"html": result, "TYPE": '1'}
        return date
    elif sidebars.display_type == sidebars.DISPLAY_LATEST:
        result = Post.latest_posts()
        date = {"posts":result,'TYPE':'2'}
        return date
    elif sidebars.display_type == sidebars.DISPLAY_HOT:
        result = Post.hot_posts()
        date = {"posts":result,'TYPE':'3'}
        return date
    elif sidebars.display_type == sidebars.DISPLAY_COMMENT:
        result = Comment.objects.filter(status=Comment.STATUS_NORMAL)
        return {"comments":result,'TYPE':'4'}