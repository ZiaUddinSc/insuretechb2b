from django.urls import path
from .views import DistrictListView,BankListAPIView,DesignationListAPIView,DepartmentView

urlpatterns = [
    path('districts/', DistrictListView.as_view()),
    path('banks/', BankListAPIView.as_view()),
    path('designations/', DesignationListAPIView.as_view()),
    path('departments/', DepartmentView.as_view()),
]