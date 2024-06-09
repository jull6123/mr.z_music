import json
import os

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from djangomusic import models
from newdemo import settings

@csrf_exempt
def serSongList(request):
    # 传参type+user+serSName,根据type查询具体的list
    # type = “search" 搜索 根据serSName搜索songList name/desc serSName="",则展示全部 is_upload=3   【delete_mark=0】
    # type = “mine" 我的歌单 查询songList uid=user.id delete_mark=0 的songList(不要求是否上传）
    # type = "collect" 我的收藏 查询listUser user_id=user.id delete_mark=0 的songList.idList，根据id查songList delete_mark=0 收藏的已上传
    # type = "hot" 热门歌单 查询songList is_upload=3 support前15 delete_mark=0 已上传，未删除
    data = json.loads(request.body)
    type = data.get('type')
    userId = data.get('userId')
    serSName = data.get('serSName')
    if type == 'get':
        listMine=[]
        songListMine = models.songList.objects.filter(name__icontains=serSName, uid=userId, delete_mark=0).order_by('-create_date').all()
        getsongAll(listMine, songListMine)
        listCollect=[]
        sids = models.listUser.objects.filter(user_id=userId, delete_mark=0).all()
        for sid in sids:
            songList = models.songList.objects.filter(id=sid.songList_id, name__icontains=serSName,  delete_mark=0).first()
            songList_data = {
                'id': songList.id,
                'name': songList.name,
                'description': songList.description,
                'number': songList.number,
                'support': songList.support,
                'is_upload': songList.is_upload,
                'is_upload_msg': dict(songList.choiceU)[songList.is_upload],
                'audit_id': songList.audit_id,
                'uid': songList.uid,
                'avatar': songList.get_avatar_url() if songList.avatar else None,
            }
            if songList.is_upload > 1:
                audit = models.auditLog.objects.filter(id=songList.audit_id, delete_mark=0).first()
                if audit is not None:
                    auditResult = audit.get_audit_state_display()
                    auditContent = audit.msg_content
                    songList_data.update({'auditResult': auditResult, 'auditContent': auditContent})
            listCollect.append(songList_data)
        return JsonResponse({'code': 200, 'listMine': listMine, 'listCollect': listCollect, 'msg': 'success'})
    elif type == 'hot':
        listHot = []
        songLists = models.songList.objects.filter(is_upload=3, delete_mark=0).order_by('-support').all()[:15]
        getsongAll(listHot, songLists)
    return JsonResponse({'code': 200, 'listHot': listHot, 'msg': "success"})


def getsongAll(list, songLists):
    for songList in songLists:
        songList_data = {
            'id': songList.id,
            'name': songList.name,
            'description': songList.description,
            'number': songList.number,
            'support': songList.support,
            'is_upload': songList.is_upload,
            'is_upload_msg': dict(songList.choiceU)[songList.is_upload],
            'audit_id': songList.audit_id,
            'uid': songList.uid,
            'avatar': songList.get_avatar_url() if songList.avatar else None,
        }
        if songList.is_upload > 1:
            audit = models.auditLog.objects.filter(id=songList.audit_id, delete_mark=0).first()
            if audit is not None:
                auditResult = audit.get_audit_state_display()
                auditContent = audit.msg_content
                songList_data.update({'auditResult': auditResult, 'auditContent': auditContent})
        list.append(songList_data)

@csrf_exempt
def addSongList(request):
    # 传参user+post内容， add_songList,uid=user.id return msg="创建成功"   get/post区分 查看/修改
    if request.method == 'POST':
        if request.POST.get('type') == 'edit':
            userId = request.POST.get('userId')
            sid = request.POST.get('sid')
            name = request.POST.get('name')
            description = request.POST.get('description')


            if sid == '0':
                songList = models.songList.objects.create(name=name, description=description, uid=userId)
            else:
                songList = models.songList.objects.filter(id=sid, delete_mark=0).first()

            if request.FILES.get('avatar'):
                avatar = request.FILES['avatar']
                # Save avatar file
                avatar_directory = os.path.join(settings.MEDIA_ROOT, 'avatars\songList', sid)
                print(avatar_directory)
                if not os.path.exists(avatar_directory):
                    os.makedirs(avatar_directory)

                if sid != '0':
                    original_avatar_path = songList.avatar.path
                    print(original_avatar_path)
                    # 删除原始头像文件
                    if os.path.exists(original_avatar_path):
                        os.remove(original_avatar_path)

                avatar_path = os.path.join(avatar_directory, avatar.name)
                with open(avatar_path, 'wb') as f:
                    for chunk in avatar.chunks():
                        f.write(chunk)
                songList.avatar = 'avatars/songList/{}/{}'.format(sid, avatar.name)

            # Save music info to database
            if sid != '0':
                songList.name = name
                songList.description = description
            songList.uid = userId
            songList.save()
            return JsonResponse({'code': 200, 'sid': songList.id, 'msg': "success"})
        elif request.POST.get('type') == 'get':
            sid = request.POST.get('sid')
            songList = models.songList.objects.filter(id=sid, delete_mark=0).first()
            if songList is None:
                return JsonResponse({'code': 501, 'msg': "该歌单不存在"})
            songList_data = {
                'id': songList.id,
                'name': songList.name,
                'description': songList.description,
                'number': songList.number,
                'support': songList.support,
                'is_upload': songList.is_upload,
                'is_upload_msg': dict(songList.choiceU)[songList.is_upload],
                'audit_id': songList.audit_id,
                'uid': songList.uid,
                'avatar': songList.get_avatar_url() if songList.avatar else None,
            }
            audit = models.auditLog.objects.filter(id=songList.audit_id).first()
            if audit is not None:
                auditResult = audit.get_audit_state_display()
                auditContent = audit.msg_content
                songList_data.update({'auditResult': auditResult, 'auditContent': auditContent})
            return JsonResponse({'code': 200, 'songList': songList_data, 'msg': "success"})

@csrf_exempt
def uploadSongList(request):
    # 传参songList的id 上传歌单 is_upload=1,add_auditLog,audit_id=id
    data = json.loads(request.body)
    sid = data.get('sid')
    songList = models.songList.objects.filter(id=sid, delete_mark=0).first()
    if songList is None:
        return JsonResponse({'code': 501, 'msg': "歌单不存在"})
    audits = models.auditLog.objects.filter(songList_id=songList.id, audit_mold=1, delete_mark=0).first()
    if audits is None:
        audit = models.auditLog.objects.create(songList_id=sid, audit_mold=1)
        print(audit)
    else:
        return JsonResponse({'code': 501, 'msg': "歌单已上传"})
    songList.is_upload = 1
    songList.audit_id = audit.id
    songList.save()
    return JsonResponse({'code': 200, 'msg': "success"})




def delSongList(request):
    # 传参songList的id+user+type 删除歌单 delete_mark=1
    # type = “mine" 我的歌单 查询songList(id) delete_mark=1
    # type = "collect" 我的收藏 查询listUser(songList_id+user_id) delete_mark=1
    data = json.loads(request.body)
    sid = data.get('sid')
    userId = data.get('userId')
    type = data.get('type')
    if type == 'mine':
        songList = models.songList.objects.filter(id=sid, delete_mark=0).first()
        if songList is None:
            return JsonResponse({'code': 501, 'msg': "歌单不存在"})
        songList.update(delete_mark=1)
        return JsonResponse({'code': 200, 'msg': "success"})
    songListUser = models.listUser.objects.filter(user_id=userId, songList_id=sid, delete_mark=0).first()
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
    userId = data.get('userId')
    models.listUser.objects.create(user_id=userId, songList_id=sid)
    return JsonResponse({'code': 200, 'msg': "success"})

@csrf_exempt
def getFormById(request):
    # 传参songList的id 正在播放/歌单查看 listMusic根据songList_id delete_mark=0得到music_ids 得到sysMusic的list
    data = json.loads(request.body)
    sid = data.get('sid')
    songList = models.songList.objects.filter(id=sid, delete_mark=0).first()
    songList_data = {
        'id': songList.id,
        'name': songList.name,
        'description': songList.description,
        'number': songList.number,
        'support': songList.support,
        'is_upload': songList.is_upload,
        'is_upload_msg': dict(songList.choiceU)[songList.is_upload],
        'audit_id': songList.audit_id,
        'uid': songList.uid,
        'avatar': songList.get_avatar_url() if songList.avatar else None,
    }
    audit = models.auditLog.objects.filter(id=songList.audit_id).first()
    if audit is not None:
        auditResult = audit.get_audit_state_display()
        auditContent = audit.msg_content
        songList_data.update({'auditResult': auditResult, 'auditContent': auditContent})
    return JsonResponse({'code': 200, 'songList': songList_data, 'msg': "success"})


@csrf_exempt
def getListById(request):
    # 传参songList的id 正在播放/歌单查看 listMusic根据songList_id delete_mark=0得到music_ids 得到sysMusic的list
    data = json.loads(request.body)
    sid = data.get('sid')
    mids = models.listMusic.objects.filter(songList_id=sid, delete_mark=0).all()
    print(mids)
    musicList = []
    for mid in mids:
        music = models.sysMusic.objects.filter(id=mid.music_id).first()
        music_data = {
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
            'is_upload_msg': dict(music.choiceU)[music.is_upload],
            'audit_id': music.audit_id,
            'delete_mark': dict(music.choiceD)[music.delete_mark],  # Get the readable choice label
            'create_date': music.create_date.strftime('%Y-%m-%d'),
            'upload_time': music.upload_time.strftime('%Y-%m-%d %H:%M:%S'),
            'pid': music.pid,
            'uid': music.uid,
        }
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
        music_data["userName"] = userName
        music_data['parentName'] = parentName
        music_data['auditorName'] = auditorName
        musicList.append(music_data)
    return JsonResponse({'code': 200, 'musicList': musicList, 'msg': "success"})