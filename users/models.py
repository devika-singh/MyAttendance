from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
class Class(models.Model):
  user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='classes',
    )
  date = models.DateField()
  cid = models.CharField(max_length=7)
  code = models.CharField(max_length=10)
  attendance_status = models.CharField(max_length=3)
  constraints = [
            models.UniqueConstraint(
                fields=['date', 'cid', 'code'], name='the_duplicate_checker'
            )
        ]
