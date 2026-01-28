from django.contrib import admin
from .models import (Organization,Bank,Designation,SalaryRange,Plan,Department,
                     Insurer,InsurerContact,InsurerPolicy,InsurerPolicyDocuments
                     ,OrganizationContact,OrganizationPolicy,OrganizationPolicyDocuments,
                     CompanyPlan,CompanyPlanItem,CompanyPlanDocument,CompanyType,District,HospitalContact,HospitalInformation,GopInformation 
                     )
# Register your models here.

admin.site.register(Bank)
admin.site.register(Designation)
admin.site.register(SalaryRange)
admin.site.register(Plan)
admin.site.register(Department)
admin.site.register(Insurer)
admin.site.register(InsurerContact)
admin.site.register(InsurerPolicy)
admin.site.register(InsurerPolicyDocuments)
admin.site.register(Organization)
admin.site.register(OrganizationContact)
admin.site.register(OrganizationPolicy)
admin.site.register(OrganizationPolicyDocuments)
admin.site.register(CompanyPlan)
admin.site.register(CompanyPlanItem)
admin.site.register(CompanyPlanDocument)
admin.site.register(CompanyType)
admin.site.register(HospitalInformation)
admin.site.register(HospitalContact)
admin.site.register(GopInformation)