from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=64, verbose_name='用户名')
    email = models.EmailField(max_length=128, verbose_name='邮箱')
    role = models.ManyToManyField('Role')
    usergroup = models.ForeignKey('UserGroup')

    def __str__(self):
        return self.username


class UserGroup(models.Model):
    title = models.CharField(max_length=64, verbose_name='用户组名')

    def __str__(self):
        return self.title


class Role(models.Model):
    title = models.CharField(max_length=64, verbose_name='用户角色名')

    def __str__(self):
        return self.title
