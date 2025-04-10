from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']



class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) # Display basic user info
   
    class Meta:
        model = UserProfile
        fields = ['user', 'job_title', 'location', 'profile_pic']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['user','job_title', 'location', 'profile_pic']


    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
       
        return instance
    

#done on april 8
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True, style={'input_type':'password'})
    new_password1 = serializers.CharField(write_only=True, required=True, style={'input_type':'password'})
    new_password2 = serializers.CharField(write_only=True, required=True, style={'input_type':'password'})
    
    def validate(self, data):
        request = self.context.get('request')
        user = request.user if request else None

        if not user.check_password(data['old_password']):
            raise serializers.ValidationError({'old_password': 'Old password is incorrect'})

        elif data['old_password']== data['new_password1']:
            raise serializers.ValidationError({'new_password1':'new password must be different from old password'})
        elif data['new_password1']!= data['new_password2']:
            raise serializers.ValidationError({'new_password2':'passwords must match'})
        return data
    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password1'])
        instance.save()
        return instance