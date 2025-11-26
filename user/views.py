from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import MyUser
from .serializers import MyUserSerializers
# Create your views here.


@api_view(['POST'])
def register(request):
    serializer = MyUserSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'OK': 'user added !'})
    else:
        return Response(serializer.errors)


@api_view(['GET'])
def check_token(request):
    authentication_classes = [TokenAuthentication]
    user = request.user
    return Response({'user': user.username})