from django import template

from comment.forms import CommentForm
from comment.models import Comment


register = template.Library()


@register.inclusion_tag('comment/block.html')
def comment_block(target):
    '''
    :param target: /post/5.html/
    :return: block.html需要的参数
    '''
    return {
        'target':target,
        'comment_form':CommentForm,
        'comment_list':Comment.get_by_target(target)
    }


@register.filter()
def detach_char(char):
    res = char.split('.')[0]
    return res



@register.filter()
def get_title(target):
    '''
    :param target: /post/5.html
    :return:  5 --> title(str)
    '''
    import re
    from blog.models import Post

    find_num = re.compile('\d+')
    post_pk = re.search(find_num, target).group()
    post_title = Post.objects.get(pk=post_pk)
    return post_title
