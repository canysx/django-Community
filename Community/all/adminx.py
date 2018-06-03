from .models import Topic,UserFavorite,UserComment,UserMessage,OtherUrl
import xadmin
from xadmin import views


class BaseSetting(object):
    # 页面主题
    enable_thems = True
    use_bootswatch = True


class GlobalSettings(object):
    # 页面信息
    site_title = "社区后台管理系统"
    site_footer = "Canysx社区"
    menu_style = "accordion"


class TopicAadmin(object):
    list_display = ['title','content','click_nums','add_time']
    search_fields = ['title','content']
    list_filter = ['title','content','click_nums','add_time']


class UserFavoriteAadmin(object):
    list_display = ['user','topic','add_time']
    search_fields = ['user','topic']
    list_filter = ['user','topic','add_time']


class UserCommentAadmin(object):
    list_display = ['user','topic','add_time','comments']
    search_fields = ['user','topic','comments']
    list_filter = ['user','topic','add_time','comments']


class UserMessageAadmin(object):
    list_display = ['user','message','has_read','add_time']
    search_fields = ['user','message','has_read']
    list_filter = ['user','message','has_read','add_time']


class OtherUrlAadmin(object):
    list_display = ['name','url','add_time']
    search_fields = ['name','url']
    list_filter = ['name','url','add_time']



xadmin.site.register(Topic,TopicAadmin)
xadmin.site.register(UserFavorite,UserFavoriteAadmin)
xadmin.site.register(UserComment,UserCommentAadmin)
xadmin.site.register(UserMessage,UserMessageAadmin)
xadmin.site.register(OtherUrl,OtherUrlAadmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)
