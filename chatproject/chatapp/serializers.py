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


from rest_framework import serializers
from .models import UserSubscription,OneTimePayment

class UserPaySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = [
            'user_email', 
            'customer_name', 
            'order_reference', 
            'plan', 
            'start_date', 
            'current_period_end', 
            'status', 
            'payment_status',
            'created_at'
        ]

class OneTimePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OneTimePayment
        fields = ['order_reference', 'payment_id', 'amount', 'currency', 'payment_status', 'payment_date', 'user_email', 'customer_name']