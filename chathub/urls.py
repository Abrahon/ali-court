from django.urls import path
from . import views

urlpatterns = [
    path('plans/', views.list_plans),                # GET: all plans
    path('plans/create/', views.create_plan),        # POST: create title
    path('plans/<int:plan_id>/update/', views.update_plan),  # PUT: rename/save
    path('plans/<int:plan_id>/delete/', views.delete_plan),  # DELETE: remove plan
    path('chat/', views.chat_with_ai), 

    path('classes/create/', views.create_class),
    path('classes/', views.list_classes),

]
