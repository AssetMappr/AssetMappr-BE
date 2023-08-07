"""User Manager models"""
# models.py
import base64
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
import bcrypt


class UserManager(BaseUserManager):
    """User manager class"""

    def create_user(self, email, password=None, **extra_fields):
        """Creating user"""
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Creating superuser"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class Users(AbstractBaseUser):
    """User class"""
    id = models.BigAutoField(primary_key=True,
                             verbose_name="User ID")
    email = models.EmailField(unique=True,
                              verbose_name="User's email ID")
    password = models.CharField(max_length=255, verbose_name="Password hash")
    salt = models.CharField(max_length=255, verbose_name="Salt")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    def set_password(self, raw_password):
        """Password set function"""
        salt = bcrypt.gensalt()
        salt_str = base64.b64encode(salt).decode(
            "ascii"
        )  # Convert salt to ASCII string
        hashed_password = bcrypt.hashpw(raw_password.encode(), salt)

        self.password = hashed_password.decode()
        self.salt = salt_str

    def check_password(self, raw_password):
        """Password check function"""
        hashed_password = bcrypt.hashpw(
            raw_password.encode(), base64.b64decode(self.salt.encode())
        )
        return self.password == hashed_password.decode()

    def __str__(self):
        """Return user email"""
        return str(self.email)

    class Meta:  # pylint: disable=too-few-public-methods
        """DB table for user"""
        db_table = "users"


class UserProfile(models.Model):
    """User Info model"""
    TYPE_CHOICES = [
        ('planner', 'planner'),
        ('citizen', 'citizen'),
    ]
    u_id = models.BigIntegerField(null=False, 
                                  default=-1, 
                                  verbose_name="User ID")
    type = models.CharField(max_length=25,
                            null=False,
                            choices=TYPE_CHOICES,
                            default="",
                            verbose_name="planner or citizen")
    first_name = models.CharField(max_length=255,
                                  null=False,
                                  default="",
                                  verbose_name="First name")
    last_name = models.CharField(max_length=255,
                                 null=True,
                                 verbose_name="Last name")
    mobile = models.CharField(max_length=15,
                              null=False,
                              default="",
                              verbose_name="Mobile number")
    com_name = models.CharField(max_length=255,
                                null=False,
                                default="",
                                verbose_name="Community name")
    com_geo_id = models.IntegerField(null=False,
                                     default=-1,
                                     verbose_name="Community geo ID")
    dob = models.DateField(null=False,
                           default=None,
                           verbose_name="Date of birth")
    ethnicity = models.CharField(max_length=100,
                                 default="",
                                 verbose_name="Ethnicity")
    race = models.CharField(max_length=50,
                            default="",
                            verbose_name="Race")
    gender = models.CharField(max_length=50,
                              default="",
                              verbose_name="Gender")
    

    # Relations
    # one-to-one
    user = models.OneToOneField("Users", 
                                on_delete=models.CASCADE, 
                                related_name="profile")
    # many(user)-to-one(community)
    # Delete all users if a community is deleted 
    community = models.ForeignKey("assets.Communities", 
                                  on_delete=models.CASCADE,
                                  related_name="profile_of_community")

    class Meta:  # pylint: disable=too-few-public-methods
        """Table for user info"""
        db_table = "user_profiles"
