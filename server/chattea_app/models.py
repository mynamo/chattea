from django.db import models


class Chats(models.Model):
    messages = models.CharField(max_length=5000)
    sender = models.CharField(max_length=10, default="user")   # "user" or "bot"
    mode = models.CharField(max_length=30, default="quotes")
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"[{self.sender}] {self.messages[:40]}"
