
from django.http import FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from demoone import models

@csrf_exempt
def app(request):
    if request.method == 'POST':
        # if not request.META.get('HTTP_X_CSRFTOKEN'):
        #     return JsonResponse({'success': False, 'error_msg': 'CSRF验证失败'})

        # 获取POST请求中的用户名和密码
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(username, password)
        # 在数据库中查找用户
        try:
            user = models.sysuser.objects.get(username=username, password=password)
            # 找到用户，返回成功的响应
            return JsonResponse({'success': True})
        except models.sysuser.DoesNotExist:
            # 用户不存在或密码错误，返回错误信息
            return JsonResponse({'success': False, 'error_msg': '账户或密码错误'})

    # 如果不是POST请求，返回错误响应
    return JsonResponse({'success': False, 'error_msg': '请求方法错误'})