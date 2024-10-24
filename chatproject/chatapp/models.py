import uuid

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class ChatThread(models.Model):
    """
    Table for storing chat thread
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    query = models.CharField(
        max_length=10000, blank=True, null=True, default=""
    )
    response = models.TextField(blank=True, null=True, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.id

    def __str__(self):
        return f"chat_id:{self.id}--{self.user.username}"

    class Meta:
        db_table = "chat_thread"


class ChatHistory(models.Model):
    """
    Table for storing chat history
    """

    chat_thread = models.ForeignKey(
        ChatThread, on_delete=models.CASCADE, related_name="chat_thread"
    )
    query = models.CharField(
        max_length=10000, blank=True, null=True, default=""
    )
    standalone_question = models.CharField(
        max_length=10000, blank=True, null=True, default=""
    )
    response = models.TextField(blank=True, null=True, default="")
    is_active = models.BooleanField(default=True)
    is_bookamarked = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        self.id

    def __str__(self):
        return f"thread_id: {self.chat_thread.id} | chat_id: {self.id} | {self.chat_thread.user.username}"

    class Meta:
        db_table = "chat_history"
