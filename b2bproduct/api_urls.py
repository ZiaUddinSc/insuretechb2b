from django.urls import path
from .views import ProductListAPIView,BenifitViewBuClaim

urlpatterns = [
    path('claim_types/', ProductListAPIView.as_view()),
    path('benifit_types_claim/', BenifitViewBuClaim.as_view())
    ]