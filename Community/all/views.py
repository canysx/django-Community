from django.core.urlresolvers import reverse
from django.shortcuts import render,redirect
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import UserProfile, Topic, UserFavorite, UserComment, OtherUrl
from .forms import RegisterForm, LoginForm, WriteForm
# Create your views here.


class LoginView(View):
    # 登录
    def get(self,request):
        login_form = LoginForm()
        return render(request, 'login.html', {'login_form':login_form})

    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username")
            pass_word = request.POST.get("password")
            user = authenticate(username=user_name, password=pass_word)
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        return render(request, 'login.html', {'login_form': login_form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class RegisterView(View):
    # 用户注册
    def get(self,request):
        register_form = RegisterForm()
        return render(request, 'reg.html', {'register_form': register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("username")
            if UserProfile.objects.filter(username=user_name):
                return render(request, 'reg.html', {'msg': '用户名已存在',
                                                    'register_form': register_form})
            pass_word = request.POST.get("password")
            user_email = request.POST.get("email")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.password = make_password(pass_word)
            user_profile.email = user_email
            user_profile.save()
            return render(request, 'login.html', {})
        else:
            return render(request, 'reg.html', {'register_form': register_form})


class IndexView(View):
    # 首页
    def get(self,request):
        other_url = OtherUrl.objects.all()
        topic_type = request.GET.get("type")
        all_content = Topic.objects.all()
        hot_content = Topic.objects.order_by("-click_nums")[:3]
        if topic_type == "hot":
            all_content = Topic.objects.order_by("-click_nums")
        elif topic_type == "new":
            all_content = Topic.objects.order_by("-add_time")
        # 排序
        paginator = Paginator(all_content,10)
        page = request.GET.get("page", "")
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator._num_pages)

        return render(request, 'index.html', {'contacts': contacts, "topic_type": topic_type,
                                              "hot_content": hot_content, "other_url": other_url})


class TopicView(View):
    def get(self,request,topic_id):
        other_url = OtherUrl.objects.all()
        hot_content = Topic.objects.order_by("-click_nums")[:3]
        all_comments = UserComment.objects.filter(topic_id=topic_id)
        try:
            contents = Topic.objects.get(id=int(topic_id))
        except:
            contents = Topic.objects.get(id=1)
        has_fav_topic = False
        contents.click_nums += 1
        contents.save()
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=topic_id):
                has_fav_topic = True
        return render(request, "tiezi.html", {'contents': contents, 'has_fav_topic':has_fav_topic,
                                              "all_comments": all_comments, "hot_content": hot_content,
                                              "other_url": other_url})


class AddFavView(View):
    # 用户收藏
    def post(self,request):
        fav_id = request.POST.get("fav_id","1")
        has_fav = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id))
        # 判断是否已经收藏
        if has_fav:
            has_fav.delete()
            topic_fav = Topic.objects.get(id=int(fav_id))
            topic_fav.fav_nums -= 1
            if topic_fav.fav_nums <= 0:
                topic_fav.fav_nums = 0
            topic_fav.save()
            return HttpResponse('{"status": "success", "msg": "收藏"}', content_type="application/json")
        else:
            if int(fav_id) > 0:
                user_fav = UserFavorite()
                user_fav.fav_id = fav_id
                user_fav.user = request.user
                user_fav.save()
                topic_fav = Topic.objects.get(id=int(fav_id))
                topic_fav.fav_nums += 1
                topic_fav.save()
                return HttpResponse('{"status": "success", "msg": "已收藏"}', content_type="application/json")
            return HttpResponse('{"statue": "fail", "msg": "收藏出错 "}', content_type='application/json')


class AddCommentsView(View):
    # 用户评论
    def post(self,request):
        comments = request.POST.get("comments","")
        topic_id = request.POST.get("topic_id","0")
        if int(topic_id)>0:
            topic_comment = UserComment()
            topic = Topic.objects.get(id=int(topic_id))
            topic_comment.comments = comments
            topic_comment.topic = topic
            topic_comment.user = request.user
            topic_comment.save()
            return HttpResponse('{"status": "success","msg": "评论成功"}', content_type="application/json")
        else:
            return HttpResponse('{"status": "fail", "msg": "添加失败"}', content_type='application/json')


class UserHomeView(View):
    def get(self,request):
        return render(request, 'user_home.html', {'home': 'home'})


class UserInfoView(View):
    def get(self,request):
        return render(request, 'user_info.html', {'info': 'info'})


class UserTopicView(View):
    def get(self,request):
        all_topics = Topic.objects.filter(user=request.user)
        return render(request, 'user_topic.html', {'topic': 'topic', 'all_topics': all_topics})


class UserFavoriteView(View):
    def get(self,request):
        all_favs = []
        user_fav_ids = UserFavorite.objects.filter(user=request.user)
        for user_fav_id in user_fav_ids:
            if Topic.objects.filter(id=int(user_fav_id.fav_id)):
                all_fav = Topic.objects.get(id=user_fav_id.fav_id)
                all_favs.append(all_fav)
        return render(request, 'user_fav.html', {'topic': 'topic', 'all_fav': all_favs})


class WriteView(View):
    def get(self,request):
        return render(request, "write.html", {})

    def post(self,request):
        write_form = WriteForm(request.POST, request.FILES)
        topic = Topic()
        if write_form.is_valid():
            topic.user = request.user
            image = write_form.cleaned_data['image']
            title = write_form.cleaned_data['title']
            content = write_form.cleaned_data['content']
            topic.image = image
            topic.title = title
            topic.content = content
            topic.save()
            return HttpResponseRedirect(reverse('index'))


class DeleteView(View):
    def get(self, request):
        topic_id = request.GET.get("topic_id", "1")
        user = request.user
        if Topic.objects.filter(user=user, id=topic_id):
            user_topic = Topic(user=user, id=topic_id)
            user_topic.delete()
            return HttpResponseRedirect(reverse('user_topic'))


class DeleteFavView(View):
    def get(self, request):
        fav_id = request.GET.get("fav", "1")
        user = request.user
        fav_num = Topic()
        if UserFavorite.objects.filter(user=user, fav_id=fav_id):
            UserFavorite.objects.filter(user=user, fav_id=fav_id).delete()
            fav_num.fav_nums -= 1
            if fav_num.fav_nums <= 0:
                fav_num.fav_nums = 0
            return HttpResponseRedirect(reverse('user_fav'))
