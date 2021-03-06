from django.urls import path
from .views import AgentListView,AgentCreateView ,AgentDetailView,AgentUpdateViewFunc,AgentDeleteView


app_name = 'agents'

urlpatterns = [
    path('', AgentListView.as_view(), name='agent_list'),
    path("create/",AgentCreateView.as_view(), name='agent_create'),
    path('<int:pk>/update/',AgentUpdateViewFunc, name='agent_update'),
    path('<int:pk>/delete/',AgentDeleteView.as_view(), name='agent_delete'),
    path('<int:pk>/',AgentDetailView.as_view(), name='agent_detail'),
    
] 