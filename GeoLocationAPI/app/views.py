from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GeoLocationSerializer
from rest_framework_xml.renderers import XMLRenderer
import requests
import json

# Create your views here.
api_key = "AIzaSyCOD3KvY2DDzEfel-NZ_LKIWXr86EF_EUw"
# api_key = "YOUR-KEY"

def format_address(address):
    address = address.replace("#","")
    result = address.replace(" ","+")
    return result


class AddressAPI(APIView):
    def post(self, request):
        try:
            serializer = GeoLocationSerializer(data=request.data)

            if serializer.is_valid():
                address = serializer.data['address']
                output_format = serializer.data['output_format']
                address_body = format_address(address)

                url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address_body}&key={api_key}"

                response = requests.request("GET", url)
                source = response.text
                data = json.loads(source)

                for source in data['results']:
                    if output_format == 'json' or output_format == 'JSON':
                        return Response(data={
                            'coordinates' : source['geometry']['location'],
                            'address' : address,
                        }, content_type='application/json')
                    elif output_format == 'xml' or output_format == 'XML':
                        xml_data = XMLRenderer()
                        xml_data = xml_data.render({'address' : address, 'coordinates' : source['geometry']['location']})
                        return Response(data=xml_data, content_type='application/xml')
                    else:
                        return Response({
                            'message' : 'Invalid output_format'
                        })
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
