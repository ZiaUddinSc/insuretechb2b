from rest_framework import viewsets
from accounts.models import CustomUser
from decimal import Decimal
from rest_framework.response import Response
from rest_framework import status
from b2bmanagement.models import OrganizationPolicy,Bank,Designation,Branch,Department,CompanyPlanItem,Organization
from .models import SalesEmployee,Channel,SalesRole,CommissionRule,PremiumCollection
from .serializers import SalesEmployeeCreateSerializer
from .services import generate_employee_code
from django.shortcuts import render
from django.db import transaction
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.utils import timezone
from datetime import date,timedelta
from calendar import monthrange


def add_salesman_view(request):
    if request.method == "POST":
        # save logic here
        pass

    context = {
        "designations": Designation.objects.all(),
        "branches": Branch.objects.all(),
        "roles":SalesRole.objects.all(),
        "managers": SalesEmployee.objects.filter(role__name='Line Manager'),
        "channels": Channel.objects.all(),        # ✅ REQUIRED
        "departments": Department.objects.all(),  # ✅ REQUIRED
    }
    return render(request, "add-salesman.html",context)

def salesman_list_view(request):
    return render(request, 'salesman-list.html')


class SalesEmployeeViewSet(
    viewsets.ViewSet
):

    def create(self,request):

        serializer = SalesEmployeeCreateSerializer(
            data=request.data
        )

        if serializer.is_valid():
            employee = serializer.save()

            return Response(
                {
                    "message":
                    "Employee created successfully",

                    "id":
                    employee.id
                },
                status=status.HTTP_201_CREATED
            )
        else:
            print(serializer.errors)   
        return Response(
            {
                "errors":
                serializer.errors
            },
            status=400
        )



class SalesEmployeeListAPIView(APIView):

    def get(self, request):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')

        queryset = SalesEmployee.objects.all()

        # 🔍 Search
        if search_value:
            queryset = queryset.filter(employee_name__icontains=search_value)

        total = queryset.count()

        # 📄 Pagination
        queryset = queryset[start:start + length]

        data = []
        for obj in queryset:
            data.append({
                "id": obj.id,
                "full_name": obj.employee_name,
                "employee_code": obj.employee_code,
                "line_manager": obj.line_manager.employee_name if obj.line_manager else "N/A",
                "department": obj.department.name if obj.department else "N/A",
                "designation": obj.designation.title if obj.designation else "N/A",
                "joining_date": obj.joining_date,
                "status": obj.status
            })

        return Response({
            "draw": draw,
            "recordsTotal": total,
            "recordsFiltered": total,
            "data": data
        })


@api_view(['GET'])
def salesman_premium_summary(request, salesman_id):
    total = CompanyPlanItem.objects.filter(
        company_document__companyplan__organization_policy__org_sales_polices__sales_employee_id=salesman_id
    ).aggregate(
        total_premium=Sum('premium_amount')
    )
    
    employee = SalesEmployee.objects.filter(id=salesman_id).first()

    commission_percent = 0

    if employee:
        rule = CommissionRule.objects.filter(
            designation=employee.designation
        ).order_by('-min_achievement').first()

        if rule:
            commission_percent = rule.commission_rate

    return Response({
        "salesman_id": salesman_id,
        "total_premium": total['total_premium'] or 0,
        "commission_percent": commission_percent
    })
    
def get_employee_details(request, employee_id):
    try:
        emp = SalesEmployee.objects.select_related(
            'department',
            'designation',
            'role',
            'manager',
            'line_manager',
            'user'
        ).get(id=employee_id)

        data = {
            "employee_code": emp.employee_code,
            "name": emp.employee_name,
            "email": getattr(emp.user, 'email', ''),
            "phone": emp.phone,
            "father_name": emp.father_name,
            "mother_name": emp.mother_name,
            "department": emp.department.name if emp.department else "",
            "designation": emp.designation.title if emp.designation else "",
            "role": emp.role.name if emp.role else "",
            "line_manager": emp.line_manager.employee_name if emp.line_manager else "",
        }

        return JsonResponse({"success": True, "data": data})

    except SalesEmployee.DoesNotExist:
        return JsonResponse({"success": False, "message": "Employee not found"})

def create_collection(request):

    if request.method == "POST":

        try:
            # =========================
            # BASIC DATA
            # =========================
            org_id = request.POST.get("organization_id")

            premium_amount = Decimal(request.POST.get("premimum_amount") or 0)
            collected_amount = Decimal(request.POST.get("collected_amount") or 0)
            due_amount = Decimal(request.POST.get("due_amount") or 0)

            status = request.POST.get("status")
            payment_type = request.POST.get("payment_type")
            collection_date = request.POST.get("collection_date")

            commission_percent = Decimal(request.POST.get("commission_percent") or 0)
            commission_amount = Decimal(request.POST.get("commision_amount") or 0)

            # =========================
            # GET ORGANIZATION
            # =========================
            org = Organization.objects.select_related('sales_employee').get(id=org_id)

            # =========================
            # DEFAULT VALUES (IMPORTANT)
            # =========================
            bank_obj = None
            bank_account_name = None
            account_number = None
            bank_image = None

            mfs_provider_name = None
            transaction_id = None

            cash_received_by = None
            cash_note = None

            # =========================
            # HANDLE PAYMENT TYPE
            # =========================
            if payment_type == "bank":

                bank_id = request.POST.get("bank_account")
                bank_obj = Bank.objects.filter(id=bank_id).first() if bank_id else None

                account_name = request.POST.get("bank_account_name")
                account_number = request.POST.get("bank_account_number")
                bank_image = request.FILES.get("bank_image")

                # optional transaction id (if you add later)
                transaction_id = request.POST.get("transaction_id")

            elif payment_type == "mfs":

                mfs_provider= request.POST.get("mfs_account")  # select dropdown
                bank_obj = Bank.objects.filter(id=mfs_provider).first() if mfs_provider else None
                account_name = request.POST.get("mfs_account_name")
                account_number = request.POST.get("mfs_account_number")  # ✅ common field
                transaction_id = request.POST.get("mfs_txn_id")

            elif payment_type == "cash":
                account_name = ""
                cash_received_by = request.POST.get("cash_received_by")
                cash_note = request.POST.get("cash_note")

            # =========================
            # CREATE COLLECTION
            # =========================
            collection = PremiumCollection.objects.create(

                organization=org,
                collected_by=org.sales_employee,

                premium_amount=premium_amount,
                collected_amount=collected_amount,
                due_amount=due_amount,

                status=status,
                payment_type=payment_type,

                commission_percent=commission_percent,
                commission_amount=commission_amount,

                collection_date=collection_date,

                # BANK
                bank=bank_obj,
                account_name=account_name,
                account_number=account_number,
                bank_image=bank_image,

                # MFS
                transaction_id=transaction_id,

                # CASH
                cash_received_by=cash_received_by,
                cash_note=cash_note,
            )

            return JsonResponse({
                "success": True,
                "message": "Collection saved successfully",
                "id": collection.id
            })

        except Organization.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "Organization not found"
            })

        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": str(e)
            })

    return JsonResponse({
        "success": False,
        "message": "Invalid request"
    })


def get_commission(request):

    salesman_id = request.GET.get("salesman_id")

    try:
        employee = SalesEmployee.objects.select_related('designation').get(id=salesman_id)

        rule = CommissionRule.objects.filter(
            designation=employee.designation
        ).order_by('-min_achievement').first()

        return JsonResponse({
            "success": True,
            "commission_percent": float(rule.commission_rate) if rule else 0
        })

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})



def collection_report(request):

    organizations = Organization.objects.all()

    context = {
        "organizations": organizations,
      
    }

    return render(request, "reports/collection_summary.html", context)

def collection_report_api(request):

    organization_id = request.GET.get('organization_id')

    today = date.today()

    first_day = today.replace(day=1)
    last_day = today.replace(day=monthrange(today.year, today.month)[1])

    # base filter
    organization = None
    org_filter = {}

    if organization_id:
        org_filter["organization_id"] = organization_id
        organization = Organization.objects.filter(id=organization_id).values(
            "id", "organization_name"
        ).first()
  

    def sum_collection(qs):
        return qs.aggregate(total=Sum('collected_amount'))['total'] or 0

    # =========================
    # COLLECTIONS
    # =========================
    today_collection = sum_collection(
        PremiumCollection.objects.filter(
            **org_filter,
            collection_date=today
        )
    )

    current_month_collection = sum_collection(
        PremiumCollection.objects.filter(
            **org_filter,
            collection_date__range=[first_day, last_day]
        )
    )

    new_business = OrganizationPolicy.objects.filter(
        **org_filter,
        enrollment_date__range=[first_day, last_day]
    ).count()

    renewal_business = OrganizationPolicy.objects.filter(
        **org_filter,
        end_date__range=[first_day, last_day]
    ).count()

    prev_month_end = first_day - timedelta(days=1)
    prev_month_start = prev_month_end.replace(day=1)

    previous_month_collection = sum_collection(
        PremiumCollection.objects.filter(
            **org_filter,
            collection_date__range=[prev_month_start, prev_month_end]
        )
    )

    current_year_collection = sum_collection(
        PremiumCollection.objects.filter(
            **org_filter,
            collection_date__year=today.year
        )
    )

    previous_year_collection = sum_collection(
        PremiumCollection.objects.filter(
            **org_filter,
            collection_date__year=today.year - 1
        )
    )

    # =========================
    # SAFE JSON RESPONSE
    # =========================
    return JsonResponse({
        "organization": organization,
        "date": str(today),

        "today_collection": float(today_collection),
        "current_month_collection": float(current_month_collection),
        "new_business": new_business,
        "renewal_business": renewal_business,
        "previous_month_collection": float(previous_month_collection),
        "current_year_collection": float(current_year_collection),
        "previous_year_collection": float(previous_year_collection),
        "date": str(today),
        "organization_id": organization_id
    })