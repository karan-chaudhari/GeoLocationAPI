from rest_framework import serializers

class GeoLocationSerializer(serializers.Serializer):
    address = serializers.CharField()
    output_format = serializers.CharField()
    