from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadForm,LeadModelForm

#Get all Leads
def lead_list(request):
  #  return HttpResponse("hellooo")
    leads = Lead.objects.all()
    context = {
        "leads": leads
    }
    return render(request,"leads/lead_list.html",context)

#Get Lead's Detail
def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead
    }
    return render(request,"leads/lead_detail.html",context)

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

#delete lead
def lead_delete(request,pk):
    lead= Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')
