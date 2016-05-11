import datetime
import re
import markdown2
from bs4 import BeautifulSoup
from django import forms
from .models import Article, Message, Type
import datetime


class ArticleCreateForm(forms.Form):
    # 每次访问创建文章视图时刷新分类选择框
    def __init__(self, *args, **kwargs):
        super(ArticleCreateForm, self).__init__(*args, **kwargs)
        choices = []
        types = Type.objects.all()
        for type in types:
            choices += [(type.name, type.name)]
        self.fields['type'].choices = choices

    title_en = forms.CharField(
        max_length=50,
        label='标题en',
        widget=forms.TextInput(attrs={'class': '', 'placeholder': '文章标题en'}),
    )
    title_cn = forms.CharField(
        max_length=50,
        label='标题cn',
        widget=forms.TextInput(attrs={'class': '', 'placeholder': '文章标题cn'})
    )
    content = forms.CharField(
        label='内容',
        min_length=10,
        widget=forms.Textarea(),
    )
    type = forms.ChoiceField(choices=(),
                             widget=forms.Select)

    def save(self, username='高亮', article=None):
        cd = self.cleaned_data
        title_en = cd['title_en']
        title_cn = cd['title_cn']
        content_md = cd['content']
        type = cd['type']
        type = Type.objects.get(name=type)
        content_html = markdown2.markdown(cd['content'])
        soup = BeautifulSoup(content_html, 'lxml')
        content_text = soup.get_text()[:200] + '......'
        url = '/article/%s' % (title_en)
        if article:
            article.url = url
            article.title_cn = title_cn
            article.title_en = title_en
            article.content_md = content_md
            article.content_html = content_html
            article.content_text = content_text
            article.update_time = datetime.datetime.now()
            article.type.article_numbers -= 1
            article.type.save()
            article.type = Type.objects.get(name=type)
            article.type.article_numbers += 1
            article.type.save()
        else:
            article = Article(
                url=url,
                title_cn=title_cn,
                title_en=title_en,
                content_md=content_md,
                content_html=content_html,
                view_times=0,
                comment_times=0,
                content_text=content_text,
                create_time=datetime.datetime.now(),
                type=type
            )
            type.article_numbers += 1
            type.save()
        article.save()


class MessageForm(forms.Form):
    email = forms.EmailField(label="邮箱", widget=forms.TextInput(attrs={'class': 'email_input', 'placeholder': "邮箱"}))
    name = forms.CharField(label="名字", widget=forms.TextInput(attrs={'class': 'name_input', 'placeholder': '名字'}))
    content = forms.CharField(widget=forms.Textarea)

    def save(self):
        cd = self.cleaned_data
        email = cd['email']
        name = cd['name']
        content = cd['content']
        message = Message(
            email=email,
            name=name,
            content=content,
        )
        message.save()
