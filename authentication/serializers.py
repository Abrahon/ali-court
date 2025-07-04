from rest_framework import serializers
from authentication.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

# signup
# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['email', 'username','password']
#         extra_kwargs = {'password',{'write_only' : True}}

#     def create(self, validated_data):
#         user  = User.objects.create_user(
#             email = validated_data['email'],
#             username = validated_data['username'],
#             password = validated_data['password']
#         )
#         return user

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField(write_only = True)
    confirm_password = serializers.CharField(write_only = True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('password dont match')
        return data
    
    def create(self, validated_data):
        # Remove confirm_password before creating the user
        validated_data.pop('confirm_password')

        return User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
    
    

# login  
class LoginSerializer(serializers.Serializer): 
    email = serializers.EmailField()
    password = serializers.CharField()



# otp send 
class OTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    # send_otp = serializers.CharField()

# otp verify 
class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()


# password reset 
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField()
    # confirm_password = serializers.CharField()



# password change 
class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    






        