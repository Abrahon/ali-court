from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class ChatPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    # user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    content = models.TextField()  # full chat content (markdown or plain)
    is_edited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title





class ClassRoom(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.user}"

