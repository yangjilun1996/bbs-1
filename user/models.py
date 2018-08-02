from django.db import models


class User(models.Model):
    SEX = (
        ('M', '男性'),
        ('F', '女性'),
        ('U', '保密'),
    )

    nickname = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=128)
    icon = models.ImageField()
    plt_icon = models.CharField(max_length=256, default='')
    age = models.IntegerField(default=18)
    sex = models.CharField(max_length=8, choices=SEX)

    @property
    def avatar(self):
        return self.icon.url if self.icon else self.plt_icon

    def has_perm(self, perm_name):
        need_perm = Permission.objects.get(name=perm_name)
        return self.perm.level >= need_perm.level


class UserRoleRelation(models.Model):
    uid = models.IntegerField()
    role_id = models.IntegerField()

    @classmethod
    def add_role_to_user(cls, uid, role_id):
        pass

    @classmethod
    def del_role_from_user(cls, uid, role_id):
        pass


class Role(models.Model):
    '''
    角色表

        admin   管理员
        manager 版主
        user    用户
    '''
    name = models.CharField(max_length=16, unique=True)


class RolePermRelation(models.Model):
    role_id = models.IntegerField()
    perm_id = models.IntegerField()

    @classmethod
    def add_perm_to_role(cls, role_id, perm_id):
        pass

    @classmethod
    def del_perm_from_role(cls, role_id, perm_id):
        pass


class Permission(models.Model):
    '''
    权限表

        add_post    发表帖子
        del_post    删除帖子
        add_comment 发表评论
        del_comment 删除评论
        dle_user    删除用户
    '''
    name = models.CharField(max_length=16, unique=True)
