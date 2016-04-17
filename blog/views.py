import json

from django.contrib import auth
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.shortcuts import render, HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.defaultfilters import lower
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import F
from .forms import *
from .models import *


# 限制只有管理员可以写文章视图的Mixin类
class AdminRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(AdminRequiredMixin, cls).as_view(**initkwargs)
        return staff_member_required(view)


# 文章列表视图类，以列表的形式显示文章的提要
class ArticleListView(ListView):
    template_name = 'index.html'
    context_object_name = 'article_list'

    def get_queryset(self, **kwargs):
        article_list = Article.objects.all().order_by(F('create_time').desc())[:100]
        paginator = Paginator(article_list, 5)
        page = self.request.GET.get('page')
        try:
            article_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            article_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            article_list = paginator.page(paginator.num_pages)
        return article_list


# 创建文章的视图类，用于显示编辑器并获取表单提交的数据
class ArticleCreateView(AdminRequiredMixin, FormView):
    template_name = 'article_create.html'
    form_class = ArticleCreateForm
    success_url = '/index/'

    def form_valid(self, form):
        form.save()
        return super(ArticleCreateView, self).form_valid(form)


# 显示文章详细页面的视图类
class ArticleDetailView(DetailView):
    template_name = 'article_detail.html'
    context_object_name = 'article'

    def get_object(self, **kwargs):
        title = self.kwargs.get('title_en')
        try:
            article = Article.objects.get(title_en=title)
            article.view_times += 1
            article.save()
        except Article.DoesNotExist:
            raise Http404("文章不存在")
        return article


# 文章编辑界面，提取文章的原始内容，修改内容并提交保存
class ArticleEditView(AdminRequiredMixin
    , FormView):
    template_name = 'article_create.html'
    form_class = ArticleCreateForm

    def get_initial(self, **kwargs):
        title_en = self.kwargs.get('title_en')
        print(title_en)
        try:
            self.article = Article.objects.get(title_en=title_en)
            initial = {
                'title_en': title_en,
                'title_cn': self.article.title_cn,
                'content': self.article.content_md,
                'tags': self.article.tags
            }
            return initial
        except Article.DoesNotExist:
            raise Http404("文章不存在")

    def form_valid(self, form):
        form.save(self.request, self.article)
        return super(ArticleEditView, self).form_valid(form)

    def get_success_url(self):
        title_en = self.request.POST.get('title_en')
        successful_url = reverse('detail_view', args=(title_en,))
        return successful_url


class MessageView(ListView, FormView):
    template_name = 'message_board.html'
    model = Message
    context_object_name = "message_list"
    form_class = MessageForm
    success_url = '/messageboard/'
    content_type = 'mmm'

    def form_valid(self, form):
        form.save()
        return super(MessageView, self).form_valid(form)

    def get_queryset(self, **kwargs):
        message_list = Message.objects.all().order_by(F('create_time').desc())[:100]
        paginator = Paginator(message_list, 10)
        page = self.request.GET.get('page')
        try:
            message_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            message_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            message_list = paginator.page(paginator.num_pages)
        return message_list


def UserCreationView(request):
    if request.method == 'POST':
        url = request.POST['url']
        name = request.POST['name']
        email = lower(request.POST['email'])
        password = request.POST['password1']
        MyUser.objects.create_user(name=name, email=email, password=password)
        user = auth.authenticate(username=email, password=password)
        auth.login(request, user)
        return HttpResponseRedirect(url)
    else:
        return render(request, 'register.html')


def is_exist(request):
    name = request.POST['name']
    email = lower(request.POST['email'])
    if MyUser.objects.filter(name=name).__len__():
        msg_name = '用户名已存在，换一个吧'
    else:
        msg_name = ''
    if name == '':
        msg_name = '请输入用户名'
    if MyUser.objects.filter(email=email).__len__():
        msg_email = '邮箱已被使用，换一个吧'
    else:
        msg_email = ''
    if email == '':
        msg_email = ''
    return HttpResponse(json.dumps({"msg_name": msg_name, "msg_email": msg_email}))


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        url = request.POST['url']
        a = MyUser.objects.filter(email=email)
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            print("ok")
            print(user.is_active)
            auth.login(request, user)
            return HttpResponseRedirect(url)
        else:
            return render(request, 'warning.html', {'information': '密码或账户不正确，请重试', 'back_url': 'ss'})


def logout_user(request):
    url = request.GET['url']
    auth.logout(request)
    return HttpResponseRedirect(url)
