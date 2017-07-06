from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models


class Token(models.Model):
    email = models.EmailField()
    uid = models.CharField(max_length=255)


class ListUserManager(BaseUserManager):
    """ListUser's objects"""
    def create_user(self, email):
        ListUser.objects.create(email=email)

    def create_superuser(self, email, password):
        self.create_user(email)


class ListUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(primary_key=True)
    USERNAME_FIELD = 'email'

    objects = ListUserManager()

    @property
    def is_staff(self):
        return self.email == 'zxy@example.com'

    @property
    def is_active(self):
        return True
