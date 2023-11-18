from django.db import models

class Chats(models.Model):
    messages = models.CharField(max_length=255)
