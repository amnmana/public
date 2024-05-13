from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import User

class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Enter Email!')
        user = self.model(
            username=username,
            email=email,
            is_active=True  # ユーザーをアクティブに設定
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.model(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)  # デフォルトをTrueに変更
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ユーザーとの関連付け
    destination = models.CharField(max_length=100)
    startDate = models.DateField()  # DateTimeField から DateField に変更する場合
    endDate = models.DateField()

    def __str__(self):
        return f"{self.destination} from {self.startDate} to {self.endDate}"

class Location(models.Model):
    name = models.CharField(max_length=128, verbose_name="名称")
    address = models.TextField(verbose_name="住所")
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)  # この行を追加

    def __str__(self):
        return self.name

class TestModel(models.Model):
    pass

class Picture(models.Model):
    image = models.ImageField(upload_to='images/')
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)  # この行を追加

class Item(models.Model):
    name = models.CharField(max_length=100)
    checked = models.BooleanField(default=False)
    trip = models.ForeignKey('Trip', on_delete=models.CASCADE, null=True)  # NULLを許容する

    def __str__(self):
        return self.name

class Memo(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)  # この行を確認
    category = models.CharField(max_length=128)
    detail = models.TextField()

    def __str__(self):
        return self.category