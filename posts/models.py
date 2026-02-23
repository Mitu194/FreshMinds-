from django.db import models

# Create your models here.
from core.models import TimeStampedModel

class Post(TimeStampedModel):
    title = models.CharField(max_length=200)