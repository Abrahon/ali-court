from rest_framework import serializers
from .models import ChatPlan
from .models import ClassRoom

class ChatPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatPlan
        fields = '__all__'



class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = '__all__'  # You can also list them manually if you prefer
