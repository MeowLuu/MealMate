from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
from django.core.exceptions import ValidationError
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # initial profile setup
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    contact_info = models.TextField(blank=True)

    # Dietary Preference
    dietary_preferences = models.CharField(
        max_length=100,
        choices=[
            ('vegetarian', 'Vegetarian'),
            ('vegan', 'Vegan'),
            ('halal', 'Halal'),
            ('kosher', 'Kosher'),
            ('none', 'No Preference'),
        ],
        default='none',
        blank=True
    )


    def __str__(self):
        return self.user.username



class ProfileTag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name



class MealEvent(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    max_participants = models.PositiveIntegerField()
    participants = models.ManyToManyField(User, through='Participation', related_name='events_joined')

    status = models.CharField(max_length=20, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    privacy = models.CharField(max_length=10, choices=[('public', 'Public'), ('private', 'Private')])
    invitation_code = models.CharField(max_length=10, blank=True, null=True)  

    


    def clean(self):
        if self.date_time:
    
            if timezone.is_naive(self.date_time):
                self.date_time = timezone.make_aware(self.date_time)
            if self.date_time < timezone.now():
                raise ValidationError("Event time must be in the future.")
        
    def save(self, *args, **kwargs):
        if self.privacy == 'private' and not self.invitation_code:
            self.invitation_code = str(random.randint(1000, 9999))

        self.full_clean()
        super().save(*args, **kwargs)

    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_events')

    def __str__(self):
        return self.title
    

class Participation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(MealEvent, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} in {self.event.title}"


class Bill(models.Model):
    event = models.OneToOneField(MealEvent, on_delete=models.CASCADE)
    is_split_equally = models.BooleanField(default=True)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)  

class Payment(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])

class Message(models.Model):
    event = models.ForeignKey(MealEvent, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
