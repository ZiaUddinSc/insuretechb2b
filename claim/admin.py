from django.contrib import admin
from .models import District,FileTransferHistory,ClaimInformation,ClaimDocuments,EmployeeInformation,ClaimCostItem,Currency
# Register your models here.
admin.site.register(EmployeeInformation)
admin.site.register(ClaimInformation)
admin.site.register(ClaimDocuments)
admin.site.register(FileTransferHistory)
admin.site.register(Currency)
admin.site.register(ClaimCostItem)
admin.site.register(District)

