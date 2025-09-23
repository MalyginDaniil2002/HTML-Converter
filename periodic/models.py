from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Sheet(models.Model):
    name            = models.CharField(max_length=100)
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    source_link     = models.URLField()
    work_link       = models.URLField(null=True)
    #last_update     = models.DateTimeField()
