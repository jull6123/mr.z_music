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
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        print(username, password)
        try:
            user = models.sysUser.objects.get(username=username, password=password)
            userData = user.to_dict()
            return JsonResponse({'code': 200, 'user': userData, 'msg': ""})
        except models.sysUser.DoesNotExist:
            return JsonResponse({'code': 506, 'msg': '不存在，账户或密码错误'})

@csrf_exempt
def register(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    print(username, password, email)
    try:
        user1 = models.sysUser .objects.filter(email=email).first()
        if user1 is None:
            user3 = models.sysUser .objects.create(username=username, password=password)
            return JsonResponse({'code': 200, 'msg': ""})
        else:
            for user2 in user1:
                print(user2)
            return JsonResponse({'code': 506, 'mag':'该邮箱已被注册'})
    except models.sysUser.DoesNotExist:
        # 用户不存在或密码错误，返回错误信息
        return JsonResponse({'code': 506, 'msg': '账户或密码错误'})

@csrf_exempt
def updateperson(request):
    data = json.loads(request.body)
    uid = data.get('id')
    if request.method == 'GET':
        try:
            user = get_object_or_404(models.sysUser, id=uid)
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
        except ObjectDoesNotExist:
            return JsonResponse({'code': 404, 'msg': '用户不存在'})

    elif request.method == 'POST':
        try:
            user = models.sysUser.objects.get(id=uid)
            data = json.loads(request.body)
            # 更新用户信息
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            user.description = data.get('description', user.description)
            # 更新头像
            if 'avatar' in request.FILES:
                user.avatar = request.FILES['avatar']
            # 保存更新后的用户信息
            user.save()
            return JsonResponse({'code': 200, 'msg': '用户信息更新成功'})
        except ObjectDoesNotExist:
            return JsonResponse({'code': 404, 'msg': '用户不存在'})


def getTest(request):
    user = request.GET.get('user')
    print(user)
    music_list = models.sysUser.objects.get(id=user).music.all()
    print(music_list)
    return JsonResponse({'code': 200, 'music_list': music_list})
