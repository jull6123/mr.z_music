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
from djangomusic.views import basicFuction, song, songList, comment, audit, admin
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
    # json 传参username+password
    # return user

    path('register/', basicFuction.register),
    # json 传参username+password+email

    # 个人信息与修改密码
    path('updateperson/', basicFuction.updateperson),
    # 表单
    # post:传表单填写信息
    #      return user


    # 用户端相关功能
    # 歌曲：增删改查+点赞+上传+收藏

    # 我听过的--歌曲列表
    path('listHistoryById/', song.listHistoryById),
    # json 传参user
    # return musicList

    # 清空登录用户的 “我听过的” 数据
    path('clearHistoryById/', song.clearHistoryById),
    # json 传参user

    # 全部歌曲搜索：推荐：各榜单 + 搜索
    path('serMusic/', song.serMusic),
    # json 传参type：search/hot/new/ai +serName,根据type查询具体的榜单
    # return musicList

    # 新增歌曲表单填写
    path('song/addMusic/', song.addMusic),
    # 表单 传参post表单+user+（pid)只有ai生成有
    # return music

    # ai生成新歌曲
    path('song/createMusic/', song.createMusic),
    # json 传参 源music的id mid

    # 上传歌曲
    path('song/uploadMusic/', song.uploadMusic),
    # json 传参music的id mid

    # 删除歌曲 / 自己的该歌单中删除某歌曲
    path('song/delMusic/', song.delMuisc),
    # json 传参music的id mid  songList.id->sid type:delm/dels

    # 点赞歌曲
    path('song/supportMusic/', song.supportMusic),
    # json 传参music的id mid

    # 收藏歌曲至自己的歌单中
    path('song/collectMusicToList/', song.collectMusicToList),
    # json 传参music的id mid  歌单id sid

    # 歌曲添加至 我听过的
    path('song/listenedMusic/', song.listenedMusic),
    # json 传参music的id mid + user


    # 歌单：增删改查+点赞+收藏+上传
    # 歌单搜索：我的歌单 + 我的收藏 + 热门歌单
    path('serSongList/', songList.serSongList),
    # json 传参 type: search/mine/collect/hot + user + serSName,根据type查询具体的list
    # return songList

    # 新增歌单
    path('songList/addSongList/', songList.addSongList),
    # 表单
    # post：user+表单内容
    # get：歌单id:sid
    # return songList

    # 上传歌单
    path('songList/uploadSongList/', songList.uploadSongList),
    # json 传参songList.id-> sid

    # 删除歌单/取消收藏
    path('songList/delSongList/', songList.delSongList),
    # json 传参songList的id->sid + user + type： min/collect

    # 点赞歌单
    path('songList/supportSongList/', songList.supportSongList),
    # json 传参songList的id->sid

    # 收藏歌单
    path('songList/collectSongList/', songList.collectSongList),
    # json 传参songList的id->sid + user

    # 正在播放/歌单查看
    path('getListById/', songList.getListById),
    # json 传参songList的id->sid
    # return musicList

    # 我听过的 歌单
    # path('listenedList/', music.listenedList),
    # # 传参songList的id+user 听过，add_userMusic

    # 评论界面
    # 搜索评论：热门评论 + 最新评论
    path("getComments", comment.getComments),
    # json 传参type: hot/new + music.id->mid 根据type查询具体的list
    # return comment(comment+user.id+user.name+user.avatar

    # 新增评论/回复评论
    path('comment/addComment/', comment.addComment),
    # json 传参 content + user + music_id->mid + pid(针对回复时

    # 删除评论
    path('comment/delComment/', comment.delComment),
    # json 传参sysComment.id->cid

    # 点赞评论
    path('comment/supportComment', comment.supportComment),
    # json 传参sysComment.id->cid


    # 审核端
    # 审核数据搜索：待完成/已完成/歌曲/歌单
    path('getAuditList/', audit.getAuditList),
    # json 传参user + type:unAudited/Audited + state:music/songList
    # return auditList:auditLog+ m/s.id + m/s.name + m.url + type(music_net/music_ai/song_list) + m/s.uid.name

    # 审核内容
    path('audit/auditById/', audit.auditById),
    # json 传参audit.id->aid + music.id->mid + songList.id->id + type:music/songList
    # return music: music    songList: songList

    # 审核结果
    path('audit/auditResult/', audit.auditResult),
    # json 传参 user + auditLog.id->aid + type:music/songList + state:3 fail/4 success + content

    # 查看审核结果
    path('audit/getauditResult/', audit.getauditResult),
    # json 传参 user + id + type:music/songList
    # return audit



    # 管理员端
    path('serUserList/', admin.serUserList),
    # json 传参serName,serEmail,serDel,serRole
    # return userList

    path('serMusicList/', admin.serMusicList),
    # json 传参serName,serDesc,serSinger,serMold,serUpload,orderBy:duration_time/support/,ascOrder
    # return userList

    path('serSongList/', admin.serSongList),
    # json 传参serName,serDesc,serUpload,orderBy:duration_time/support/,ascOrder
    # return userList
    # 返回所有歌单信息---按钮(getListById/)

]

from django.conf import settings
from django.conf.urls.static import static

# 在开发环境中，为媒体文件配置 URL
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
