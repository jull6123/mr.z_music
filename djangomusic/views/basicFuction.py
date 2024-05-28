
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from djangomusic import models
from django.contrib.auth.models import User
import uuid

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
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = models.sysUser .objects.get(username=username, password=password)
    try:
        user = models.sysUser .objects.get(username=username, password=password)
        return JsonResponse({'success': True, 'user': user, 'msg': ""})
    except models.sysUser.DoesNotExist:
        # 用户不存在或密码错误，返回错误信息
        return JsonResponse({'success': False, 'msg': '账户或密码错误'})

@csrf_exempt
def register(request):

    return JsonResponse({'success': False, 'msg': '请求错误'})

@csrf_exempt
def updateperson(request):
    uid = request.POST.get('uid')
    try:
        user = models.sysUser.objects.get(id=uid)
        if(request.method == 'POST'):
            models.sysUser.objects.filter(id=uid).update(name=request.POST.get('name'))
            return JsonResponse({'success': True, 'msg': "修改成功"})
        return JsonResponse({'success': True, 'user': user, 'msg': ""})
    except models.sysuser.DoesNotExist:
        return JsonResponse({'success': False, 'msg': '用户不存在'})
