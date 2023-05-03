from rest_framework import serializers
from . import models

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contract
        fields = '__all__'

class CustomerSerializer(serializers.Serializer):
    commercialname = serializers.CharField(max_length = 50)
    brand = serializers.CharField(max_length = 25)

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Agent
        fields = '__all__'

class WirelessSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Wireless
        fields = '__all__'
