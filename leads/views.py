from django.core.mail import send_mail
from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from .models import Lead, Agent,Category
from .forms import LeadForm,LeadModelForm,CustomUserCreationForm,AssignAgentForm,CategoryModelForm,LeadCategoryUpdateForm
from django.views import generic 
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganisorAndLoginRequiredMixin
import datetime

class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")
#___________________________________________________________
# Landing page class Based View
class LandingPageView(generic.TemplateView):
    template_name = 'landing.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)

#Landing page function based view
def landing_page(request):
    return render(request, 'landing.html')

class LeadListView(LoginRequiredMixin,generic.ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        #initial queryset of leads for the entire organization 
        if user.is_organisor:
            queryset = Lead.objects.filter(organization = user.userprofile )
        else:
            queryset = Lead.objects.filter(organization = user.agent.organization )
        # filtrer  for the agentlogged in 
            queryset = queryset.filter(agent__user=user)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organization=user.userprofile, 
                agent__isnull=True
            )
            context.update({
                "unassigned_leads": queryset
            }) 
        return context    

#Get all Leads based on function 
def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads": leads
    }
    return render(request,"leads/lead_list.html",context)

#___________________________________________________________
#Get Lead's Detail
def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead
    }
    return render(request,"leads/lead_detail.html",context)
#Lead detail view based on class
class LeadDetailView(LoginRequiredMixin,generic.DetailView):
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"
    
    def get_queryset(self):
        user = self.request.user
        #initial queryset of leads for the entire organization 
        if user.is_organisor:
            queryset = Lead.objects.filter(organization = user.userprofile )
        else:
            queryset = Lead.objects.filter(organization = user.agent.organization )
        # filtrer  for the agentlogged in 
            queryset = queryset.filter(agent__user=user)
        return queryset     

# #Create LeadForm
# def lead_create(request):
    # form = LeadForm()
    # if request.method == "POST":
    #     print('reciving a post request')
    #     form = LeadForm(request.POST)
    #     if form.is_valid():
    #         print('successfully valid')
    #         print(form.cleaned_data)
    #         first_name = form.cleaned_data['first_name']
    #         last_name = form.cleaned_data['last_name']
    #         age = form.cleaned_data['age']
    #         agent=Agent.objects.first()
    #         Lead.objects.create(
    #             first_name=first_name,
    #             last_name=last_name,s
    #             age=age,
    #             agent = agent
    #         )
    #         print("the Lead is succesfully created")
    #         return redirect('/leads')
    # context={
    #     "form": form
    # }
#     return render(request,"leads/lead_create.html",context)

class LeadCreateView(OrganisorAndLoginRequiredMixin,generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm
    context_object_name = "lead"
    
    def get_success_url(self):
        return "/leads"

    def form_valid(self, form):
        send_mail(
            subject="A Lead has been created successfully",
            message=" Check all Leads in The DJ-CRM  to see the new lead",
            from_email="test@test.com",
            recipient_list=["nshamadi@gmail.com"],
        )
        return super (LeadCreateView,self).form_valid(form)

#Create Lead ModeForm
def lead_create(request):
    form = LeadModelForm()
    if request.method == "POST":
        print('reciving a post request')
        form = LeadModelForm(request.POST)
        if form.is_valid():
            print('successfully valid')
            print(form.cleaned_data)
            form.save()
            print("the Lead is succesfully created")
            return redirect('/leads')
    context={
        "form": form
    }
    return render(request,"leads/lead_create.html",context)


#Lead update using the LeadForm
# def lead_update(request,pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadForm()
#     if request.method == "POST":
#         print('reciving a post request')
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             print('successfully valid')
#             print(form.cleaned_data)
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             agent=Agent.objects.first()
#             lead.first_name=first_name
#             lead.last_name=last_name
#             lead.age=age
#             lead.save()
#             print("the Lead is succesfully created")
#             return redirect('/leads')

#     context = {
#         "lead" : lead,
#         "form": form

#     }
#     return render(request,"leads/lead_update.html",context)



class AssignAgentView(OrganisorAndLoginRequiredMixin, generic.FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs
        
    def get_success_url(self):
        return reverse("leads:lead_list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)

class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organisor:
            queryset = Lead.objects.filter(
                organization=user.userprofile
            )
        else:
            queryset = Lead.objects.filter(
                organization=user.agent.organization
            )

        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organisor:
            queryset = Category.objects.filter(
                organization=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization
            )
        return queryset


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organisor:
            queryset = Category.objects.filter(
                organization=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization
            )
        return queryset


class CategoryCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/category_create.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("leads:category-list")

    def form_valid(self, form):
        category = form.save(commit=False)
        category.organization = self.request.user.userprofile
        category.save()
        return super(CategoryCreateView, self).form_valid(form)


class CategoryUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/category_update.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("leads:category-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organisor:
            queryset = Category.objects.filter(
                organization=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization
            )
        return queryset


class CategoryDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/category_delete.html"

    def get_success_url(self):
        return reverse("leads:category-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organisor:
            queryset = Category.objects.filter(
                organization=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization
            )
        return queryset


class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organisor:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().id})

    def form_valid(self, form):
        lead_before_update = self.get_object()
        instance = form.save(commit=False)
        converted_category = Category.objects.get(name="Converted")
        if form.cleaned_data["category"] == converted_category:
            # update the date at which this lead was converted
            if lead_before_update.category != converted_category:
                # this lead has now been converted
                instance.converted_date = datetime.datetime.now()
        instance.save()
        return super(LeadCategoryUpdateView, self).form_valid(form)



def lead_update(request,pk):
    lead= Lead.objects.get(id=pk)
    form = LeadModelForm(instance =lead)
    if request.method == "POST":
        print('reciving a post request')
        form = LeadModelForm(request.POST,instance =lead)
        if form.is_valid():
            print('successfully valid')
            print(form.cleaned_data)
            form.save()
            print("the Lead is succesfully created")
            return redirect('/leads')
    context={
        "form": form
    }
    return render(request,"leads/lead_update.html",context)

class LeadUpdateView(LoginRequiredMixin,generic.UpdateView):
    template_name = "leads/lead_update.html"
    queryset =Lead.objects.all()
    form_class = LeadModelForm
    context_object_name = "lead"
    
    def get_success_url(self):
        return "/leads"
    
    def get_queryset(self):
        user = self.request.user
        #initial queryset of leads for the entire organization 
        return Lead.objects.filter(organization = user.userprofile )

def lead_delete(request,pk):
    lead= Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')

class LeadDeleteView(LoginRequiredMixin,generic.DeleteView):
    template_name = "leads/lead_delete.html"
    queryset =Lead.objects.all()

    def get_success_url(self):
        return "/leads"
    
    def get_queryset(self):
        user = self.request.user
        #initial queryset of leads for the entire organization 
        return Lead.objects.filter(organization = user.userprofile )
        
        
class DashboardView(OrganisorAndLoginRequiredMixin, generic.TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        user = self.request.user

        # How many leads we have in total
        total_lead_count = Lead.objects.filter(organization=user.userprofile).count()

        # How many new leads in the last 30 days
        thirty_days_ago = datetime.date.today() - datetime.timedelta(days=30)

        total_in_past30 = Lead.objects.filter(
            organization=user.userprofile,
            date_added__gte=thirty_days_ago
        ).count()

        # How many converted leads in the last 30 days
        converted_category = Category.objects.get(name="Converted")
        converted_in_past30 = Lead.objects.filter(
            organization=user.userprofile,
            category=converted_category,
            converted_date__gte=thirty_days_ago
        ).count()

        context.update({
            "total_lead_count": total_lead_count,
            "total_in_past30": total_in_past30,
            "converted_in_past30": converted_in_past30
        })
        return context

