from django.shortcuts import redirect,render
from django.views.generic import TemplateView,View
# Create your views here.

from .forms import CommentForm


class CommentView(TemplateView):
    http_method_names = ['post']
    template_name = 'comment/result.html'

    def post(self,request,*args,**kwargs):
        comment_form = CommentForm(request.POST)
        target = request.POST.get('target')

        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            # print(instance,'xxxxx')     # Comment object (None) xxxxx
            instance.target = target
            instance.save()
            return redirect(target)
        else:
            succeed = False
        context = {
            'succeed':succeed,
            'form':comment_form,
            'target':target,
        }
        return self.render_to_response(context)  #  TemplateView 中的模板渲染方法 render_to_response()


