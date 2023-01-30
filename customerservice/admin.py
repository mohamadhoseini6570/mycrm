from django.contrib import admin
from pyexpat import model
from . import models

# Register your models here.

# @admin.register(models.Contract)
class ContractAdmin(admin.ModelAdmin):
    admin.site.register(models.Contract)

#-----------------------------
class AgentAdmin(admin.ModelAdmin):
    admin.site.register(models.Agent)
    
#-----------------------------   

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass
    # list_display = ('commercialname_brand', 'address')
    # list_filter = ('commercialname', 'brand', 'address')
    # fields = (('commercialname', 'brand'), 'address')
    # inlines = [AgentInline, CloudInline]
    
# admin.site.register(models.Customer, CustomerAdmin)   
 
#-----------------------------

class CloudAdmin(admin.ModelAdmin):
    admin.site.register(models.Cloud)

#-----------------------------

class WirelessAdmin(admin.ModelAdmin):
    admin.site.register(models.Wireless)
    