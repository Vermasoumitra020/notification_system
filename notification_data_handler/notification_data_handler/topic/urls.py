from django.urls import path
from .api.views import GetUserSubscriptionDetailsView, CreateUserSubscription, UpdateUserSubscription, \
    ListUserSubscription, DeleteUserSubscription

app_name = "subscription"

urlpatterns = [
    path("get-subscribed-users/<int:id>/", GetUserSubscriptionDetailsView.as_view(), name="subscribed-user"),
    path("create-subscription/", CreateUserSubscription.as_view(), name="create-subscribed-user"),
    path("update-subscription/", UpdateUserSubscription.as_view(), name="update-subscribed-user"),
    path("list-subscription/", ListUserSubscription.as_view(), name="list-subscription"),
    path("remove-subscription/<int:id>/", DeleteUserSubscription.as_view(), name="delete-subscription"),
]
