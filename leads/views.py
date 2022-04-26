from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadForm,LeadModelForm
from django.views import generic 
#___________________________________________________________
# Landing page class Based View
class LandingPageView(generic.TemplateView):
    template_name = 'landing.html'
#Landing page function based view
def landing_page(request):
    return render(request, 'landing.html')


#___________________________________________________________
 #Lead list view based on class
class LeadListView(generic.ListView):
    template_name = "leads/lead_list.html"
    queryset =Lead.objects.all()
    context_object_name = "leads"

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
class LeadDetailView(generic.DetailView):
    template_name = "leads/lead_detail.html"
    queryset =Lead.objects.all()
    context_object_name = "lead"
    


#___________________________________________________________


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

class LeadCreateView(generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm
    context_object_name = "lead"
    
    def get_success_url(self):
        return "/leads"

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




class LeadUpdateView(generic.UpdateView):
    template_name = "leads/lead_update.html"
    queryset =Lead.objects.all()
    form_class = LeadModelForm
    context_object_name = "lead"
    
    def get_success_url(self):
        return "/leads"

#delete lead
def lead_delete(request,pk):
    lead= Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')


class LeadDeleteView(generic.DeleteView):
    template_name = "leads/lead_delete.html"
    queryset =Lead.objects.all()

    def get_success_url(self):
        return "/leads"
        
