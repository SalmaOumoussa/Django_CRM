
from django.views import generic
from django.shortcuts import reverse
from leads.models import Agent
from .forms import AgentModelForm
from django.contrib.auth.mixins import  LoginRequiredMixin
from .mixins import OrganisorAndLoginRequiredMixin

class AgentListView(OrganisorAndLoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"
    
    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization =organization )

class AgentCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent_list")

    def form_valid(self, form):
        agent = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.save()
        Agent.objects.create(
            user=user,
            organization=self.request.user.userprofile
        )
        send_mail(
            subject="You are invited to be an agent",
            message="You were added as an agent on DJCRM. Please come login to start working.",
            from_email="admin@test.com",
            recipient_list=[user.email]
        )
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganisorAndLoginRequiredMixin,generic.DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"
    def get_queryset(self):
        return Agent.objects.all()
    

class AgentUpdateView(OrganisorAndLoginRequiredMixin,generic.UpdateView):
    template_name = "agents/agent_update.html"
    queryset =Agent.objects.all()
    form_class = AgentModelForm
    context_object_name = "agent"
    
    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization =organization )

    def get_success_url(self):
         return "/Agents"



class AgentDeleteView(OrganisorAndLoginRequiredMixin,generic.DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = "agent"

    def get_success_url(self):
        return reverse("agents:agent_list")
        
    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization =organization )
# #Lead detail view based on class
