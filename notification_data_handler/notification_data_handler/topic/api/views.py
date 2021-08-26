from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, ListAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.pagination import PageNumberPagination
from .serializers import *


class GetUserSubscriptionDetailsView(RetrieveAPIView):
    serializer_class = GetUserSubscriptionDetailsSerializer
    queryset = Subscription.objects.all()
    lookup_field = "id"


class CreateUserSubscription(CreateAPIView):
    serializer_class = CreateUserSubscriptionSerializer
    queryset = Subscription.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_dependencies_create(request.data)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_dependencies_create(self, data):
        name = data.get("name")
        try:
            Topic.objects.get(name=name.lower)
        except Topic.DoesNotExist:
            Topic.objects.create(name=name.lower())

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class UpdateUserSubscription(UpdateAPIView):
    serializer_class = CreateUserSubscriptionSerializer
    queryset = Subscription.objects.all()


class ListUserSubscription(ListAPIView):
    serializer_class = CreateUserSubscriptionSerializer
    queryset = Subscription.objects.all()
    pagination_class = PageNumberPagination


class DeleteUserSubscription(DestroyAPIView):
    serializer_class = CreateUserSubscriptionSerializer
    queryset = Subscription.objects.all()
    lookup_field = "id"
