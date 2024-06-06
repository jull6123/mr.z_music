import json

from django.http import JsonResponse

from djangomusic import models


def getAuditList(request):
    # 传参user+type+state delete_mark=0
    # state = “代办"  查询auditLog audit_state=0
    # state = “已完成"  查询auditLog audit_id=user.id audit_state>2
    # type = “music"  查询auditLog audit_mold=0 得到music_id对应的sysMusic name……
    # type = “songList"  查询auditLog audit_mold=1 得到songList_id对应的songList name……
    data = json.loads(request.body)
    user = data.get("user")
    type = data.get('type')
    state = data.get('state')
    # 审核记录+审核数据id+name+url+type+所属者
    if state == "unAudited":
        if type == "music":
            auditList = models.auditLog.objects.filter(audit_state__lte=2, delete_mark=0, audit_mold=0).all()
            for auditM in auditList:
                music = models.sysMusic.objects.filter(id=auditM.music_id, delete_mark=0).first()
                if music is not None:
                    auditM.append(music.id, music.name, music.url)
                    if music.mold == 1:
                        auditM.append("music_net", music.singer)
                    elif music.mold == 3:
                        auditM.append("music_ai")
                        auditM.append(models.sysUser.objects.filter(id=music.uid).first().name)
        auditList = models.auditLog.objects.filter(audit_state__lte=2, delete_mark=0, audit_mold=1).all()
        for auditS in auditList:
            songList = models.songList.objects.filter(id=auditS.songList_id, delete_mark=0).first()
            if songList is not None:
                auditS.append(songList.id, songList.name, "", "song_list")
                auditS.append(models.sysUser.objects.filter(id=songList.uid).first().name)
    else:
        if type == "music":
            auditList = models.auditLog.objects.filter(audit_id=user.id, audit_state__gte=3, delete_mark=0, audit_mold=0).all()
            for auditM in auditList:
                music = models.sysMusic.objects.filter(id=auditM.music_id, delete_mark=0).first()
                if music is not None:
                    auditM.append(music.id, music.name, music.url)
                    if music.mold == 1:
                        auditM.append("music_net", music.singer)
                    elif music.mold == 3:
                        auditM.append("music_ai")
                        auditM.append(models.sysUser.objects.filter(id=music.uid).first().name)
        auditList = models.auditLog.objects.filter(audit_id=user.id, audit_state__gte=3, delete_mark=0, audit_mold=1).all()
        for auditS in auditList:
            songList = models.songList.objects.filter(id=auditS.songList_id, delete_mark=0).first()
            if songList is not None:
                auditS.append(songList.id, songList.name, "", "song_list")
                auditS.append(models.sysUser.objects.filter(id=songList.uid).first().name)
    return JsonResponse({'code': 200, 'auditList': auditList, 'msg': "success"})


def auditById(request):
    # 传参user+id+type
    # type = “music"  根据auditLog的id找到music_id得到sysMusic,展示歌曲内容查看界面
    # type = “songList" 根据auditLog的id找到songList_id（审核顺序）
    #                   1. 根据listMusic查询歌单对应的musicList name……  group by is_upload    addSongList/
    #                   2. 根据songList查询歌单信息name……         addMusic/
    data = json.loads(request.body)
    aid = data.get('aid')
    mid = data.get('mid')
    sid = data.get('sid')
    type = data.get('type')
    if type == "music":
        music = models.sysMusic.objects.filter(id=mid, delete_mark=0).first()
        if music is None:
            return JsonResponse({'code': 501, 'msg': "歌曲不存在"})
        return JsonResponse({'code': 200, 'music': music, 'msg': "歌曲不存在"})
    songList = models.songList.objects.filter(id=sid, delete_mark=0).first()
    if songList is None:
        return JsonResponse({'code': 501, 'msg': "歌单不存在"})
    return JsonResponse({'code': 200, 'songList': songList, 'msg': "success"})


def auditResult(request):
    # 传参user+总id+type+state+content state:3/4
    # type = “music"  查询auditLog 总id对应的audit_mold,相同则修改audit_state+msg_content   歌曲审核
    #                                由于歌单添加歌曲时只能添加已上传的歌曲
    # type = “songList" 查询auditLog  修改audit_state+msg_content
    data = json.loads(request.body)
    user = data.get('user')
    aid = data.get('aid')
    type = data.get('type')
    state = data.get('state')
    content = data.get('content')
    audit = models.auditLog.objects.filter(id=aid, delete_mark=0).first()
    if audit is None:
        return JsonResponse({'code': 501, 'msg': "该审核不存在"})
    if type == "music":
        music = models.sysMusic.objects.filter(id=audit.music_id, delete_mark=0).first()
        if music is None:
            return JsonResponse({'code': 501, 'msg': "所审核的音乐已删除"})
        music.update(is_upload=state-1)
        audit.update(audit_state=state, msg_content=content, audit_id=user.id)
        return {'code': 200, 'msg': "success"}
    songList = models.songList.objects.filter(id=audit.songList_id, delete_mark=0).first()
    if songList is None:
        return JsonResponse({'code': 501, 'msg': "所审核的歌单已删除"})
    songList.update(is_upload=state-1)
    audit.update(audit_state=state, msg_content=content, audit_id=user.id)
    return {'code': 200, 'msg': "success"}


def getauditResult(request):
    data = json.loads(request.body)
    id = data.get('id')
    type = data.get('type')
    if type == "music":
        audit = models.auditLog.objects.filter(music_id=id, delete_mark=0).first()
        if audit is None:
            return JsonResponse({'code': 501, 'msg': "审核记录不存在"})
        return JsonResponse({'code': 200, 'audit': audit, 'msg': "success"})
    audit = models.auditLog.objects.filter(songList_id=id, delete_mark=0).first()
    if audit is None:
        return JsonResponse({'code': 501, 'msg': "审核记录不存在"})
    return JsonResponse({'code': 200, 'audit': audit, 'msg': "success"})
    return None