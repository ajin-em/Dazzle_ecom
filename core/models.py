from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from . manager import CustomUserManager
# from store.models import *

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for your application.

    This model represents a custom user with email as the unique identifier.
    It includes fields for email, user status (active/staff), and a custom manager.

    Attributes:
        id (UUIDField): The primary key for the user, a universally unique identifier.
        email (EmailField): The user's unique email address used for authentication.
        is_active (BooleanField): Indicates whether the user is active.
        is_staff (BooleanField): Indicates whether the user has staff privileges.
        USERNAME_FIELD (str): The field used as the unique identifier (email).
        REQUIRED_FIELDS (list): The list of fields required for user creation (username).
        objects (CustomUserManager): The custom manager for the user model.

    Methods:
        __str__(self): Returns a string representation of the user.

    Usage:
        You can use this custom user model for authentication and user management in your Django application.
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class UserAddress(models.Model):
    """
    Represents a user's address information.

    Attributes:
    - id (UUIDField): Identifier for the address.
    - user (ForeignKey to CustomUser): User associated with this address.
    - first_name (CharField): First name of the user.
    - last_name (CharField): Last name of the user.
    - gender (CharField): Gender of the user (choices: 'Mr', 'Mrs').
    - mobile (CharField): User's mobile number.
    - email (EmailField): User's email address.
    - address_type (CharField): Type of address (choices: 'home', 'work').
    - place (CharField): Specific place or locality.
    - address (CharField): User's full address.
    - landmark (CharField): Landmark near the address.
    - pincode (CharField): Pincode of the address.
    - post (CharField): Post associated with the address.
    - district (CharField): District of the address.
    - state (CharField): State of the address.
    """
    
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_addresses')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('Mr', 'male'),('Mrs', 'female')])
    mobile = models.CharField(max_length=11)
    email = models.EmailField()
    address_type = models.CharField(max_length=20, choices=[('home','home'),('work','work')]) 
    place = models.CharField(max_length=100) 
    address = models.CharField(max_length=250)
    landmark = models.CharField(max_length=200)
    pincode =  models.CharField(max_length=6)
    post = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=50)

  