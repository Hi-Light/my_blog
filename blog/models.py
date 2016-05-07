from django.db import models
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from auth_system.models import MyUser


class Type(models.Model):
    name = models.CharField(max_length=20, verbose_name='类别名称')
    name_en = models.CharField(max_length=20, verbose_name='类别名称英语')
    article_numbers = models.IntegerField(default=0, verbose_name='该分类下文章数目')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural =  '分类'


class Article(models.Model):
    title_en = models.CharField(max_length=50, primary_key=True, verbose_name='中文标题')
    title_cn = models.CharField(max_length=50, verbose_name='英文标题')
    type = models.ForeignKey(Type, null=True, verbose_name='分类')
    url = models.CharField(max_length=50, verbose_name='链接地址')
    content_md = models.TextField(verbose_name='md格式内容')
    content_html = models.TextField(verbose_name='html格式内容')
    content_text = models.TextField(verbose_name='内容概览')
    view_times = models.IntegerField(default=0, verbose_name='查看次数')
    create_time = models.DateTimeField(auto_now=False, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now_add=True, verbose_name='最后更新时间')
    comment_times = models.IntegerField(default=0, verbose_name='评论次数')
    author = models.CharField(max_length=100, default='高亮', verbose_name='作者')

    class Meta:
        ordering = ['create_time']
        verbose_name_plural = '文章'

    def __str__(self):
        return self.title_cn


class Comment(models.Model):
    author = models.ForeignKey(MyUser, verbose_name='作者')
    article = models.ForeignKey(Article, null=True, verbose_name='所属文章')
    content = models.CharField(max_length=200, verbose_name='内容')
    create_time = models.DateTimeField(auto_now=True, verbose_name='评论时间')
    floor = models.IntegerField(verbose_name='楼层')

    class Meta:
        verbose_name = verbose_name_plural = '评论'



class Message(models.Model):
    author = models.ForeignKey(MyUser, verbose_name='作者')
    content = models.CharField(max_length=200, verbose_name='内容')
    create_time = models.DateTimeField(auto_now=True, verbose_name='留言时间')
    floor = models.IntegerField(verbose_name='楼层')

    class Meta:
        verbose_name = verbose_name_plural = '留言'

