from django.urls import path
from .views import create_subscription_session

urlpatterns = [
     path("create-subscription/", create_subscription_session),
]