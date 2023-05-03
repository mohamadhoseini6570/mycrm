from django.urls import path, re_path
# from django.conf.urls import url
from django.views.generic import TemplateView
from . import views
from rest_framework import routers
from django.conf.urls import include

app_name = 'customerservice'

router = routers.DefaultRouter()
router.register('wireless', views.RestWirelessViewSet)

urlpatterns = [
    path('rest/', include(router.urls)), #router instance is assigned under the
        #r'^rest/' url, which means the final root url
    path('', views.Index.as_view(), name='index'),
    path('search/', views.SearchPanel.as_view(), name='search-panel'),
    path('basic_usage/', views.BasicUsageListingView.as_view(),
        name='basic_usage'),
    path('contract/create', views.ContractCreate, name='contract-create'),
    path('agent/create', views.AgentCreate, name='agent-create'),
    path('customers/', views.CustomerList.as_view(), name='customers-list'),
    path('customers/<str:customers_name>', TemplateView.as_view(
        template_name='customers_name.html'),
         {'VIP':True}, name='customers-name'),
    path('contracts/', views.ContractList.as_view(), name='contracts-list'),
    path('agents/', views.AgentList.as_view(), name='agents-list'),
    path('customer/create', views.CustomerCreate.as_view(),
        name='customer-create'),
    path('customer/<int:pk>', views.CustomerDetailList.as_view(),
        name='customer-detail-list'),
    path('contract/<int:pk>', views.ContractDetailList.as_view(),
        name='contract-detail-list'),
    path('agent/<int:pk>', views.AgentDetailList.as_view(),
        name='agent-detail-list'),
    path('wireless/<int:pk>', views.WirelessDetailList.as_view(),
        name='wireless-detail-list'),
    path('customer/<int:pk>/update', views.CustomerUpdate.as_view(),
        name='customer-update'),
    path('contract/<int:pk>/update', views.ContractUpdate.as_view(),
        name='contract-update'),
    path('wireless/<int:pk>/update', views.WirelessUpdate.as_view(),
        name='wireless-update'),
    path('cloud/<int:pk>/update', views.CloudUpdate.as_view(),
        name='cloud-update'),
    path('agent/<int:pk>/update', views.AgentUpdate.as_view(),
        name='agent-update'),
    path('customer/<int:pk>/delete', views.CustomerDelete.as_view(),
        name='customer-delete'),
    path('contract/<int:pk>/delete', views.ContractDelete.as_view(),
        name='contract-delete'),
    path('agent/<int:pk>/delete', views.AgentDelete.as_view(),
        name='agent-delete'),
    path('wireless/<int:pk>/delete', views.WirelessDelete.as_view(),
        name='wireless-delete'),
    path('cloud/<int:pk>/delete', views.CloudDelete.as_view(),
        name='cloud-delete'),
    path('search', views.Search,
        name='search'), # finalized
    path('search/<int:pk>/customers', views.CustomersSearchFound,
        name='customer-search-found'),
    path('search/<int:pk>/agents', views.AgentsSearchFound,
        name='agents-search-found'),
    path('wireless/create', views.WirelessCreate.as_view(),
        name='wireless-create'),
    path('otherservices/create', views.OtherSevicesCreate,
        name='otherservices-create'),
    path('wirelesses/', views.WirelessList.as_view(),
        name='wirelesses-list'),  
    path('otherserviceses/', views.OtherSevicesList.as_view(),
        name='otherserviceses-list'),  
    path('clouds/', views.CloudList.as_view(),
        name='clouds-list'),
    path('cloud/create', views.CloudCreate.as_view(),
        name='cloud-create'),
    path('cloud/<int:pk>', views.CloudDetailList.as_view(),
        name='cloud-detail-list'),
    path('rest/customer', views.rest_customer,
        name='rest-customer'),
    path('rest/customer/<int:customer_id>', views.rest_customer_detail,
        name='rest-customer-detail'),
    path('restdrf/customer', views.rest_customer_drf,
        name='rest-customer-drf'),
    path('restdrf/contract', views.RestContractList.as_view(),
        name='rest-contract-drf'),
    path('restdrf/agent', views.RestAgentList.as_view(),
        name='rest-agent-drf'),
]