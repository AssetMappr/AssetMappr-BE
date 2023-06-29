# models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
import bcrypt
import base64


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    def set_password(self, raw_password):
        salt = bcrypt.gensalt()
        salt_str = base64.b64encode(salt).decode(
            "ascii"
        )  # Convert salt to ASCII string
        hashed_password = bcrypt.hashpw(raw_password.encode(), salt)

        self.password = hashed_password.decode()
        self.salt = salt_str

    def check_password(self, raw_password):
        hashed_password = bcrypt.hashpw(
            raw_password.encode(), base64.b64decode(self.salt.encode())
        )
        return self.password == hashed_password.decode()

    def __str__(self):
        return self.email

    class Meta:
        db_table = "User"


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="info")
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    community = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    community_geo_id = models.IntegerField()
    dob = models.DateField()
    ethnicity = models.CharField(max_length=255)
    race = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    # Add other fields as needed

    def __str__(self):
        return self.name

    class Meta:
        db_table = "UserInfo"
