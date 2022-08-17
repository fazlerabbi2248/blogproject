from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

# Create your models here.

class UserManager(BaseUserManager):
  def create_user(self, email, username,otp, password=None, password2=None):

      if not email:
          raise ValueError('User must have an email address')

      user = self.model(
          email=self.normalize_email(email),
          username=username,
          otp=otp,
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, username,otp, password=None):

      user = self.create_user(
          email,
          password=password,
          username=username,
          otp=otp,

      )
      user.is_admin = True
      user.is_verified=True
      user.save(using=self._db)
      return user

class User(AbstractBaseUser):
  email = models.EmailField(
      verbose_name='Email',
      max_length=255,
      unique=True,
  )
  username = models.CharField(max_length=200)
  is_verified = models.BooleanField(default=True)
  otp = models.CharField(max_length=200, null=True, blank=True)
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username','otp']

  def __str__(self):
      return self.email

  def has_perm(self, perm, obj=None):

      return self.is_admin

  def has_module_perms(self, app_label):

      return True

  @property
  def is_staff(self):

      return self.is_admin

class otpmodel(models.Model):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.email

class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile', validators=[
                              FileExtensionValidator(['png', 'jpg'])])

    def __str__(self):
        return self.user.username