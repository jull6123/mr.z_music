from django.db import models


class sysUser(models.Model):
    username = models.CharField(max_length=20, verbose_name="用户名")
    password = models.CharField(max_length=20, verbose_name="密码")
    email = models.EmailField(null=False, blank=False, verbose_name="邮箱")
    description = models.TextField(null=True, blank=True, verbose_name="个性标签")
    avatar = models.ImageField(null=True, blank=True, upload_to='avater', verbose_name="头像")
    choiceR = (
        (0, "admin"),
        (1, "user"),
    )
    role = models.IntegerField(choices=choiceR, default=1, verbose_name="角色标签,0:admin,1:user")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    choiceD = (
        (0, "未删"),
        (1, "已删"),
    )
    delete_mark = models.IntegerField(choices=choiceD, default=0, verbose_name="删除标志,0:未删,1:已删")


class songList(models.Model):
    name = models.CharField(max_length=20, verbose_name="歌单名")
    description = models.TextField(null=True, blank=True, verbose_name="歌单描述")
    duration_time = models.TimeField(verbose_name="歌曲时长")
    avatar = models.ImageField(null=True, blank=True, upload_to='avater', verbose_name="歌单图片展示")
    support = models.IntegerField(default=0, verbose_name="点赞数")
    choiceU = (
        (0, "未上传"),
        (1, "已上传"),
    )
    is_upload = models.IntegerField(choices=choiceU, default=1, verbose_name="上传标识，针对AI歌曲")
    choiceD = (
        (0, "未删"),
        (1, "已删"),
    )
    delete_mark = models.IntegerField(choices=choiceD, default=0, verbose_name="删除标志,0:未删,1:已删")
    create_date = models.DateField(auto_now_add=True, verbose_name="创建时间")
    upload_date = models.DateField(auto_now=True, verbose_name="上传时间")
    uid = models.IntegerField(verbose_name="歌单创建用户id")


class sysMusic(models.Model):
    name = models.CharField(max_length=20, verbose_name="歌曲名")
    singer = models.CharField(max_length=20, verbose_name="歌手")
    description = models.TextField(null=True, blank=True, verbose_name="音乐描述")
    avatar = models.ImageField(null=True, blank=True, upload_to='avater', verbose_name="歌曲图片展示")
    duration_time = models.TimeField(verbose_name="歌曲时长")
    support = models.IntegerField(default=0, verbose_name="点赞数")
    choiceM = (
        (1, "网络音乐"),
        (2, "源音频"),
        (3, "AI音频"),
    )
    mold = models.IntegerField(choices=choiceM, default=1, verbose_name="音乐来源")
    MD5 = models.CharField(null=False, max_length=40, verbose_name="MD5，唯一标识")
    url = models.URLField(null=False, verbose_name="音频的url地址")
    choiceU = (
        (0, "未上传"),
        (1, "已上传"),
    )
    is_upload = models.IntegerField(choices=choiceU, default=1, verbose_name="上传标识，针对AI歌曲")
    choiceD = (
        (0, "未删"),
        (1, "已删"),
    )
    delete_mark = models.IntegerField(choices=choiceD, default=0, verbose_name="删除标志,0:未删,1:已删")
    create_date = models.DateField(auto_now_add=True, verbose_name="创建时间")
    upload_time = models.DateTimeField(auto_now=True, verbose_name="上传时间，新歌榜需针对上传时间进行排序")
    pid = models.IntegerField(default=0, verbose_name="针对AI音频，记录源音频id")
    uid = models.IntegerField(default=0, verbose_name="针对AI音频，记录创建用户id")


class listMusic(models.Model):
    songList_id = models.IntegerField(verbose_name="歌单id")
    music_id = models.IntegerField(verbose_name="歌曲id")
    choiceD = (
        (0, "未删"),
        (1, "已删"),
    )
    delete_mark = models.IntegerField(choices=choiceD, default=0, verbose_name="删除标志,0:未删,1:已删")

class listUser(models.Model):
    user_id = models.IntegerField(verbose_name="用户id")
    songList_id = models.IntegerField(verbose_name="歌单id")
    choiceD = (
        (0, "未删"),
        (1, "已删"),
    )
    delete_mark = models.IntegerField(choices=choiceD, default=0, verbose_name="删除标志,0:未删,1:已删")

class sysComment(models.Model):
    user_id = models.IntegerField(verbose_name="评论者id")
    music_id = models.IntegerField(verbose_name="歌曲id")
    content = models.TextField(verbose_name="评论内容")
    support = models.IntegerField(default=0, verbose_name="点赞数")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="评论创建时间")
    choiceD = (
        (0, "未删"),
        (1, "已删"),
    )
    delete_mark = models.IntegerField(choices=choiceD, default=0, verbose_name="删除标志,0:未删,1:已删")
    pid = models.IntegerField(default=0, verbose_name="父级评论id")


class userMusic(models.Model):
    user_id = models.IntegerField(verbose_name="用户id")
    music_id = models.IntegerField(verbose_name="歌曲id")
    listen_time = models.DateTimeField(auto_now=True, verbose_name="听歌时间")