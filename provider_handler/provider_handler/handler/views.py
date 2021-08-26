from django.shortcuts import render
from kafka import KafkaConsumer
from json import loads
from config.celery_app import app
from provider_handler.handler.providers import NotificationProvider


@app.task(time_limit=100000)
def consume_mail_notification():
    consumer = KafkaConsumer(
        'mail',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda m: loads(m.decode('utf-8')),
        bootstrap_servers=['192.168.0.104:9093'])

    notify = NotificationProvider()
    for m in consumer:
        print(m.value)
        notify.get_provider_instance(m.value, "mail")


@app.task(time_limit=100000)
def consume_sms_notification():
    consumer = KafkaConsumer(
        'sms',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda m: loads(m.decode('utf-8')),
        bootstrap_servers=['192.168.0.104:9093'])

    notify = NotificationProvider()
    for m in consumer:
        notify.get_provider_instance(m.value, "mail")


@app.task(time_limit=100000)
def consume_in_app_notification():
    consumer = KafkaConsumer(
        'sms',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda m: loads(m.decode('utf-8')),
        bootstrap_servers=['192.168.0.104:9093'])

    notify = NotificationProvider()
    for m in consumer:
        notify.get_provider_instance(m.value, "mail")


consume_mail_notification.delay()
consume_sms_notification.delay()
consume_in_app_notification.delay()
