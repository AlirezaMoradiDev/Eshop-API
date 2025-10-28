from rest_framework import serializers
from .models import MyUser

class MyUserSerializers(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, max_length=150)
    email = serializers.CharField(write_only=True, max_length=225)
    date_of_birth = serializers.DateField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = ('id', 'username', 'firstName', 'lastName', 'email', 'address', 'phone', 'date_of_birth', 'password')
        read_only_fields = ['id', ]
