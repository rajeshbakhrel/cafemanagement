from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from restro.validatino import isalphavalidator,isimagevalidator
from django.core.exceptions import ValidationError
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, password2=None):
        """
        Creates and saves a User with the given email, name,tc and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            # role = role, # defingig the role of a user
        )
        # if  role in [User.Roles.TEACHER ,User.Roles.ADMIN] :
        #     user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,name, password=None):
        """
        Creates and saves a superuser with the given email, name,tc and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            # role=User.Roles.ADMIN,
       
        )
        user.is_admin = True
        user.is_superuser=True
        user.save(using=self._db)
        return user
# def Contact_Validate(value):
#     # contact = str(value)
#     print("Contact:", contact)
#     print("Starts with '98' or '97'?", contact.startswith('98') or contact.startswith('97'))
#     print("Length is not 10?", len(contact) != 10)
    
#     if (contact.startswith('98') or contact.startswith('97')) and  len(contact) != 10 :
#         raise ValidationError("the contact number should starts with 98 or 97 and should be of 10 digits.")


class User(AbstractBaseUser):

    # class Roles(models.TextChoices):
    #     ADMIN='ADMIN'


    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
       
    )
    name = models.CharField(max_length=64, validators=[isalphavalidator])
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    objects = UserManager()

    USERNAME_FIELD = "email"
    # USERNAME_FIELD = "name"

    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin





