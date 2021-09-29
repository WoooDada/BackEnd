from django.db import models

# Create your models here.
from django.db import models
from api.models import User



class recent_type(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recent_type_uid')
    type = models.CharField(max_length=2, null=True)