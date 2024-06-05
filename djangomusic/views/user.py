from django.shortcuts import render, HttpResponse, redirect
from django.utils import timezone
from djangomusic import models
import os

#
# # 导入form包
# from django import forms
# # 这里规定models的类，在用modelform的时候必须要有这么一个类
# class UserModelForm(forms.ModelForm):
#
#     # 校验用的，我们在这里重写下它
#     # name = forms.CharField()
#
#     class Meta:
#         # 这里把它实例化是为了之后可以挑选自己想要的字段而不是所有字段
#         model = models.sysuser
#         # 相当于在User里面取元素，注意这里的变量名一定是fields。
#         # User类里面的东西在ModelForm里面几乎都能取出来。
#         fields = ["username", "password", "email", "description", "role"]
#         # 当然可以这么做，但是会比较麻烦，要一条一条写过去，所以我们采取后面的重定义类的方法
#         # widgets = {
#         #     # 默认插件是input标签，我们通过控制插件做到对几个输入框的控制
#         #     "name": forms.TextInput(attrs={"class": "form-control"}),
#         #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
#         #     "age": forms.TextInput(attrs={"class": "form-control"})
#         # }
#     # 这部分一定要注意def的缩进
#     def __init__(self, *args, **kwargs):
#         # 重定义初始化方法，并执行继承父类的方法
#         super().__init__(*args, **kwargs)
#         # 相当于在这里把field里所有的要定义的字段的名字都拿到，这部分是根据源码改编的，不能改name，
#         # 循环找到所有的插件并给它添加class=form-control的样式
#         for name, field in self.fields.items():
#             if name == "password":
#                 field.widget.attrs = {"class": "form-control", "placeholder": field.label, "type": "password"}
#             field.widget.attrs = {"class": "form-control", "placeholder": field.label}
#
#
# # 添加用户modelform
# def userAdd(request):
#     nid = request.GET.get('nid')
#     error_msg = ""
#     if request.method == "GET":
#         form = UserModelForm()
#         return render(request, "user/userAdd.html", {"nid": nid, "form": form, "error_msg": error_msg})
#     # 与之前相比，这部分多了个数据的校验
#     form = UserModelForm(data=request.POST)
#     if form.is_valid():
#         # form.cleaned_data相当于是获取到了数据
#         print(form.cleaned_data)
#         # 在modelform中这句话可以替换掉之前的models.User.objects.create，目标的表就是Meta中的model的表
#         queryset = models.sysuser.objects.filter(email=form.cleaned_data["email"]).first()
#         if queryset is not None:
#             form = UserModelForm()
#             return render(request, "user/userAdd.html", {"nid": nid, "form": form, "error_msg": "该邮箱已注册"})
#         queryset = models.sysuser.objects.filter(username=form.cleaned_data["username"]).first()
#         if queryset is not None:
#             form = UserModelForm()
#             return render(request, "user/userAdd.html", {"nid": nid, "form": form, "error_msg": "用户名已存在，请修改"})
#         form.save()
#         models.sysuser.objects.filter(username=form.cleaned_data["username"]).update(create_time=timezone.now())
#         return redirect('/user/list/?nid='+str(nid))
#     return render(request, "user/userAdd.html", {"nid": nid, "form": form, "error_msg": error_msg})
#
#
# # 编辑用户
# def userEdit(request, nid):
#     uid = request.GET.get("uid")
#     # 先获取需要编辑的那一行的数据
#     row = models.sysuser.objects.filter(id=nid).first()
#     email = row.email
#     username = row.username
#     if request.method == "GET":
#         # 我们继续用之前的form
#         # 只要写上instance的对象，默认会把每一个值在value中显示出来 => 简单到有点害怕
#         form = UserModelForm(instance=row)
#         return render(request, "user/userEdit.html", {"nid": uid, "form": form})
#     # 校验
#     # 这里一定要加instance，不然的话会再添加一个修改后的数据。instance相当于告诉Django你要再哪里更新
#     form = UserModelForm(data=request.POST, instance=row)
#     if form.is_valid():
#         print(form.cleaned_data["username"], username)
#         if(form.cleaned_data["email"] != email):
#             queryset = models.sysuser.objects.filter(email=form.cleaned_data["email"]).first()
#             if queryset is not None:
#                 form = UserModelForm(instance=row)
#                 return render(request, "user/userEdit.html", {"nid": uid, "form": form, "error_msg": "修改后的邮箱已注册"})
#         if(form.cleaned_data["username"] != username):
#             queryset2 = models.sysuser.objects.filter(username=form.cleaned_data["username"]).first()
#             if queryset2 is not None:
#                 form = UserModelForm(instance=row)
#                 return render(request, "user/userEdit.html", {"nid": uid, "form": form, "error_msg": "修改后的用户名已注册"})
#         form.save()
#         # 上面的是批量保存，我们如果有其他的想保存的但是不在fields里面的（用户输入的值以外的），可以用以下方法。
#         # form.instance.字段名 = 值
#         return redirect('/user/list/?nid='+str(uid))
#     return render(request, "user/userEdit.html", {"nid": uid, "form": form})
#
#
# def userList(request):
#     nid = request.GET.get("nid")
#     user = models.sysuser.objects.filter(id=nid).first()
#     print(nid, user)
#     user_list = models.sysuser.objects.all()
#     return render(request, 'user/userList.html', {"user": user, 'user_list': user_list})
#
#
# def userDelete(request):
#     nid = request.GET.get("nid")
#     uid = request.GET.get("uid")
#     models.sysuser.objects.filter(id=nid).delete()
#     return redirect('/user/list/?nid='+str(uid))
#
#
# def search(request, uid):
#     if request.method == "GET":
#         queryname = request.GET.get("queryname")
#         queryemail = request.GET.get("queryemail")
#         querydesc = request.GET.get("querydesc")
#         print(queryname, queryemail, querydesc)
#         user_list = models.sysuser.objects.filter(username__icontains=queryname, email__icontains=queryemail, description__icontains=querydesc).order_by('create_time')
#         for user in user_list:
#             print(user.username, user.email, user.description)
#         user = models.sysuser.objects.filter(id=uid).first()
#         return render(request, 'user/userList.html', {"user": user, "user_list": user_list})