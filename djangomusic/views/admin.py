import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from djangomusic import models

@csrf_exempt
def serUserList(request):
    data = json.loads(request.body)
    serName = data.get('serNameU', None)
    serEmail = data.get('serEmail', None)
    serDel = data.get('serDel', None)
    serRole = data.get('serRole', None)
    userList = models.sysUser.objects.filter(username__icontains=serName,
                                             email__icontains=serEmail).order_by('create_time')
    if serDel == 2:
        userList = userList.filter(delete_mark__lt=serDel)
    else:
        userList = userList.filter(delete_mark=serDel)

    if serRole == 3:
        userList = userList.filter(role__lt=serRole)
    else:
        userList = userList.filter(role=serRole)

    userList_data = []
    for user in userList:
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'description': user.description,
            'avatar': user.get_avatar_url() if user.avatar else None,
            'role': dict(user.choiceR)[user.role],
            'create_time': user.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'delete_mark': dict(user.choiceD)[user.delete_mark],
        }
        userList_data.append(user_data)
    return JsonResponse({'code': 200, 'userList': userList_data, 'msg': "success"})

@csrf_exempt
def serMusicList(request):
    data = json.loads(request.body)
    serName = data.get('serNameM', None)
    serDesc = data.get('serDesc', None)
    serSinger = data.get('serNameM', None)
    serMold = data.get('serMold', None)
    serUpload = data.get('serUpload', None)
    orderBy = data.get('orderBy', None)
    ascOrderBy = data.get('ascOrderBy', None)
    musicList = models.sysMusic.objects.filter(name__icontains=serName,
                                               singer__icontains=serSinger,
                                               description__icontains=serDesc).all()
    if orderBy == '':
        musicList = musicList.order_by('id')
    else:
        if ascOrderBy == 'asc':
            musicList = musicList.order_by(orderBy)
        else:
            musicList = musicList.order_by('-'+orderBy)

    if serMold == 4:
        musicList = musicList.filter(mold__lt=serMold)
    else:
        musicList = musicList.filter(mold=serMold)

    if serUpload == 4:
        musicList = musicList.filter(is_upload__lt=serUpload)
    else:
        musicList = musicList.filter(is_upload=serUpload)

    list = []
    for music in musicList:
        music_dict = {
            'id': music.id,
            'name': music.name,
            'singer': music.singer,
            'description': music.description,
            'avatar': music.get_avatar_url() if music.avatar else None,
            'duration_time': music.duration_time.strftime('%H:%M:%S'),  # Convert TimeField to string
            'support': music.support,
            'mold': dict(music.choiceM)[music.mold],  # Get the readable choice label
            'MD5': music.MD5,
            'url': music.url,
            'is_upload': dict(music.choiceU)[music.is_upload],  # Get the readable choice label
            'audit_id': music.audit_id,
            'delete_mark': dict(music.choiceD)[music.delete_mark],  # Get the readable choice label
            'create_date': music.create_date.strftime('%Y-%m-%d'),
            'upload_time': music.upload_time.strftime('%Y-%m-%d %H:%M:%S'),
            'pid': music.pid,
            'uid': music.uid,
        }
        print(music_dict)
        userName = parentName = auditorName = ""
        if music.mold != 1:
            userName = models.sysUser.objects.filter(id=music.uid, delete_mark=0).first().username
            if music.mold == 3:
                parentName = models.sysMusic.objects.filter(id=music.pid, delete_mark=0).first().name
        if music.is_upload != 0:
            userid = models.auditLog.objects.filter(id=music.audit_id, delete_mark=0).first().audit_id
            if userid != 0:
                # userid==0:未审核
                auditorName = models.sysUser.objects.filter(id=userid, delete_mark=0).first().username
        music_dict["userName"] = userName
        music_dict['parentName'] = parentName
        music_dict['auditorName'] = auditorName
        list.append(music_dict)
    return JsonResponse({'code': 200, 'musicList': list, 'msg': "success"})


@csrf_exempt
def serSongLists(request):
    data = json.loads(request.body)
    serName = data.get('serNameS', None)
    serDesc = data.get('serDescS', None)
    serUpload = data.get('serUploadS', None)
    orderBy = data.get('orderByS', None)
    ascOrderBy = data.get('ascOrderByS', None)
    songList = models.songList.objects.filter(name__icontains=serName,
                                              description__icontains=serDesc).all()
    if orderBy == '':
        songList = songList.order_by('id')
    else:
        if ascOrderBy == 'asc':
            songList = songList.order_by(orderBy)
        else:
            songList = songList.order_by('-'+orderBy)

    if serUpload == 4:
        songList = songList.filter(is_upload__lt=serUpload)
    else:
        songList = songList.filter(is_upload=serUpload)

    list = []
    for song in songList:
        song_dict = {
            'id': song.id,
            'name': song.name,
            'description': song.description,
            'number': song.number,
            'avatar': song.get_avatar_url() if song.avatar else None,
            'support': song.support,
            'is_upload': dict(song.choiceU)[song.is_upload],  # Get the readable choice label
            'audit_id': song.audit_id,
            'delete_mark': dict(song.choiceD)[song.delete_mark],  # Get the readable choice label
            'create_date': song.create_date.strftime('%Y-%m-%d'),
            'upload_date': song.upload_date.strftime('%Y-%m-%d'),
            'uid': song.uid,
        }
        userName = models.sysUser.objects.filter(id=song.uid, delete_mark=0).first().username
        song_dict["userName"] = userName
        list.append(song_dict)
    return JsonResponse({'code': 200, 'songLists': list, 'msg': "success"})

@csrf_exempt
def delById(request):
    data = json.loads(request.body)
    type = data.get('getType', None)
    id = data.get('id', None)
    print(type,id)
    # 删除用户
    if type == 'user':
        user = models.sysUser.objects.filter(id=id, delete_mark=0).first()
        if user is None:
            return JsonResponse({'code': 501, 'msg': "该用户已不存在"})
        user.delete_mark = 1
        user.save()
        return JsonResponse({'code': 200, 'msg': "success"})
    # 删除评论
    elif type == 'comment':
        comment = models.sysComment.objects.filter(id=id, delete_mark=0).first()
        if comment is None:
            return JsonResponse({'code': 501, 'msg': "该评论已不存在"})
        comment.delete_mark = 1
        comment.save()
        return JsonResponse({'code': 200, 'msg': "success"})
    # 删除歌单，我创建的
    elif type == 'mine':
        songList = models.songList.objects.filter(id=id, delete_mark=0).first()
        if songList is None:
            return JsonResponse({'code': 501, 'msg': "该歌单已不存在"})
        songList.delete_mark = 1
        songList.save()
        return JsonResponse({'code': 200, 'msg': "success"})
    # 删除歌单，我收藏的
    elif type == 'collect':
        userId = data.get('userId', None)
        songListUser = models.listUser.objects.filter(user_id=userId, songList_id=id, delete_mark=0).first()
        if songListUser is None:
            return JsonResponse({'code': 501, 'msg': "该收藏歌单已不存在"})
        songListUser.delete_mark = 1
        songListUser.save()
        return JsonResponse({'code': 200, 'msg': "success"})
    # 删除歌曲,我创建/上传的
    elif type == 'music':
        userId = data.get('userId', None)
        music = models.sysMusic.objects.filter(id=id, delete_mark=0, uid=userId).first()
        if music is None:
            return JsonResponse({'code': 501, 'msg': "不是您的歌曲，无权删除"})
        music.delete_mark = 1
        music.save()
        return JsonResponse({'code': 200, 'msg': "success"})
    # 删除歌单中的歌曲
    elif type == 'musicCollect':
        sid = data.get('sid')
        listMusic = models.listMusic.objects.filter(music_id=id, songList_id=sid, delete_mark=0).first()
        if listMusic is None:
            return JsonResponse({'code': 501, 'msg': "该歌曲已不再歌单中"})
        return JsonResponse({'code': 200, 'msg': "success"})

@csrf_exempt
def supportById(request):
    data = json.loads(request.body)
    id = data.get("id")
    type = data.get("type", None)
    # 点赞评论
    if type == 'comment':
        comment = models.sysComment.objects.filter(id=id, delete_mark=0).first()
        if comment is None:
            return JsonResponse({'code': 501, 'msg': "该评论不存在"})
        comment.support += 1
        comment.save()
        return JsonResponse({'code': 200, 'msg': "success"})
    # 点赞歌单
    elif type == 'songList':
        songList = models.songList.objects.filter(id=id, delete_mark=0).first()
        if songList is None:
            return JsonResponse({'code': 501, 'msg': "该歌单不存在"})
        songList.support += 1
        songList.save()
        return JsonResponse({'code': 200, 'msg': "success"})
    # 点赞歌曲
    elif type == 'music':
        music = models.sysMusic.objects.filter(id=id, delete_mark=0).first()
        if music is None:
            return JsonResponse({'code': 501, 'msg': "该音乐不存在"})
        music.support += 1
        music.save()
        return JsonResponse({'code': 200, 'msg': "success"})