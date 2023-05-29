from django.db import models
import uuid

# Create your models here.
class Notification(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    title       = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title