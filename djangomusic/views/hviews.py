import json
from datetime import timezone

from django.shortcuts import render,  redirect
from djangomusic import models
from django.http import JsonResponse


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    username = request.POST.get("username")
    password = request.POST.get("pwd")
    queryset = models.sysuser.objects.filter(username=username, password=password).first()
    if queryset is not None:
        return redirect("/home/?nid="+str(queryset.id))
    return render(request, "login.html", {"error_msg": "用户名或密码错误"})


def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    username = request.POST.get("user")
    password = request.POST.get("pwd")
    email = request.POST.get("email")
    description = request.POST.get("desc")
    queryset = models.sysuser.objects.filter(email=email).first()
    if queryset is not None:
        return render(request, "register.html", {"error_msg": "该邮箱已注册"})
    queryset = models.sysuser.objects.filter(username=username).first()
    if queryset is not None:
        return render(request, "register.html", {"error_msg": "用户名已存在，请修改"})
    models.sysuser.objects.create(username=username, password=password, email=email, description=description)
    return redirect("/login/")


def person(request):
    nid = request.GET.get("nid")
    if request.method == "GET":
        row_data = models.sysuser.objects.filter(id=nid).first()
        return render(request, 'lay/person.html', {'row_data': row_data})
    desc = request.POST.get("desc")
    models.sysuser.objects.filter(id=nid).update(description=desc)
    queryset = models.sysuser.objects.filter(id=nid).first()
    return redirect("/home/?nid="+str(queryset.id))


def update(request):
    nid = request.GET.get("nid")
    if request.method == "GET":
        row_data = models.sysuser.objects.filter(id=nid).first()
        return render(request, 'lay/update.html', {'row_data': row_data})
    print(request.POST)
    oldpassword = request.POST.get("oldpwd")
    newpassword1 = request.POST.get("newpwd1")
    newpassword2 = request.POST.get("newpwd2")
    row_data = models.sysuser.objects.filter(id=nid).first()
    password = row_data.password
    if password == oldpassword:
        if newpassword1 is not None and newpassword2 is not None:
            if oldpassword != newpassword1:
                if newpassword1 == newpassword2:
                    models.sysuser.objects.filter(id=nid).update(password=newpassword1)
                    return redirect("/home/?nid="+str(nid))
                return render(request, "lay/update.html", {'row_data': row_data, "error_msg": "两次输入的密码不同，请重新输入"})
            return render(request, "lay/update.html", {'row_data': row_data, "error_msg": "新旧密码不能相同，请重新输入"})
        return render(request, "lay/update.html", {'row_data': row_data, "error_msg": "请输入修改后的密码"})
    return render(request, "lay/update.html", {'row_data': row_data, "error_msg": "旧密码不正确，请重新输入"})


def home(request):
    nid = request.GET.get("nid")
    queryset = models.sysuser.objects.filter(id=nid).first()
    print(queryset.role)
    # if queryset.role == 0:
    #     return render(request, "lay/layout.html", {"user": queryset})
    return render(request, "lay/layout.html", {"user": queryset})

