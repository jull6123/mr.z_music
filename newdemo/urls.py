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
from djangomusic.views import basicFuction, song, songList, comment, audit
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
    # 传参username+password
    # user.role=0------admin
    # user.role=1------user
    # user.role=2------audit
    path('register/', basicFuction.register),
    # 传参username+password+email
    # email是否存在 存在则报错，不存在则add_sysUser

    # 个人信息与修改密码
    path('updateperson/', basicFuction.updateperson),
    # 传参user,get/post


    # 用户端相关功能
    # 歌曲：增删改查+点赞+上传+收藏
    path('listHistoryById/', song.listHistoryById),
    # 传参user,我听过的，通过user.id在userMusic得到music_id（orderby -listen_time）列表，通过music_id查询musicList

    path('serMusic/', song.serMusic),
    # 传参type+serMusic,根据type查询具体的榜单
    # type = “search" 搜索 根据serMusic搜索sysMusic name/singer serMusic="",则展示全部is_upload=3   【delete_mark=0】
    # type = "hot" 热歌榜 查询sysMusic support前10  is_upload=3 delete_mark=0 已上传，未删除，网络/Ai音乐（mold=1)时无法上传不用添加条件
    # type = "new" 新歌榜 查询sysMusic upload_time前30 support前10 is_upload=3 delete_mark=0 已上传，未删除，网络/Ai音乐
    # type = "ai" AI榜  查询sysMusic is_upload=3 mold=2 delete_mark=0 已上传，Ai

    path('addMusic/', song.addMusic),
    # 传参post表单+user+（pid)只有ai生成有       get/post区分 查看/修改
    # mold = 1 网络音乐，先查看MD5是否重复，若重复直接返回msg="已存在"
    #                  若不存在，则将post内容写入，add_sysMusic,
    #                                          add_auditLog, sysMusic:is_upload=1,audit_id=id  return msg="已上传，等待审核"
    # mold = 2 源音频，先查看MD5是否重复, post内容写入add_sysMusic，is_upload=0,uid=user.id return msg="源音频已上传，等待下一步"
    # mold = 3 ai音乐，post内容写入add_sysMusic，is_upload=0,pid = pid ,uid=user.id return msg="AI歌曲创建成功，等待下一步"

    path('uploadMusic/', song.uploadMusic),
    # 传参music的id ai有单独的上传按钮，修改sysMusic is_upload为1，add_auditLog，改sysMusic audit_id=id

    path('delMusic/', song.delMuisc),
    # 传参music的id 删除音乐，修改sysMusic的delete_mark=1

    path('supportMusic/', song.supportMusic),
    # 传参music的id 点赞音乐，修改sysMusic的 support+1

    path('collectMusicToList/', song.collectMusicToList),
    # 传参music的id+songList的id 收藏音乐，新增listMusic数据，修改songList的数量 number+1

    path('listenedMusic/', song.listenedMusic),
    # 传参music的id+user 听过，add_userMusic


    # 歌单：增删改查+点赞+收藏+上传
    path('serSongList/', songList.serSongList),
    # 传参type+user+serSongList,根据type查询具体的list
    # type = “search" 搜索 根据serSongList搜索songList name/desc serSongList="",则展示全部 is_upload=3   【delete_mark=0】
    # type = “mine" 我的歌单 查询songList uid=user.id delete_mark=0 的songList(不要求是否上传）
    # type = "collect" 我的收藏 查询listUser user_id=user.id delete_mark=0 的songList.idList，根据id查songList delete_mark=0 收藏的已上传
    # type = "hot" 热门歌单 查询songList is_upload=3 support前15 delete_mark=0 已上传，未删除

    path('addSongList/', songList.addSongList),
    # 传参user+post内容， add_songList,uid=user.id return msg="创建成功"   get/post区分 查看/修改

    path('uploadSongList/', songList.uploadSongList),
    # 传参songList的id 上传歌单 is_upload=1,add_auditLog,audit_id=id

    path('delSongList/', songList.delSongList),
    # 传参songList的id+user+type 删除歌单 delete_mark=1
    # type = “mine" 我的歌单 查询songList(id) delete_mark=1
    # type = "collect" 我的收藏 查询listUser(songList_id+user_id) delete_mark=1

    path('supportSongList/', songList.supportSongList),
    # 传参songList的id 点赞歌单 support+1

    path('collectSongList/', songList.collectSongList),
    # 传参songList的id+user 收藏歌单 add_listUser

    path('delCollectSongList/', songList.delCollectSongList),
    # 传参songList的id+user 取消收藏 listUser中delete_mark=1

    path('getListById/', songList.getListById),
    # 传参songList的id 正在播放/歌单查看 listMusic根据songList_id delete_mark=0得到music_ids 得到sysMusic的list

    # path('listenedList/', music.listenedList),
    # # 传参songList的id+user 听过，add_userMusic

    # 评论界面
    path("getComments", comment.getComments),
    # 传参type+user,根据type查询具体的list
    # type = “hot" 热门评论 查询sysComment support前五 delete_mark=0+其user_id对应的用户name,avater
    # type = “new" 最新评论 查询sysComment create_time前30 delete_mark=0 pid=0 +其user_id对应的用户name,avater
    #                     循环：根据查询到的id查询pid=id(查询子评论)delete_mark=0 得到commentList +其user_id对应的用户name,avater
    #                     return ????

    path('addComment/', comment.addComment),
    # 传参sysComment的content+user+music_id+pid(针对子评论）评论回复 add_sysComment

    path('delComment/', comment.delComment),
    # 传参sysComment的id 删除评论 sysComment:delete_mark=1

    path('supportComment', comment.supportComment),
    # 传参sysComment的id 点赞评论 sysComment:support+1


    # 审核端
    path('getAuditList/', audit.getAuditList),
    # 传参user+type+state delete_mark=0
    # state = “代办"  查询auditLog audit_state=0
    # state = “已完成"  查询auditLog audit_id=user.id audit_state>2
    # type = “music"  查询auditLog audit_mold=0 得到music_id对应的sysMusic name……
    # type = “songList"  查询auditLog audit_mold=1 得到songList_id对应的songList name……

    path('auditById/', audit.auditById),
    # 传参user+id+type
    # type = “music"  根据auditLog的id找到music_id得到sysMusic,展示歌曲内容查看界面
    # type = “songList" 根据auditLog的id找到songList_id（审核顺序）
    #                   1. 根据listMusic查询歌单对应的musicList name……  group by is_upload    addSongList/
    #                   2. 根据songList查询歌单信息name……         addMusic/


    path('auditResult/', audit.auditResult),
    # 传参user+总id+type+state+content
    # type = “music"  查询auditLog 总id对应的audit_mold,相同则修改audit_state+msg_content   歌曲审核
    #                                 不同，若state=false,修改audit_state=3 + msg_content（部分歌曲审核未通过+原content） 歌单审核
    #                                        state=true,不修改，返回原审核列表界面
    # type = “songList" 查询auditLog  修改audit_state+msg_content



]

from django.conf import settings
from django.conf.urls.static import static

# 在开发环境中，为媒体文件配置 URL
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
