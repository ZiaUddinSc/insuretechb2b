from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include
from .views import policyCategoriesList,policyCategoriesCreate,policyCreateHelth

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

# router.register('devices',CampaignViewSet,basename='devices')
urlpatterns = [
    path('policy-categories/',policyCategoriesList,name='categories'),
    path('policy-categorie-create/',policyCategoriesCreate,name='policy-categorie-create'),
    path('policies-create-health/',policyCreateHelth,name='policies-create-health'),
]