from rest_framework import serializers


class ChatThreadSerializers(serializers.ModelSerializer):
    user_query = serializers.ReadOnlyField(source="query")
    id = serializers.ReadOnlyField(source="id")

    class Meta:
        fields = [
            "chat_thread_id",
            "user_id",
            "user_query",
            "response",
            "created_on",
            "updated_on",
            "is_active",
        ]


class ChatHistorySerializers(serializers.ModelField):
    user_query = serializers.ReadOnlyField(source="query")
    chat_id = serializers.ReadOnlyField(source="id")

    class Meta:
        fields = [
            "chat_id",
            "is_bookmarked",
            "chat_thread_id",
            "user_query",
            "response",
            "created_on",
            "updated_on",
        ]
