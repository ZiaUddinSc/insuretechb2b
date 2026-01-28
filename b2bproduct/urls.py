from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include
from .views import (life,IPDHospitalizationCoverage,OPDCoverage,
                    criticalIllness,maternityCoverage,createB2bProduct,createPlan1,ClaimDashboard,
                    ProductView,ProductViewSigleList,getProductList,
                    ProductListView,
                    PolicytListView,getPolicyList,PolicyView,PolicyViewSigleList,TableTemp,MyFamily,GroupeClaim
                )

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

urlpatterns = [
    path('life-list/',life,name='life-list'),
    path('IPD-hospitalization-coverage/',IPDHospitalizationCoverage,name='IPD-hospitalization-coverage'),
    path('OPD-coverage-list/',OPDCoverage,name='OPD-coverage-list'),
    path('critical-Illness-list/',criticalIllness,name='critical-Illness-list'),
    path('maternity-coverage-list/',maternityCoverage,name='maternity-coverage-list'),
    path('create-b2b-product/',createB2bProduct,name='create-b2b-product'),
    path('create-plan1/',createPlan1,name='create-plan1'),
    path('claim-dashboard/',ClaimDashboard,name='claim-dashboard'),
    path('group-claim/',GroupeClaim,name='b2b-group-claim'),
    # path('create-claim/',CreateClaim,name='create-claim'),
    
    #Product Add URL
    path('products/',ProductListView,name='products'),
    path('product-list/',getProductList,name='product-list'),
    path('product-save/',ProductView.as_view(),name='product-save'),
    path('product-save/<int:pk>/',ProductView.as_view(),name='product-save'),
    path('product-details/<int:item_id>/',ProductViewSigleList.as_view(),name='product-details'),

    path('policies/',PolicytListView,name='policies'),
    path('policy-list-info/',getPolicyList,name='policy-list-info'),
    path('create-policy/',PolicyView.as_view(),name='create-policy'),
    path('create-policy/<int:pk>/',PolicyView.as_view(),name='create-policy'),
    path('policy-details/',PolicyViewSigleList.as_view(),name='policy-details'),
    path('table-temp/',TableTemp,name='table-temp'),
    # path('group-claim/',GroupeClaim,name='group-claim'),
    path('my-family/',MyFamily,name='my-family'),
   
  

]