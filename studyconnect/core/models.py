from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class CustomUser(AbstractUser):
    user_id = models.CharField(max_length=12, unique=True, editable=False)
    email = models.EmailField(unique=True)

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.user_id})"
    

class Course(models.Model):
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.code} - {self.name}"
    
class Note(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="notes/")
    uploaded_by = models.ForeignKey("CustomUser", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Meeting(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    creator = models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    participants = models.ManyToManyField("CustomUser", related_name="joined_meetings", blank=True)
    date = models.DateTimeField()
    topic = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.topic} - {self.date}"

class StudySession(models.Model):
    requester = models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.CharField(max_length=10)
    time = models.CharField(max_length=10)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.requester.username} - {self.course.code} - {self.date}"

class Notification(models.Model):
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.message


class Message(models.Model):
    sender = models.ForeignKey(
        "CustomUser",
        on_delete=models.CASCADE,
        related_name="sent_messages"   # ✅ ADD THIS
    )
    receiver = models.ForeignKey(
        "CustomUser",
        on_delete=models.CASCADE,
        related_name="messages_received"
    )
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)   # ✅ also fixed here
