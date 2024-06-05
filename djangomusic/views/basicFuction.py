import json
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from djangomusic import models

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
    data = json.loads(request.body)
    user = data.get('user')
    if request.method == 'GET':
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'description': user.description,
            'avatar': user.avatar.url if user.avatar else None,
            'role': user.get_role_display(),
            'create_time': user.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'delete_mark': user.get_delete_mark_display(),
        }
        return JsonResponse({'code': 200, 'user': user_data, 'msg': ""})
    elif request.method == 'POST':
        data = json.loads(request.body)
        # 更新用户信息
        user.description = data.get('description', user.description)
        if user.role is not None:
            user.role = data.get('role', user.role)
        # 更新头像
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
        # 保存更新后的用户信息
        user.save()
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'description': user.description,
            'avatar': user.avatar.url if user.avatar else None,
            'role': user.get_role_display(),
            'create_time': user.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'delete_mark': user.get_delete_mark_display(),
        }
        return JsonResponse({'code': 200, 'user': user_data, 'msg': '用户信息更新成功'})


def getTest(request):
    user = request.GET.get('user')
    print(user)
    music_list = models.sysUser.objects.get(id=user).music.all()
    print(music_list)
    return JsonResponse({'code': 200, 'music_list': music_list})
