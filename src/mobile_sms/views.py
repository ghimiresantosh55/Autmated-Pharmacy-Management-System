from rest_framework import generics, serializers, status
from rest_framework.response import Response
from .serializers import smsSerializer
import requests
# Create your views here.

class smsView(generics.CreateAPIView):
    serializer_class = smsSerializer

    def create(self,request):
        try : 
            phone_number = request.data["phone_number"]
            message = request.data["message"]

            r = requests.post(
            "http://api.sparrowsms.com/v2/sms/",
            data={'token' : 'v2_mFFnZi74b6DNOuc8OwoQHiERFN0.BatJ',
                  'from'  : 'EazyCare',
                  'to'    : phone_number,
                  'text'  : message 
                 })

            status_code = r.status_code
            response = r.text
            response_json = r.json()
            # print(status_code)
            # print(response)
            # print(response_json)            
            return Response({"message":f"{status_code,response_json,response}"})

        except KeyError:
            return Response({"message":"please provide phone number and message"},status = status.HTTP_400_BAD_REQUEST)



   
            