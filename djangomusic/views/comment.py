import json

from django.http import JsonResponse

from djangomusic import models


def getComments(request):
    # 传参type+music_id,根据type查询具体的list
    # type = “hot" 热门评论 查询sysComment support前五 delete_mark=0+其user_id对应的用户name,avater
    # type = “new" 最新评论 查询sysComment create_time前30 delete_mark=0 pid=0 +其user_id对应的用户name,avater
    #                     循环：根据查询到的id查询pid=id(查询子评论)delete_mark=0 得到commentList +其user_id对应的用户name,avater
    #                     return ????
    data = json.loads(request.body)
    mid = data.get("mid")
    type = data.get("type")
    if type == "hot":
        commentList = models.sysComment.objects.filter(music_id=mid, delete_mark=0).order_by('-support').all()[
                      :5].order_by('-create_time')
    else:
        commentList = models.sysComment.objects.filter(music_id=mid, delete_mark=0, pid=0).order_by('-create_time').all()[:30]
        for comment in commentList:
            commentList.append(models.sysComment.objects.filter(pid=comment.id).all())
    for comment in commentList:
        cUser = models.sysUser.objects.filter(id=comment.user_id, delete_mark=0).first()
        if cUser is not None:
            comment.append(cUser.id)
            comment.append(cUser.name)
            comment.append(cUser.avatar)
    return JsonResponse({'code': 200, 'commentList': commentList, 'msg': "success"})


def addComment(request):
    # 传参sysComment的content+user+music_id+pid(针对子评论）评论回复 add_sysComment
    data = json.loads(request.body)
    mid = data.get("mid")
    user = data.get("user")
    content = data.get("content")
    pid = data.get("pid")
    if pid is None:
        models.sysComment.objects.create(user_id=user, music_id=mid, content=content)
    else:
        models.sysComment.objects.create(user_id=user, music_id=mid, content=content, pid=pid)
    return JsonResponse({'code': 200, 'msg': "success"})


def delComment(request):
    # 传参sysComment的id 删除评论 sysComment:delete_mark=1
    data = json.loads(request.body)
    cid = data.get("cid")
    comment = models.sysComment.objects.filter(id=cid, delete_mark=0).first()
    if comment is None:
        return JsonResponse({'code': 501, 'msg': "评论不存在"})
    comment.update(delete_mark=1)
    return JsonResponse({'code': 200, 'msg': "success"})


def supportComment(request):
    # 传参sysComment的id 点赞评论 sysComment:support+1
    data = json.loads(request.body)
    cid = data.get("cid")
    comment = models.sysComment.objects.filter(id=cid, delete_mark=0).first()
    if comment is None:
        return JsonResponse({'code': 501, 'msg': "评论不存在"})
    comment.support += 1
    comment.save()
    return JsonResponse({'code': 200, 'msg': "success"})