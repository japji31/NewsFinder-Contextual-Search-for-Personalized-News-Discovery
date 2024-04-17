from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        
    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        age = data.get('age')
       
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email already exists")
        
        if not username.isalnum() or len(username) == 0:
            raise serializers.ValidationError("Invalid username")
        
        elif int(age) < 10:
            raise serializers.ValidationError("Invalid age")
        
        return data
