from django.contrib import admin
from .models import Article, Message
from .models import *
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.

admin.site.register(Article)
admin.site.register(Message)

admin.site.register(MyUser)
admin.site.unregister(Group)

admin.site.register(Comment)
