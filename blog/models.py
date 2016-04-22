from django.db import models
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class Article(models.Model):
    title_en = models.CharField(max_length=50, primary_key=True)
    title_cn = models.CharField(max_length=50)
    url = models.URLField()
    content_md = models.TextField()
    content_html = models.TextField()
    content_text = models.TextField()
    tags = models.CharField(max_length=50, verbose_name="标签组", help_text="务必用英文逗号分割")
    view_times = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now=False)
    update_time = models.DateTimeField(auto_now_add=True)
    comment_times = models.IntegerField(default=0)
    auther = models.CharField(max_length=100, default='高亮')

    def get_tags(self):
        tags_list = self.tags.split(',')
        while '' in tags_list:
            tags_list.remove('')
        return tags_list

    class Meta:
        ordering = ['create_time']
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.title_cn


class Message(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=20)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password):
        if not email:
            raise ValueError("no email address")
        if not name:
            raise ValueError('no name')

        user = self.model(email=self.normalize_email(email), name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):

        user = self.create_user(email=email,
                                name=name,
                                password=password,
                                )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    def get_short_name(self):
        return ' '

    email = models.EmailField(
        verbose_name='email address',
        unique=True,
    )
    name = models.CharField(max_length=10, unique=True)
    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.name

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.name + ' ' + self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Comment(models.Model):
    author = models.ForeignKey(MyUser)
    content = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now=True)
    floor = models.IntegerField()
