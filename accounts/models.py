from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, blank=True, null=True, unique=True)
    email = models.EmailField("email address", unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone_no = models.CharField(max_length=15, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "phone_no"]

    def __str__(self):
        return "{}".format(self.email)
    
    #-----------------Meta Class-----------------
    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"

        #----Fullname Method----
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


#-----------------Dashboard User Profile Model-----------------
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, blank=True, null=True)
    
    # city = models.CharField(max_length=50, blank=True, null=True)
    # state = models.CharField(max_length=50, blank=True, null=True)
    # country = models.CharField(max_length=50, blank=True, null=True)
    # profile_picture = models.ImageField(
    #     upload_to="user/profile_pictures/", blank=True, null=True
    # )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email    