from django.shortcuts import render
from kafka import KafkaConsumer
from json import loads
from config.celery_app import app
from provider_handler.handler.providers import NotificationProvider
from django.conf import settings
from celery.exceptions import SoftTimeLimitExceeded

@app.task()
def consume_mail_notification():
    '''
    Gets the notification from the mail topic and performs further operations 
    :return: None
    '''
    try:
        consumer = KafkaConsumer(
            'mail',
            auto_offset_reset='latest',
            enable_auto_commit=True,
            value_deserializer=lambda m: loads(m.decode('utf-8')),
            bootstrap_servers=settings.BOOTSTRAP_SERVER_CONSUMER)

        notify = NotificationProvider()
        for m in consumer:
            print(m.value)
            notify.get_provider_instance(m.value, "mail")

    except SoftTimeLimitExceeded:
        print("Restarting...")


@app.task()
def consume_sms_notification():
    '''
    Gets the notification from the sms topic and performs further operations 
    :return: None
    '''
    try:
        consumer = KafkaConsumer(
            'sms',
            auto_offset_reset='latest',
            enable_auto_commit=True,
            value_deserializer=lambda m: loads(m.decode('utf-8')),
            bootstrap_servers=settings.BOOTSTRAP_SERVER_CONSUMER)

        notify = NotificationProvider()
        for m in consumer:
            notify.get_provider_instance(m.value, "mail")

    except SoftTimeLimitExceeded:
        print("Restarting...")


@app.task()
def consume_in_app_notification():
    '''
    Gets the notification from the in_app topic and performs further operations 
    :return: None
    '''
    try:
        consumer = KafkaConsumer(
            'sms',
            auto_offset_reset='latest',
            enable_auto_commit=True,
            value_deserializer=lambda m: loads(m.decode('utf-8')),
            bootstrap_servers=settings.BOOTSTRAP_SERVER_CONSUMER)

        notify = NotificationProvider()
        for m in consumer:
            notify.get_provider_instance(m.value, "mail")

    except SoftTimeLimitExceeded:
        print("Restarting...")



consume_mail_notification.delay()
consume_sms_notification.delay()
consume_in_app_notification.delay()
