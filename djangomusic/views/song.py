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
    # 传参post表单+user+（pid)只有ai生成有       get/post区分 查看/修改
    # mold = 1 网络音乐，先查看MD5是否重复，若重复直接返回msg="已存在"
    #                  若不存在，则将post内容写入，add_sysMusic,
    #                                          add_auditLog, sysMusic:is_upload=1,audit_id=id  return msg="已上传，等待审核"
    # mold = 2 源音频，先查看MD5是否重复, post内容写入add_sysMusic，is_upload=0,uid=user.id return msg="源音频已上传，等待下一步"
    # mold = 3 ai音乐，post内容写入add_sysMusic，is_upload=0,pid = pid ,uid=user.id return msg="AI歌曲创建成功，等待下一步"
    # 表单提交
#     import os
# import hashlib
# from django.conf import settings
# from django.http import JsonResponse
# from .models import Music
#
# def upload_music(request):
#     if request.method == 'POST' and request.FILES.get('avatar') and request.FILES.get('musicFile'):
#         name = request.POST.get('name')
#         singer = request.POST.get('singer')
#         avatar = request.FILES['avatar']
#         music_file = request.FILES['musicFile']
#
#         # Calculate MD5 hash of the music file
#         music_hasher = hashlib.md5()
#         for chunk in music_file.chunks():
#             music_hasher.update(chunk)
#         music_md5_hash = music_hasher.hexdigest()
#
#         # Save music file
#         music_file_path = os.path.join(settings.MEDIA_ROOT, 'music', music_md5_hash + '.mp3')
#         with open(music_file_path, 'wb') as f:
#             for chunk in music_file.chunks():
#                 f.write(chunk)
#
#         # Save avatar file
#         avatar_path = os.path.join(settings.MEDIA_ROOT, 'avatars', avatar.name)
#         with open(avatar_path, 'wb') as f:
#             for chunk in avatar.chunks():
#                 f.write(chunk)
#
#         # Save music info to database
#         music = Music.objects.create(
#             name=name,
#             singer=singer,
#             avatar=avatar_path,
#             music_file=music_file_path,
#             music_md5_hash=music_md5_hash
#         )
#
#         # Generate URL for music
#         music_url = request.build_absolute_uri(settings.MEDIA_URL + 'music/' + music_md5_hash + '.mp3')
#
#         return JsonResponse({'status': 'success', 'music_url': music_url})
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Invalid request or missing files'})
    data = json.loads(request.body)
    user = data.get('user')
    musicList = data.get('musicList')
    pid = data.get('pid')
    if request.method == 'GET':
        music = models.sysMusic.objects.filter(id=musicList.id).first()
        if music:
            return JsonResponse({'code': 200, 'music': music, 'msg': "success"})
        return JsonResponse({'code': 501, 'msg': "歌曲存在"})
    elif request.method == 'POST':

        # 更新用户信息
        user.description = data.get('description', user.description)
        if user.role is not None:
            user.role = data.get('role', user.role)
        # 更新头像
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
        # 保存更新后的用户信息
        user.save()
        return JsonResponse({'code': 200, 'user': user, 'msg': '用户信息更新成功'})
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

