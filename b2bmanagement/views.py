import json
from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .models import (Organization,District,CompanyType,Bank,SalaryRange,Designation,Plan,Insurer,OrganizationPolicy,
                     CompanyPlanItem,CompanyPlan,CompanyPlanDocument,Department,HospitalInformation,HospitalContact,GopInformation
                     )
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, status,permissions
from collections import defaultdict
from rest_framework.views import APIView
from .serializers import (OrganizationsSerializer,BankSerializer,DesignationSerializer,
                          SalaryRangeSerializer,PlanSerializer,InsurerSerializer,DistrictSerializer,
                          PlanListSerializer,
                          InsurerContactSerializer,
                          InsurerPolicyDocumentsSerializer,
                          HospitalSerializer,
                          InsurerPolicySerializer,
                          InsurerListSerializer,
                          OrganizationContactSerializer,
                          OrganizationPolicyDocumentsSerializer,
                          OrganizationPolicySerializer,
                          OrganizationListSerializer,
                          CompanyPlanItemSerializer,
                          CompanyPlanSerializer,
                          CompanyPlanListSerializer,
                          CompanyPlanDocumentSerializer,
                          CompanyPlanDocumentListSerializer,
                          OrgnaizationListSerializer,
                          CompanyTypeSerializer,
                          HospitalListSerializer,
                          HospitalContactSerializer,
                          GOPSerializer,
                          GOPListSerializer,
                          DepartmentSerializer
                          )
from datetime import date,datetime
from django.db import transaction,IntegrityError
from django.db.models import Q
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.core.paginator import Paginator
from .models import Bank,Designation,Product
from core.utils import  generate_auto_id,group_required_multiple
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view





def create_management_orgonization(request):
    banks=Bank.objects.all()
    designations=Designation.objects.all()
    products=Product.objects.all()
    insurers=Insurer.objects.all()
    plans=Plan.objects.all()
    departments=Department.objects.filter(status=1)
    new_org_auto_id = generate_auto_id(Organization,3)
    company_types=CompanyType.objects.filter(status=1)
    template_name = 'b2bmanagement/add-new-b2b-orgonization.html'
    return render(request, template_name=template_name,context={"company_types":company_types,'banks':banks,"designations":designations,"products":products,"plans":plans,"departments":departments,"insurers":insurers,'new_org_auto_id':new_org_auto_id})

def create_insure(request):
    designations=Designation.objects.all()
    products=Product.objects.all()
    banks=Bank.objects.all()
    new_insurer_auto_id = generate_auto_id(Insurer,3,True)
    company_types=CompanyType.objects.filter(status=1)
    template_name = 'b2bmanagement/add-new-insure.html'
    return render(request, template_name=template_name,context={"company_types":company_types,'banks':banks,"designations":designations,"products":products,"new_insurer_auto_id":new_insurer_auto_id})

def hospitalList(request):
    
    template_name = 'b2bmanagement/hospital_list.html'
    return render(request, template_name=template_name)

def create_hospital(request):
    designations=Designation.objects.all()
    products=Product.objects.all()
    banks=Bank.objects.all()
    districts=District.objects.all()
    template_name = 'b2bmanagement/add-new-hospital.html'
    return render(request, template_name=template_name,context={"districts":districts,'banks':banks,"designations":designations,"products":products})


def b2bOrganizationList(request):
    template_name = 'b2bmanagement/b2b-organization-list.html'
    return render(request, template_name=template_name)


def assignPolicies(request):
    template_name = 'b2bmanagement/assign-policies.html'
    return render(request, template_name=template_name)


def addAssignPolicies(request):
    template_name = 'b2bmanagement/add-assign-policies.html'
    return render(request, template_name=template_name)


def b2bSetting(request):
    template_name = 'b2bmanagement/b2b-setting.html'
    return render(request, template_name=template_name)


def addOrganizationType(request):
    template_name = 'b2bmanagement/add-organization-type.html'
    return render(request, template_name=template_name)


def b2bCustomerEdit(request):
    template_name = 'b2bmanagement/b2b-customer-edit.html'
    return render(request, template_name=template_name)


def bankView(request):
    template_name = 'b2bmanagement/bank-list.html'
    return render(request, template_name=template_name)

def designationView(request):
    template_name = 'b2bmanagement/designation-list.html'
    return render(request, template_name=template_name)

def salaryRangeView(request):
    template_name = 'b2bmanagement/salary-range-list.html'
    return render(request, template_name=template_name)


class InsurerDetailsView(APIView):

    def get(self, request, pk, *args, **kwargs):
        insurer = Insurer.objects.get(pk=pk)
        serializer = InsurerListSerializer(insurer)
        # if request.headers.get('Content-Type') == 'application/json' or request.accepts('application/json'):
        #     return Response({
        #         "status": True,
        #         "message": "Company Plan fetched successfully",
        #         "data": serializer.data,
        #     }, status=status.HTTP_200_OK)
        context = {
            "insurer": serializer.data,
        }
        return render(request, "b2bmanagement/insurer-details-view.html", context)
    
    def put(self, request, pk, *args, **kwargs):
        if request.method == "PUT":
            try:
                insurer = get_object_or_404(Insurer, pk=pk)
                data = json.loads(request.body)  # parse JSON
                # Update fields dynamically
                for field, value in data.items():
                    if hasattr(insurer, field):
                        setattr(insurer, field, value)

                insurer.save()
                return JsonResponse({
                    "success": True,
                    "message": f"Insurer  updated successfully."
                })
            except Exception as e:
                return JsonResponse({"success": False, "error": str(e)})
        return JsonResponse({"success": False, "error": "Invalid request"}, status=400)
    
class OrganizationDetailsView(APIView):

    def get(self, request, pk, *args, **kwargs):
        organization = Organization.objects.get(pk=pk)
        serializer = OrgnaizationListSerializer(organization)
        # if request.headers.get('Content-Type') == 'application/json' or request.accepts('application/json'):
        #     return Response({
        #         "status": True,
        #         "message": "Organization data fetched successfully",
        #         "data": serializer.data,
        #     }, status=status.HTTP_200_OK)
        context = {
            "organization": serializer.data,
        }
        return render(request, "b2bmanagement/org-details-view.html", context)
    
    def put(self, request, pk, *args, **kwargs):
        if request.method == "PUT":
            try:
                org = get_object_or_404(Organization, pk=pk)
                data = json.loads(request.body)  # parse JSON
                # Update fields dynamically
                for field, value in data.items():
                    if hasattr(org, field):
                        setattr(org, field, value)

                org.save()
                return JsonResponse({
                    "success": True,
                    "message": f"Organization  updated successfully."
                })
            except Exception as e:
                return JsonResponse({"success": False, "error": str(e)})
        return JsonResponse({"success": False, "error": "Invalid request"}, status=400)




class OrganizationPolicyView(APIView):    

    def post(self, request, *args, **kwargs):
        data=request.POST
        organization_policy =OrganizationPolicy.objects.filter(
            organization_contract_no=data.get('contract_no'),
            organization=data.get('org_id'),
            ).first()
        if organization_policy:
            organization_policy.delete()
            return Response(
            {"success": True, "message": "Organization policy deleted successfully"},
            status=status.HTTP_200_OK
            )
        return Response(
            {"success": True, "message": "Organization policy didn't deleted successfully"},
            status=status.HTTP_200_OK
            )


def organizationsBoard(request):
    template_name = 'b2bmanagement/organizations-board.html'
    return render(request, template_name=template_name)

def getBankList(request):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        queryset=Bank.objects.all().order_by('-id')      
        # Grabing data with Search value        
        if search_value:
            queryset =  queryset.filter(
                Q(name__icontains=search_value) |
                Q(short_name__icontains=search_value) 
            )
        # counting All records           
        total_records = Bank.objects.count()
        #Count Filetred Data
        filtered_records = queryset.count()
        # Range query data
        banks=queryset[start:start+length]
        #Paginate Query data
        # Serilization by Data        
        serializer = BankSerializer(banks, many=True)
        # Response Data
        return JsonResponse({
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': serializer.data
        })


def getOrganizationData(request):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        # Receiving params from external search fields       

        status = request.GET.get('status')    
        #Get all query data and Orderring by dec     
        queryset=Organization.objects.all().order_by('-id')      
        #Start and End Date check  
        if status:
            queryset=queryset.filter(status=status)    
        # Grabing data with Search value        
        if search_value:
            queryset =  queryset.filter(
                Q(organization_code__icontains=search_value) |
                Q(organization_name__icontains=search_value) |
                Q(trade_license_no__icontains=search_value)
                
            )
        # counting All records           
        total_records = Organization.objects.count()
        #Count Filetred Data
        filtered_records = queryset.count()
        # Range query data
        organizations=queryset[start:start+length]
    
        serializer = OrganizationsSerializer(organizations, many=True)
        # Response Data
        return JsonResponse({
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': serializer.data
        })

def updateOrganization(request,id):
    try:
        banks=Bank.objects.all()
        designations=Designation.objects.all()
        products=Product.objects.all()
        insurers=Insurer.objects.all()
        plans=Plan.objects.all()
        departments=Department.objects.filter(status=1)
        new_org_auto_id = generate_auto_id(Organization,3)
        company_types=CompanyType.objects.filter(status=1)
        organization_data = Organization.objects.get(pk=id)
        serializer = OrgnaizationListSerializer(organization_data)
        print(serializer.data)
        # if request.headers.get('Content-Type') == 'application/json' or request.accepts('application/json'):
        #     return Response({
        #         "status": True,
        #         "message": "Company Plan fetched successfully",
        #         "data": serializer.data,
        #     }, status=status.HTTP_200_OK)
        
        context = { 'form':serializer.data,"company_types":company_types,'banks':banks,"designations":designations,"products":products,"plans":plans,"departments":departments,"insurers":insurers,'new_org_auto_id':new_org_auto_id }
        
        return render(request, 'b2bmanagement/update-b2b-orgonization.html', context) 
    except Organization.DoesNotExist:  # Be explicit about exceptions
        return render(request, 'b2bmanagement/b2b-organization-list.html') 

def designiationPaginationList(request):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        queryset=Designation.objects.all().order_by('-id')      
        # Grabing data with Search value        
        if search_value:
            queryset =  queryset.filter(
                Q(title__icontains=search_value) 
            )
        # counting All records           
        total_records = Designation.objects.count()
        #Count Filetred Data
        filtered_records = queryset.count()
        # Range query data
        banks=queryset[start:start+length]
        #Paginate Query data
        # Serilization by Data        
        serializer = DesignationSerializer(banks, many=True)
        # Response Data
        return JsonResponse({
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': serializer.data
        })


def salaryRangePaginationList(request):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        queryset=SalaryRange.objects.all().order_by('-id')      
        # Grabing data with Search value        
        if search_value:
            queryset =  queryset.filter(
                Q(initial_amount__icontains=search_value) |
                Q(final_amount__icontains=search_value)
            )
        # counting All records           
        total_records = SalaryRange.objects.count()
        #Count Filetred Data
        filtered_records = queryset.count()
        # Range query data
        banks=queryset[start:start+length]
        #Paginate Query data
        # Serilization by Data        
        serializer = SalaryRangeSerializer(banks, many=True)
        # Response Data
        return JsonResponse({
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': serializer.data
        })


class BasicPagination(PageNumberPagination):
    page_size_query_param = 10

class OrganizationView(APIView,PageNumberPagination):
    template_name = 'b2bmanagement/update-organization-type.html'
    queryset = Organization.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = BasicPagination
    serializer_class = OrganizationsSerializer
    
    def post(self, request):
        data = request.POST    
        files =request.FILES   
        data._mutable = True
        if data.get('organization_code'):
            data['organization_contract_no']=f"{data.get('organization_code')}{'-A'}"
        if files.get('trade_license_file'):
            data['trade_license_file']=files.get('trade_license_file')
        if files.get('bin_file'):
            data['bin_file']=files.get('bin_file')
        if files.get('company_logo'):
            data['company_logo']=files.get('company_logo')    
        index = 0
        created_contacts = []
        while True:
            name = request.POST.get(f'name[{index}]')
            designation = request.POST.get(f'designation[{index}]')
            mobile_no = request.POST.get(f'mobile_no[{index}]')
            email=None
            if  request.POST.get(f'email[{index}]'):
                email = request.POST.get(f'email[{index}]')
            if not name:
                break  # Stop when no more rows
            created_contacts.append({
                "name": name,
                "designation": designation,
                "mobile_no":mobile_no,
                "email": email
            }) 
            index += 1    
        if request.method == 'POST':      
            serializer = OrganizationsSerializer(data=data)
            try:
                with transaction.atomic():  
                    if serializer.is_valid(raise_exception=True):
                        organization = serializer.save(created_by=request.user)
                    if organization and len(created_contacts)>0:
                        contactSerilizer = OrganizationContactSerializer(data=created_contacts,many=True)
                        if contactSerilizer.is_valid(raise_exception=True):
                            contacts = contactSerilizer.save(organization=organization,created_by=request.user)
                return Response({'success':True,"message":'Organization has  been saved',"data": {"organization": OrganizationsSerializer(organization).data,
                                    "contacts": OrganizationContactSerializer(contacts,many=True).data}})
            except IntegrityError as e:
                return Response({'status': False, 'message': 'Unexpected error: ' + str(e)},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'status': False, 'message': 'Unexpected error: ' + str(e)},status=status.HTTP_400_BAD_REQUEST)

    
    def put(self, request, pk):
        data =  request.data
        data._mutable = True
        if data['commencement_date']:
            data['commencement_date'] = datetime.strptime(data['commencement_date'], "%d-%m-%Y").date()
        if data['renewal_date']:
            data['renewal_date'] = datetime.strptime(data['renewal_date'], "%d-%m-%Y").date()
        if data['contract_date']:
            data['contract_date'] = datetime.strptime(data['contract_date'], "%d-%m-%Y").date()
        try:
          organization = Organization.objects.get(id=pk) 
        except Organization.DeesNotExist:
            return Response({"error": "Organization not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrganizationsSerializer(organization, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            organization = serializer.save(updated_by=request.user)
            return Response({
                "message": "Organization has been updated",
                "success":True,
                "data":serializer.data
                })  
        return Response({
            "message": "Organization don'/t updated",
            "success":False,
            "data":serializer.errors
            })


    def delete(self, request, pk):
        try:
          #Retrieve Iten by ID
          organization = Organization.objects.get(id=pk)

        except Organization.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        #Delete the organization from the database 
        organization.delete()
        #Return a 284 response
        return Response({"error": False,"message":'Organization deleted'})
    



class OrganizationPolicyCreate(APIView,PageNumberPagination):
    queryset = Insurer.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    pagination_class = BasicPagination
    serializer_class = OrganizationPolicySerializer
    def get(self, request):
        try:
            insurer = OrganizationPolicy.objects.all() #Serialize single item
            serializer = OrganizationPolicySerializer(insurer,many=True)
            return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)

        except Insurer.DoesNotExist:
            return Response({"success":False,"error": "Item not found"},status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        data = request.POST    
        files =request.FILES   
        policy_indices = set()
        for key in data.keys():
            if "contract_title[" in key:
                index = key.split("[")[1].split("]")[0]
                policy_indices.add(index)
        # Iterate over each policy index
        policy_data=[]
        for i in policy_indices:
            organization = data.get('organization')
            policy_type = data.get(f'policy_type[{i}]')
            policy_mode=None
            if data.get(f'policy_mode[{i}]') !="":
                policy_mode = data.get(f'policy_mode[{i}]')
            contract_title = data.get(f'contract_title[{i}]')
            insurer = data.get(f'insurer[{i}]')
            end_date=None
            enrollment_date=None
            remark = data.get(f'remark[{i}]')
            if data.get(f'enroolment_date[{i}]'):
               enrollment_date =  datetime.strptime(data.get(f'enroolment_date[{i}]'), "%d-%m-%Y").date()
            if data.get(f'end_date[{i}]'):
                end_date =  datetime.strptime(data.get(f'end_date[{i}]'), "%d-%m-%Y").date()
            contract_no =data.get(f'contract_no_{i}')
            organization_data={
                "insurer":insurer,
                "organization_contract_no":contract_no,
                "organization":organization,
                "policy_type":policy_type,
                "remarks":remark,
                "contract_title":contract_title,
                "policy_mode":policy_mode,
                "enrollment_date":enrollment_date,
                "end_date":end_date
            }
            uploaded_files = files.getlist(f'upload_document_file[{i}][]')
            org_id =data.get('organization')
            org_policy = OrganizationPolicy.objects.filter(organization_contract_no=contract_no,organization_id=org_id).first()
            if  org_policy:
                    serializer = OrganizationPolicySerializer(org_policy, data=organization_data, partial=True)
            else:
                serializer = OrganizationPolicySerializer(data=organization_data)
            created_files = []
            if serializer.is_valid():
                org_policy = serializer.save(created_by=request.user)
                policy_data.append(serializer.data)
                for file in uploaded_files:
                    documentSerializer = OrganizationPolicyDocumentsSerializer(data={'document': file, 'organization_policy': org_policy.id})
                    if documentSerializer.is_valid():
                        documentSerializer.save(created_by=request.user)
                        created_files.append(documentSerializer.data)
                        policy_data.append({"uploaded_files": created_files})                        
                    else:     
                        return Response({"success":False,"data":documentSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        if len(policy_data) > 0: 
            return Response({"success":True,"data":policy_data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success":False,'policies_data':policy_data}, status=status.HTTP_400_BAD_REQUEST)    

    def put(self, request, pk):
        try:
          insurer = OrganizationPolicy.objects.get(id=pk) 
        except insurer.DeesNotExist:
            return Response({"error": "Organization  Policy not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrganizationPolicySerializer(insurer, data=request.data) 
        if serializer.is_valid():
            insurer = serializer.save(updated_by=request.user)
            return Response({
                "message": "Organization Policy information has been updated",
                "success":True,
                "data":serializer.data
                })  
        return Response({
            "message": "Organization Policy didn't update",
            "success":False,
            "data":serializer.errors
            })


    def delete(self, request, pk):
        try:
            policy = OrganizationPolicy.objects.get(id=pk)
        except OrganizationPolicy.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        policy.delete()
        return Response({"error": False, "message": "Organization has been deleted"})

 
class BankListAPIView(APIView,PageNumberPagination):
    queryset = Bank.objects.all()
    pagination_class = BasicPagination
    serializer_class = OrganizationsSerializer
    authentication_classes = [TokenAuthentication]   # ✔ Require token
    def get(self, request):
        try:
            bank = Bank.objects.all() #Sertalize single item
            serializer = BankSerializer(bank,many=True)
            return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)

        except Bank.DoesNotExist:
            return Response({"success":False,"error": "Item not found"},status=status.HTTP_404_NOT_FOUND)
       

    
class BankView(APIView,PageNumberPagination):
    queryset = Bank.objects.all()
    pagination_class = BasicPagination
    serializer_class = OrganizationsSerializer
    permission_classes = [IsAuthenticated] 
    def get(self, request):
        try:
            bank = Bank.objects.all() #Sertalize single item
            serializer = BankSerializer(bank,many=True)
            return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)

        except Bank.DoesNotExist:
            return Response({"success":False,"error": "Item not found"},status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        # Request Data
        serializer = BankSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({'success':True,"message":'Bank name has been saved',"data":serializer.data})
        else:           
            return Response({'success':False,"message":'Bank name has not been saved',"data":serializer.errors})

    def put(self, request, pk):
        try:
          organization = Bank.objects.get(id=pk) 
        except Bank.DeesNotExist:
            return Response({"error": "Bank not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = BankSerializer(organization, data=request.data) 
        if serializer.is_valid():
            organization = serializer.save(updated_by=request.user)
            return Response({
                "message": "Bank information has been updated",
                "success":True,
                "data":serializer.data
                })  
        return Response({
            "message": "Bank didn't update",
            "success":False,
            "data":serializer.errors
            })


    def delete(self, request, pk):
        try:
          #Retrieve Iten by ID
          bank = Bank.objects.get(id=pk)

        except Bank.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        #Delete the organization from the database 
        bank.delete()
        #Return a 284 response
        return Response({"error": False,"message":'Bank has been deleted'})
    
class BankViewSigleList(APIView):
    def get(self, request,item_id):
        try:
            #Query a single tee by ID
            bank = Bank.objects.get(id=item_id) #Sertalize single item
            serializer = BankSerializer(bank)
            return Response({"success":True,"data":serializer.data}, status=status.HTTP_200_OK)
        except Bank.DoesNotExist:
                return Response({"success":False,"error": "Item not found"},status=status.HTTP_404_NOT_FOUND)

class DepartmentView(APIView,PageNumberPagination):
    queryset = Department.objects.all()
    pagination_class = BasicPagination
    serializer_class = DepartmentSerializer
    authentication_classes = [TokenAuthentication]   # ✔ Require token
    def get(self, request):
        try:
            departments = Department.objects.filter(status=1) #Sertalize single item
            serializer = DepartmentSerializer(departments,many=True)
            return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)

        except Department.DoesNotExist:
            return Response({"success":False,"error": "Item not found"},status=status.HTTP_404_NOT_FOUND)

class DesignationListAPIView(APIView,PageNumberPagination):
    queryset = Designation.objects.all()
    pagination_class = BasicPagination
    serializer_class = DesignationSerializer
    authentication_classes = [TokenAuthentication]   # ✔ Require token
    def get(self, request):
        try:
            bank = Designation.objects.filter(status=1) #Sertalize single item
            serializer = DesignationSerializer(bank,many=True)
            return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)

        except Designation.DoesNotExist:
            return Response({"success":False,"error": "Item not found"},status=status.HTTP_404_NOT_FOUND)
        

class DesignationView(APIView,PageNumberPagination):
    queryset = Designation.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = BasicPagination
    serializer_class = DesignationSerializer
    def get(self, request):
        try:
            bank = Designation.objects.filter(status=1) #Sertalize single item
            serializer = DesignationSerializer(bank,many=True)
            return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)

        except Designation.DoesNotExist:
            return Response({"success":False,"error": "Item not found"},status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        # Request Data
        serializer = DesignationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({'success':True,"message":'Designation has been saved',"data":serializer.data})
        else:           
            return Response({'success':False,"message":'Designation has not been saved',"data":serializer.errors})

    def put(self, request, pk):
        try:
          designation = Designation.objects.get(id=pk) 
        except Designation.DeesNotExist:
            return Response({"error": "Designation not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = DesignationSerializer(designation, data=request.data) 
        if serializer.is_valid():
            designation = serializer.save(updated_by=request.user)
            return Response({
                "message": "Designation information has been updated",
                "success":True,
                "data":serializer.data
                })  
        return Response({
            "message": "Designation didn't update",
            "success":False,
            "data":serializer.errors
            })


    def delete(self, request, pk):
        try:
          #Retrieve Iten by ID
          designation = Designation.objects.get(id=pk)

        except Designation.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        #Delete the organization from the database 
        designation.delete()
        #Return a 284 response
        return Response({"error": False,"message":'Designation has been deleted'})
    
class DesignationViewSigleList(APIView):
    def get(self, request,item_id):
        try:
            #Query a single tee by ID
            designation = Designation.objects.get(id=item_id) #Sertalize single item
            serializer = DesignationSerializer(designation)
            return Response({"success":True,"data":serializer.data}, status=status.HTTP_200_OK)
        except Designation.DoesNotExist:
                return Response({"success":False,"error": "Item not found"},status=status.HTTP_404_NOT_FOUND)

class SalaryRangeView(APIView,PageNumberPagination):
    queryset = SalaryRange.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = BasicPagination
    serializer_class = SalaryRangeSerializer
    def get(self, request):
        try:
            bank = SalaryRange.objects.all() #Sertalize single item
            serializer = SalaryRangeSerializer(bank,many=True)
            return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)

        except SalaryRange.DoesNotExist:
            return Response({"success":False,"error": "Item not found"},status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        # Request Data
        serializer = SalaryRangeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({'success':True,"message":'SalaryRange has been saved',"data":serializer.data})
        else:           
            return Response({'success':False,"message":'SalaryRange has not been saved',"data":serializer.errors})

    def put(self, request, pk):
        try:
          salaryRange = SalaryRange.objects.get(id=pk) 
        except salaryRange.DeesNotExist:
            return Response({"error": "SalaryRange not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = SalaryRangeSerializer(salaryRange, data=request.data) 
        if serializer.is_valid():
            salaryRange = serializer.save(updated_by=request.user)
            return Response({
                "message": "SalaryRange information has been updated",
                "success":True,
                "data":serializer.data
                })  
        return Response({
            "message": "SalaryRange didn't update",
            "success":False,
            "data":serializer.errors
            })


    def delete(self, request, pk):
        try:
          #Retrieve Iten by ID
          salaryRange = SalaryRange.objects.get(id=pk)

        except SalaryRange.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        #Delete the organization from the database 
        salaryRange.delete()
        #Return a 284 response
        return Response({"error": False,"message":'SalaryRange has been deleted'})
    
class SalaryRangeViewSigleList(APIView):
    def get(self, request,item_id):
        try:
            #Query a single tee by ID
            salaryRange = SalaryRange.objects.get(id=item_id) #Sertalize single item
            serializer = SalaryRangeSerializer(salaryRange)
            return Response({"success":True,"data":serializer.data}, status=status.HTTP_200_OK)
        except SalaryRange.DoesNotExist:
                return Response({"success":False,"error": "Item not found"},status=status.HTTP_404_NOT_FOUND)


# Plan Section

def planView(request):
    salaryRange=SalaryRange.objects.all()
    designations=Designation.objects.all()
    context = {
        "salaryRange":salaryRange,
        "designations":designations
    }
    template_name = 'b2bmanagement/plan-list.html'
    return render(request, template_name=template_name,context=context)

def planPaginationList(request):
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')
    queryset=Plan.objects.all().order_by('id')      
    # Grabing data with Search value        
    if search_value:
        queryset =  queryset.filter(
            Q(name__icontains=search_value) |
            Q(designation__title__icontains=search_value)
        )
    # counting All records           
    total_records = Plan.objects.count()
    #Count Filetred Data
    filtered_records = queryset.count()
    # Range query data
    banks=queryset[start:start+length]
    #Paginate Query data
    # Serilization by Data        
    serializer = PlanListSerializer(banks, many=True)
    # Response Data
    return JsonResponse({
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': filtered_records,
        'data': serializer.data
    })




class PlanView(APIView,PageNumberPagination):
    queryset = Plan.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = BasicPagination
    serializer_class = PlanSerializer
    def get(self, request):
        try:
            plan = Plan.objects.all() #Sertalize single item
            serializer = SalaryRangeSerializer(plan,many=True)
            return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)

        except Plan.DoesNotExist:
            return Response({"success":False,"error": "Item not found"},status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        # Request Data
        serializer = PlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success':True,"message":'Plan has been saved',"data":serializer.data})
        else:   
            return Response({'success':False,"message":'Plan has not been saved',"data":serializer.errors})

    def put(self, request, pk):
        try:
          plan = Plan.objects.get(id=pk) 
        except plan.DeesNotExist:
            return Response({"error": "Plan not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PlanSerializer(plan, data=request.data) 
        if serializer.is_valid():
            plan = serializer.save(updated_by=request.user)
            return Response({
                "message": "Plan information has been updated",
                "success":True,
                "data":serializer.data
                }) 
        else: 
            return Response({
                "message": "Plan didn't update",
                "success":False,
                "data":serializer.errors
                })


    def delete(self, request, pk):
        try:
          #Retrieve Iten by ID
          plan = Plan.objects.get(id=pk)

        except plan.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        #Delete the plan from the database 
        plan.delete()
        return Response({"error": False,"message":'Plan has been deleted'})
    
class PlanViewSigleList(APIView):
    def get(self, request,item_id):
        try:
            #Query a single tee by ID
            plan = Plan.objects.get(id=item_id) #Sertalize single item
            serializer = PlanSerializer(plan)
            return Response({"success":True,"data":serializer.data}, status=status.HTTP_200_OK)
        except Plan.DoesNotExist:
                return Response({"success":False,"error": "Item not found"},status=status.HTTP_404_NOT_FOUND)



# Company Type Section

def companyTypeView(request):
    template_name = 'b2bmanagement/company_type.html'
    return render(request, template_name=template_name)

def companyPaginationList(request):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        queryset=CompanyType.objects.all().order_by('-id')      
        # Grabing data with Search value        
        if search_value:
            queryset =  queryset.filter(
                Q(name__icontains=search_value)  
                
            )
        # counting All records           
        total_records = CompanyType.objects.count()
        #Count Filetred Data
        filtered_records = queryset.count()
        # Range query data
        types=queryset[start:start+length]
        #Paginate Query data
        # Serilization by Data        
        serializer = CompanyTypeSerializer(types, many=True)
        # Response Data
        return JsonResponse({
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': serializer.data
        })



class CompanyTypeView(APIView,PageNumberPagination):
    queryset = CompanyType.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    pagination_class = BasicPagination
    serializer_class = CompanyTypeSerializer
    def get(self, request):
        try:
            company_types = CompanyType.objects.filter(status=1) #Serialize single item
            serializer = CompanyTypeSerializer(company_types,many=True)
            return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)

        except CompanyType.DoesNotExist:
            return Response({"success":False,"error": "Item not found"},status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        # Request Data
        serializer = CompanyTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({'success':True,"message":'Company type name has been saved',"data":serializer.data})
        else:           
            return Response({'success':False,"message":'Company type name has not been saved',"data":serializer.errors})

    def put(self, request, pk):
        try:
          companyType = CompanyType.objects.get(id=pk) 
        except companyType.DeesNotExist:
            return Response({"error": "Insurer not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CompanyTypeSerializer(companyType, data=request.data) 
        if serializer.is_valid():
            companyType = serializer.save(updated_by=request.user)
            return Response({
                "message": "Compnay type has been updated",
                "success":True,
                "data":serializer.data
                })  
        return Response({
            "message": "Compnay type didn't update",
            "success":False,
            "data":serializer.errors
            })


    def delete(self, request, pk):
        try:
        # Retrieve company type by ID
            company_type = CompanyType.objects.get(pk=pk)
        except CompanyType.DoesNotExist:
            return Response(
            {"error": "Company type not found"},
            status=status.HTTP_404_NOT_FOUND
            )
        # Direct delete from database
        company_type.delete()

        return Response(
            {"error": False, "message": "Company type has been deleted"},
            status=status.HTTP_200_OK
        
        )

class CompanyTypeViewSigleList(APIView):
    def get(self, request,item_id):
        try:
            #Query a single tee by ID
            designation = CompanyType.objects.get(id=item_id) #Sertalize single item
            serializer = CompanyTypeSerializer(designation)
            return Response({"success":True,"data":serializer.data}, status=status.HTTP_200_OK)
        except Designation.DoesNotExist:
                return Response({"success":False,"error": "Item not found"},status=status.HTTP_404_NOT_FOUND)


class HopitalCreateAPIView(APIView,PageNumberPagination):
    queryset = HospitalInformation.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    pagination_class = BasicPagination
    serializer_class = HospitalSerializer
    
    def get(self, request, pk=None):
        # GET BY ID
        if pk is not None:
            try:
                hospital = HospitalInformation.objects.get(id=pk)
            except HospitalInformation.DoesNotExist:
                return Response({"success": False, "error": "Hospital not found"}, status=404)
         
            serializer = HospitalSerializer(hospital,context={"request": request})
            districts=District.objects.filter(is_active=1)
            designations=Designation.objects.filter(status=1)
            banks=Bank.objects.filter(status=1)
            context = {
            "hospital": serializer.data,
            "districts":districts,
            "designations":designations,
            "banks":banks
            }
            return render(request, "b2bmanagement/edit-hospital.html", context)
            
        hospitals = HospitalInformation.objects.all()
        serializer = HospitalSerializer(hospitals, many=True,context={"request": request})
        context = {
            "hospital": serializer.data,
        }
        return Response({"success": True, "data": serializer.data}, status=200)


    
    def post(self, request):
        data = request.POST    
        files =request.FILES   
        data._mutable = True 
        if request.method == 'POST':
            if files.get('hospital_logo'):
                data['hospital_logo']=files.get('hospital_logo')
            if files.get('bin_file'):
                data['bin_file']=files.get('bin_file')
            if files.get('tin_file'):
                data['tin_file']=files.get('tin_file')    
            print(data)
            serializer = HospitalSerializer(data=data)
            index = 0
            created_contacts = []
            while True:
                name = request.POST.get(f'name[{index}]')
                designation = request.POST.get(f'designation[{index}]')
                mobile_no = request.POST.get(f'mobile_no[{index}]')
                status = request.POST.get(f'status[{index}]')
                email=None
                if  request.POST.get(f'email[{index}]'):
                    email = request.POST.get(f'email[{index}]')
                if not name:
                    break  # Stop when no more rows
                created_contacts.append({
                    "name": name,
                    "designation": designation,
                    "mobile_no":mobile_no,
                    "email": email,
                    "status":status
                }) 
                index += 1  
            try:
                with transaction.atomic():  
                    if serializer.is_valid(raise_exception=True):
                        hospital = serializer.save(created_by=request.user)
                        if hospital:
                            contactSerilizer = HospitalContactSerializer(data=created_contacts,many=True)
                            if contactSerilizer.is_valid(raise_exception=True):
                                contactSerilizer.save(hospital=hospital)
                        return Response({'success':True,"message":'Hospital has  been saved',"data": {"hospitalcontact": HospitalSerializer(contactSerilizer).data,                                                  }})
            except IntegrityError as e:
                return Response({"status": False,"message": f"Unexpected error: {str(e)}","data": []},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"status": False, "message": f"Unexpected error: {str(e)}", "data": []},status=status.HTTP_400_BAD_REQUEST)

   
    def put(self, request, pk):
        try:
            hospital = HospitalInformation.objects.get(id=pk)
        except HospitalInformation.DoesNotExist:
            return Response({"error": "Hospital not found"}, status=404)

        data = request.POST.copy()  # Make mutable
        files = request.FILES

        # Handle file updates
        if files.get('hospital_logo'):
            data['hospital_logo'] = files.get('hospital_logo')
        else:
            data['hospital_logo'] = hospital.hospital_logo

        if files.get('bin_file'):
            data['bin_file'] = files.get('bin_file')
        else:
            data['bin_file'] = hospital.bin_file

        if files.get('tin_file'):
            data['tin_file'] = files.get('tin_file')
        else:
            data['tin_file'] = hospital.tin_file

        serializer = HospitalSerializer(hospital, data=data, partial=True)

        # Parse contact rows
        index = 0
        updated_contacts = []
        while True:
            name = request.POST.get(f'name[{index}]')
            if not name:
                break

            designation = request.POST.get(f'designation[{index}]')
            mobile_no = request.POST.get(f'mobile_no[{index}]')
            status = request.POST.get(f'status[{index}]')
            email = request.POST.get(f'email[{index}]')

            updated_contacts.append({
                "name": name,
                "designation": designation,
                "mobile_no": mobile_no,
                "email": email,
                "status": status
            })
            index += 1

        try:
            with transaction.atomic():
                if serializer.is_valid(raise_exception=True):
                    hospital = serializer.save(updated_by=request.user)

                    # Delete old contacts first (or update logic)
                    hospital.hospital_contacts.all().delete()

                    # Create new/updated contacts
                    contact_serializer = HospitalContactSerializer(data=updated_contacts, many=True)
                    if contact_serializer.is_valid(raise_exception=True):
                        contact_serializer.save(hospital=hospital)

                    return Response({
                        "success": True,
                        "message": "Hospital updated successfully",
                        "data": {
                            "hospital": HospitalSerializer(hospital, context={"request": request}).data,
                            "contacts": contact_serializer.data
                        }
                    })

        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=400) 
   
    def delete(self, request, pk):
        try:
          #Retrieve Iten by ID
          hospital = HospitalInformation.objects.get(id=pk)

        except hospital.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        #Delete the plan insurer the database 
        hospital.delete()
        return Response({"error": False,"message":'Hospital has been deleted'})
    



class InsurerPolicyCreate(APIView,PageNumberPagination):
    queryset = Insurer.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    pagination_class = BasicPagination
    serializer_class = InsurerPolicySerializer
    def get(self, request):
        try:
            insurer = Insurer.objects.all() #Serialize single item
            serializer = InsurerPolicySerializer(insurer,many=True)
            return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)

        except Insurer.DoesNotExist:
            return Response({"success":False,"error": "Item not found"},status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        data = request.POST    
        files =request.FILES   
        policy_indices = set()
        for key in data.keys():
            if "contract_title[" in key:
                index = key.split("[")[1].split("]")[0]
                policy_indices.add(index)
        # Iterate over each policy index
        policy_data=[]
        for i in policy_indices:
            insurer = data.get('insurer')
            contract_title = data.get(f'contract_title[{i}]')
            insurer_contract_no = data.get(f'insurer_contract_no[{i}]')
            
            end_date=None
            enrollment_date=None
            remark = data.get(f'remark[{i}]')
            if data.get(f'enroolment_date[{i}]'):
               enrollment_date =  datetime.strptime(data.get(f'enroolment_date[{i}]'), "%d-%m-%Y").date()
            if data.get(f'end_date[{i}]'):
                end_date =  datetime.strptime(data.get(f'end_date[{i}]'), "%d-%m-%Y").date()
            insure_data={
                "insurer":insurer,
                "remarks":remark,
                "insurer_contract_no" :insurer_contract_no,
                "contract_title":contract_title,
                "enrollment_date":enrollment_date,
                "end_date":end_date
            }
            uploaded_files = files.getlist(f'upload_document_file[{i}][]')
            serializer = InsurerPolicySerializer(data=insure_data)
            created_files = []
            if serializer.is_valid():
                policy = serializer.save(created_by=request.user)
                policy_data.append(serializer.data)
                for file in uploaded_files:
                    documentSerializer = InsurerPolicyDocumentsSerializer(data={'document': file, 'insurer_policy': policy.id})
                    if documentSerializer.is_valid():
                        documentSerializer.save(created_by=request.user)
                        created_files.append(documentSerializer.data)
                        policy_data.append({"uploaded_files": created_files})                        
                    else:     
                        return Response({"success":False,"data":documentSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        if len(policy_data) > 0: 
            return Response({"success":True,"data":policy_data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success":False,'policies_data':policy_data}, status=status.HTTP_400_BAD_REQUEST)    

    def put(self, request, pk):
        try:
          insurer = Insurer.objects.get(id=pk) 
        except insurer.DeesNotExist:
            return Response({"error": "Insurer not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = InsurerSerializer(insurer, data=request.data) 
        if serializer.is_valid():
            insurer = serializer.save(updated_by=request.user)
            return Response({
                "message": "Insurer information has been updated",
                "success":True,
                "data":serializer.data
                })  
        return Response({
            "message": "Insurer didn't update",
            "success":False,
            "data":serializer.errors
            })


    def delete(self, request, pk):
        try:
          #Retrieve Iten by ID
          insurer = Insurer.objects.get(id=pk)

        except insurer.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        #Delete the plan insurer the database 
        insurer.delete()
        return Response({"error": False,"message":'Insurer has been deleted'})
    


    
class InsurerViewSigleList(APIView):
    def get(self, request,item_id):
        try:
            #Query a single tee by ID
            plan = Insurer.objects.get(id=item_id) #Sertalize single item
            serializer = InsurerListSerializer(plan)
            return Response({"success":True,"data":serializer.data}, status=status.HTTP_200_OK)
        except Insurer.DoesNotExist:
                return Response({"success":False,"error": "Item not found"},status=status.HTTP_404_NOT_FOUND)






def CompanyPlanView(request):
    plans=Plan.objects.all().order_by("name")
    products=Product.objects.all()
    organizations=Organization.objects.all()    
    template_name = 'b2bmanagement/company-wise-plan.html'
    return render(request, template_name=template_name,context={"plans":plans,"organizations":organizations,"products":products})




class CompanyPlanCreate(APIView,PageNumberPagination):
    queryset = CompanyPlanItem.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    pagination_class = BasicPagination
    serializer_class = CompanyPlanSerializer
    def get(self, request):
        try:
            company = CompanyPlan.objects.all() #Serialize single item
            serializer = CompanyPlanSerializer(company,many=True)
            return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)

        except Insurer.DoesNotExist:
            return Response({"success":False,"error": "Item not found"},status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        data = request.POST    
        organization = data.get('organization')
        plan = str(data.get('plan')).strip()
        policy_indices = set()
        org_contract_id=request.POST.get('contract_no')
        org_policy = OrganizationPolicy.objects.filter(organization__id=organization,organization_contract_no=org_contract_id).first()
        if org_policy:
            org_id=org_policy.id
        else:
            org_policy = OrganizationPolicy.objects.create(organization_id=organization,organization_contract_no=org_contract_id)
            org_id=org_policy.id
        compnay_plans={
            'organization_policy':org_id
        }
       
        companySerializer = CompanyPlanSerializer(data=compnay_plans)
        plans_data=[]
        if companySerializer.is_valid():
            if  data.get('plan_type_name')=='A':
                companyplan= companySerializer.save(created_by=request.user) 
            else:
                company_plan_id=data.get('company_plan_id')
                companyplan=CompanyPlan.objects.get(pk=company_plan_id)
                companySerializer = CompanyPlanSerializer(companyplan)
            if companyplan:
    
                doc_data={ 
                            "companyplan":companyplan.id,
                            "company_plan_doc" : request.FILES.get("upload_document_file", None),
                            "plan":plan
                          }   
                compnayDocSerilizer=CompanyPlanDocumentSerializer(data=doc_data)
                if compnayDocSerilizer.is_valid():
                    companydoc=compnayDocSerilizer.save(created_by=request.user)
                    if companydoc:
                        for key in data.keys():
                            if "policy_type[" in key:
                                index = key.split("[")[1].split("]")[0]
                                policy_indices.add(index)
                    
                        for i in policy_indices:          
                            coverage_type = data.get(f'coverage_type[{i}]')
                            plan = data.get('plan')
                            coverage_amount = data.get(f'coverage_amount[{i}]')
                            policy_type = data.get(f'policy_type[{i}]')
                            premium_rate = data.get(f'premium_rate[{i}]')
                            premium_amount = data.get(f'premium_amount[{i}]')
                            insured_beneficiary_no = data.get(f'insured_beneficiary_no[{i}]')
                            total = data.get(f'total[{i}]')
                            plan_data={
                                "company_document":companydoc.id,
                                "coverage_type":coverage_type,
                                "coverage_amount":coverage_amount,
                                "policy_type":policy_type,
                                "premium_rate":premium_rate,
                                "premium_amount":premium_amount,
                                "insured_beneficiary_no":insured_beneficiary_no,
                                "total":total
                            
                            }
                            plans_data.append(plan_data)
                    if len(plans_data) > 0: 
                        plansSerilizer = CompanyPlanItemSerializer(data=plans_data,many=True)
                        if plansSerilizer.is_valid():
                            plansSerilizer.save(created_by=request.user) 
                            return Response({"success":True,"message":'Company Plan Created',"data":companySerializer.data}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"success":False,"message":"Company Plan didn't save",'data':[]}, status=status.HTTP_400_BAD_REQUEST)    
            # print(companySerializer.errors)
            return Response({"success":False,"message":"Company Plan didn't save",'data':[]}, status=status.HTTP_400_BAD_REQUEST)  
    def put(self, request, pk):
        try:
          insurer = OrganizationPolicy.objects.get(id=pk) 
        except insurer.DeesNotExist:
            return Response({"error": "Organization  Policy not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrganizationPolicySerializer(insurer, data=request.data) 
        if serializer.is_valid():
            insurer = serializer.save(updated_by=request.user)
            return Response({
                "message": "Organization Policy information has been updated",
                "success":True,
                "data":serializer.data
                })  
        return Response({
            "message": "Organization Policy didn't update",
            "success":False,
            "data":serializer.errors
            })


    def delete(self, request, pk):
        try:
          #Retrieve Iten by ID
          insurer = Insurer.objects.get(id=pk)

        except insurer.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        #Delete the plan insurer the database 
        insurer.delete()
        return Response({"error": False,"message":'Insurer has been deleted'})
    

def CompanyPlanListView(request):
    plans=Plan.objects.all().order_by("name")
    products=Product.objects.all()
    organizations=Organization.objects.all()    
    template_name = 'b2bmanagement/company-plan-list.html'
    return render(request, template_name=template_name,context={"plans":plans,"organizations":organizations,"products":products})


def CompanyPlanPaginationList(request):
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')
    queryset=CompanyPlan.objects.all().prefetch_related('company_plan_documents').all().order_by('-id')      
    # Grabing data with Search value        
    if search_value:
        queryset =  queryset.filter(
            Q(organization__organization_name__icontains=search_value) |
            Q(deorganization__organization__code__icontains=search_value) 
        )
    # counting All records           
    total_records = CompanyPlan.objects.count()
    #Count Filetred Data
    filtered_records = queryset.count()
    # Range query data
    company_plans=queryset[start:start+length]
    #Paginate Query data
    # Serilization by Data        
    serializer = CompanyPlanListSerializer(company_plans, many=True)
    # Response Data
    return JsonResponse({
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': filtered_records,
        'data': serializer.data
    })


class CompanyDetailAPIView(APIView):

    def get(self, request, pk, *args, **kwargs):
        company_plan = CompanyPlan.objects.get(pk=pk)
        serializer = CompanyPlanListSerializer(company_plan)
        # if request.headers.get('Content-Type') == 'application/json' or request.accepts('application/json'):
        #     return Response({
        #         "status": True,
        #         "message": "Company Plan fetched successfully",
        #         "data": serializer.data,
        #     }, status=status.HTTP_200_OK)
        context = {
            "company_plan": serializer.data,
        }
        return render(request, "b2bmanagement/company-wise-plan-view.html", context)


def insurerView(request):
    template_name = 'b2bmanagement/insurer-list.html'
    return render(request, template_name=template_name)

def insurerPaginationList(request):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        queryset=Insurer.objects.all().order_by('-id')      
        # Grabing data with Search value        
        if search_value:
            queryset =  queryset.filter(
                Q(insurer_code__icontains=search_value | Q(insurer_contract_no__icontains=search_value)
                | Q(trade_license_no__icontains=search_value)  
                ) 
            )
        # counting All records           
        total_records = Insurer.objects.count()
        #Count Filetred Data
        filtered_records = queryset.count()
        # Range query data
        insurers=queryset[start:start+length]
        #Paginate Query data
        # Serilization by Data        
        serializer = InsurerListSerializer(insurers, many=True)
        # Response Data
        return JsonResponse({
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': serializer.data
        })


def hospitalPaginationList(request):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        queryset=HospitalInformation.objects.all().order_by('-id')      
        # Grabing data with Search value        
        if search_value:
            queryset =  queryset.filter(
                Q(hospital_name__icontains=search_value | Q(hospital__district_name__icontains=search_value)
                ) 
            )
        # counting All records           
        total_records = HospitalInformation.objects.count()
        #Count Filetred Data
        filtered_records = queryset.count()
        # Range query data
        hospitals=queryset[start:start+length]
        #Paginate Query data
        # Serilization by Data        
        serializer = HospitalSerializer(hospitals, many=True)
        # Response Data
        return JsonResponse({
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': serializer.data
        })



class InsurerView(APIView,PageNumberPagination):
    queryset = Insurer.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    pagination_class = BasicPagination
    serializer_class = InsurerSerializer
    def get(self, request):
        try:
            insurer = Insurer.objects.all() #Serialize single item
            serializer = InsurerSerializer(insurer,many=True)
            return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)

        except Insurer.DoesNotExist:
            return Response({"success":False,"error": "Item not found"},status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        data = request.POST    
        files =request.FILES   
        data._mutable = True
        if data.get('insurer_code'):
            data['insurer_contract_no']=f"{data.get('insurer_code')}{'-A'}"
        if files.get('trade_license_file'):
            data['trade_license_file']=files.get('trade_license_file')
        if files.get('bin_file'):
            data['bin_file']=files.get('bin_file')
        if files.get('company_logo'):
            data['company_logo']=files.get('company_logo')    
        if request.method == 'POST':
            serializer = InsurerSerializer(data=data)
            index = 0
            created_contacts = []
            while True:
                name = request.POST.get(f'name[{index}]')
                designation = request.POST.get(f'designation[{index}]')
                mobile_no = request.POST.get(f'mobile_no[{index}]')
                email=None
                if  request.POST.get(f'email[{index}]'):
                    email = request.POST.get(f'email[{index}]')
                if not name:
                    break  # Stop when no more rows
                created_contacts.append({
                    "name": name,
                    "designation": designation,
                    "mobile_no":mobile_no,
                    "email": email
                }) 
                index += 1  
            try:
                with transaction.atomic():  
                    if serializer.is_valid(raise_exception=True):
                        insurer = serializer.save(created_by=request.user)
                        if insurer:
                            contactSerilizer = InsurerContactSerializer(data=created_contacts,many=True)
                            if contactSerilizer.is_valid(raise_exception=True):
                                contactSerilizer.save(insurer=insurer)
                return Response({'success':True,"message":'Insurer has  been saved',"data": {"insurer": InsurerSerializer(insurer).data,
                                        }})
            except IntegrityError as e:
              return Response({"status": False,"message": f"Unexpected error: {str(e)}","data": []},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"status": False, "message": f"Unexpected error: {str(e)}", "data": []},status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
          insurer = Insurer.objects.get(id=pk) 
        except insurer.DeesNotExist:
            return Response({"error": "Insurer not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = InsurerSerializer(insurer, data=request.data) 
        if serializer.is_valid():
            insurer = serializer.save(updated_by=request.user)
            return Response({
                "message": "Insurer information has been updated",
                "success":True,
                "data":serializer.data
                })  
        return Response({
            "message": "Insurer didn't update",
            "success":False,
            "data":serializer.errors
            })


    def delete(self, request, pk):
        try:
          #Retrieve Iten by ID
          insurer = Insurer.objects.get(id=pk)

        except insurer.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        #Delete the plan insurer the database 
        insurer.delete()
        return Response({"error": False,"message":'Insurer has been deleted'})



def districtView(request):
    template_name = 'b2bmanagement/district-list.html'
    return render(request, template_name=template_name)

def DistrictiewPaginationSigleList(request):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        queryset=District.objects.all().order_by('-id')      
        # Grabing data with Search value        
        if search_value:
            queryset =  queryset.filter(
                Q(name__icontains=search_value)  
                
            )
        # counting All records           
        total_records = District.objects.count()
        #Count Filetred Data
        filtered_records = queryset.count()
        # Range query data
        types=queryset[start:start+length]
        #Paginate Query data
        # Serilization by Data        
        serializer = DistrictSerializer(types, many=True)
        # Response Data
        return JsonResponse({
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': serializer.data
        })


class DistrictListView(APIView,PageNumberPagination):
    queryset = District.objects.all()
    pagination_class = BasicPagination
    serializer_class = DistrictSerializer
    authentication_classes = [TokenAuthentication]   # ✔ Require token
    def get(self, request):
        try:
            districts = District.objects.filter(is_active=1) #Serialize single item
            serializer = DistrictSerializer(districts,many=True)
            return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)

        except District.DoesNotExist:
            return Response({"success":False,"error": "Item not found"},status=status.HTTP_404_NOT_FOUND)
 

class DistrictView(APIView,PageNumberPagination):
    queryset = District.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = BasicPagination
    serializer_class = DistrictSerializer
    def get(self, request):
        try:
            districts = District.objects.filter(is_active=1) #Serialize single item
            serializer = DistrictSerializer(districts,many=True)
            return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)

        except District.DoesNotExist:
            return Response({"success":False,"error": "Item not found"},status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        # Request Data
        
        serializer = DistrictSerializer(data=request.data)
       
        if serializer.is_valid():
            serializer.save(is_active=True)
            return Response({'success':True,"message":'District name has been saved',"data":serializer.data})
        else:           
            return Response({'success':False,"message":'District name has not been saved',"data":serializer.errors})

    def put(self, request, pk):
        data = request.data.copy()  # make mutable
        is_active_value = data.get('is_active')  
        print(data.get('is_active')  )
        if  is_active_value == 'on':
            data['is_active']=True
        else:
            data['is_active']= False
        try:
          district = District.objects.get(id=pk) 
        except district.DeesNotExist:
            return Response({"error": "Insurer not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = DistrictSerializer(district, data=request.data) 
        if serializer.is_valid():
            district = serializer.save(updated_by=request.user)
            return Response({
                "message": "District type has been updated",
                "success":True,
                "data":serializer.data
                })  
        return Response({
            "message": "District type didn't update",
            "success":False,
            "data":serializer.errors
            })


    def delete(self, request, pk):
        try:
          #Retrieve Iten by ID
          district = District.objects.get(id=pk)

        except district.DoesNotExist:
            return Response({"error": "District type not found"}, status=status.HTTP_404_NOT_FOUND)

        #Delete the plan insurer the database 
        district.is_active = False                  # example field
        district.save()
        return Response({"error": False,"message":'District type has been deleted'})


class DistrictiewSigleList(APIView):
    def get(self, request,item_id):
        try:
            #Query a single tee by ID
            designation = District.objects.get(id=item_id) #Sertalize single item
            serializer = DistrictSerializer(designation)
            return Response({"success":True,"data":serializer.data}, status=status.HTTP_200_OK)
        except District.DoesNotExist:
                return Response({"success":False,"error": "Item not found"},status=status.HTTP_404_NOT_FOUND)


@group_required_multiple("Super Admin")
def CreateGop(request):
    hospitals=HospitalInformation.objects.filter(status=1)
    template_name = 'b2bmanagement/create-gop.html'
    return render(request, template_name=template_name,context={"hospitals":hospitals})

@group_required_multiple("Super Admin")
def GopsView(request):
    template_name = 'b2bmanagement/gops.html'
    return render(request, template_name=template_name)


class GOPCreateAPIView(APIView,PageNumberPagination):
    queryset = GopInformation.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    pagination_class = BasicPagination
    serializer_class = GOPSerializer
    
    def get(self, request, pk=None):
        # GET BY ID
        if pk is not None:
            try:
                hospital = GopInformation.objects.get(id=pk)
            except GopInformation.DoesNotExist:
                return Response({"success": False, "error": "GOP not found"}, status=404)
         
            serializer = GOPSerializer(hospital,context={"request": request})
            hospital=GopInformation.objects.filter(is_active=1)
            context = {
            "hospital": serializer.data,
            }
            return render(request, "b2bmanagement/edit-gop.html", context)
            
        gops = GOPSerializer.objects.all()
        serializer = GOPSerializer(gops, many=True,context={"request": request})
        context = {
            "gops": serializer.data,
        }
        return Response({"success": True, "data": serializer.data}, status=200)


    
    def post(self, request):
        data = request.POST    
        files =request.FILES   
        print(files)
        data._mutable = True 
        if request.method == 'POST':
            if files.get('document'):
                data['document']=files.get('document')
            serializer = GOPSerializer(data=data)
            if serializer.is_valid():
                serializer.save(created_by=request.user)
                return Response({'success':True,"message":'GOP has  been saved',"data": serializer.data },status=200)
            else:
                print(serializer.errors)
                return Response({'success':False,"message":'GOP has not been saved',"data": serializer.errors}, status=404)
 
   
    def put(self, request, pk):
        try:
            hospital = HospitalInformation.objects.get(id=pk)
        except HospitalInformation.DoesNotExist:
            return Response({"error": "Hospital not found"}, status=404)

        data = request.POST.copy()  # Make mutable
        files = request.FILES

        # Handle file updates
        if files.get('hospital_logo'):
            data['hospital_logo'] = files.get('hospital_logo')
        else:
            data['hospital_logo'] = hospital.hospital_logo

        if files.get('bin_file'):
            data['bin_file'] = files.get('bin_file')
        else:
            data['bin_file'] = hospital.bin_file

        if files.get('tin_file'):
            data['tin_file'] = files.get('tin_file')
        else:
            data['tin_file'] = hospital.tin_file

        serializer = HospitalSerializer(hospital, data=data, partial=True)

        # Parse contact rows
        index = 0
        updated_contacts = []
        while True:
            name = request.POST.get(f'name[{index}]')
            if not name:
                break

            designation = request.POST.get(f'designation[{index}]')
            mobile_no = request.POST.get(f'mobile_no[{index}]')
            status = request.POST.get(f'status[{index}]')
            email = request.POST.get(f'email[{index}]')

            updated_contacts.append({
                "name": name,
                "designation": designation,
                "mobile_no": mobile_no,
                "email": email,
                "status": status
            })
            index += 1

        try:
            with transaction.atomic():
                if serializer.is_valid(raise_exception=True):
                    hospital = serializer.save(updated_by=request.user)

                    # Delete old contacts first (or update logic)
                    hospital.hospital_contacts.all().delete()

                    # Create new/updated contacts
                    contact_serializer = HospitalContactSerializer(data=updated_contacts, many=True)
                    if contact_serializer.is_valid(raise_exception=True):
                        contact_serializer.save(hospital=hospital)

                    return Response({
                        "success": True,
                        "message": "Hospital updated successfully",
                        "data": {
                            "hospital": HospitalSerializer(hospital, context={"request": request}).data,
                            "contacts": contact_serializer.data
                        }
                    })

        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=400) 
   
    def delete(self, request, pk):
        try:
          #Retrieve Iten by ID
          hospital = HospitalInformation.objects.get(id=pk)

        except hospital.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        #Delete the plan insurer the database 
        hospital.delete()
        return Response({"error": False,"message":'Hospital has been deleted'})

def gopPaginationList(request):
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')
    queryset=GopInformation.objects.all().order_by('id')      
    # Grabing data with Search value        
    if search_value:
        queryset =  queryset.filter(
            Q(hospital__hospital_name__icontains=search_value) |
            Q(bed_cabin_word_no__icontains=search_value) |
            Q(attendant_name__icontains=search_value) |
            Q(attendant_mobile__icontains=search_value)
        )
        
    # counting All records           
    total_records = GopInformation.objects.count()
    #Count Filetred Data
    filtered_records = queryset.count()
    # Range query data
    banks=queryset[start:start+length]
    #Paginate Query data
    # Serilization by Data        
    serializer = GOPListSerializer(banks, many=True)
    # Response Data
    return JsonResponse({
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': filtered_records,
        'data': serializer.data
    })


