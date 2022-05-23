from django.urls import path
from .views import lead_list,lead_detail,lead_create,lead_update, lead_delete,LeadListView,LeadDetailView,LeadCreateView,LeadUpdateView, LeadDeleteView,AssignAgentView,CategoryListView,CategoryDetailView,CategoryUpdateView,CategoryDeleteView,CategoryCreateView,DashboardView

app_name = "leads"

urlpatterns = [
    path('',LeadListView.as_view(), name='lead_list'),
    path("create/",LeadCreateView.as_view(), name='lead_create'),
     path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('<int:pk>/update/',LeadUpdateView.as_view(), name='lead_update'),
    path('<int:pk>/delete/',LeadDeleteView.as_view(), name='lead_delete'),
    path('<int:pk>/',LeadDetailView.as_view(), name='lead_detail'),
    path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name='assign-agent'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
    path('create-category/', CategoryCreateView.as_view(), name='category-create'),
]