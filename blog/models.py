from django.db import models
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from auth_system.models import MyUser
type_choices = (
    ['Python', 'Python'],
    ['Django', 'Django'],
    ['Java', 'Java'],
    ['Android', 'Android'],
    ['others', '杂项'],
    ['essay', '随笔']
)


class Article(models.Model):
    title_en = models.CharField(max_length=50, primary_key=True)
    title_cn = models.CharField(max_length=50)
    type = models.CharField(max_length=20, choices=type_choices)
    url = models.CharField(max_length=50)
    content_md = models.TextField()
    content_html = models.TextField()
    content_text = models.TextField()
    view_times = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now=False)
    update_time = models.DateTimeField(auto_now_add=True)
    comment_times = models.IntegerField(default=0)
    author = models.CharField(max_length=100, default='高亮')

    class Meta:
        ordering = ['create_time']
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.title_cn


class Comment(models.Model):
    author = models.ForeignKey(MyUser)
    article = models.ForeignKey(Article, null=True)
    content = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now=True)
    floor = models.IntegerField()


class Message(models.Model):
    author = models.ForeignKey(MyUser)
    content = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now=True)
    floor = models.IntegerField()
