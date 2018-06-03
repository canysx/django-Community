from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import datetime

# Create your models here.


class UserProfile(AbstractUser):
    # 用户信息
    nick_name = models.CharField(max_length=20,verbose_name="昵称")
    phone = models.CharField(max_length=15,verbose_name="手机号")
    address = models.CharField(max_length=100,verbose_name="用户地址")
    gender = models.CharField(max_length=7,choices=(("man","男"),("women","女")),default="man")
    image = models.ImageField(max_length=100,verbose_name="用户头像",upload_to="image/%Y/%m",default="image/default.png")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def topic_num(self):
        return self.topic_set.all().count()

    def fav_num(self):
        return self.userfavorite_set.all().count()


class Topic(models.Model):
    # 帖子信息
    user = models.ForeignKey(UserProfile,default="", verbose_name="作者")
    title = models.CharField(max_length=30, verbose_name="标题")
    image = models.ImageField(max_length=50, default="image/default.png", upload_to="image/topic/%Y/%m",
                              verbose_name="封面图")
    content = models.TextField(max_length=500, verbose_name="内容")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "帖子信息"
        verbose_name_plural = verbose_name

    def comment_num(self):
        return self.usercomment_set.all().count()

    def __str__(self):
        return self.title


class UserFavorite(models.Model):
    # 用户收藏
    user = models.ForeignKey(UserProfile, verbose_name="用户名")
    fav_id = models.IntegerField(default=0, verbose_name=u"数据id")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name


class UserComment(models.Model):
    # 用户评论
    user = models.ForeignKey(UserProfile, verbose_name="用户名")
    topic = models.ForeignKey(Topic, verbose_name="帖子")
    comments = models.CharField(max_length=200, verbose_name="评论内容")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户评论"
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    user = models.IntegerField(default=0,verbose_name=u"接收用户")
    message = models.CharField(max_length=500,verbose_name=u"消息内容")
    has_read = models.BooleanField(default=False,verbose_name=u"是否已读")
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户消息"
        verbose_name_plural = verbose_name


class OtherUrl(models.Model):
    # 友情链接
    name = models.CharField(max_length=30,verbose_name="链接名称")
    url = models.CharField(max_length=30,verbose_name="链接地址")
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"友情链接"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name