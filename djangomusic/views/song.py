import json
from datetime import timezone

from django.http import JsonResponse

from djangomusic import models


def listHistoryById(request):
    # 传参user,我听过的，通过user.id在userMusic得到music_id（orderby -listen_time）列表，通过music_id查询musicList
    data = json.loads(request.body)
    user = data.get('user')
    uMusics = models.userMusic.objects.filter(user_id=user.id).order_by('-listen_time').all()[:30]
    musicList = []
    for uMusic in uMusics:
        musicList.append(models.sysMusic.objects.filter(id=uMusic.id).first())
    return JsonResponse({'code': 200, 'musicList': musicList, 'msg': "success"})

def serMusic(request):
    # 传参type+serName,根据type查询具体的榜单
    # type = “search" 搜索 根据serMusic搜索sysMusic name/singer serMusic="",则展示全部is_upload=3   【delete_mark=0】
    # type = "hot" 热歌榜 查询sysMusic support前10  is_upload=3 delete_mark=0 已上传，未删除，网络/Ai音乐（mold=1)时无法上传不用添加条件
    # type = "new" 新歌榜 查询sysMusic upload_time前30 support前10 is_upload=3 delete_mark=0 已上传，未删除，网络/Ai音乐
    # type = "ai" AI榜  查询sysMusic is_upload=3 mold=2 delete_mark=0 已上传，Ai
    data = json.loads(request.body)
    type = data.get('type')
    serName = data.get('serName')
    if type == 'search':
        musicList = models.sysMusic.objects.filter(name__icontains=serName, singer__icontains=serName,
                                                   is_upload=3, delete_mark=0).order_by('-upload_time').all()
    elif type == 'hot':
        musicList = models.sysMusic.objects.filter(is_upload=3, delete_mark=0).order_by('-support').all()[:10]
    elif type == 'new':
        musicList = models.sysMusic.objects.filter(is_upload=3, delete_mark=0).order_by('-upload_time').all()[
                    :30].order_by('-support').all()[:10]
    elif type == 'ai':
        musicList = models.sysMusic.objects.filter(is_upload=3, mold=2, delete_mark=0).order_by('-upload_time').all()[:5]
    return JsonResponse({'code': 200, 'musicList': musicList, 'msg': "success"})

def addMusic(request):
    return None

def createMusic(request):
    # 传参源music的id 生成ai
    return None

def uploadMusic(request):
    # 传参music的id ai有单独的上传按钮，修改sysMusic is_upload为1，add_auditLog，改sysMusic audit_id=id
    data = json.loads(request.body)
    musicId = data.get('mid')
    music = models.sysMusic.objects.filter(id=musicId, delete_mark=0).first()
    if music is None:
        return JsonResponse({'code': 501, 'msg': "音乐不存在"})
    music.is_upload = 1
    audit = models.auditLog.objects.create(music_id=musicId, audit_mold=0)
    music.audit_id = audit.id
    music.save()
    return JsonResponse({'code': 200, 'msg': "success"})


def delMuisc(request):
    # 传参music的id 删除音乐，修改sysMusic的delete_mark=1
    data = json.loads(request.body)
    musicId = data.get('mid')
    music = models.sysMusic.objects.filter(id=musicId, delete_mark=0).first()
    if music is None:
        return JsonResponse({'code': 501, 'msg': "音乐不存在"})
    music.delete_mark = 1
    music.save()
    return JsonResponse({'code': 200, 'msg': "success"})


def supportMusic(request):
    # 传参music的id 点赞音乐，修改sysMusic的 support+1
    data = json.loads(request.body)
    musicId = data.get('mid')
    music = models.sysMusic.objects.filter(id=musicId, delete_mark=0).first()
    if music is None:
        return JsonResponse({'code': 501, 'msg': "音乐不存在"})
    music.support += 1
    music.save()
    return JsonResponse({'code': 200, 'msg': "success"})

def collectMusicToList(request):
    # 传参music的id+songList的id 收藏音乐，新增listMusic数据，修改songList的数量 number+1
    data = json.loads(request.body)
    musicId = data.get('mid')
    songListId = data.get('sId')
    models.listMusic.objects.create(music_id=musicId, songList_id=songListId)
    songList = models.listMusic.objects.filter(id=songListId, delete_mark=0).first()
    if songList is None:
        return JsonResponse({'code': 501, 'msg': "歌单不存在"})
    songListId.number += 1
    songList.save()
    return JsonResponse({'code': 200, 'msg': "success"})


def listenedMusic(request):
    # 传参music的id+user 听过，add_userMusic或修改听歌时间
    data = json.loads(request.body)
    musicId = data.get('mid')
    user = data.get('user')
    uMusic = models.userMusic.objects.filter(user_id=user.id, music_id=musicId)
    if uMusic is None:
        models.userMusic.objects.create(user_id=user.id, music_id=musicId)
    else:
        uMusic[0].listen_time = timezone.now().timestamp()
        uMusic[0].save()

