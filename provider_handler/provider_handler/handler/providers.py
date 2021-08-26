from abc import ABC, abstractmethod
from django.conf import settings
from django.core.mail import EmailMessage


# This file is dedicated to the integration with the providers
# Uses Factory Pattern for eaiser integration with other providers.

class NotificationProvider(object):
    def get_provider_instance(self, m, type):
        npi = NotificationProviderFactory()
        sn = npi.generate_provider_factory(type)
        sn.send_notification(m)


class NotificationProviderFactory(object):
    def generate_provider_factory(self, type):
        if type == "mail":
            return MailProviderGenerator()
        elif type == "sms":
            return SMSProviderGenerator()
        else:
            return InAppProviderGenerator()


class NotificationProviderGenerator(ABC):
    @abstractmethod
    def send_notification(self, m):
        pass


class MailProviderGenerator(NotificationProviderGenerator):
    def send_notification(self, m):
        emails = [user['email'] for user in m['users']]
        subject = m['message']['title']
        message = m['message']['description']
        email_from = settings.EMAIL_HOST_USER
        recipient_list = emails
        msg = EmailMessage(subject, message, email_from, recipient_list)
        msg.send(fail_silently=False)


class SMSProviderGenerator(NotificationProviderGenerator):
    def send_notification(self, m):
        print("Not Implement")


class InAppProviderGenerator(NotificationProviderGenerator):
    def send_notification(self, m):
        print("Not Implemented")
