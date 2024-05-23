import os

from django.http import FileResponse
from django.shortcuts import render, HttpResponse, redirect
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
import hashlib
from django.shortcuts import render
from urllib.parse import unquote

from demoone import models

# 导入form包
from django import forms

from django.conf import settings


# 这里规定models的类，在用modelform的时候必须要有这么一个类
class MusicModelForm(forms.ModelForm):

    # 校验用的，我们在这里重写下它
    # name = forms.CharField()

    class Meta:
        # 这里把它实例化是为了之后可以挑选自己想要的字段而不是所有字段
        model = models.sysmusic
        # 相当于在User里面取元素，注意这里的变量名一定是fields。
        # User类里面的东西在ModelForm里面几乎都能取出来。
        fields = ["name", "description", "types", "mold"]
        # 当然可以这么做，但是会比较麻烦，要一条一条写过去，所以我们采取后面的重定义类的方法
        # widgets = {
        #     # 默认插件是input标签，我们通过控制插件做到对几个输入框的控制
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"})
        # }
    # 这部分一定要注意def的缩进
    def __init__(self, *args, **kwargs):
        # 重定义初始化方法，并执行继承父类的方法
        super().__init__(*args, **kwargs)
        # 相当于在这里把field里所有的要定义的字段的名字都拿到，这部分是根据源码改编的，不能改name，
        # 循环找到所有的插件并给它添加class=form-control的样式
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

def musicAdd(request):
    uid = request.GET.get('nid')
    print(uid)
    if request.method == "GET":
        return render(request, 'music/musicAdd.html', {"nid": request.GET.get('nid'), "error_msg": ""})
    if request.FILES['file']:
        uploaded_file = request.FILES['file']
        name = request.POST['name']
        types = request.POST['types']
        mold = request.POST['mold']
        description = request.POST['description']
        size = uploaded_file.size / 1024  # Converting bytes to KB
        md5 = calculate_md5(uploaded_file)
        print(name, types, mold, description, size, uid)
        print(md5)
        # 先通过MD5与uid查找是否该用户已上传过此文件
        obj = models.sysmusic.objects.filter(MD5=md5, uid=uid).first()
        # 已存在该文件
        if obj is not None:
            # 未删除，提示已存在
            if obj.is_delete == 0:
                return render(request, 'music/musicAdd.html', {"nid": request.GET.get('nid'), "error_msg": "该文件已上传"})
            # 已删除，更新该条数据信息为新的post信息
            models.sysmusic.objects.filter(MD5=md5, uid=uid).first().update(is_delete=0, name=name, description=description, upload_date=timezone.now())
        # 不存在该文件，则生成url，保存文件至后台，并创建新的数据
        url = handle_uploaded_file(uploaded_file)
        models.sysmusic.objects.create(name=name, types=types, mold=mold, description=description, size=size, url=url, MD5=md5, upload_date=timezone.now(), create_time=timezone.now(), uid=uid)
        return redirect('/music/list/?nid='+str(uid))


def handle_uploaded_file(file):
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    return fs.url(filename)


def calculate_md5(file):
    md5 = hashlib.md5()
    for chunk in file.chunks():
        md5.update(chunk)
    return md5.hexdigest()


def musicEdit(request, nid):
    # nid为要编辑的音乐文件的id
    # uid为登录用户id
    uid = request.GET.get("uid")
    # 先获取需要编辑的那一行的数据
    row = models.sysmusic.objects.filter(id=nid).first()
    if request.method == "GET":
        form = MusicModelForm(instance=row)
        return render(request, "music/musicEdit.html", {"nid": uid, "form": form})
    # 校验
    # 这里一定要加instance，不然的话会再添加一个修改后的数据。instance相当于告诉Django你要再哪里更新
    form = MusicModelForm(data=request.POST, instance=row)
    if form.is_valid():
        form.save()
        return redirect('/music/list/?nid='+str(uid))
    return render(request, "music/musicEdit.html", {"nid": uid, "form": form})


def musicList(request):
    # nid为登录的用户的id
    nid = request.GET.get("nid")
    user = models.sysuser.objects.filter(id=nid).first()
    print(nid, user)
    # role==1 表示为用户，查看该登录用户的所有音乐
    if user.role:
        music_list = models.sysmusic.objects.filter(is_delete=False, uid=nid).order_by('create_time')
    # role==0 表示为管理员，可查看所有音乐,包含已删除的
    else:
        music_list = models.sysmusic.objects.all().order_by('create_time')
    for music in music_list:
        musicurl = unquote(music.url)
        print(musicurl, music.url)
    return render(request, 'music/musicList.html', {"user": user, 'music_list': music_list})


def musicDelete(request):
    # uid为登录的用户id，nid为要删除的音乐的id
    uid = request.GET.get('uid')
    nid = request.GET.get("nid")
    models.sysmusic.objects.filter(id=nid).update(is_delete=True)
    return redirect('/music/list/?nid='+str(uid))


def down(request):
    uid = request.GET.get('uid')
    nid = request.GET.get("nid")
    music = models.sysmusic.objects.filter(id=nid, uid=uid).first()
    if music is not None:
        # 获取音乐文件的路径，这里假设音乐文件是存储在本地的
        musicurl = unquote(music.url)
        music_file_path = "E:/program/newdemo/" + musicurl
        print(musicurl, music_file_path)
        return FileResponse(open(music_file_path, 'rb'), as_attachment=True, filename=f"{music.name}.mp3")
    return HttpResponse("下载错误")



def change(request):
    uid = request.GET.get('uid')
    nid = request.GET.get("nid")
    # music = models.sysmusic.objects.filter(id=nid, is_delete=False).first()
    # music.url得到文件，算法函数
    # 将生成结果新增至数据库中，更新相应的pid=nid,uid=uid

    return redirect('/music/list/?nid='+str(uid))


def theList(request):
    uid = request.GET.get('uid')
    nid = request.GET.get("nid")
    user = models.sysuser.objects.filter(id=uid).first()
    from django.db.models import Q
    # 使用 Q 对象创建过滤条件
    filter_condition = Q(id=nid, is_delete=False) | Q(pid=nid, is_delete=False)
    # 查询集合并
    list = models.sysmusic.objects.filter(filter_condition).order_by('upload_date')
    return render(request, "music/musictheList.html", {"user": user, "music_list": list})


def search(request, uid):
    if request.method == "GET":
        queryname = request.GET.get("queryname")
        querydesc = request.GET.get("querydesc")
        querytypes = request.GET.get("querytypes")
        querymolds = request.GET.get("querymolds")
        print(queryname, querydesc, querytypes, querymolds)
        user = models.sysuser.objects.filter(id=uid).first()
        if user.role:
            music_list = models.sysmusic.objects.filter(name__icontains=queryname, description__icontains=querydesc, types=querytypes, mold=querymolds, is_delete=False, uid=uid).order_by('upload_date')
        else:
            music_list = models.sysmusic.objects.filter(name__icontains=queryname, description__icontains=querydesc, types=querytypes, mold=querymolds).order_by('upload_date')
        for music in music_list:
            print(music.name, music.description)
        user = models.sysuser.objects.filter(id=uid).first()
        return render(request, 'music/musicList.html', {"user": user, "music_list": music_list})



