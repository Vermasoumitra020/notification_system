from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from kafka import KafkaProducer
from json import dumps
from django.conf import settings
from .validation import FieldsValidation


class SendMessageToQueue(APIView):
    '''
    Serves the notifications from the user by validating and
    pushing it to the kafka topics.
    '''
    def post(self, request):
        producer = KafkaProducer(
           value_serializer=lambda m: dumps(m).encode('utf-8'),
           bootstrap_servers=settings.BOOTSTRAP_SERVERS)

        data = FieldsValidation(request.data)
        if data.is_valid():
            producer.send("notification", value=request.data)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)







