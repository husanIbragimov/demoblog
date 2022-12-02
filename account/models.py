from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class AccountManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if phone_number is None:
            raise TypeError('User should have a phone')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        if password is None:
            raise TypeError('Password should not be None')
        user = self.create_user(
            phone_number=phone_number,
            password=password,
            **extra_fields,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    GENDER = (
        (0, 'None'),
        (1, 'Male'),
        (2, 'Female'),
    )
    full_name = models.CharField(max_length=50, verbose_name='First name', null=True)
    phone_number = models.CharField(max_length=16, unique=True, db_index=True, verbose_name='Phone number', null=True)
    email = models.EmailField(unique=True, db_index=True, null=True)
    gender = models.IntegerField(choices=GENDER, default=0)
    town_city = models.CharField(max_length=221, null=True)
    date_birth = models.DateField(null=True)
    is_superuser = models.BooleanField(default=False, verbose_name='Super user')
    is_staff = models.BooleanField(default=False, verbose_name='Staff user')
    is_active = models.BooleanField(default=True, verbose_name='Active user')
    date_login = models.DateTimeField(auto_now=True, verbose_name='Date login')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date created')

    objects = AccountManager()

    EMAIL_FIELD = 'phone_number'
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.full_name:
            return f'{self.full_name}'
        return f'{self.phone_number}'

    @property
    def token(self):
        refresh = RefreshToken.for_user(self)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return data
