from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):  # extends the abstract user class
    email = models.EmailField(unique=True)