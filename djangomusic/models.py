from django.db import models
MEDIA_ADDR = "http://localhost:9091/media/"

class sysUser(models.Model):
    username = models.CharField(max_length=20, verbose_name="用户名")
    password = models.CharField(max_length=20, verbose_name="密码")
    email = models.EmailField(null=False, blank=False, verbose_name="邮箱")
    description = models.TextField(null=True, blank=True, verbose_name="个性标签")
    avatar = models.ImageField(null=True, blank=True, upload_to='avater', verbose_name="头像")
    choiceR = (
        (0, "admin"),
        (1, "user"),
        (2, "auditor")
    )
    role = models.IntegerField(choices=choiceR, default=1, verbose_name="角色标签,0:admin,1:user")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    choiceD = (
        (0, "未删"),
        (1, "已删"),
    )
    delete_mark = models.IntegerField(choices=choiceD, default=0, verbose_name="删除标志,0:未删,1:已删")

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'description': self.description,
            'avatar': self.get_avatar_url() if self.avatar else None,
            'role': self.role,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'delete_mark': self.delete_mark,
        }

    def get_avatar_url(self):
        return MEDIA_ADDR + str(self.avatar)


class songList(models.Model):
    name = models.CharField(max_length=20, verbose_name="歌单名")
    description = models.TextField(null=True, blank=True, verbose_name="歌单描述")
    number = models.IntegerField(default=0, verbose_name="歌单含歌曲数量")
    avatar = models.ImageField(null=True, blank=True, upload_to='avater', verbose_name="歌单图片展示")
    support = models.IntegerField(default=0, verbose_name="点赞数")
    choiceU = (
        (0, "未上传"),
        (1, "审核中"),
        (2, "审核失败，无法上传"),
        (3, "审核成功，上传成功"),
    )
    is_upload = models.IntegerField(choices=choiceU, default=0, verbose_name="上传标识")
    audit_id = models.IntegerField(default=0, verbose_name="上传审核id")
    choiceD = (
        (0, "未删"),
        (1, "已删"),
    )
    delete_mark = models.IntegerField(choices=choiceD, default=0, verbose_name="删除标志,0:未删,1:已删")
    create_date = models.DateField(auto_now_add=True, verbose_name="创建时间")
    upload_date = models.DateField(auto_now=True, verbose_name="上传时间")
    uid = models.IntegerField(verbose_name="歌单创建用户id")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'number': self.number,
            'avatar': self.get_avatar_url() if self.avatar else None,
            'support': self.support,
            'is_upload': dict(self.choiceU)[self.is_upload],  # Get the readable choice label
            'audit_id': self.audit_id,
            'delete_mark': dict(self.choiceD)[self.delete_mark],  # Get the readable choice label
            'create_date': self.create_date.strftime('%Y-%m-%d'),
            'upload_date': self.upload_date.strftime('%Y-%m-%d'),
            'uid': self.uid,
        }

    def get_avatar_url(self):
        return MEDIA_ADDR + str(self.avatar)


class sysMusic(models.Model):
    name = models.CharField(max_length=20, verbose_name="歌曲名")
    singer = models.CharField(max_length=20, verbose_name="歌手")
    description = models.TextField(null=True, blank=True, verbose_name="音乐描述")
    avatar = models.ImageField(null=True, blank=True, upload_to='avater', verbose_name="歌曲图片展示")
    duration_seconds = models.IntegerField(default=0, verbose_name="歌曲时长（秒）")
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
        (1, "审核中"),
        (2, "审核失败，无法上传"),
        (3, "审核成功，上传成功"),
    )
    is_upload = models.IntegerField(choices=choiceU, default=1, verbose_name="上传标识，针对AI歌曲")
    audit_id = models.IntegerField(default=0, verbose_name="上传审核id")
    choiceD = (
        (0, "未删"),
        (1, "已删"),
    )
    delete_mark = models.IntegerField(choices=choiceD, default=0, verbose_name="删除标志,0:未删,1:已删")
    create_date = models.DateField(auto_now_add=True, verbose_name="创建时间")
    upload_time = models.DateTimeField(auto_now=True, verbose_name="上传时间，新歌榜需针对上传时间进行排序")
    pid = models.IntegerField(default=0, verbose_name="针对AI音频，记录源音频id")
    uid = models.IntegerField(default=0, verbose_name="针对AI音频，记录创建用户id")


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'singer': self.singer,
            'description': self.description,
            'avatar': self.get_avatar_url() if self.avatar else None,
            'duration_time': self.duration_time.strftime('%H:%M:%S'),  # Convert TimeField to string
            'support': self.support,
            'mold': dict(self.choiceM)[self.mold],  # Get the readable choice label
            'MD5': self.MD5,
            'url': self.url,
            'is_upload': dict(self.choiceU)[self.is_upload],  # Get the readable choice label
            'audit_id': self.audit_id,
            'delete_mark': dict(self.choiceD)[self.delete_mark],  # Get the readable choice label
            'create_date': self.create_date.strftime('%Y-%m-%d'),
            'upload_time': self.upload_time.strftime('%Y-%m-%d %H:%M:%S'),
            'pid': self.pid,
            'uid': self.uid,
        }

    def get_avatar_url(self):
        return MEDIA_ADDR + str(self.avatar)


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

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'music_id': self.music_id,
            'content': self.content,
            'support': self.support,
            'delete_mark': dict(self.choiceD)[self.delete_mark],  # Get the readable choice label
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'pid': self.pid,
        }


class userMusic(models.Model):
    user_id = models.IntegerField(verbose_name="用户id")
    music_id = models.IntegerField(verbose_name="歌曲id")
    listen_time = models.DateTimeField(auto_now=True, verbose_name="听歌时间")


class auditLog(models.Model):
    songList_id = models.IntegerField(default=0, verbose_name="歌单id")
    choiceM = (
        (0, "music"),
        (1, "songList"),
    )
    audit_mold = models.IntegerField(default=0, choices=choiceM, verbose_name="审核类型")
    music_id = models.IntegerField(default=0, verbose_name="歌曲id")
    audit_id = models.IntegerField(default=0, verbose_name="审核人id,便于查找审核记录")
    choiceS = (
        (0, "审核未开始"),
        (1, "歌曲审核中"),
        (2, "歌单审核中"),
        (3, "不予上传"),
        (4, "审核成功，可上传"),
    )
    audit_state = models.IntegerField(choices=choiceS, default=0, verbose_name="审核阶段")
    msg_content = models.TextField(verbose_name="审核结果")
    choiceD = (
        (0, "未删"),
        (1, "已删"),
    )
    delete_mark = models.IntegerField(choices=choiceD, default=0, verbose_name="删除标志,0:未删,1:已删")

    def to_dict(self):
        return {
            'id': self.id,
            'songList_id': self.songList_id,
            'audit_mold': dict(self.choiceM)[self.audit_mold],  # 将整数转换为对应的值
            'music_id': self.music_id,
            'audit_id': self.audit_id,
            'audit_state': dict(self.choiceS)[self.audit_state],  # 将整数转换为对应的值
            'msg_content': self.msg_content,
            'delete_mark': dict(self.choiceD)[self.delete_mark],  # 将整数转换为对应的值
        }

