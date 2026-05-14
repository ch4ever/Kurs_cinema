from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

# Create your models here.

class UsersManager(BaseUserManager):
    def get_role(self, role):
        return {
            'CUSTOMER': 'Customers',
            'ADMIN': 'Admins'
        }.get(role,'Customers')
        
    def create_user(self, username, password, role='CUSTOMER', **extra_fields):
        user = self.model(username=username, role=self.get_role(role), **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, password,role='ADMIN' ,**extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        
        return self.create_user(username,password,**extra_fields)

class defaultUser(AbstractBaseUser):
    username=models.CharField('username', max_length=20, unique=True)
    role = models.CharField('role', choices=(('CUSTOMER', 'Customers'),
                                            ('ADMIN', 'Admins')), default='CUSTOMER')
    is_staff = models.BooleanField('staff', default=False)
    is_superuser = models.BooleanField('superuser', default=False)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    objects = UsersManager()
    
    def __str__(self):
        return f'({self.pk} - {self.username})'

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

