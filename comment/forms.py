from django import forms
import mistune
from .models import Comment


class CommentForm(forms.ModelForm):
    nickname = forms.CharField(
        label='昵称',
        max_length=16,
        min_length=3,
        error_messages={
            'max_length': '太长了',
            'min_length': '太短了',
            'required': '不能为空',  # 为空时触发
        },
        widget=forms.widgets.Input(
          attrs={'class':'form-control','style':'width: 40%;'}
        ),
    )
    email = forms.EmailField(
        label = 'Email',
        max_length = 50,
        error_messages={
            'invalid': '必须是邮箱格式',
            'required': '不能为空',
        },
        widget=forms.widgets.EmailInput(
            attrs={'class':'form-control','style':'width: 40%;'}
        ),
    )
    website = forms.CharField(
        label='网站',
        max_length=100,
        widget=forms.widgets.URLInput(
            attrs={'class': 'form-control', 'style': 'width: 40%;'}
        ),
    )
    content = forms.CharField(
        label='内容',
        max_length=500,
        widget=forms.widgets.Textarea(
            attrs={'row':6,'col':60,'class':'form-control'}
        )
    )

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content)<10:
            raise forms.ValidationError('内容太少了,需要超过10个字符！')
        content = mistune.markdown(content)
        return content

    class Meta:
        model = Comment
        fields =['nickname','email','website','content']