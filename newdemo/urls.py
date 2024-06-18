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
from django.views.static import serve

from djangomusic.views import basicFuction, song, songList, comment, audit, admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # 基本功能
    path('login/', basicFuction.login),
    path('register/', basicFuction.register),
    path('updateperson/', basicFuction.updateperson),


    # 用户端相关功能

    # 我听过的--歌曲列表
    path('listHistoryById/', song.listHistoryById),

    # 清空登录用户的 “我听过的” 数据
    path('clearHistoryById/', song.clearHistoryById),

    # 全部歌曲搜索：推荐：各榜单 + 搜索
    path('serMusic/', song.serMusic),

    # 新增歌曲表单填写
    path('song/addMusic/', song.addMusic),

    path('get_urls/', song.get_urls),

    path('create/', song.create),

    path('getMusic/<int:mid>', song.getMusic),

    # ai生成新歌曲
    path('song/createMusic/', song.createMusic),

    # 上传歌曲
    path('song/uploadMusic/', song.uploadMusic),

    # 收藏歌曲至自己的歌单中
    path('song/collectMusicToList/', song.collectMusicToList),

    # 歌曲添加至 我听过的
    path('song/listenedMusic/', song.listenedMusic),


    # 歌单：增删改查+点赞+收藏+上传
    # 歌单搜索：我的歌单 + 我的收藏 + 热门歌单
    path('serSongList/', songList.serSongList),

    # 新增歌单
    path('songList/addSongList/', songList.addSongList),

    # 收藏歌单
    path('songList/collectSongList/', songList.collectSongList),

    # 正在播放/歌单查看
    path('getFormById/', songList.getFormById),   # 获取歌单数据
    path('getListById/', songList.getListById),   # 获取歌单包含的歌曲列表数据


    # 评论界面
    # 搜索评论：热门评论 + 最新评论
    path("getComments/", comment.getComments),

    # 新增评论/回复评论
    path('comment/addComment/', comment.addComment),


    # 审核端
    path('getAuditList/', audit.getAuditList),
    path('audit/auditById/', audit.auditById),
    path('audit/auditResult/', audit.auditResult),

    # 管理员端
    path('serUserList/', admin.serUserList),
    path('delAll/', admin.delAll),  # 删除delete_mark=1及其对应文件与关联数据
    path('editRole/', admin.editRole), # 修改用户角色
    path('serMusicList/', admin.serMusicList),
    path('serSongLists/', admin.serSongLists),

    # 方法合并
    path('delById/', admin.delById),    # 各种删除
    path('supportById/', admin.supportById),   # 各种点赞
    path('upload/', admin.upload),  # 各种上传（上传按钮）

]

# 在开发环境中，为媒体文件配置 URL
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
