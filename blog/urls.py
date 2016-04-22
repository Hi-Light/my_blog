from django.conf.urls import url, include
from blog.views import *

urlpatterns = [
    url(r'^$', ArticleListView.as_view(), name='index-view'),
    url(r'^create/', ArticleCreateView.as_view(), name='create_view'),
    url(r'^index/', ArticleListView.as_view()),
    url(r'^article/(?P<title_en>\w+)/edit', ArticleEditView.as_view(), name='edit_view'),
    url(r'^article/(?P<pk>\w+)$', ArticleWithComment.as_view(), name='detail_view'),
    url(r'^messageboard/', MessageView.as_view(), name='message_view'),
    url(r'^register/', UserCreationView, name='user_create_view'),
    url(r'^is_exist', is_exist, name='is_exist'),
    url(r'^login/', login, name='login'),
    url(r'^logout', logout_user, name='logout')
]