from django.conf.urls import url, include
from django.views.generic import RedirectView

from blog.views import *

urlpatterns = [
    url(r'^$', ArticleListView.as_view(), name='index-view'),
    url(r'^create/', ArticleCreateView.as_view(), name='create_view'),
    url(r'^index/', ArticleListView.as_view()),
    url(r'^article/(?P<title_en>\w+)/create_comment', create_comment, name='create_comment'),
    url(r'^article/(?P<title_en>\w+)/edit', ArticleEditView.as_view(), name='edit_view'),
    url(r'^article/(?P<pk>\w+)$', ArticleWithComment.as_view(), name='detail_view'),
    url(r'^messageboard/', MessageView.as_view(), name='message_view'),
    url(r'^register/', create_user, name='user_create_view'),
    url(r'^type/(?P<type>\w+)$',ArticleListView.as_view(),name='type_view')
]
