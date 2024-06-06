import json
import os

from django.http import JsonResponse

from djangomusic import models
from newdemo import settings


def serSongList(request):
    # 传参type+user+serSName,根据type查询具体的list
    # type = “search" 搜索 根据serSName搜索songList name/desc serSName="",则展示全部 is_upload=3   【delete_mark=0】
    # type = “mine" 我的歌单 查询songList uid=user.id delete_mark=0 的songList(不要求是否上传）
    # type = "collect" 我的收藏 查询listUser user_id=user.id delete_mark=0 的songList.idList，根据id查songList delete_mark=0 收藏的已上传
    # type = "hot" 热门歌单 查询songList is_upload=3 support前15 delete_mark=0 已上传，未删除
    data = json.loads(request.body)
    type = data.get('type')
    user = data.get('user')
    serSName = data.get('serSName')
    if type == 'search':
        songList = models.songList.objects.filter(name__icontains=serSName, singer__icontains=serSName,
                                                   is_upload=3, delete_mark=0).order_by('-upload_time').all()
    elif type == 'mine':
        songList = models.songList.objects.filter(uid=user.id, delete_mark=0).order_by('-create_date').all()
    elif type == 'collect':
        sids = models.listUser.objects.filter(user_id=user.id, delete_mark=0).all().songList_id
        songList = []
        for sid in sids:
            songList.append(models.songList.objects.filter(id=sid, delete_mark=0).first())
    elif type == 'hot':
        songList = models.songList.objects.filter(is_upload=3, delete_mark=0).order_by('-support').all()[:15]
    return JsonResponse({'code': 200, 'songList': songList, 'msg': "success"})


def addSongList(request):
    # 传参user+post内容， add_songList,uid=user.id return msg="创建成功"   get/post区分 查看/修改
    if request.method == 'POST':
        if request.FILES.get('avatar'):
            user = request.POST.get('user')
            sid = request.POST.get('sid')
            name = request.POST.get('name')
            description = request.POST.get('description')
            avatar = request.FILES['avatar']

            # Save avatar file
            avatar_path = os.path.join(settings.MEDIA_ROOT, 'avatars/'+user.id, avatar.name)
            with open(avatar_path, 'wb') as f:
                for chunk in avatar.chunks():
                    f.write(chunk)
            if sid is not None:
                # Update music info to database
                songL = models.songList.objects.filter(id=sid, delete_mark=0).first()
                if songL is None:
                    return JsonResponse({'code': 501, 'msg': "该歌单不存在"})
                songL.update(name=name, description=description, avatar=avatar_path)
            # Save music info to database
            songL = models.songList.objects.create(
                name=name,
                description=description,
                avatar=avatar_path,
            )
            return JsonResponse({'code': 200, 'songList': songL, 'msg': "success"})
        else:
            return JsonResponse({'code': 506, 'msg': 'Invalid request or missing files'})
    if request.method == 'GET':
        sid = request.GET.get('sid')
        songL = models.songList.objects.filter(id=sid, delete_mark=0).first()
        if songL is None:
            return JsonResponse({'code': 501, 'msg': "该歌单不存在"})
        return JsonResponse({'code': 200, 'songList': songL, 'msg': "success"})


def uploadSongList(request):
    # 传参songList的id 上传歌单 is_upload=1,add_auditLog,audit_id=id
    data = json.loads(request.body)
    sid = data.get('sid')
    songList = models.songList.objects.filter(id=sid, delete_mark=0).first()
    if songList is None:
        return JsonResponse({'code': 501, 'msg': "歌单不存在"})
    audit = models.auditLog.objects.create(user_id=request.user.id, audit_mold=1)
    songList.update(is_upload=1, audit_id=audit.id)
    return JsonResponse({'code': 200, 'msg': "success"})


def delSongList(request):
    # 传参songList的id+user+type 删除歌单 delete_mark=1
    # type = “mine" 我的歌单 查询songList(id) delete_mark=1
    # type = "collect" 我的收藏 查询listUser(songList_id+user_id) delete_mark=1
    data = json.loads(request.body)
    sid = data.get('sid')
    user = data.get('user')
    type = data.get('type')
    if type == 'mine':
        songList = models.songList.objects.filter(id=sid, delete_mark=0).first()
        if songList is None:
            return JsonResponse({'code': 501, 'msg': "歌单不存在"})
        songList.update(delete_mark=1)
        return JsonResponse({'code': 200, 'msg': "success"})
    songListUser = models.listUser.objects.filter(user_id=user.id, songList_id=sid, delete_mark=0).first()
    if songListUser is None:
        return JsonResponse({'code': 501, 'msg': "该收藏歌单不存在"})
    songListUser.update(delete_mark=1)
    return JsonResponse({'code': 200, 'msg': "success"})


def supportSongList(request):
    # 传参songList的id 点赞歌单 support+1
    data = json.loads(request.body)
    sid = data.get('sid')
    songList = models.songList.objects.filter(id=sid, delete_mark=0).first()
    if songList is None:
        return JsonResponse({'code': 501, 'msg': "歌单不存在"})
    songList.support += 1
    songList.save()
    return JsonResponse({'code': 200, 'msg': "success"})


def collectSongList(request):
    # 传参songList的id+user 收藏歌单 add_listUser
    data = json.loads(request.body)
    sid = data.get('sid')
    user = data.get('user')
    models.listUser.objects.create(user_id=user.id, songList_id=sid)
    return JsonResponse({'code': 200, 'msg': "success"})


def getListById(request):
    # 传参songList的id 正在播放/歌单查看 listMusic根据songList_id delete_mark=0得到music_ids 得到sysMusic的list
    data = json.loads(request.body)
    sid = data.get('sid')
    mids = models.listMusic.objects.filter(songList_id=sid, delete_mark=0).all().music_id
    musicList = []
    for mid in mids:
        musicList.append(models.sysMusic.objects.filter(id=mid).first())
    return JsonResponse({'code': 200, 'musicList': musicList, 'msg': "success"})