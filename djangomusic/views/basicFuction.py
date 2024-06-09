import json
import os

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from djangomusic import models
from newdemo import settings


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
        return JsonResponse({'code': 501, 'msg': "账号或密码错误"})
    elif len(user) > 1:
        return JsonResponse({'code': 502, 'msg': "查询到多个账号"})
    else:
        user = user[0]
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'description': user.description,
            'avatar': user.get_avatar_url() if user.avatar else None,
            'role': user.role,
            'create_time': user.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'delete_mark': user.delete_mark,
        }
        return JsonResponse({'code': 200, 'msg': "success", 'user': user_data})


@csrf_exempt
def register(request):
    # 传参username+password+email
    # email是否存在 存在则报错，不存在则add_sysUser
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    print(username, password, email)
    if models.sysUser.objects.filter(email=email).first() is not None:
        return JsonResponse({'code': 502, 'msg': "该邮箱已注册"})
    if models.sysUser.objects.filter(username=username).first() is not None:
        return JsonResponse({'code': 502, 'msg': "该用户名已存在"})
    models.sysUser.objects.create(username=username, password=password, email=email)
    return JsonResponse({'code': 200, 'msg': "success"})


@csrf_exempt
def updateperson(request):
    # get 时，user信息由浏览器存储，可直接回显在前端
    if request.method == 'POST':
        uid = request.POST.get('id')
        user = models.sysUser.objects.filter(id=uid).first()
        if request.POST.get('type') == 'pwd':
            if user.password != request.POST.get('oldPassword'):
                return JsonResponse({'code': 502, 'msg': "原密码填写错误"})
            else:
                user.password = request.POST.get('password')
                user.save()
                user_data = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'description': user.description,
                    'avatar': user.get_avatar_url() if user.avatar else None,
                    'role': user.role,
                    'create_time': user.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'delete_mark': user.delete_mark,
                }
                return JsonResponse({'code': 200, 'user': user_data, 'msg': "修改密码：success"})
        elif request.POST.get('type') == 'edit':
            description = request.POST.get('description')
            role = request.POST.get('role')
            if request.FILES.get('avatar'):
                avatar = request.FILES['avatar']
                # Save avatar file
                avatar_directory = os.path.join(settings.MEDIA_ROOT, 'avatars/user', uid)
                print(avatar_directory)
                if not os.path.exists(avatar_directory):
                    os.makedirs(avatar_directory)

                original_avatar_path = user.avatar.path
                print(user.avatar)
                # 删除原始头像文件
                if os.path.exists(original_avatar_path):
                    os.remove(original_avatar_path)
                avatar_path = os.path.join(avatar_directory, avatar.name)
                with open(avatar_path, 'wb') as f:
                    for chunk in avatar.chunks():
                        f.write(chunk)
                user.avatar = 'avatars/{}/{}'.format(uid, avatar.name)

            # Save music info to database
            user.description = description
            user.role = int(role)
            user.save()
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'description': user.description,
                'avatar': user.get_avatar_url() if user.avatar else None,
                'role': user.role,
                'create_time': user.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'delete_mark': user.delete_mark,
            }
            return JsonResponse({'code': 200, 'user': user_data, 'msg': "修改个人信息：success"})
        else:
            if user is None:
                return JsonResponse({'code': 501, 'msg': "查找用户不存在"})
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'description': user.description,
                'avatar': user.get_avatar_url() if user.avatar else None,
                'role': user.role,
                'create_time': user.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'delete_mark': user.delete_mark,
            }
            return JsonResponse({'code': 200, 'user': user_data, 'msg': "查找用户信息：success"})

