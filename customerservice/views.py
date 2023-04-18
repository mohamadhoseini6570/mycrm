from re import template
from unicodedata import name
from django.core.files import File
from http.client import HTTPResponse
from multiprocessing import context
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.views.generic.list import ListView
# from django import forms
from urllib import request
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponseRedirect
from . import models
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import CreateView, UpdateView, DeleteView, FormView, View #may be deleted 
from django.urls import reverse_lazy, reverse
from django.forms import modelformset_factory
from django.views.generic.detail import SingleObjectMixin, DetailView
from .forms import AgentForm, AgentForm2, ContractForm, ContractForm2, CustomerForm, CustomerSearch, WirelessForm, CloudForm, OtherSevicesForm
# from .forms import AgentForm2
from django.forms.models import inlineformset_factory

class BasicUsageListingView(generic.TemplateView):
    template_name = 'basic_usage.html'
    # See 'Customer' definition in "Read me first" at home page.
    #In this exemple, Customer is a model and is exported as 
    # customers_as_model into the template basic_usage.html.
    # If you want, you can also use get_context_data() method instead of
    # extra_context attribute.
    extra_context = dict(customers_as_model = models.Customer)



# CBV dashboard for homepage by TempalteView---------------------------------------    
class Index(generic.TemplateView):
    # login_url = '/accounts/login/'
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        user_ip = self.request.META['REMOTE_ADDR']
        context1 = super().get_context_data(**kwargs)
        # context1['latest_customers'] = models.Customer.objects.all()[:7]
        context1['latest_customers'] = models.Customer.objects.all().order_by('-id')[:5]
        context2 = {
                    'user_ip': user_ip,
                    'num_contract' : models.Contract.objects.all().count(),
                    'num_customer' : models.Customer.objects.all().count(),
                    'num_agent' : models.Agent.objects.all().count(),
                    'num_wireless' : models.Wireless.objects.all().count(),
                    }
        context3 = dict(context1)
        context3.update(context2)
        return context3

#==================================================================

# CBV contracts list by ListView--------------------------------------------------
class ContractList(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = models.Contract 
    template_name = 'contracts/contract_list.html'
    paginate_by = 5
    # login_url = '/accounts/login/'
    # login_url = '/'
    queryset = models.Contract.objects.all()
    permission_required = ('customerservice.view_contract')
    
# CBV contract detail list by DetailView  --------------------------------------------------  
class ContractDetailList(generic.DetailView):# min 10
    model = models.Contract 
    template_name = 'contracts/contract_detail.html'
    
  

# FBV contract creation by ContractForm (forms.Form) (forms.py)---------------------------------------    
@permission_required('customerservice.add_contract', raise_exception=True)
def ContractCreate(request):
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            contract = models.Contract(name=form.cleaned_data['name'],
                                       start_time=form.cleaned_data['start_time'],
                                       end_time=form.cleaned_data['end_time'],
                                       contract_time=form.cleaned_data['contract_time'],
                                       state=form.cleaned_data['state'],
                                       notes=form.cleaned_data['notes'])
            contract.save()
            # with open('./myfile', 'w') as f:
            #     myfile = File(f)
            #     myfile.write(str(form.cleaned_data['date_time']))
            #     myfile.closed
            #     f.closed
            return HttpResponseRedirect(reverse('customerservice:contracts-list'))
            # return HttpResponseRedirect('Thank You')
    else:
        form = ContractForm(initial={'name':'ali'})
    return render(request, 'contracts/contract_create.html', {'form': form})


# CBV contract update by UpdateView----------------------------------------------------
class ContractUpdate(UpdateView):
    model = models.Contract
    # form_class = ContractForm # must be a modelform no form like ContractForm
    form_class = ContractForm2 # must be a modelform like ContractForm2
    template_name = 'contracts/contract_update.html'
    # fields = "__all__"
    
# CBV contract deletion by DeleteView----------------------------------------------------
class ContractDelete(DeleteView):
    model = models.Contract
    template_name = 'contracts/contract_delete.html'
    success_url ="/contracts/"

#==================================================================
    
# CBV customers list by ListView--------------------------------------------------
class CustomerList(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = models.Customer #template_name = customer_list.html context = customer_list
    template_name = 'customers/customer_list.html'
    paginate_by = 5
    queryset = models.Customer.objects.all()
    permission_required = ('customerservice.view_customer')

# CBV customer detail list by DetailView--------------------------------------------------  
class CustomerDetailList(generic.DetailView):# min 10
    model = models.Customer 
    template_name = 'customers/customer_detail.html'
    
# CBV customer creation by CreateView----------------------------------------------------
class CustomerCreate(LoginRequiredMixin, PermissionRequiredMixin ,CreateView):
    model = models.Customer
    template_name = 'customers/customer_create.html'
    form_class= CustomerForm
    # initial = {'':}
    # success_url = reverse_lazy('customerservice:customers-list')
    permission_required = ('customerservice.add_customer')


# CBV customer update by UpdateView----------------------------------------------------
class CustomerUpdate(UpdateView):
    model = models.Customer
    form_class= CustomerForm
    template_name = 'customers/customer_update.html'
    # success_url ="/customers/"
    
# CBV customer deletion by DeleteView----------------------------------------------------
class CustomerDelete(DeleteView):
    model = models.Customer
    template_name = 'customers/customer_delete.html'
    success_url ="/customers/"

        
# # FBV customer search ---------------------------------------    
# #https://www.youtube.com/watch?v=AGtae4L5BbI
def CustomerSearch(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        customers = models.Customer.objects.filter(commercialname__contains=searched)
        return render(request,'customers/customers_search_result.html',{'searched': searched, 'customers': customers})
    else:
        return render(request,'customers/customers_search_result.html',{})

# # FBV customer search list result ---------------------------------------
def CustomerListServices(request, pk):
    customer = models.Customer.objects.get(id=pk)
    clouds = models.Cloud.objects.filter(customer=customer)
    wirelesses = models.Wireless.objects.filter(customer=customer)
    return render(request,'customers/customer_list_services.html',{
        'customer': customer, 'clouds': clouds, 'wirelesses': wirelesses})

# FBV customer search with pagination ---------------------------------------    
#https://www.youtube.com/watch?v=AGtae4L5BbI
#https://www.youtube.com/watch?v=N-PB-HMFmdo
def CustomerSearchP(request):
    
    
    # if request.method == 'POST':
        # searched = request.POST['searched']
        # customers = models.Customer.objects.filter(commercialname__contains=searched)
        
        
        # p = Paginator(customers.all(), 2)
        p = Paginator(models.Customer.objects.all(), 2) # returns <django.core.paginator.Paginator object at 0x000001BF990FCBB0>
        page = request.GET.get('page') #page of current request # returns int number
        customerspage = p.get_page(page) # returns <Page 3 of 7>
        with open('./myfile', 'w') as f:
                myfile = File(f)
                myfile.write(str(customerspage))
                myfile.closed
                f.closed
        # return render(request,'customer_search_result1.html',{'searched': searched, 'customers': customers, 'customerspage': customerspage})
        return render(request,'customers/customer_search_result1.html',{'customerspage': customerspage})
    # else:
    #     return render(request,'customer_search_result1.html',{})

# FBV customer search with all related services  ---------------------------------------    
def NewCustomerSearch(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        try:
            customer = models.Customer.objects.get(commercialname=searched)
        except models.Customer.DoesNotExist:
            customer = None
        if customer is not None:
            clouds = models.Cloud.objects.filter(customer=customer)
            wirelesses = models.Wireless.objects.filter(customer=customer)
            return render(request,'customers/result.html',{'searched': searched,
                'customer': customer, 'clouds': clouds, 'wirelesses': wirelesses})
        else:
            return render(request,'customers/result.html',{})
    else:
        return render(request,'customers/result.html',{})
#==================================================================

# CBV agent list by ListView--------------------------------------------------
class AgentList(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = models.Agent #template_name = customer_list.html context = customer_list
    template_name = 'agents/agent_list.html'
    paginate_by = 5
    # login_url = '/accounts/login/'
    # login_url = '/'
    queryset = models.Agent.objects.all()
    permission_required = ('customerservice.view_agent')
    
# CBV agent detail list by DetailView--------------------------------------------------  
class AgentDetailList(generic.DetailView):# min 10
    model = models.Agent 
    template_name = 'agents/agent_detail.html'

# FBV agent creation by AgentForm (forms.Form) (forms.py)---------------------------------------    
def AgentCreate(request):
    if request.method == 'POST':
        form = AgentForm(request.POST)
        if form.is_valid():
            agent = models.Agent(name=form.cleaned_data['name'],
                email=form.cleaned_data['email'], phone=form.cleaned_data['phone'],
                mobile=form.cleaned_data['mobile'], role=form.cleaned_data['role'],
                notes=form.cleaned_data['notes'])
            agent.save()
            # with open('./myfile', 'w') as f:
            #     myfile = File(f)
            #     myfile.write(str(form.cleaned_data['date_time']))
            #     myfile.closed
            #     f.closed
            return HttpResponseRedirect(reverse('customerservice:agents-list'))
            # return HttpResponseRedirect('Thank You')
    else:
        form = AgentForm(initial={'email':'johndoe@coffeehouse.com','name':'حسینی',
            'user': request.user})
    return render(request, 'agents/agent_create.html', {'form': form})

# CBV agent update by UpdateView----------------------------------------------------
class AgentUpdate(UpdateView):
    model = models.Agent
    form_class = AgentForm2 # must be a modelform no form like ContractForm
    template_name = 'agents/agent_update.html'
    
    
# CBV agent deletion by DeleteView----------------------------------------------------
class AgentDelete(DeleteView):
    model = models.Agent
    template_name = 'agents/agent_delete.html'
    success_url ="/agents/"

#==================================================================

# CBV wireless list by ListView--------------------------------------------------
class WirelessList(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = models.Wireless #template_name = customer_list.html context = customer_list
    template_name = 'wirelesses/wireless_list.html'
    paginate_by = 5
    # login_url = '/accounts/login/'
    # login_url = '/'
    queryset = models.Wireless.objects.all()
    permission_required = ('customerservice.view_wireless')

    
# CBV wireless detail list by DetailView--------------------------------------------------  
class WirelessDetailList(generic.DetailView):# min 10
    model = models.Wireless 
    template_name = 'wirelesses/wireless_detail.html'


# CBV wireless creation by CreateView using forms.py and bootstrap ----------------------------------------------------
class WirelessCreate(CreateView):
    model = models.Wireless
    template_name = 'wirelesses/wireless_create.html'
    form_class = WirelessForm
    # initial = {'':}
    # success_url = reverse_lazy('customerservice:wirelesses-list')

# CBV wireless update by UpdateView----------------------------------------------------
class WirelessUpdate(UpdateView):
    model = models.Wireless
    form_class = WirelessForm # must be a modelform no form like ContractForm
    template_name = 'wirelesses/wireless_update.html'

# CBV wireless deletion by DeleteView----------------------------------------------------
class WirelessDelete(DeleteView):
    model = models.Wireless
    template_name = 'wirelesses/wireless_delete.html'
    success_url ="/wirelesses/"


#==================================================================

# CBV cloud list by ListView--------------------------------------------------
class CloudList(LoginRequiredMixin, PermissionRequiredMixin ,generic.ListView):
    model = models.Cloud 
    template_name = 'clouds/cloud_list.html'
    paginate_by = 5
    # queryset = models.Cloud.objects.all()
    permission_required = ('customerservice.view_cloud')


# CBV cloud detail list by DetailView--------------------------------------------------  
class CloudDetailList(generic.DetailView):
    model = models.Cloud
    template_name = 'clouds/cloud_detail.html'

# CBV cloud creation by CreateView using forms.py and bootstrap ----------------------------------------------------
class CloudCreate(CreateView):
    model = models.Cloud
    form_class = CloudForm
    template_name = 'clouds/cloud_create.html'

# CBV cloud update by UpdateView----------------------------------------------------
class CloudUpdate(UpdateView):
    model = models.Cloud
    form_class = CloudForm # must be a modelform no form like ContractForm
    template_name = 'clouds/cloud_update.html'

# CBV cloud deletion by DeleteView----------------------------------------------------
class CloudDelete(DeleteView):
    model = models.Cloud
    template_name = 'clouds/cloud_delete.html'
    success_url ="/clouds/"

#==================================================================

# FBV otherservices creation by OtherSevicesForm (forms.Form) (forms.py)---------------------------------------    
def OtherSevicesCreate(request):
    if request.method == 'POST':
        form = OtherSevicesForm(request.POST)
        if form.is_valid():
            otherservices = models.OtherSevices(extra_ip = form.cleaned_data['extra_ip'],
                ip1 = form.cleaned_data['ip1'],
                subnet_mask1 = form.cleaned_data['phone'],
                notes = form.cleaned_data['notes'])
            otherservices.save()
            return HttpResponseRedirect(reverse('customerservice:otherserviceses-list'))
            # return HttpResponseRedirect('Thank You')
    else:
        form = OtherSevicesForm(initial={'email':'johndoe@coffeehouse.com','name':'حسینی',
            'user': request.user})
    return render(request, 'otherservices_create.html', {'form': form})

# CBV othersevices list by ListView--------------------------------------------------
class OtherSevicesList(generic.ListView):
    model = models.OtherSevices 
    template_name = 'otherservices_list.html'
    paginate_by = 5
    # permission_required = ('customerservice.view_cloud')