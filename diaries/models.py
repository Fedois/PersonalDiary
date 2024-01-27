from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Diary(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="diaries")

    def __str__(self):
        return f"{self.name}"

class Todo(models.Model):
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE, related_name="todos")
    title = models.CharField(max_length=150)
    description = models.TextField()
    is_important = models.BooleanField(default=False)
    done = models.BooleanField(default=False)
    date = models.DateField()

    def __str__(self):
        return f"todo: {self.title}, diary: {self.diary.name}"