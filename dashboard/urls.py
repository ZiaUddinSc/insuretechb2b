from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include
from .views import WaadaaOperationDashboard, insurer_audit_dashboard,insurer_claim_dashboard,dashboard,hr_admin_dashboard,insurer_dashboard,b2b_employee_dashboard,download_excel_template, insurer_finance_dashboard,upload_excel,my_policy,required_document,GroupClaim,waadaaSupervisor,insurer_supervisor_dashboard

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

# router.register('devices',CampaignViewSet,basename='devices')
urlpatterns = [
    path('',dashboard,name='dashboard'),
    #Different user Login Dashboard
    path('hr_admin/', hr_admin_dashboard, name='hr_admin_dashboard'),
    path('insurer_dashboard/', insurer_dashboard, name='insurer_dashboard'),
    path('b2b_employee_dashboard/', b2b_employee_dashboard, name='b2b_employee_dashboard'),
    path('insurer_claim_dashboard/', insurer_claim_dashboard, name='insurer_claim_dashboard'),
    path('insurer_audit_dashboard/', insurer_audit_dashboard, name='insurer_audit_dashboard'),
    path('insurer_supervisor_dashboard/', insurer_supervisor_dashboard, name='insurer_supervisor_dashboard'),
    path('insurer_finance_dashboard/', insurer_finance_dashboard, name='insurer_finance_dashboard'),
    path('download-template/', download_excel_template, name='download_excel_template'),
    path('upload-excel/', upload_excel, name='upload_excel'),
    path('my-policy/', my_policy, name='my_policy'),
    path('required-document/', required_document, name='required_document'),
    path('group-claim/',GroupClaim,name='group-claim'),
    path('waadaa_operation_dashboard/',WaadaaOperationDashboard,name='waadaa_operation_dashboard'),
    path('waadaa_supervisor/',waadaaSupervisor,name='waadaa_supervisor'),
]