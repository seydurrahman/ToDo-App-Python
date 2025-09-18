from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    STATUS=[
        ('Pending','Pending'),
        ('In Progress','In Progress'),
        ('Completed','Completed'), 
    ]
    CATEGORY=[
        ('Work','Work'),
        ('Personal','Personal'),
        ('Urgent','Urgent'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    due_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS, default='Pending')
    category = models.CharField(max_length=100, choices=CATEGORY, null=True, blank=True, default='Work')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.title