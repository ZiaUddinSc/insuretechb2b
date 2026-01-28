from django.contrib.auth import views as auth_views
from django.urls import path,include

from .views  import EmployeeCreateAPIView,currencyeView,EmployeesView,AllEmployeeList,CompnayDetailProfileAPIView,EmployeeDetailAPIView, getCurrencyList,CurrencySigleList,test_send_email,CurrencyView,CreateClaim,suggest_benificiary,create_claim_api,FileTransferWithHistoryView,ClaimList,ClaimDetailAPIView,ClaimView,EmployeeList,EmployeeListView,ReceiveClaimList,FileReceiveWithHistoryView,update_claim_status,UpdateClaimView,delete_claim_document,update_claim_api,claim_action,update_claim_item
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

# router.register('devices',CampaignViewSet,basename='devices')
urlpatterns = [
     path('create-claim/',CreateClaim,name='create-claim'),
     path('suggest/', suggest_benificiary, name='suggest_benificiary'),
     path("create-claim-api/", create_claim_api, name="create_claim_api"),
     path("update-claim-api/", update_claim_api, name="update-claim-api"),
     path('claim-list/',ClaimList,name='claim_list'),
     path('received-claim-list/',ReceiveClaimList,name='received-claim-list'),
     path('employee-list-view/<int:policy_id>/',EmployeeList,name='employee-list-view'),
     path('employees/',EmployeesView,name='employees'),
     path("claim-view/<int:pk>/", ClaimView,name="claim_view"),
     path("update-claim-view/<int:pk>/", UpdateClaimView,name="update_claim_view"),
     path("employee-create/<int:pk>/", EmployeeCreateAPIView.as_view(), name="employee-create"),
     path("claim-with-history/", FileTransferWithHistoryView.as_view(),name="claim_with_history"),
     path("file-receive-with-history/", FileReceiveWithHistoryView.as_view(),name="file_receive_with_history"),
     path("update-claim-status/", update_claim_status,name="update-claim-status"),
     path('claim-details/<int:pk>/', ClaimDetailAPIView.as_view(), name='claim-details'),
     path('profile-details/', CompnayDetailProfileAPIView.as_view(), name='profile-details'),
     path('delete-claim-document', delete_claim_document, name='delete-claim-document'),
     path("employee/<int:policy_id>", EmployeeListView.as_view(),name="employee"),
     path("employee/", EmployeeListView.as_view(),name="employee"),
     path("all-employee/", AllEmployeeList.as_view(),name="all-employee"),
     path('employee-details/<int:pk>/', EmployeeDetailAPIView.as_view(), name='employee-details'),
     path('claims/<int:claim_id>/action/', claim_action, name='claim_action'),
     path('claims/update-item/', update_claim_item, name='update_claim_item'),
     path('mail_check/', test_send_email, name='mail_check'),
     
     path('currency-view/',currencyeView,name='currency-view'),
     path('currency-list/',getCurrencyList,name='currency-list'),
     path('create-currency/',CurrencyView.as_view(),name='create-currency'),
     path('create-currency/<int:pk>/',CurrencyView.as_view(),name='create-currency'),
     path('currency-details/<int:item_id>/',CurrencySigleList.as_view(),name='currency-details'),  

]