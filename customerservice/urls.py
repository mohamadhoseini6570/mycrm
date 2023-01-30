from django.urls import path, re_path
# from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

app_name = 'customerservice'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('contract/create', views.ContractCreate, name='contract-create'),
    path('agent/create', views.AgentCreate, name='agent-create'),
    path('customers/', views.CustomerList.as_view(), name='customers-list'),
    path('customers/<str:customers_name>', TemplateView.as_view(
        template_name='customers_name.html'),
         {'VIP':True}, name='customers-name'),
    path('contracts/', views.ContractList.as_view(), name='contracts-list'),
    path('agents/', views.AgentList.as_view(), name='agents-list'),
    path('customer/create', views.CustomerCreate.as_view(), name='customer-create'),
    path('customer/<int:pk>', views.CustomerDetailList.as_view(), name='customer-detail-list'),
    path('contract/<int:pk>', views.ContractDetailList.as_view(), name='contract-detail-list'),
    path('agent/<int:pk>', views.AgentDetailList.as_view(), name='agent-detail-list'),
    path('wireless/<int:pk>', views.WirelessDetailList.as_view(), name='wireless-detail-list'),
    path('customer/<int:pk>/update', views.CustomerUpdate.as_view(), name='customer-update'),
    path('contract/<int:pk>/update', views.ContractUpdate.as_view(), name='contract-update'),
    path('wireless/<int:pk>/update', views.WirelessUpdate.as_view(), name='wireless-update'),
    path('agent/<int:pk>/update', views.AgentUpdate.as_view(), name='agent-update'),
    path('customer/<int:pk>/delete', views.CustomerDelete.as_view(), name='customer-delete'),
    path('contract/<int:pk>/delete', views.ContractDelete.as_view(), name='contract-delete'),
    path('agent/<int:pk>/delete', views.AgentDelete.as_view(), name='agent-delete'),
    path('wireless/<int:pk>/delete', views.WirelessDelete.as_view(), name='wireless-delete'),
    # path('customers/search/', views.CustomerSearchList.as_view(), name='customers-search'),
    path('customers/search/', views.CustomerSearch, name='customers-search'),
    path('customers/searchp/', views.CustomerSearchP, name='customers-searchp'),
    path('customers/newsearch/', views.NewCustomerSearch, name='new-customers-search'),
    path('wireless/create', views.WirelessCreate.as_view(), name='wireless-create'),
    path('wirelesses/', views.WirelessList.as_view(), name='wirelesses-list'),  

]