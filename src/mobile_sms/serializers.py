from rest_framework import serializers

class smsSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    message = serializers.CharField(max_length=150)