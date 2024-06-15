import json
from itertools import chain

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from djangomusic import models

@csrf_exempt
def getComments(request):
    # 传参type+music_id,根据type查询具体的list
    # type = “hot" 热门评论 查询sysComment support前五 delete_mark=0+其user_id对应的用户name,avater
    # type = “new" 最新评论 查询sysComment create_time前30 delete_mark=0 pid=0 +其user_id对应的用户name,avater
    #                     循环：根据查询到的id查询pid=id(查询子评论)delete_mark=0 得到commentList +其user_id对应的用户name,avater
    #                     return ????
    data = json.loads(request.body)
    mid = data.get("musicId")
    listHot=[]
    listNew=[]
    commentListHot = models.sysComment.objects.filter(music_id=mid, delete_mark=0).order_by('-support', '-create_time').all()[:5]
    commentListNew = models.sysComment.objects.filter(music_id=mid, delete_mark=0, pid=0).order_by('-create_time').all()[:30]
    sub_comments = []
    for comment in commentListNew:
        sub_comments += models.sysComment.objects.filter(pid=comment.id, delete_mark=0).all()
    commentListNew = list(chain(commentListNew, sub_comments))

    for comment in commentListHot:
        comment_data = {
            'id': comment.id,
            'user_id': comment.user_id,
            'music_id': comment.music_id,
            'content': comment.content,
            'support': comment.support,
            'delete_mark': dict(comment.choiceD)[comment.delete_mark],  # Get the readable choice label
            'create_time': comment.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'pid': comment.pid,
        }
        user = models.sysUser.objects.filter(id=comment.user_id, delete_mark=0).first()
        if user is not None:
            comment_data['username'] = user.username
            comment_data['avatar'] = user.get_avatar_url() if user.avatar else None,
        listHot.append(comment_data)

    for comment in commentListNew:
        comment_data = {
            'id': comment.id,
            'user_id': comment.user_id,
            'music_id': comment.music_id,
            'content': comment.content,
            'support': comment.support,
            'delete_mark': dict(comment.choiceD)[comment.delete_mark],  # Get the readable choice label
            'create_time': comment.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'pid': comment.pid,
        }
        user = models.sysUser.objects.filter(id=comment.user_id, delete_mark=0).first()
        if user is not None:
            comment_data['username'] = user.username
            comment_data['avatar'] = user.get_avatar_url() if user.avatar else None,
        listNew.append(comment_data)

    return JsonResponse({'code': 200, 'commentListHot': listHot, 'commentListNew': listNew, 'msg': "success"})

@csrf_exempt
def addComment(request):
    # 传参sysComment的content+user+music_id+pid(针对子评论）评论回复 add_sysComment
    data = json.loads(request.body)
    mid = data.get("mid")
    userId = data.get("userId")
    content = data.get("content")
    pid = data.get("pid")
    comment = models.sysComment.objects.create(user_id=userId, music_id=mid, content=content, pid=pid)
    comment_data = {
        'id': comment.id,
        'user_id': comment.user_id,
        'music_id': comment.music_id,
        'content': comment.content,
        'support': comment.support,
        'delete_mark': dict(comment.choiceD)[comment.delete_mark],  # Get the readable choice label
        'create_time': comment.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        'pid': comment.pid,
    }
    return JsonResponse({'code': 200, 'comment': comment_data, 'msg': "success"})
