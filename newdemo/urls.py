"""
URL configuration for newdemo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from djangomusic.views import basicFuction, recommend, comment, user, audit
from django.urls import path

urlpatterns = [
    # path("admin/", admin.site.urls),
    # path('login/', hviews.login),
    # path('register/', hviews.register),
    # path("person/", hviews.person),
    # path("update/", hviews.update),
    #
    # path("home/", hviews.home),
    #
    # # 管理员界面对用户的增删改查
    # path("user/<int:uid>/search/", user.search),
    # path("user/list/", user.userList),
    # path("user/add/", user.userAdd),
    # path("user/delete/", user.userDelete),
    # path("user/<int:nid>/edit/", user.userEdit),
    #
    # path("music/down/", music.down),
    # path("music/change/", music.change),
    # path("music/theList/", music.theList),
    # path("music/<int:uid>/search/", music.search),
    # path("music/list/", music.musicList),
    # path("music/add/", music.musicAdd),
    # path("music/delete/", music.musicDelete),
    # path("music/<int:nid>/edit/", music.musicEdit),
    #
    # path("test/", home.app),


    # 基本功能
    path('login/', basicFuction.login),
    path('register/', basicFuction.register),
    # 个人信息与修改密码
    path('updateperson/', basicFuction.updateperson),

    # 用户端相关功能
    # 歌曲：增删改查+点赞+上传
    path('listHistoryById/', user.listHistoryById),
    path('serMusic/', user.serMusic),
    path('addMusic/', user.addMusic),
    path('delMusic/', user.delMuisc),
    path('supportMusic', user.supportMusic),
    path('uploadMusic', user.uploadMusic),
    # 歌单：增删改查+点赞+收藏+上传
    path('listSongListById/', user.listSongListById),
    path('serSongList/', user.serSongList),
    path('addSongList/', user.addSongList),
    path('delSongList/', user.delSongList),
    path('supportSongList/', user.supportSongList),
    path('collectSongList/', user.collectSongList),
    path('uploadSongList/', user.uploadSongList),
    # 推荐界面
    path("getOriginalSongs/", recommend.getOriginalSongs),
    path("getHotSongs/", recommend.getHotSongs),
    path("getNewSongs/", recommend.getNewSongs),
    path("getHotLists/", recommend.getHotLists),
    # 评论界面
    path("getHotComments", comment.getHotComments),
    path("getNewComments", comment.getNewComments),
    path('addComment/', comment.addComment),
    path('delComment/', comment.delComment),
    path('supportComment', comment.supportComment),

    # 审核端
    path('auditMusic/', audit.auditMusic),
    path('auditSongList/', audit.auditSongList),


]

from django.conf import settings
from django.conf.urls.static import static

# 在开发环境中，为媒体文件配置 URL
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
