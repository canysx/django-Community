"""Community URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve

from Community.settings import MEDIA_ROOT
from all.views import RegisterView, LoginView, LogoutView, IndexView, TopicView, AddFavView, AddCommentsView, UserHomeView, UserInfoView, \
    UserTopicView, UserFavoriteView, WriteView, DeleteView, DeleteFavView
import xadmin

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$',IndexView.as_view(),name="index"),
    url(r'^register/$',RegisterView.as_view(),name="register"),
    url(r'^login/$',LoginView.as_view(),name="login"),
    url(r'^logout/$',LogoutView.as_view(),name="logout"),
    url(r'^topic/(?P<topic_id>\d*)$',TopicView.as_view(),name="topic"),
    url(r'^user/home/$',UserHomeView.as_view(),name="user_home"),
    url(r'^user/info/$',UserInfoView.as_view(),name="user_info"),
    url(r'^user/topic/$',UserTopicView.as_view(),name="user_topic"),
    url(r'^user/favorite/$',UserFavoriteView.as_view(),name="user_favorite"),
    url(r'^write/$',WriteView.as_view(),name="write"),



    url(r'^media/(?P<path>.*)$',serve,{"document_root":MEDIA_ROOT}),
    # 添加收藏
    url(r'^add_fav/$',AddFavView.as_view(),name="add_fav"),
    # 添加评论
    url(r'^add_comment/$',AddCommentsView.as_view(),name="add_comment"),
    # 删除主题
    url(r'^topic_delete/$',DeleteView.as_view(),name="topic_delete"),
    # 取消收藏
    url(r'^fav_delete/$',DeleteFavView.as_view(),name="fav_delete"),
]
