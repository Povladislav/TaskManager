from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError("User should have a username!")
        if email is None:
            raise TypeError("User should have an email!")
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if email is None:
            raise TypeError("Email should not be none!")
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_verified = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractUser):
    class Roles(models.TextChoices):
        WORKER = 'worker'
        CUSTOMER = 'customer'
        ADMIN_WORKER = 'admin_worker'

    role = models.CharField(max_length=12, choices=Roles.choices, default=Roles.WORKER,
                            help_text="Роль пользователя в системе")
    email = models.EmailField(unique=True, help_text="EMAIL пользователя")
    first_name = models.CharField(max_length=15, help_text="Имя")
    second_name = models.CharField(max_length=15, help_text="Фамилия")
    patronymic = models.CharField(max_length=15, help_text="Отчество")
    phone_number = PhoneNumberField(unique=True, help_text="Контактный номер телефона")
    photo = models.ImageField(upload_to='photos/', help_text="Фото сотрудника")

    def __str__(self):
        return f"{self.first_name} {self.second_name}"
