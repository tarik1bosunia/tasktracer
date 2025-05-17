from django.db import models
from django.utils import timezone
import pytz

class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class DailyCompletion(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.localdate)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('task', 'date')  # Ensures one entry per task per day
        verbose_name = 'Daily Completion'
        verbose_name_plural = 'Daily Completions'

    def __str__(self):
        return f"{self.task.name} - {self.date}: {'Completed' if self.completed else 'Not Completed'}"
    
    

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = models.CharField(
        max_length=50,
        default='UTC',
        choices=[(tz, tz) for tz in pytz.all_timezones]
    )

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()