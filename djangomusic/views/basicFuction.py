import json
import os

from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from djangomusic import models
from newdemo import settings


# # Create your models here.
# #  文件上传
# def user_directory_path(instance, filename):
#     ext = filename.split('.')[-1]
#     filename = '{}.{}'.format(uuid.uuid4().hex[:8], ext)
#     # return the whole path to the file
#     return "{0}/{1}/{2}".format(instance.user.id, "avatar", filename)
#
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     avatar = models.ImageField(upload_to=user_directory_path, verbose_name="头像")


@csrf_exempt
def login(request):
    # 传参username+password
    # 前端实现：user.role=0------admin
    #         user.role=1------user
    #         user.role=2------audit
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    print(username, password)
    user = models.sysUser.objects.filter(username=username, password=password)
    if user is None or len(user) == 0 or len(user) > 1:
        return JsonResponse({'code': 501, 'msg': "账号不存在"})
    elif len(user) > 1:
        return JsonResponse({'code': 502, 'msg': "查询到多个账号"})
    else:
        return JsonResponse({'code': 200, 'msg': "success", 'user': user[0]})


@csrf_exempt
def register(request):
    # 传参username+password+email
    # email是否存在 存在则报错，不存在则add_sysUser
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    print(username, password, email)
    if models.sysUser.objects.filter(email=email) is not None:
        return JsonResponse({'code': 502, 'msg': "该邮箱已注册"})
    if models.sysUser.objects.filter(username=username) is not None:
        return JsonResponse({'code': 502, 'msg': "该用户名已存在"})
    models.sysUser.objects.create(username=username, password=password, email=email)
    return JsonResponse({'code': 200, 'msg': "success"})


@csrf_exempt
def updateperson(request):
    # get 时，user信息由浏览器存储，可直接回显在前端
    if request.method == 'POST':
        if request.FILES.get('avatar'):
            user = request.POST.get('user')
            username = request.POST.get('username')
            password = request.POST.get('password')
            description = request.POST['description']
            avatar = request.FILES['avatar']

            # Save avatar file
            avatar_path = os.path.join(settings.MEDIA_ROOT, 'avatars/' + user.id, avatar.name)
            with open(avatar_path, 'wb') as f:
                for chunk in avatar.chunks():
                    f.write(chunk)
            if username != user.username:
                if models.sysUser.objects.filter(username=user.username) is not None:
                    return JsonResponse({'code': 502, 'msg': "该用户名已存在，请更改"})
            # Save music info to database
            user.update(username=username, password=password, description=description, avatar=avatar_path)
            return JsonResponse({'code': 200, 'user': user, 'msg': "success"})
        else:
            return JsonResponse({'code': 506, 'msg': 'Invalid request or missing files'})


