from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, username, fullname, password=None, **kwargs):
        if not username:
            raise ValueError("Users must have an username")

        user = self.model(username=username, fullname=fullname, **kwargs)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, fullname, password=None):
        user = self.create_user(
            username,
            password=password,
            fullname=fullname,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=10, unique=True)
    fullname = models.CharField(max_length=100)
    email = models.EmailField("email address", blank=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    student_class = models.ForeignKey(
        "StudentClass", on_delete=models.SET_NULL, null=True, blank=True
    )

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["fullname"]

    def __str__(self):
        return self.fullname

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Subject(models.Model):
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class StudentClass(models.Model):
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=10, blank=True)

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        ordering = ["name"]

    def __str__(self):
        return self.name
