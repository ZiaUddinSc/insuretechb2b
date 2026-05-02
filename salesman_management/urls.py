from django.urls import path
from .views import (
    add_salesman_view,
    salesman_list_view,
    SalesEmployeeViewSet,
    SalesEmployeeListAPIView,
    salesman_premium_summary,
    get_employee_details,
    create_collection,
    get_commission,
    collection_report,
    collection_report_api
)

employee_create = SalesEmployeeViewSet.as_view({
    'post': 'create'
})

urlpatterns = [
    path('add_salesman/', add_salesman_view, name='add-salesman'),
    path('collection/create/', create_collection, name='create-collection'),
    path('salesman_list/', salesman_list_view, name='salesman-list'),
    path('get_commission/', get_commission, name='get-commission'),
      # ajax submit api url
    path(
        'employee/create/',
        employee_create,
        name='employee-create'
    ),
    path('sales-employee-list/', SalesEmployeeListAPIView.as_view(), name='sales-employee-list'),
    path(
        'get-salesman-premium/<int:salesman_id>/',
        salesman_premium_summary,
        name='get-salesman-premium'
    ),
    
     path('employee/<int:employee_id>/', get_employee_details, name='employee-details'),
    path('reports/collection_report_summary/', collection_report, name='collection_report_summary'),
     path('reports/collection/', collection_report_api, name='collection_report'),
]