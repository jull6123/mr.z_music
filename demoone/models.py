from django.db import models


class sysuser(models.Model):
    username = models.CharField(max_length=20, verbose_name="用户名")
    password = models.CharField(max_length=20, verbose_name="密码")
    email = models.EmailField(null=True, blank=True, verbose_name="邮箱")
    description = models.TextField(null=True, blank=True, verbose_name="个性标签")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # avatar = models.ImageField(null=True, blank=True, upload_to='avatars', verbose_name="头像")
    choice = (
        (0, "admin"),
        (1, "user"),
    )
    role = models.IntegerField(choices=choice, default=1, verbose_name="角色标签,0:admin,1:user")

# class role(models.Model):
#     role = models.CharField(verbose_name="角色标签")


class sysmusic(models.Model):
    name = models.CharField(max_length=10, verbose_name="文件名")
    size = models.IntegerField(verbose_name="文件大小")
    description = models.TextField(null=True, blank=True, verbose_name="音乐描述")
    choice_type = (
        (0, "mp3"),
        (1, "txt"),
    )
    types = models.IntegerField(choices=choice_type, default=0, verbose_name="文件类型,0:mp3,1:txt")
    choice_mold = (
        (1, "net_music"),
        (2, "it_music"),
        (3, "txt_music"),
    )
    mold = models.IntegerField(choices=choice_mold, default=1, verbose_name="音乐来源,0:net_music,1:it_music,2:txt_music")
    MD5 = models.CharField(max_length=40, verbose_name="MD5")
    url = models.URLField()
    is_delete = models.BooleanField(default=False)
    upload_date = models.DateField(auto_now=True, verbose_name="记录修改时间")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    pid = models.IntegerField(default=0, verbose_name="若为算法生成的文件，则记录对应的源文件id")
    uid = models.IntegerField(default=0, verbose_name="该文件对应的用户id")