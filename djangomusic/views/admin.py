import json

from django.http import JsonResponse

from djangomusic import models


def serUserList(request):
    data = json.loads(request.body)
    serName = data.get('serName', None)
    serEmail = data.get('serEmail', None)
    serDel = data.get('serDel', None)
    serRole = data.get('serRole', None)
    userList = models.sysUser.objects.filter(username__icontains=serName,
                                             email__icontains=serEmail,
                                             delete_mark=serDel,
                                             role=serRole).order_by('create_time')
    return JsonResponse({'code': 200, 'userList': userList, 'msg': "success"})


def serMusicList(request):
    data = json.loads(request.body)
    serName = data.get('serName', None)
    serDesc = data.get('serDesc', None)
    serSinger = data.get('serSinger', None)
    serMold = data.get('serMold', None)
    serUpload = data.get('serUpload', None)
    orderBy = data.get('orderBy', None)
    ascOrderBy = data.get('aecOrderBy', None)
    musicList = models.sysMusic.objects.filter(name__icontains=serName,
                                               singer__icontains=serSinger,
                                               description__icontains=serDesc,
                                               mold=serMold,
                                               is_upload=serUpload).all().order_by(orderBy, ascOrderBy)
    list = []
    for music in musicList:
        userName = parentName = auditorName = ""
        if music.mold != 1:
            userName = models.sysUser.objects.filter(id=music.uid, delete_mark=0).first().username
            if music.mold ==3:
                parentName = models.sysMusic.objects.filter(id=music.pid, delete_mark=0).first().name
        if music.is_upload !=0:
            id = models.auditLog.objects.filter(id=music.audit_id, delete_mark=0).first().audit_id
            auditorName = models.sysUser.objects.filter(id=id, delete_mark=0).first().username
        list.append(music,userName, parentName, auditorName)
    return JsonResponse({'code': 200, 'musicList': list, 'msg': "success"})


def serSongList(request):
    return None