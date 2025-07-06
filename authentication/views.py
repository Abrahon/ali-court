from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
import requests as ext_requests
import jwt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

# import firebase_admin
# from firebase_admin import credentials, auth as firebase_auth

User = get_user_model()


from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    OTPSerializer,
    VerifyOTPSerializer,
    ResetPasswordSerializer,
    ChangePasswordSerializer,
    UserProfileSerializer,
)


User = get_user_model()
# One-time initialization
# cred = credentials.Certificate('firebase_config.json')
# firebase_admin.initialize_app(cred)

# TO DO

# if not firebase_admin._apps:
#     cred = credentials.Certificate("")
#     firebase_admin.initialize_app(cred)


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


# social login 

# Firebase

# Google Login
@api_view(['POST'])
def google_login(request):
    id_token = request.data.get('id_token')
    if not id_token:
        return Response({"error": "Missing id_token"}, status=400)

    try:
        decoded_token = firebase_auth.verify_id_token(id_token)
        email = decoded_token['email']
        name = decoded_token.get('name', 'NoName')

        user, _ = User.objects.get_or_create(email=email, defaults={"username": name})
        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {"email": user.email, "username": user.username}
        })
    except Exception as e:
        return Response({"error": str(e)}, status=400)

# Facebook Login
@api_view(['POST'])
def facebook_login(request):
    access_token = request.data.get('access_token')
    if not access_token:
        return Response({"error": "Missing access_token"}, status=400)

    try:
        fb_url = f"https://graph.facebook.com/me?fields=id,name,email&access_token={access_token}"
        fb_response = ext_requests.get(fb_url)
        fb_data = fb_response.json()

        email = fb_data.get('email')
        name = fb_data.get('name')

        if not email:
            return Response({"error": "Email not found in Facebook data"}, status=400)

        user, _ = User.objects.get_or_create(email=email, defaults={"username": name})
        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {"email": user.email, "username": user.username}
        })

    except Exception as e:
        return Response({"error": str(e)}, status=400)

# Apple Login (Simple ID token decode)
@api_view(['POST'])
def apple_login(request):
    id_token = request.data.get('id_token')
    if not id_token:
        return Response({"error": "Missing id_token"}, status=400)

    try:
        decoded_token = jwt.decode(id_token, options={"verify_signature": False})
        email = decoded_token.get("email")

        if not email:
            return Response({"error": "Email not found in Apple token"}, status=400)

        user, _ = User.objects.get_or_create(email=email, defaults={"username": email.split('@')[0]})
        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {"email": user.email, "username": user.username}
        })
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    
    # create profile

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])  
def create_profile(request):
    email = request.data.get('email')
    try:
        user = User.objects.get(email=email)
        return HttpResponse({'error': 'User already exists'}, status=400)
    except User.DoesNotExist:
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse('profile created succesfully')
        return HttpResponse(serializer.errors, status=400)


@api_view(['PUT', 'PATCH'])
@parser_classes([MultiPartParser, FormParser])  # For image upload
def update_profile(request):
    email = request.data.get('email')
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return HttpResponse("User not found", status=404)

    serializer = UserProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return HttpResponse( "Profile updated", "data", serializer.data)
    return HttpResponse(serializer.errors, status=400)

# GET DATA
@api_view(['GET'])
def get_profile(request):
    email = request.query_params.get('email')
    try:
        user = User.objects.get(email=email)
        serializer = UserProfileSerializer(user)
        return HttpResponse(serializer.data)
    except User.DoesNotExist:
        return HttpResponse('user not found', status=404)


