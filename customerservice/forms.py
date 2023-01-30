from dataclasses import fields
from email.policy import default
import imp
from pyexpat import model
from random import choices
from secrets import choice
from socket import fromshare
from tabnanny import verbose
from tkinter import Widget
from tkinter.tix import Form
from django import forms
from django.forms import ModelForm
from .models import Wireless, Customer, Contract, Agent
from django.forms.models import inlineformset_factory, InlineForeignKeyField
from django.core.exceptions import ValidationError
from django_jalali.forms import jDateTimeField, jDateField
from django_jalali.admin.widgets import AdminSplitjDateTime, AdminjDateWidget
# https://ordinarycoders.com/blog/article/using-django-form-fields-and-widgets 


class ContractForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='نام قرارداد') 
    start_time = jDateField(widget=AdminjDateWidget(),
        label='تاریخ شروع')
    end_time = jDateField(widget=AdminjDateWidget(),
        label='تاریخ پایان')
    contract_time = jDateField(widget=AdminjDateWidget(),
        label='تاریخ انعقاد')
    state_choices = (
        ('فعال', 'فعال'),
        ('در حال تمدید', 'در حال تمدید'),
        ('پیش نویس', 'پیش نویس'),
        ('منقضی کمتر از 30 روز', 'منقضی کمتر از 30 روز'),
        ('منقضی', 'منقضی'),
    )
    state = forms.CharField(widget=forms.Select(choices=state_choices,
        attrs={'class': 'form-control'}), label='وضعیت')
    notes = forms.CharField(widget=forms.Textarea(
        attrs={'rows':3, 'class': 'form-control'}), label='توضیحات')
    
    
# ------------------------------------------------------------------------    

class ContractForm2(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='نام قرارداد') 
    start_time = jDateField(widget=AdminjDateWidget(),
        label='تاریخ شروع')
    end_time = jDateField(widget=AdminjDateWidget(),
        label='تاریخ پایان')
    contract_time = jDateField(widget=AdminjDateWidget(),
        label='تاریخ انعقاد')
    state_choices = (
        ('فعال', 'فعال'),
        ('در حال تمدید', 'در حال تمدید'),
        ('پیش نویس', 'پیش نویس'),
        ('منقضی کمتر از 30 روز', 'منقضی کمتر از 30 روز'),
        ('منقضی', 'منقضی'),
    )
    state = forms.CharField(widget=forms.Select(choices=state_choices,
        attrs={'class': 'form-control'}), label='وضعیت')
    notes = forms.CharField(widget=forms.Textarea(
        attrs={'rows':3, 'class': 'form-control'}), label='توضیحات')
    
    class Meta: 
        model = Contract
        fields = '__all__'

# =======================================================================

class CustomerForm(forms.ModelForm):
    commercialname = forms.CharField(widget=forms.TextInput(attrs=
        {'class': 'form-control'}), label='نام تجاری') 
    brand = forms.CharField(widget=forms.TextInput(attrs=
        {'class': 'form-control'}), label='برند')
    kindchoices = (
        ('عادی', 'عادی'),
        ('ویژه', 'ویژه'),
    )
    kind = forms.CharField(widget=forms.Select(choices=kindchoices,
        attrs={'class': 'form-control'}), label='نوع')
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='شهر')
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='آدرس')
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='تلفن')
    notes = forms.CharField(widget=forms.Textarea(
        attrs={'rows':3, 'class': 'form-control'}), label='توضیحات')
    
    class Meta: 
        model = Customer
        fields = '__all__'


# ------------------------------------------------------------------------
class CustomerSearch(forms.Form):
    commercialname = forms.CharField()
    # brand = forms.CharField()
    # city = forms.CharField()
    # address = forms.CharField()
    # phone = forms.CharField()
    # kind = forms.CharField()
    # notes = forms.CharField()

# =================================================================
    
class AgentForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs=
        {'class': 'form-control'}), max_length=10, label='نام',
        error_messages={'required':'پرش کن!'},
        required=True, help_text='نام نماینده را وارد کنید') # CharField has default widget
    # of TextInput, that renders the HTML code <input type="text" ...>.
    email = forms.EmailField(widget=forms.TextInput(attrs=
        {'class': 'form-control'}), label='ایمیل',
        error_messages={'max_length':'ddd'}) # EmailField() has the default widget of 
        # EmailInput and renders as <input type="email" ...>
        # This field also uses the built-in Django validation EmailValidator that
        # requires an @ symbol within the input for it to be considered valid.
    phone = forms.CharField(widget=forms.TextInput(attrs=
        {'class': 'form-control'}), max_length=11, label='تلفن',
        help_text='تلفن نماینده را وارد کنید')
    mobile = forms.CharField(widget=forms.TextInput(attrs=
        {'class': 'form-control'}), max_length=11, label='موبایل')
    role_choices = (
        ('فنی', 'فنی'),
        ('بازرگانی', 'بازرگانی'),
        ('حقوقی', 'حقوقی'),
    ) 
    # role = forms.CharField(widget=forms.Select(choices=role_choices)
    # , label='نقش') this works also like the next line
    role = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'form-control'}), choices=role_choices, label='نقش')
    notes = forms.CharField(widget=forms.Textarea(
        attrs={'rows':3, 'class': 'form-control'}), label='توضیحات') #  if you are looking to add a multi-line input field to your
        #form, add the Textarea widget to CharField(). Textarea widget renders the 
        # field as <textarea>...</textarea>,
    # notes = forms.Textarea(label='توضیحات') # this doesnt work also like the previous line
    error_css_class = 'error'
    required_css_class = 'bold'

# ----------------------------------------------------------------------

class AgentForm2(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs=
        {'class': 'form-control'}), max_length=10, label='نام',
        error_messages={'required':'پرش کن!'},
        required=True, help_text='نام نماینده را وارد کنید') 
    email = forms.EmailField(widget=forms.TextInput(attrs=
        {'class': 'form-control'}), label='ایمیل',
        error_messages={'max_length':'ddd'}) 
    phone = forms.CharField(widget=forms.TextInput(attrs=
        {'class': 'form-control'}), max_length=12, label='تلفن',
        help_text='تلفن نماینده را وارد کنید')
    mobile = forms.CharField(widget=forms.TextInput(attrs=
        {'class': 'form-control'}), max_length=13, label='موبایل')
    role_choices = (
        ('فنی', 'فنی'),
        ('بازرگانی', 'بازرگانی'),
        ('حقوقی', 'حقوقی'),
    )
    role = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'form-control'}), choices=role_choices, label='نقش')
    notes = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'class': 'form-control'})
        , label='توضیحات') 
    error_css_class = 'error'
    required_css_class = 'bold'
    
    class Meta: 
        model = Agent
        fields = '__all__'
    
# ==================================================================

class WirelessForm(forms.ModelForm):
    class Meta: 
        model = Wireless
        fields = ('popsite', 'contract', 'customer', 'agent', 'internet_t_bw', 'internet_r_bw',
                  'intranet_t_bw', 'intranet_r_bw', 'throughput_t_bw', 
                'throughput_r_bw', 'ip', 'notes')
        
        widgets = {
           'popsite': forms.Select(attrs={'class': 'form-control'}),
           'internet_t_bw': forms.TextInput(attrs={'class': 'form-control'}),
           'internet_r_bw': forms.TextInput(attrs={'class': 'form-control'}),
           'intranet_t_bw': forms.TextInput(attrs={'class': 'form-control'}),
           'intranet_r_bw': forms.TextInput(attrs={'class': 'form-control'}),
           'throughput_t_bw': forms.TextInput(attrs={'class': 'form-control'}),
           'throughput_r_bw': forms.TextInput(attrs={'class': 'form-control'}),
           'ip': forms.TextInput(attrs={'class': 'form-control'}),
           'notes': forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
           'contract': forms.Select(attrs={'class': 'form-control', 'id': 'contract'}),
        #    'contract': forms.widgets.CheckboxInput()
        #    'contract': forms.Select(attrs={'class': 'select2-selection__rendered', 'id': 'select2-select2-single-input-sm-container'}),
           'customer': forms.Select(attrs={'class': 'form-control', 'id': 'customer'}),
           'agent': forms.Select(attrs={'class': 'form-control', 'id': 'agent'}),

        }
        
                