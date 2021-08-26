from django.contrib.auth import get_user_model
from rest_framework import serializers
from ..models import UserDevice

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }

class GetUserDetailsSerializer(serializers.ModelSerializer):
    device = serializers.SerializerMethodField()
    def get_device(self, obj):
        instance = UserDevice.objects.filter(user=obj).values("device_type", "device_id")
        print(instance)
        return instance

    class Meta:
        model = User
        fields = ["id", "name", "first_name", "last_name", "email", "phone", "device"]
