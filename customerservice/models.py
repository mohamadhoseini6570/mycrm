from asyncio.windows_events import NULL
from cProfile import label
from dataclasses import fields
from email.headerregistry import Address
from enum import unique
from pyexpat import model
from random import choices
from django import forms
from secrets import choice
from tabnanny import verbose
from tkinter import Widget
from unittest.util import _MAX_LENGTH
from django.db import models
from django.urls import reverse
# from django.forms import ModelForm
from django_jalali.db.models import jDateTimeField, jDateField
from django_jalali.admin.widgets import AdminSplitjDateTime, AdminjDateWidget
from django_jalali.forms import widgets


class Contract(models.Model):
    name = models.CharField(max_length=50, verbose_name='نام قرارداد')
    start_time = jDateField(verbose_name='تاریخ شروع')
    end_time = jDateField(verbose_name='تاریخ پایان')
    contract_time = jDateField(verbose_name='تاریخ انعقاد')
    state_choices = (
        ('فعال', 'فعال'),
        ('در حال تمدید', 'در حال تمدید'),
        ('پیش نویس', 'پیش نویس'),
        ('منقضی کمتر از 30 روز', 'منقضی کمتر از 30 روز'),
        ('منقضی', 'منقضی'),
        
    )
    state = models.CharField(max_length=25, choices=state_choices, default='فعال', verbose_name= 'وضعیت')
    notes = models.CharField(max_length=500, verbose_name='توضیحات',blank=True, null=True)
    
    def get_absolute_url(self):
        return reverse('customerservice:contract-detail-list', args=[str(self.id)])
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['id']

#----------------------------------------------------------

class Customer(models.Model):
    commercialname = models.CharField(max_length=50, unique=True, verbose_name='نام تجاری')
    brand = models.CharField(max_length=25, unique=True, verbose_name='برند')
    city = models.CharField(max_length=15, verbose_name='شهر')
    address = models.CharField(max_length=100, verbose_name='آدرس', blank=True, null=True)
    phone = models.CharField(max_length=11, verbose_name='تلفن', blank=True, null=True)
    kindchoices = (
        ('عادی', 'عادی'),
        ('ویژه', 'ویژه'),
    )
    kind = models.CharField(max_length=4, choices=kindchoices, default='عادی', verbose_name='نوع')
    notes = models.CharField(max_length=500, verbose_name='توضیحات',blank=True, null=True)

    
    def __str__(self):
        return '%s (%s)' % (self.commercialname,self.brand)
        
    def commercialname_brand(self): #To display in list_display at Adminmodel
        return '%s (%s)' % (self.commercialname,self.brand)
    commercialname_brand.short_description = 'Commercial Name (Brand)'
          
    def get_absolute_url(self):
        return reverse('customerservice:customer-detail-list', args=[str(self.id)])

    class Meta:
        ordering = ['id']

#----------------------------------------------------------
                
class Agent(models.Model):
    name = models.CharField(max_length=25, verbose_name='نام و نام خانوادگی')
    email = models.EmailField(verbose_name='ایمیل')
    phone = models.CharField(max_length=11, verbose_name='تلفن')
    mobile = models.CharField(max_length=11, verbose_name='تلفن همراه')
    rolechoices = (
        ('فنی', 'فنی'),
        ('بازرگانی', 'بازرگانی'),
        ('حقوقی', 'حقوقی'),
    )
    role = models.CharField(max_length=8, choices= rolechoices, default='فنی', verbose_name='نقش نماینده',)
    notes = models.CharField(max_length=500, verbose_name='توضیحات',blank=True, null=True)
    
    # def related_customer(self):         #To display in list_display at Adminmodel
    #     return '%s (%s)' % (self.customer.commercialname,self.customer.brand)
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('customerservice:agent-detail-list', args=[str(self.id)])
    
    class Meta:
        ordering = ['id']
    
#----------------------------------------------------------

def ip_test(value):
    value = int(value)
    if value >= 16 and value<=30:
        return True
    else:
        raise forms.ValidationError('ff')

class Wireless(models.Model):
    
    popsite_choices = (
        ('بوتان', 'بوتان'),
        ('شریعتی', 'شریعتی'),
        ('زرین', 'زرین'),
        ('کردستان', 'کردستان'),
        ('سنایی', 'سنایی'),
        ('پلاستیران', 'پلاستیران'),
    )
    popsite = models.CharField(max_length=25, choices=popsite_choices, default='بوتان',
        verbose_name='پاپ سایت', help_text= 'اسم پاپ سایت')
    # t stands for transmit, r for recieve
    internet_t_bw = models.BigIntegerField(verbose_name='پهنای باند ارسال اینترنت',
        blank=True, null=True)
    internet_r_bw = models.BigIntegerField(verbose_name='پهنای باند دریافت اینترنت',
        blank=True, null=True)
    intranet_t_bw = models.BigIntegerField(verbose_name='پهنای باند ارسال اینترانت',
        blank=True, null=True)
    intranet_r_bw = models.BigIntegerField(verbose_name='پهنای باند دریافت اینترانت',
        blank=True, null=True)
    throughput_t_bw = models.BigIntegerField(verbose_name='پهنای باند ارسال نقطه به نقطه',
        blank=True, null=True)
    throughput_r_bw = models.BigIntegerField(verbose_name='پهنای باند دریافت نقطه به نقطه',
        blank=True, null=True)
    ip = models.GenericIPAddressField(verbose_name='آدرس IP',
        error_messages={'required':'پرش کن!'})
    prefix = models.PositiveSmallIntegerField(verbose_name = 'ُPrefix', blank= True,
        null= True, default=29, validators= [ip_test] )
    notes = models.CharField(max_length=500, verbose_name='توضیحات',
        blank=True, null=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE,
        verbose_name='قرارداد')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,
        verbose_name='مشترک')
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE,
        verbose_name='نماینده')
    
    def __str__(self):
        return self.popsite
    
    def get_absolute_url(self):
        return reverse('customerservice:wireless-detail-list', args=[str(self.id)])
    
    class Meta:
        ordering = ['id']
        
#----------------------------------------------------------
    
class Cloud(models.Model):
    sizechoices = (
        ('Micro', 'Micro'),
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
        ('XLarge', 'XLarge'),
        ('XXLarge', 'XXLarge'),
    )
    size = models.CharField(max_length=7, choices=sizechoices, default='Medium')
    ip = models.GenericIPAddressField(verbose_name='آدرس IP')
    notes = models.CharField(max_length=500, verbose_name='توضیحات',blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)  

    def __str__(self):
        return self.size

    def get_absolute_url(self):
        return reverse('customerservice:cloud-detail-list', args=[str(self.id)])

    class Meta:
        ordering = ['id']

#----------------------------------------------------------

class OtherSevices(models.Model):
    extra_ip = models.BooleanField()
    ip1 = models.GenericIPAddressField(verbose_name='IP1')
    subnet_mask1 = models.PositiveSmallIntegerField(verbose_name='Subnet Mask1')
    ip2 = models.GenericIPAddressField(verbose_name='IP2')
    subnet_mask2 = models.PositiveSmallIntegerField(verbose_name='Subnet Mask2')
    ip3 = models.GenericIPAddressField(verbose_name='IP3')
    subnet_mask3 = models.PositiveSmallIntegerField(verbose_name='Subnet Mask3')
    ip4 = models.GenericIPAddressField(verbose_name='IP4')
    subnet_mask4 = models.PositiveSmallIntegerField(verbose_name='Subnet Mask4')
    ip5 = models.GenericIPAddressField(verbose_name='IP5')
    subnet_mask5 = models.PositiveSmallIntegerField(verbose_name='Subnet Mask5')
    ip6 = models.GenericIPAddressField(verbose_name='IP6')
    subnet_mask6 = models.PositiveSmallIntegerField(verbose_name='Subnet Mask6')
    ip7 = models.GenericIPAddressField(verbose_name='IP7')
    subnet_mask7 = models.PositiveSmallIntegerField(verbose_name='Subnet Mask7')
    ip8 = models.GenericIPAddressField(verbose_name='IP8')
    subnet_mask8 = models.PositiveSmallIntegerField(verbose_name='Subnet Mask8')
    ip9 = models.GenericIPAddressField(verbose_name='IP9')
    subnet_mask9 = models.PositiveSmallIntegerField(verbose_name='Subnet Mask9')
    IP10 = models.GenericIPAddressField(verbose_name='IP10')
    subnet_mask10 = models.PositiveSmallIntegerField(verbose_name='Subnet Mask10')
    first_vlan = models.PositiveSmallIntegerField(verbose_name='first_vlan')
    router_first_vlan = models.CharField(max_length=15,
        verbose_name='router_first_vlan')
    second_vlan = models.PositiveSmallIntegerField(verbose_name='second_vlan')
    router_second_vlan = models.CharField(max_length=15,
        verbose_name='router_second_vlan')
    third_vlan = models.PositiveSmallIntegerField(verbose_name='third_vlan')
    router_third_vlan = models.CharField(max_length=15,
        verbose_name='router_third_vlan')
    forth_vlan = models.PositiveSmallIntegerField(verbose_name='forth_vlan')
    router_forth_vlan = models.CharField(max_length=15,
        verbose_name='router_forth_vlan')
    fifth_vlan = models.PositiveSmallIntegerField(verbose_name='fifth_vlan')
    router_fifth_vlan = models.CharField(max_length=15,
        verbose_name='router_fifth_vlan')
    transmission = models.CharField(max_length=500, verbose_name='transmission')

#----------------------------------------------------------

class Cohost(models.Model):
    online = models.BooleanField()
    ip = models.GenericIPAddressField(verbose_name='IP1', 
        blank= True, null= True)
    dev_name = models.CharField(verbose_name='نام تجهیز', max_length=20,
        blank= True, null= True)
    dev_rack = models.CharField(verbose_name='شماره رک', max_length=5,
        blank= True, null= True)
    dev_scale_choices = (
        ('اقتصادی', 'اقتصادی'),
        ('استاندارد', 'استاندارد'),
        ('پیشرفته', 'پیشرفته'),
        ('سازمانی', 'سازمانی'),
        ('سازمانی ویژه', 'سازمانی ویژه'),
        ('G10-سازمانی', 'G10-سازمانی'),
        ('G10-سازمانی ویژه', 'G10-سازمانی ویژه'),
    )
    dev_scale = models.CharField(max_length=20, choices=dev_scale_choices,
        default='اقتصادی', verbose_name = 'مقیاس تجهیز')
    dev_dc_choices = (
        ('سهند ط 2', 'سهند ط 2'),
        ('سهند ط 3', 'سهند ط 3'),
        ('سهند ط 5', 'سهند ط 5'),
        ('شاهین همکف', 'شاهین همکف'),
        ('شاهین زیرزمین', 'شاهین زیرزمین'),
        ('بهشتی', 'بهشتی'),
        ('رمضانی', 'رمضانی'),
    )
    dev_dc = models.CharField(max_length=13, choices=dev_dc_choices,
        default='اقتصادی', verbose_name = 'مقیاس تجهیز')
    notes = models.CharField(max_length=500, verbose_name='توضیحات',
        blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)

#----------------------------------------------------------

class Ip(models.Model):
    # size = models.CharField(max_length=9, choices=sizechoices, default='اقتصادی')
    IP = models.GenericIPAddressField(verbose_name='IP', 
        blank= True, null= True)
    subnet_mask = models.PositiveSmallIntegerField(verbose_name = 'ُsubnet_mask',
        blank= True, null= True, default=29)
    vlan = models.PositiveSmallIntegerField(verbose_name = 'vlan',
        blank= True, null= True)
    notes = models.CharField(max_length=500, verbose_name='توضیحات',
        blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)

#----------------------------------------------------------

class Mpls(models.Model):
    IP = models.GenericIPAddressField(verbose_name='IP', 
        blank= True, null= True)
    subnet_mask = models.PositiveSmallIntegerField(verbose_name = 'ُsubnet_mask',
        blank= True, null= True, default=29)
    vlan = models.PositiveSmallIntegerField(verbose_name = 'vlan',
        blank= True, null= True)
    notes = models.CharField(max_length=500, verbose_name='توضیحات',
        blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)

#----------------------------------------------------------

class Colocation(models.Model):
    dev_brand_choices = (
        ('HP', 'HP'),
        ('DELL', 'DELL'),
        ('Cisco', 'Cisco'),
        ('MikroTik', 'MikroTik'),
        ('EMC', 'EMC'),
        ('Other', 'Other'),
    )
    dev_brand = models.CharField(max_length=8, choices=dev_brand_choices,
        default='HP', verbose_name = 'برند تجهیز')
    dev_name = models.CharField(verbose_name='نام تجهیز', max_length=20,
        blank= True, null= True)
    dev_rack = models.CharField(verbose_name='شماره رک', max_length=5,
        blank= True, null= True)
    dev_scale_choices = (
        ('اقتصادی', 'اقتصادی'),
        ('استاندارد', 'استاندارد'),
        ('پیشرفته', 'پیشرفته'),
    )
    dev_scale = models.CharField(max_length=9, choices=dev_scale_choices,
        default='اقتصادی', verbose_name = 'مقیاس تجهیز')
    dev_dc_choices = (
        ('سهند ط 2', 'سهند ط 2'),
        ('سهند ط 3', 'سهند ط 3'),
        ('سهند ط 5', 'سهند ط 5'),
        ('شاهین همکف', 'شاهین همکف'),
        ('شاهین زیرزمین', 'شاهین زیرزمین'),
        ('بهشتی', 'بهشتی'),
        ('رمضانی', 'رمضانی'),
    )
    dev_dc = models.CharField(max_length=13, choices=dev_dc_choices,
        default='اقتصادی', verbose_name = 'مقیاس تجهیز')
    notes = models.CharField(max_length=500, verbose_name='توضیحات',
        blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)    
    