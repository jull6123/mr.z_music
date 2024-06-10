import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from djangomusic import models

@csrf_exempt
def getAuditList(request):
    # 传参user+type+state delete_mark=0
    # state = “代办"  查询auditLog audit_state=0
    # state = “已完成"  查询auditLog audit_id=user.id audit_state>2
    # type = “music"  查询auditLog audit_mold=0 得到music_id对应的sysMusic name……
    # type = “songList"  查询auditLog audit_mold=1 得到songList_id对应的songList name……
    data = json.loads(request.body)
    userId = data.get("userId")
    type = data.get('type')
    state = data.get('state')
    # 审核记录+审核数据id+name+url+type+所属者
    list = []
    if type == 'music':
        if state == "unAudited":
            auditList = models.auditLog.objects.filter(audit_state__lte=2, delete_mark=0, audit_mold=0).all()
        elif state == "Audited":
            auditList = models.auditLog.objects.filter(audit_id=userId, audit_state__gte=3, delete_mark=0, audit_mold=0).all()

        for auditM in auditList:
            music = models.sysMusic.objects.filter(id=auditM.music_id, delete_mark=0).first()
            if music is not None:
                # Create a dictionary to hold the modified data
                audit_dict = {
                    'id': auditM.id,
                    'songList_id': auditM.songList_id,
                    'audit_mold': dict(auditM.choiceM)[auditM.audit_mold],
                    'music_id': auditM.music_id,
                    'audit_id': auditM.audit_id,
                    'audit_state': auditM.audit_state,
                    'audit_state_msg': dict(auditM.choiceS)[auditM.audit_state],
                    'msg_content': auditM.msg_content,
                    'delete_mark': dict(auditM.choiceD)[auditM.delete_mark],
                    "iid": music.id,
                    "name": music.name,
                    "url": music.url
                }
                if music.mold == 1:
                    audit_dict["type"] = "music_net"
                    audit_dict["owner"] = music.singer
                    audit_dict["ownerId"] = 0
                elif music.mold == 2:
                    audit_dict["type"] = "music_ori"
                    owner = models.sysUser.objects.filter(id=music.uid).first()
                    if owner:
                        audit_dict["owner"] = owner.name
                        audit_dict["ownerId"] = owner.id
                elif music.mold == 3:
                    audit_dict["type"] = "music_ai"
                    owner = models.sysUser.objects.filter(id=music.uid).first()
                    if owner:
                        audit_dict["owner"] = owner.name
                        audit_dict["ownerId"] = owner.id
            list.append(audit_dict)
    elif type == 'songList':
        if state == "unAudited":
            auditList = models.auditLog.objects.filter(audit_state__lte=2, delete_mark=0, audit_mold=1).all()
        elif state == "Audited":
            auditList = models.auditLog.objects.filter(audit_id=userId, audit_state__gte=3, delete_mark=0, audit_mold=1).all()
        for auditS in auditList:
            songList = models.songList.objects.filter(id=auditS.songList_id, delete_mark=0).first()
            if songList is not None:
                audit_dict = {
                    "id": auditS.id,
                    'songList_id': auditS.songList_id,
                    'audit_mold': dict(auditS.choiceM)[auditS.audit_mold],
                    'music_id': auditS.music_id,
                    'audit_id': auditS.audit_id,
                    'audit_state': auditS.audit_state,
                    'audit_state_msg': dict(auditS.choiceS)[auditS.audit_state],
                    'msg_content': auditS.msg_content,
                    'delete_mark': dict(auditS.choiceD)[auditS.delete_mark],
                    "iid": songList.id,
                    "name": songList.name,
                    "url": '',
                    'type': "songList",
                    'owner': models.sysUser.objects.filter(id=songList.uid).first().username,
                    'ownerId': models.sysUser.objects.filter(id=songList.uid).first().id,
                }
            list.append(audit_dict)
    return JsonResponse({'code': 200, 'auditList': list, 'msg': "success"})


@csrf_exempt
def auditById(request):
    # 传参user+id+type
    # type = “music"  根据auditLog的id找到music_id得到sysMusic,展示歌曲内容查看界面
    # type = “songList" 根据auditLog的id找到songList_id（审核顺序）
    #                   1. 根据listMusic查询歌单对应的musicList name……  group by is_upload    addSongList/
    #                   2. 根据songList查询歌单信息name……         addMusic/
    data = json.loads(request.body)
    id = data.get('id')
    print(id)
    audit = models.auditLog.objects.filter(id=id, delete_mark=0).first()
    if audit is None:
        return JsonResponse({'code': 501, 'msg': "不存在该审核记录"})
    iid = data.get('iid')
    type = data.get('type')
    owner = data.get('owner')
    ownerId = data.get('ownerId')
    if type == "songList":
        audit.audit_state = 2
        audit.save()
        songList = models.songList.objects.filter(id=iid, delete_mark=0).first()
        if songList is None:
            return JsonResponse({'code': 501, 'msg': "歌单不存在"})
        songList.is_upload = 1
        songList.save()
        song_data = {
            'aid': id,
            'id': songList.id,
            'name': songList.name,
            'description': songList.description,
            'avatar': songList.get_avatar_url() if songList.avatar else None,
            'owner': owner,
            'uid': ownerId,
            'type': type,
            'audit_state': dict(audit.choiceS)[audit.audit_state],
            'content': audit.msg_content,
        }
        return JsonResponse({'code': 200, 'songList': song_data, 'msg': "success"})
    music = models.sysMusic.objects.filter(id=iid, delete_mark=0).first()
    if music is None:
        return JsonResponse({'code': 501, 'msg': "歌曲不存在"})
    music.is_upload = 1
    music.save()
    audit.audit_state = 1
    audit.save()
    if music.uid != 0:
        userName = models.sysUser.objects.filter(id=music.uid, delete_mark=0).first().username
    else:
        userName = '无所有者'
    music_data = {
        'aid': id,
        'id': music.id,
        'name': music.name,
        'singer': music.singer,
        'description': music.description,
        'avatar': music.get_avatar_url() if music.avatar else None,
        'mold': music.get_mold_display(),
        'url': music.url,
        'uid': music.uid,
        'userName': userName,
        'type': type,
        'audit_state': dict(audit.choiceS)[audit.audit_state],
        'content': audit.msg_content,
    }
    return JsonResponse({'code': 200, 'music': music_data, 'msg': "success"})


@csrf_exempt
def auditResult(request):
    # 传参user+总id+type+state+content state:3/4
    # type = “music"  查询auditLog 总id对应的audit_mold,相同则修改audit_state+msg_content   歌曲审核
    #                                由于歌单添加歌曲时只能添加已上传的歌曲
    # type = “songList" 查询auditLog  修改audit_state+msg_content
    data = json.loads(request.body)
    userId = data.get('userId')
    aid = data.get('aid')
    type = data.get('type')
    state = data.get('state')
    if state == "failure":
        stateInt = 3
    else:
        stateInt = 4
    content = data.get('content')
    print(state, stateInt)

    audit = models.auditLog.objects.filter(id=aid, delete_mark=0).first()
    if audit is None:
        return JsonResponse({'code': 501, 'msg': "该审核不存在"})
    print(audit)
    audit.audit_state = stateInt
    print(audit.audit_state)
    audit.msg_content = content
    print(audit.msg_content)
    audit.audit_id = userId
    print(audit.audit_id)
    return JsonResponse({'code': 501, 'msg': "该审核不存在"})
    audit.save()


    if type == "songList":
        songList = models.songList.objects.filter(id=audit.songList_id, delete_mark=0).first()
        if songList is None:
            return JsonResponse({'code': 501, 'msg': "所审核的歌单已删除"})
        songList.is_upload = stateInt-1
        songList.save()
        return JsonResponse({'code': 200, 'msg': "success"})
    music = models.sysMusic.objects.filter(id=audit.music_id, delete_mark=0).first()
    if music is None:
        return JsonResponse({'code': 501, 'msg': "所审核的音乐已删除"})
    music.is_upload = stateInt-1
    if music.mold == 1:
        music.uid = 0
    music.save()
    return JsonResponse({'code': 200, 'msg': "success"})
