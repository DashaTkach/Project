from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have an username')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        return self.get(username=username)


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=150, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class UserImages(models.Model):
    user_image = models.CharField(verbose_name='Фото')
    user = models.ForeignKey(User, verbose_name='Пользователь', related_name='user', blank=True,
                             on_delete=models.CASCADE)
    user_image_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Фотография пользователя'
        verbose_name_plural = 'Фотографии (пользователь)'


class UserPartFace(models.Model):
    user_part_face = models.CharField(verbose_name='Часть лица', max_length=50)
    user_image = models.ForeignKey(UserImages, verbose_name='Фото пользователя', related_name='image', blank=True,
                                   on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Часть лица пользователя'
        verbose_name_plural = 'Части лица (пользователь)'


class UserShades(models.Model):
    bcor_user_photo = models.PositiveIntegerField(verbose_name='Коор1_фото_пользователя')
    gcor_user_photo = models.PositiveIntegerField(verbose_name='Коор2_фото_пользователя')
    rcor_user_photo = models.PositiveIntegerField(verbose_name='Коор3_фото_пользователя')
    user_part_face = models.ForeignKey(UserPartFace, verbose_name='Часть лица пользователя', related_name='us_partface',
                                       blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Оттенок части лица пользователя'
        verbose_name_plural = 'Оттенки части лица (пользователь)'


class Posts(models.Model):
    post_image = models.CharField(verbose_name='Фото', max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Фотография из поста ВК'
        verbose_name_plural = 'Фотографии (пост ВК)'


class PartFace(models.Model):
    post_part_face = models.CharField(verbose_name='Часть лица', max_length=50)
    post = models.ForeignKey(Posts, verbose_name='Пост', related_name='post',
                             blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Часть лица фотографии поста'
        verbose_name_plural = 'Части лица (пост ВК)'


class Shades(models.Model):
    bcor_photo = models.PositiveIntegerField(verbose_name='Коор1_фото')
    gcor_photo = models.PositiveIntegerField(verbose_name='Коор2_фото')
    rcor_photo = models.PositiveIntegerField(verbose_name='Коор3_фото')
    part_face = models.ForeignKey(PartFace, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Оттенок части лица (пост ВК)'
        verbose_name_plural = 'Оттенки части лица (пост ВК)'


class Color(models.Model):
    name = models.CharField(verbose_name='Цвет', max_length=200)
    code = models.CharField(verbose_name='RGB код', max_length=200)
    bcor = models.PositiveIntegerField(verbose_name='Коор1')
    gcor = models.PositiveIntegerField(verbose_name='Коор2')
    rcor = models.PositiveIntegerField(verbose_name='Коор3')
