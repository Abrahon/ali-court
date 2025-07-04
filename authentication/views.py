from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
import random

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    OTPSerializer,
    VerifyOTPSerializer,
    ResetPasswordSerializer,
    ChangePasswordSerializer,
)

User = get_user_model()


@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return HttpResponse("Register Success")
    return HttpResponse(serializer.errors, status=400)


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        return HttpResponse("Login Success")
    return HttpResponse(serializer.errors, status=400)


@api_view(['POST'])
def send_otp(request):
    serializer = OTPSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            otp = str(random.randint(100000, 999999))
            user.otp = otp
            user.otp_created_at = timezone.now()
            user.save()
            send_mail(
                'OTP Verification',
                f'Your OTP is {otp}',
                'user121@example.com',
                [email],
            )
            return HttpResponse("OTP sent to email")
        except User.DoesNotExist:
            return HttpResponse("User with this email does not exist", status=404)
    return HttpResponse(serializer.errors, status=400)


@api_view(['POST'])
def verify_otp(request):
    serializer = VerifyOTPSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        try:
            user = User.objects.get(email=email)
            if user.otp == otp and user.otp_created_at and timezone.now() <= user.otp_created_at + timedelta(minutes=5):
                return HttpResponse("OTP verified")
            return HttpResponse("Invalid or expired OTP")
        except User.DoesNotExist:
            return HttpResponse("User not found", status=404)
    return HttpResponse(serializer.errors, status=400)


@api_view(['POST'])
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = User.objects.get(email=serializer.validated_data['email'])
            user.set_password(serializer.validated_data['new_password'])
            user.otp = None
            user.save()
            return HttpResponse("Password reset successful")
        except User.DoesNotExist:
            return HttpResponse("Email is not valid", status=404)
    return HttpResponse(serializer.errors, status=400)


@api_view(['POST'])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        try:
            user = User.objects.get(email=email)
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                return HttpResponse("Password changed successfully")
            else:
                return HttpResponse("Old password is incorrect", status=400)
        except User.DoesNotExist:
            return HttpResponse("User does not exist", status=404)
    return HttpResponse(serializer.errors, status=400)


@api_view(['POST'])
def logout(request):
    return HttpResponse("Logout Page")
