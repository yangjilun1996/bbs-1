from django.db import models

'''
用户
 ^
 |  多对多
 v
角色
 ^
 |  多对多
 v
权限


权限分配情况
    dev
        admin: 'del_user'
        admin: 'del_post'
        admin: 'del_comment'

    abc
        manager: 'add_post'
        manager: 'del_post'
        manager: 'add_comment'
        manager: 'del_comment'

    xyz
        user: 'add_comment'
        user: 'add_post'
'''


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

    def roles(self):
        '''用户所绑定的所有角色'''
        # 通过关系表筛选关联的 role_id
        relations = UserRoleRelation.objects.filter(uid=self.id).only('role_id')
        role_id_list = [r.role_id for r in relations]

        return Role.objects.filter(id__in=role_id_list)

    def has_perm(self, perm_name):
        for role in self.roles():
            for perm in role.perms():
                if perm.name == perm_name:
                    return True
        return False


class UserRoleRelation(models.Model):
    uid = models.IntegerField()
    role_id = models.IntegerField()

    @classmethod
    def add_role_to_user(cls, uid, role_name):
        role = Role.objects.get(name=role_name)
        return cls.objects.create(uid=uid, role_id=role.id)

    @classmethod
    def del_role_from_user(cls, uid, role_name):
        role = Role.objects.get(name=role_name)
        cls.objects.get(uid=uid, role_id=role.id).delete()


class Role(models.Model):
    '''
    角色表

        admin   管理员
        manager 版主
        user    用户
    '''
    name = models.CharField(max_length=16, unique=True)

    def perms(self):
        '''角色所绑定的所有权限'''
        # 通过关系表筛选关联的 perm_id
        relations = RolePermRelation.objects.filter(role_id=self.id).only('perm_id')
        perm_id_list = [r.perm_id for r in relations]

        return Permission.objects.filter(id__in=perm_id_list)


class RolePermRelation(models.Model):
    role_id = models.IntegerField()
    perm_id = models.IntegerField()

    @classmethod
    def add_perm_to_role(cls, role_id, perm_name):
        '''给角色添加权限'''
        perm = Permission.objects.get(name=perm_name)
        return cls.objects.create(role_id=role_id, perm_id=perm.id)

    @classmethod
    def del_perm_from_role(cls, role_id, perm_name):
        '''删除角色绑定的一个权限'''
        perm = Permission.objects.get(name=perm_name)
        cls.objects.get(role_id=role_id, perm_id=perm.id).delete()


class Permission(models.Model):
    '''
    权限表

        add_post    发表帖子
        del_post    删除帖子
        add_comment 发表评论
        del_comment 删除评论
        del_user    删除用户
    '''
    name = models.CharField(max_length=16, unique=True)
#数据库查询数据
def get_reset_record():
    q = db.session.query(ResetField)
    records = q.filter_by(exec_user='yangjilun').order_by(ResetField.exec_time).all()
    records = records[::-1]
    return records
