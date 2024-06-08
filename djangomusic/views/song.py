import hashlib
import json
import os
from datetime import timezone

from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from djangomusic import models
from newdemo import settings


def listHistoryById(request):
    # 传参user,我听过的，通过user.id在userMusic得到music_id（orderby -listen_time）列表，通过music_id查询musicList
    data = json.loads(request.body)
    userId = data.get('userId')
    uMusics = models.userMusic.objects.filter(user_id=userId).order_by('-listen_time').all()[:30]
    musicList = []
    for uMusic in uMusics:
        musicList.append(models.sysMusic.objects.filter(id=uMusic.id).first())
    return JsonResponse({'code': 200, 'musicList': musicList, 'msg': "success"})


def clearHistoryById(request):
    # 传参user,清空我听过的，通过user.id在userMusic删除
    data = json.loads(request.body)
    userId = data.get('userId')
    models.userMusic.objects.filter(user_id=userId).all().delete()
    return JsonResponse({'code': 200, 'msg': "success"})


def serMusic(request):
    # 传参type+serName,根据type查询具体的榜单
    # type = “search" 搜索 根据serMusic搜索serName name/singer serName="",则展示全部is_upload=3   【delete_mark=0】
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

@csrf_exempt
def addMusic(request):
    # 传参post表单+user+（pid)只有ai生成有       get/post区分 查看/修改
    # mold = 1 网络音乐，先查看MD5是否重复，若重复直接返回msg="已存在"
    #                  若不存在，则将post内容写入，add_sysMusic,
    #                                          add_auditLog, sysMusic:is_upload=1,audit_id=id  return msg="已上传，等待审核"
    # mold = 2 源音频，先查看MD5是否重复, post内容写入add_sysMusic，is_upload=0,uid=user.id return msg="源音频已上传，等待下一步"
    # mold = 3 ai音乐，post内容写入add_sysMusic，is_upload=0,pid = pid ,uid=user.id return msg="AI歌曲创建成功，等待下一步"
    # 表单提交
    if request.method == 'POST':
        # 第一步：上传音乐
        if request.POST.get('type') == 'music':
            music_file = request.FILES.get('musicFile')
            # Calculate MD5 hash of the music file
            music_hasher = hashlib.md5()
            for chunk in music_file.chunks():
                music_hasher.update(chunk)
            music_md5_hash = music_hasher.hexdigest()
            obj = models.sysMusic.objects.filter(MD5=music_md5_hash).first()
            # 已存在该文件
            if obj is not None:
                if obj.is_delete == 1:
                    # 已删除，修改删除字段
                    obj.update(is_delete=0)
                return JsonResponse({'code': 502, 'msg': "该音乐已存在，不必上传"})
            # Save music file
            music_file_path = os.path.join(settings.MEDIA_ROOT, 'music')
            if not os.path.exists(music_file_path):
                os.makedirs(music_file_path)

            music_path = os.path.join(music_file_path, music_md5_hash + '.mp3')
            with open(music_path, 'wb') as f:
                for chunk in music_file.chunks():
                    f.write(chunk)

            # Generate URL for music
            url = request.build_absolute_uri(settings.MEDIA_URL + 'music/' + music_md5_hash + '.mp3')
            # Save music info to database
            music = models.sysMusic.objects.create(
                duration_time='00:00',
                MD5=music_md5_hash,
                url=url
            )
            return JsonResponse({'code': 200, 'mid': music.id, 'msg': "等待进一步补充信息"})
        # 第二步：补充信息
        elif request.POST.get('type') == 'post':
            userId = request.POST.get('userId')
            mid = request.POST.get('mid')
            name = request.POST.get('name')
            singer = request.POST.get('singer')
            description = request.POST.get('description')
            duration = request.POST.get('duration')
            mold = request.POST.get('mold')
            pid = request.POST.get('pid')
            music = models.sysMusic.objects.filter(id=mid).first()

            if request.FILES.get('avatar'):
                avatar = request.FILES.get('avatar')
                avatar_directory = os.path.join(settings.MEDIA_ROOT, 'avatars/music', mid)
                if not os.path.exists(avatar_directory):
                    os.makedirs(avatar_directory)
                original_avatar_path = music.avatar.path
                # 删除原始头像文件
                if os.path.exists(original_avatar_path):
                    os.remove(original_avatar_path)
                avatar_path = os.path.join(avatar_directory, avatar.name)
                with open(avatar_path, 'wb') as f:
                    for chunk in avatar.chunks():
                        f.write(chunk)
                music.avatar = 'avatars/music/{}/{}'.format(mid, avatar.name)

            # Save music info to database
            music.name = name
            music.singer = singer
            music.description = description
            music.duration_time = duration
            music.mold = int(mold)
            if mold == '1':
                # 已有审核数据
                if music.is_upload == 1 and music.audit_id != 0:
                    return JsonResponse({'code': 504, 'msg': "正在审核中，不可修改"})
                audit = models.auditLog.objects.create(music_id=mid)
                music.audit_id = audit.id
                msg = "已上传，等待审核"
            elif mold == '2':
                music.is_upload = 0
                music.uid = userId
                msg = "源音频已上传，等待下一步"
            elif mold == '3':
                music.is_upload = 0
                music.uid = userId
                music.pid = pid
                msg = "AI歌曲创建成功，等待下一步"
            else:
                return JsonResponse({'code': 504, 'msg': "mold错误"})
            music.save()
            return JsonResponse({'code': 200, 'mid': music.id, 'msg': msg})
        elif request.POST.get('type') == 'get':
            mid = request.POST.get('mid')
            music = models.sysMusic.objects.filter(id=mid, delete_mark=0).first()
            if music is None:
                return JsonResponse({'code': 501, 'msg': "该歌曲文件不存在"})
            audit = models.auditLog.objects.filter(id=music.audit_id).first()
            auditResult = audit.get_audit_state_display()
            auditContent = audit.msg_content
            music_data = {
                'id': music.id,
                'name': music.name,
                'singer': music.singer,
                'avatar': music.get_avatar_url() if music.avatar else None,
                'duration': music.duration_time.strftime('%H:%M:%S'),
                'description': music.description,
                'support': music.support,
                'mold': music.get_mold_display(),
                'url': music.url,
                'is_upload': music.is_upload,
                'audit_id': music.audit_id,
                'pid': music.pid,
                'uid': music.uid,
                'auditResult': auditResult,
                'auditContent': auditContent,
            }
            return JsonResponse({'code': 200, 'music': music_data, 'msg': "success"})


def createMusic(request):
    # 传参源music的id 生成ai
    return None

def uploadMusic(request):
    # 传参music的id ai有单独的上传按钮，修改sysMusic is_upload为1，add_auditLog，改sysMusic audit_id=id
    data = json.loads(request.body)
    mid = data.get('mid')
    music = models.sysMusic.objects.filter(id=mid, delete_mark=0).first()
    if music is None:
        return JsonResponse({'code': 501, 'msg': "音乐不存在"})
    audit = models.auditLog.objects.create(music_id=mid, audit_mold=0)
    music.update(is_upload=1, audit_id=audit.id)
    return JsonResponse({'code': 200, 'msg': "success"})


def delMuisc(request):
    # 传参music的id 删除音乐，修改sysMusic的delete_mark=1
    #  mid+sid       自己的该歌单中删除某歌曲   listMusic delete_mark=1
    data = json.loads(request.body)
    mid = data.get('mid')
    sid = data.get('sid')
    type = data.get('type')
    if type == "delm":
        music = models.sysMusic.objects.filter(id=mid, delete_mark=0).first()
        if music is None:
            return JsonResponse({'code': 501, 'msg': "音乐不存在"})
        music.update(delete_mark=1)
        return JsonResponse({'code': 200, 'msg': "success"})
    models.listMusic.objects.filter(music_id=mid, songList_id=sid).delete()
    return JsonResponse({'code': 200, 'msg': "success"})


def supportMusic(request):
    # 传参music的id 点赞音乐，修改sysMusic的 support+1
    data = json.loads(request.body)
    mid = data.get('mid')
    music = models.sysMusic.objects.filter(id=mid, delete_mark=0).first()
    if music is None:
        return JsonResponse({'code': 501, 'msg': "音乐不存在"})
    music.support += 1
    music.save()
    return JsonResponse({'code': 200, 'msg': "success"})

def collectMusicToList(request):
    # 传参music的id+songList的id 收藏音乐，新增listMusic数据，修改songList的数量 number+1
    data = json.loads(request.body)
    mid = data.get('mid')
    sid = data.get('sId')
    music = models.sysMusic.objects.filter(id=mid, delete_mark=0, is_upload=3)
    if music is None:
        return JsonResponse({'code': 503, 'msg': "该歌曲未上传，不可收藏"})
    models.listMusic.objects.create(music_id=mid, songList_id=sid)
    songList = models.listMusic.objects.filter(id=sid, delete_mark=0).first()
    if songList is None:
        return JsonResponse({'code': 501, 'msg': "歌单不存在"})
    songList.number += 1
    songList.save()
    return JsonResponse({'code': 200, 'msg': "success"})


def listenedMusic(request):
    # 传参music的id+user 听过，add_userMusic或修改听歌时间
    data = json.loads(request.body)
    mid = data.get('mid')
    userId = data.get('userId')
    uMusic = models.userMusic.objects.filter(user_id=userId, music_id=mid)
    if uMusic is None:
        models.userMusic.objects.create(user_id=userId, music_id=mid)
    else:
        uMusic[0].update(listen_time=timezone.now().timestamp())

