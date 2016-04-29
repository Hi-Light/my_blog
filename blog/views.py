import json

from django.template import context
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.shortcuts import render, HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.defaultfilters import lower
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView, SingleObjectMixin
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


class BaseMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)
        try:
            context['hot_article'] = Article.objects.order_by('-view_times')[0:10]
            context['new_commnet'] = Comment.objects.order_by('-create_time')[0:10]
            context['python_len'] = Article.objects.filter(type='Python').__len__()
        except Exception as e:
            raise AttributeError('信息不正确')
        return context


# 文章列表视图类，以列表的形式显示文章的提要
class ArticleListView(BaseMixin, ListView):
    template_name = 'index.html'
    context_object_name = 'article_list'

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleListView, self).get_context_data()
        context['type'] = self.kwargs.get('type')
        return context

    def get_queryset(self, **kwargs):
        type = self.kwargs.get('type')
        if type == None:
            article_list = Article.objects.all().order_by(F('create_time').desc())[:100]
            paginator = Paginator(article_list, 5)
            page = self.request.GET.get('page')
        else:
            article_list = Article.objects.filter(type=type).order_by(F('create_time').desc())[:100]
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


# 文章编辑界面，提取文章的原始内容，修改内容并提交保存
class ArticleEditView(AdminRequiredMixin
    , FormView):
    template_name = 'article_create.html'
    form_class = ArticleCreateForm

    def get_initial(self, **kwargs):
        title_en = self.kwargs.get('title_en')
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


# 留言板
class MessageView(ListView):
    template_name = 'message_board.html'
    model = Message
    context_object_name = "message_list"

    def post(self, request):
        content = request.POST['content']
        user = request.user
        floor = Message.objects.all().__len__() + 1
        message = Message(author=user, content=content, floor=floor)
        message.save()
        return HttpResponseRedirect('/messageboard')

    def get_queryset(self, **kwargs):
        message_list = Message.objects.all()
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


# 注册一个新用户
def create_user(request):
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


# 带有回复的文章详细页面
class ArticleWithComment(SingleObjectMixin, ListView):
    template_name = 'article_with_comments.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Article.objects)
        self.object.view_times += 1
        self.object.save()
        return super(ArticleWithComment,
                     self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ArticleWithComment, self).get_context_data(**kwargs)
        context['article'] = self.object
        return context

    def get_queryset(self):
        return self.object.comment_set.all()


def create_comment(request, title_en):
    if request.method == "POST":
        url = request.get_full_path()[:-15]
        content = request.POST['content']
        user = request.user
        article = Article.objects.get(title_en=title_en)
        article.comment_times += 1
        floor = article.comment_times
        article.save()
        comment = Comment(author=user, article=article, content=content, floor=floor)
        comment.save()
        return HttpResponseRedirect(url)
    else:
        raise Http404
