
from django.views import generic
import django.shortcuts import reverse
from leads.models import Agent
from django.contrib.auth.mixins import  LoginRequiredMixin


class AgentListView(LoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"
    
    def get_queryset(self):
        return Agent.objects.all()

class AgentCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = None

    def get_queryset(self):
        return reverse('agents:agent_list')

