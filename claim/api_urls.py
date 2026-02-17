from django.urls import path
from .views import SuggestBeneficiaryView,ClaimListView,ClaimDetailsListView,CurrencyListView,create_claim_api,accept_claim

urlpatterns = [
    path('claim_for/', SuggestBeneficiaryView.as_view()),    
    path('currencies/', CurrencyListView.as_view()),
    path('claim_details/<int:pk>/', ClaimDetailsListView.as_view()),
    path('claim_list/', ClaimListView.as_view()),
    path('create-claim/', create_claim_api),
    path('update-claim-status/', accept_claim)
]