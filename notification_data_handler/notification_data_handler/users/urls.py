from django.urls import path

from notification_data_handler.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
)

from .api.views import *



app_name = "users"

urlpatterns = [
    path("get-user-details/<int:id>/", GetUserDetailsView.as_view(), name="user-details"),

    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
