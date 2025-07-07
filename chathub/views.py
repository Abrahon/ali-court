from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ChatPlan
from .serializers import ChatPlanSerializer
from django.conf import settings
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from.models import ClassRoom




# Create a new chat plan (title)
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def create_plan(request):
    title = request.data.get('title')
    if not title:
        return Response({"error": "Title is required"}, status=400)

    plan = ChatPlan.objects.create(user=request.user, title=title, content="")
    serializer = ChatPlanSerializer(plan)
    return Response(serializer.data)

# Save or update chat content
@api_view(['PUT'])
# @permission_classes([IsAuthenticated])
def update_plan(request, plan_id):
    try:
        plan = ChatPlan.objects.get(id=plan_id, user=request.user)
    except ChatPlan.DoesNotExist:
        return Response({"error": "Plan not found"}, status=404)

    plan.title = request.data.get('title', plan.title)  # Rename if sent
    plan.content = request.data.get('content', plan.content)  # Save chat
    plan.is_edited = True
    plan.save()
    serializer = ChatPlanSerializer(plan)
    return Response(serializer.data)

# Delete a plan
@api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
def delete_plan(request, plan_id):
    try:
        plan = ChatPlan.objects.get(id=plan_id, user=request.user)
        plan.delete()
        return Response({"message": "Deleted successfully"})
    except ChatPlan.DoesNotExist:
        return Response({"error": "Plan not found"}, status=404)

# Get all plans for the user
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def list_plans(request):
    plans = ChatPlan.objects.filter(user=request.user).order_by('-updated_at')
    serializer = ChatPlanSerializer(plans, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_plans(request):
    plans = ChatPlan.objects.all().order_by('-updated_at')
    serializer = ChatPlanSerializer(plans, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def save_plan(request):
    serializer = ChatPlanSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)




@api_view(['POST'])
def chat_with_ai(request):
    user_input = request.data.get('message', '')
    if not user_input:
        return Response({"error": "No message provided"}, status=400)

    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": "llama3",  # or mistral, codellama, etc.
                "prompt": user_input,
                "stream": False
            }
        )

        data = response.json()
        reply = data.get("response", "").strip()
        return Response({"reply": reply})
    except Exception as e:
        return Response({"error": str(e)}, status=500)



@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def create_class(request):
    name = request.data.get('name')
    if not name:
        return Response({'error': 'Class name is required'}, status=400)
    
    new_class = ClassRoom.objects.create(user=request.user, name=name)
    return Response({'id': new_class.id, 'name': new_class.name})


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def list_classes(request):
    classes = ClassRoom.objects.filter(user=request.user).order_by('-created_at')
    data = [{'id': cls.id, 'name': cls.name} for cls in classes]
    return Response(data)

