from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Friendship(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friendship_requests_sent")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friendship_requests_received")
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')