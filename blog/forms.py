import datetime
import re
import markdown
from bs4 import BeautifulSoup

from django import forms

from .models import Article, Message

import datetime


class ArticleCreateForm(forms.Form):
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
    tags = forms.CharField(
        label=u'标签',
        max_length=30,
        widget=forms.TextInput(attrs={'class': '', 'placeholder': '文章标签，用英文逗号分割'}),
    )

    def save(self, username='高亮', article=None):
        cd = self.cleaned_data
        title_en = cd['title_en']
        title_cn = cd['title_cn']
        content_md = cd['content']
        tags = cd['tags']
        content_html = markdown.markdown(cd['content'])
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
            article.tags = tags
        else:
            article = Article(
                url=url,
                title_cn=title_cn,
                title_en=title_en,
                content_md=content_md,
                content_html=content_html,
                tags=tags,
                view_times=0,
                comment_times=0,
                content_text=content_text,
                create_time=datetime.datetime.now()
            )
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
