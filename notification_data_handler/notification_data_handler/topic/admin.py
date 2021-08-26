from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    model = Topic
    list_display = ["id", "name"]


@admin.register(Subscription)
class TopicAdmin(admin.ModelAdmin):
    model = Subscription
    list_display = ["id", "name",  "topic"]
