from rest_framework import serializers
from ..models import Subscription, Topic
from notification_data_handler.users.api.serializers import GetUserDetailsSerializer


class GetUserSubscriptionDetailsSerializer(serializers.ModelSerializer):
    user = GetUserDetailsSerializer(many=True)
    topic = serializers.SerializerMethodField()

    def get_topic(self, obj):
        return obj.topic.name

    class Meta:
        model = Subscription
        fields = "__all__"


class CreateUserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
