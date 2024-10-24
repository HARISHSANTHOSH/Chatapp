import random

from django.contrib.auth.models import User
from django.core import exceptions
from django.db.models import QuerySet
from rest_framework import serializers

from chatapp import models


class ChatHistoryController:

    @staticmethod
    def mockchat(user_query):

        response = [
            "**Hello! How can I assist you today?**",
            "## Hi there! What can I help you with?",
            "### Greetings! How can I make your day easier?",
            "# Hey! Need help with something? I'm here for you.",
            "***Welcome! How may I be of service to you today?***",
        ]
        return f"```markdown\n{random.choice(response)}\n```"

    @staticmethod
    def create_thread(
        user: User, query: str, is_active: bool = True
    ) -> models.ChatThread:
        """
        Create a chatthread

        Args:
        user : Current user
        query : User asked question

        Returns:
        models.Chathistory : Chathistory model


        """
        chat_thread = models.ChatThread.objects.create(
            user=user,
            query=query,
            is_active=is_active,
        )
        return chat_thread

    @staticmethod
    def get_thread(
        user: User, thread_id: str
    ) -> tuple[models.ChatThread, models.ChatHistory]:
        """
        get the chatthread using the uuid

        user: current user

        chat_thread : the uuid

        Returns:

        tuple of chat hsitory and chatthread


        """
        try:
            chat_thread = models.ChatThread.objects.get(
                id=thread_id, user=user, is_active=True
            )
        except exceptions.ObjectDoesNotExist:
            raise serializers.ValidationError(
                {"result": False, "msg": "thread doesnt exist"}
            )

        return chat_thread

    @staticmethod
    def save_chat_history(
        query: str, chat_thread: str, response: str
    ) -> models.ChatHistory:
        """
         store conversation to chathistory
         Args:
            chat_thread (str): chat thread uuid
            query (str): user query
            response (str): llm response
        Return:
            models.ChatHistory : ChatHistory model object


        """

        add_chat_history = models.ChatHistory.objects.create(
            chat_thread=chat_thread, query=query, response=response
        )
        return add_chat_history

    @staticmethod
    def delete_chat_history(chat_id: str, thread_id: str) -> None:
        """
           Soft delete chat history by setting is_active to False
        Args:
            chat_id (str): The user's chat ID.
            thread_id (str): The user's thread ID.
        Returns:
            None


        """

        if chat_id:
            try:
                user_chat = models.ChatHistory.objects.get(
                    chat_id=chat_id, is_active=True
                )
            except exceptions.ObjectDoesNotExist:
                raise serializers.ValidationError(
                    {"result": False, "msg": "doesnt exist"}
                )
            user_chat.is_active = False
            user_chat.save()
        elif thread_id:

            try:
                chat_thread = models.ChatThread.objects.get(
                    id=thread_id, is_active=True
                )
            except exceptions.ObjectDoesNotExist:
                raise serializers.ValidationError(
                    {"result": False, "msg": "doesnt exist"}
                )

            models.ChatHistory.objects.filter(
                chat_thread=chat_thread, is_active=True
            ).update(is_active=False)
            chat_thread.is_active = False
            chat_thread.save()

    @staticmethod
    def get_chat_history(
        user: User, thread_id: str
    ) -> QuerySet[models.ChatHistory]:
        """
         Retrieve chat history and threads.
        Args:
            user (user_model.models): The user model instance.
            thread_id (str, optional): User's UUID. Defaults to ''.

        Returns:
            models: The model object containing chat history and threads.

        """

        try:
            chat_thread = models.ChatThread.objects.get(
                id=thread_id, user=user, is_active=True
            )
        except exceptions.ObjectDoesNotExist:
            raise serializers.ValidationError(
                {"result": False, "msg": "doesnt exist"}
            )

        chat_data = models.ChatHistory.objects.filter(
            chat_thread=chat_thread, is_active=True
        ).order_by("-created_on")

        return chat_data
