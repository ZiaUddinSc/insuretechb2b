import json
import base64
import uuid
from django.core.files.base import ContentFile
from django.utils import timezone
from django.shortcuts import render
from django.http import JsonResponse
from b2bproduct.models import Policy
from rest_framework import status
from rest_framework import status
from .models import District,Currency,EmployeeInformation, ClaimInformation, FileTransferHistory, ClaimDocuments,ClaimCostItem
from django.contrib.auth.hashers import make_password
from b2bmanagement.models import Bank,Insurer
from rest_framework.decorators import api_view, parser_classes,permission_classes,authentication_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.contrib.auth.models import Group
from rest_framework.views import APIView
from .serializers import EmployeeInformationOrgSerializer,ClaimInformationListSerializer,CurrencySerializer,ClaimCostItemSerializer,ClaimInformationSerializer, ClaimInformationFileSerializer, FileTransferHistorySerializer, EmployeeListSerializer
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from core.utils import permission_required_or_superuser_with_token, group_required_multiple
from rest_framework.pagination import PageNumberPagination
from accounts.models import CustomUser
from b2bproduct.models import Product
from decimal import Decimal
from b2bmanagement.models import OrganizationPolicy,Designation,Department,Plan
from claim.serializers import EmployeeInformationSerializer
from .services.workflow import process_claim_action
from core.utils import send_dynamic_email
# Create your views here.

class BasicPagination(PageNumberPagination):
    page_size_query_param = 10

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class SuggestBeneficiaryView(APIView):
    authentication_classes = [TokenAuthentication]  # Require token
    permission_classes = [IsAuthenticated]          # Only authenticated users

    def get(self, request):
        employee = EmployeeInformation.objects.filter(user=request.user).first()

        # Superuser gets all
        if request.user.is_superuser:
            beneficiaries = EmployeeInformation.objects.all().order_by('id')
        else:
            if employee:
                member_id = employee.member_id
                new_member_id = member_id[:-1]  # remove last character
                beneficiaries = EmployeeInformation.objects.filter(
                    member_id__startswith=new_member_id
                ).order_by('id')
            else:
                beneficiaries = []

        results = [
            {
                'id': p.id,
                'member_id': p.member_id,
                'member_name': p.member_name,
                'relation': p.relation,
                'relation_name': f"{(p.relation.capitalize())}-{p.member_id.split('-')[-1]}" if p.relation else ''
            }
            for p in beneficiaries
        ]

        return Response({"success": True, "data": results})

def suggest_benificiary(request):
    employee = EmployeeInformation.objects.filter(user=request.user).first()
    if request.user.is_superuser:
        benificiaries = EmployeeInformation.objects.all().order_by('id')
    else:
        if employee:
            member_id = employee.member_id
            new_member_id = member_id[:-1]  # removes the last character
            benificiaries = EmployeeInformation.objects.filter(
                member_id__startswith=new_member_id).order_by('id')
        else:
            benificiaries = []
    results = [{'id': p.id, 'member_id': p.member_id, 'member_name': p.member_name, "relation": p.relation,
                'relation_name': f"{(p.relation.capitalize())}-{p.member_id.split('-')[-1]}" if p.relation else ''} for p in benificiaries]
    return results

@group_required_multiple("B2B Employee","Super Admin")
def CreateClaim(request):
    banks = Bank.objects.all()
    products = Product.objects.all()
    claim_relations = suggest_benificiary(request)
    currencies=Currency.objects.all()
    districts=District.objects.filter(is_active=True)
    template_name = 'claim/create-claim.html'
    return render(request, template_name=template_name, context={"banks": banks, "products": products, "claim_relations": claim_relations,"currencies":currencies,"districts":districts})


@group_required_multiple('Insurer Audit Officer','Insurer Finance', 'Claim Supervisor','Organization HR', 'Shield Operation',"B2B Employee","Insurer Claim Officer")
def ClaimList(request):
    template_name = 'claim/claim-list.html'
    return render(request, template_name=template_name,context={'request': request})


@group_required_multiple('Insurer Audit Officer','Claim Supervisor', 'Organization HR', 'Shield Operation',"B2B Employee","Insurer Claim Officer")
def ReceiveClaimList(request):
    template_name = 'claim/receive-claim-list.html'
    return render(request, template_name=template_name,context={'request': request})


@group_required_multiple('Super Admin')
def EmployeeList(request,policy_id):
    template_name = 'claim/employee-list.html'
    return render(request, template_name=template_name,context={"policy_id":policy_id})


def EmployeesView(request):
    template_name = 'claim/employees.html'
    return render(request, template_name=template_name)

def ClaimView(request, pk):
    obj = get_object_or_404(
        ClaimInformation.objects.prefetch_related('claim_history'),
        pk=pk
    )
    serializer = ClaimInformationFileSerializer(obj,context={'request': request})
    # if request.headers.get('Content-Type') == 'application/json' or request.accepts('application/json'):
    #     return Response({
    #         "status": True,
    #         "message": "Company Plan fetched successfully",
    #         "data": serializer.data,
    #     }, status=status.HTTP_200_OK)
    context = {
        "claim_view": serializer.data,
    }
    template_name = 'claim/claim-view.html'
    return render(request, template_name, context)


def UpdateClaimView(request, pk):
    claim_relations = suggest_benificiary(request)
    products = Product.objects.all()
    banks = Bank.objects.all()
    template_name = 'claim/update_claim.html'
    return render(request, template_name=template_name, context={"banks": banks,"claim_relations":claim_relations,"products":products})


def claim_hr_receiver(request):
    employee = EmployeeInformation.objects.filter(user=request.user).first()
    # Filter By Organization Hr
    if employee:
        hr_employee = EmployeeInformation.objects.filter(
            contract_no=employee.contract_no, hr_type='y').first()
        if hr_employee:
            # Filter By Reciver Organization User
            hr_user = CustomUser.objects.filter(pk=hr_employee.user.id).first()
            return hr_user
        else:
            None
    return None


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser,JSONParser])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def create_claim_api(request):
    if request.method == "POST":
        # Save Document
        if request.content_type == 'application/json':
            import json
            data = json.loads(request.body)
        else:
            data = request.POST.copy()
        data['product'] = data.get('ClaimType')
        data['policy'] = data.get('BeneficiaryType')
        policy = Policy.objects.filter(id=data.get('BeneficiaryType')).first()
        exchange_rate = data.get('exchange_rate')
        print(exchange_rate)
        policy_name = ''
        if policy:
            policy_name = str(policy.name).strip()
        # NATURAL DEATH   
        if policy_name == 'Natural Death':
            data['hospital_or_clinic_name'] = data['hospital_or_clinic_name']
        serializer = ClaimInformationSerializer(data=data)
        if serializer.is_valid():
            group_instance= Group.objects.get(name__in=["Organization HR"])
            from_group= Group.objects.get(name__in=["B2B Employee"])
            hr_reciver = claim_hr_receiver(request)
            instance = serializer.save(current_group=group_instance,
                created_by=request.user, sender=request.user, current_holder=hr_reciver,file_status=8)
            saveClaimCost(request,policy_name,instance,exchange_rate)
            FileTransferHistory.objects.create(
                file=instance,
                to_group=group_instance,
                from_group=from_group,
                sender=request.user,
                receiver=hr_reciver,
                received_at=timezone.now(),
                remarks=""
            )
        documentType = {}
        documentFile = {}
        documents = request.data.get('documents', [])
        combined_data = []
        if  documents:
            MIME_EXT_MAP = {
            'application/pdf': 'pdf',
            'image/jpeg': 'jpg',
            'image/png': 'png',
            'image/webp': 'webp'
            }

            for doc in documents:
                base64_string = doc['file_base64']
                # Split header and data
                header, encoded = base64_string.split(';base64,')
                mime_type = header.replace('data:', '')
                # Get extension
                extension = MIME_EXT_MAP.get(mime_type, 'bin')
                # Decode file
                file_content = base64.b64decode(encoded)
                # Generate correct filename
                filename = f"{uuid.uuid4()}.{extension}"
                file = ContentFile(file_content, name=filename)
                combined_data.append({
                    'claim': instance,
                    'document_type': doc['document_type'],
                    'document': file
                }) 
        else:     
        # Collect Document Type Selection
            for key, value in request.POST.items():
                if key.startswith('documentType['):
                    idx = key.split('[')[1].split(']')[0]  # extract index number
                    documentType[int(idx)] = value

            # Collect images
            for key, file in request.FILES.items():
                if key.startswith('documentFile['):
                    idx = key.split('[')[1].split(']')[0]
                    documentFile[int(idx)] = file

            # Combine by index
                
                for idx in sorted(documentType.keys()):
                    combined_data.append({
                        'claim': instance,
                        'document_type': documentType.get(idx),
                        'document': documentFile.get(idx)
                    })
        filtered_document_list = [
            item for item in combined_data if item['document'] is not None]
        length = len(filtered_document_list)
        if length > 0:
            # create instances
            objs = [ClaimDocuments(**item) for item in filtered_document_list]
            ClaimDocuments.objects.bulk_create(objs)
    return Response({"success":True,"message": "Claim Created Suucessfully"})

def saveClaimCost(request,policy_name="",claim=any,exchange_rate="1"):
    items_to_create = []
    if not exchange_rate:
        exchange_rate=1
    else:
        exchange_rate=Decimal(exchange_rate)
    if policy_name == 'Health - IPD' or policy_name == 'Health - Daycare' or policy_name == 'Health - OPD-Optical' or policy_name =='Health - OPD-Dental' or policy_name =='Accidental Death':
        room_rent = request.data.get('room_rent')
        surgery = request.data.get('surgery')
        icu_or_ccu_or_nsu = request.data.get('icu_or_ccu_or_nsu')
        consultation_fee = request.data.get('consultation_fee')
        investigation_fee = request.data.get('investigation_fee')     
        ancillary = request.data.get('ancillary')
        medical_investigation = request.data.get('medical_investigation')
        medicine = request.data.get('medicine')
        others = request.data.get('others')
        funeral_expenses = request.data.get('funeral_expenses')
        outstanding_medical_bills = request.data.get('outstanding_medical_bills')
        is_other_description = request.data.get('is_other_description', False)
    
 
        if policy_name == 'Accidental Death':
            others = request.data.get('others')
            items_to_create.append({'claim': claim.id, 'key': 'others', 'currency_amount': others,'claimed_amount': Decimal(others)*exchange_rate})
        if funeral_expenses:
            items_to_create.append({'claim': claim.id, 'key': 'funeral_expenses', 'currency_amount': funeral_expenses,'claimed_amount': Decimal(funeral_expenses)*exchange_rate})
        if outstanding_medical_bills:
            items_to_create.append({'claim': claim.id, 'key': 'outstanding_medical_bills', 'currency_amount': outstanding_medical_bills,'claimed_amount': Decimal(outstanding_medical_bills)*exchange_rate})
        if investigation_fee:
            items_to_create.append({'claim': claim.id, 'key': 'investigation_fee', 'currency_amount': investigation_fee,'claimed_amount': Decimal(investigation_fee)*exchange_rate})
        if icu_or_ccu_or_nsu:
            items_to_create.append({'claim': claim.id, 'key': 'icu_or_ccu_or_nsu', 'currency_amount': icu_or_ccu_or_nsu,'claimed_amount': Decimal(icu_or_ccu_or_nsu)*exchange_rate})
        if room_rent:
            items_to_create.append({'claim': claim.id, 'key': 'room_rent', 'currency_amount': room_rent,'claimed_amount': Decimal(room_rent)*exchange_rate})
        if consultation_fee:
            items_to_create.append({'claim': claim.id, 'key': 'consultation_fee', 'currency_amount': consultation_fee,'claimed_amount': Decimal(consultation_fee)*exchange_rate})
        if ancillary:
            items_to_create.append({'claim': claim.id, 'key': 'ancillary', 'currency_amount': ancillary,'claimed_amount': Decimal(ancillary)*exchange_rate})
        if medical_investigation:
            items_to_create.append({'claim': claim.id, 'key': 'medical_investigation', 'currency_amount': medical_investigation,'claimed_amount': Decimal(medical_investigation)*exchange_rate})
        if medicine:
            items_to_create.append({'claim': claim.id, 'key': 'medicine', 'currency_amount': medicine,'claimed_amount': Decimal(medicine)*exchange_rate})
        if surgery:
            items_to_create.append({'claim': claim.id, 'key': 'surgery', 'currency_amount': surgery,'claimed_amount': Decimal(surgery)*exchange_rate})
        if others and is_other_description:
            items_to_create.append({'claim': claim.id, 'key': 'others', 'currency_amount': others,'claimed_amount': Decimal(others)*exchange_rate})
    elif policy_name == 'Health - OPD' :
        consultation_fee = request.data.get('consultation_fee')
        investigation_fee = request.data.get('investigation_fee')
        medicine = request.data.get('medicine')
        emergency_treatment = request.data.get('emergency_treatment')
        physiotherapy_fee = request.data.get('physiotherapy_fee')
        others = request.data.get('others')
        is_other_description = request.data.get('is_other_description', False)
        if emergency_treatment:
            items_to_create.append({'claim': claim.id, 'key': 'emergency_treatment', 'currency_amount': emergency_treatment,'claimed_amount': Decimal(emergency_treatment)*exchange_rate})
        if investigation_fee:
            items_to_create.append({'claim': claim.id, 'key': 'investigation_fee', 'currency_amount': investigation_fee,'claimed_amount': Decimal(investigation_fee)*exchange_rate})
        if consultation_fee:
            items_to_create.append({'claim': claim.id, 'key': 'consultation_fee', 'currency_amount': consultation_fee,'claimed_amount': Decimal(consultation_fee)*exchange_rate})
        if physiotherapy_fee:
            items_to_create.append({'claim': claim.id, 'key': 'physiotherapy_fee', 'currency_amount': physiotherapy_fee,'claimed_amount': Decimal(physiotherapy_fee)*exchange_rate})
        if medicine:
            items_to_create.append({'claim': claim.id, 'key': 'medicine', 'currency_amount': medicine,'claimed_amount': Decimal(medicine)*exchange_rate})
        if others and is_other_description:
            items_to_create.append({'claim': claim.id, 'key': 'others', 'currency_amount': others,'claimed_amount': Decimal(others)*exchange_rate})
    elif policy_name == 'Health - Maternity' :
        package_cost = request.data.get("package_cost")
        items_to_create = []
        if package_cost and float(package_cost) > 0:
            items_to_create.append({'claim': claim.id, 'key': 'package_cost', 'currency_amount': package_cost,'claimed_amount': Decimal(package_cost)*exchange_rate})
        else:     
            room_rent = request.data.get('room_rent')
            icu_or_ccu_or_nsu = request.data.get('icu_or_ccu_or_nsu')
            consultation_fee = request.data.get('consultation_fee')
            ancillary = request.data.get('ancillary')
            medical_investigation = request.data.get('medical_investigation')
            medicine = request.data.get('medicine')
            others = request.data.get('others')
            is_other_description = request.data.get('is_other_description', False)
            if room_rent:
                items_to_create.append({'claim': claim.id, 'key': 'room_rent', 'currency_amount': room_rent,'claimed_amount': Decimal(room_rent)*exchange_rate})
            if icu_or_ccu_or_nsu:
                items_to_create.append({'claim': claim.id, 'key': 'icu_or_ccu_or_nsu', 'currency_amount': icu_or_ccu_or_nsu,'claimed_amount': Decimal(icu_or_ccu_or_nsu)*exchange_rate})
            if consultation_fee:
                items_to_create.append({'claim': claim.id, 'key': 'consultation_fee', 'currency_amount': consultation_fee,'claimed_amount': Decimal(consultation_fee)*exchange_rate})
            if ancillary:
                items_to_create.append({'claim': claim.id, 'key': 'ancillary', 'currency_amount': ancillary,'claimed_amount': Decimal(ancillary)*exchange_rate})
            if medicine:
                items_to_create.append({'claim': claim.id, 'key': 'medicine', 'currency_amount': medicine,'claimed_amount': Decimal(medicine)*exchange_rate})
            if medical_investigation:
                items_to_create.append({'claim': claim.id, 'key': 'medical_investigation', 'currency_amount': medical_investigation,'claimed_amount': Decimal(medical_investigation)*exchange_rate})
            if others and is_other_description:
                items_to_create.append({'claim': claim.id, 'key': 'others', 'currency_amount': others,'claimed_amount': Decimal(others)*exchange_rate})
    serializer = ClaimCostItemSerializer(data=items_to_create, many=True)
    if serializer.is_valid():
        serializer.save()
        return True
    return False
        

@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def update_claim_api(request):
    if request.method == "POST":
        # Save Document
        data = request.data
        claim = get_object_or_404(ClaimInformation, pk=data.get('id'))
        data._mutable = True
        data['product'] = data.get('ClaimType')
        data['policy'] = data.get('BeneficiaryType')
        # NATURAL DEATH
        policy = Policy.objects.filter(id=data.get('BeneficiaryType')).first()
        policy_name = ''
        if policy:
            policy_name = str(policy.name).strip()
        if policy_name == 'Natural Death':
            data['death_date'] = datetime.strptime(
                data['death_date'], "%d-%m-%Y").date()
            data['hospital_or_clinic_name'] = data['hospital_or_clinic_name']
        if policy_name == 'Permanent Total Disability' or policy_name == 'Partial Disability':
            data['incident_date'] = datetime.strptime(
                data['incident_date'], "%d-%m-%Y").date()
        if policy_name == 'Health - IPD' or policy_name == 'Health - Maternity' or policy_name == 'Health - Daycare' or policy_name == 'Critical Illness':
            data['date_of_admission'] = datetime.strptime(
                data['date_of_admission'], "%d-%m-%Y").date()
            data['date_of_discharge'] = datetime.strptime(
                data['date_of_discharge'], "%d-%m-%Y").date()
        if policy_name == 'Health - OPD' or policy_name == 'Health - OPD-Optical' or policy_name == 'Health - OPD-Dental':
            data['date_of_treatment'] = datetime.strptime(
                data['date_of_treatment'], "%d-%m-%Y").date()
        serializer = ClaimInformationSerializer(instance=claim, data=data)
        if serializer.is_valid():
            group_instance = Group.objects.get(name="HR Admin")
            hr_reciver = claim_hr_receiver(request)
            instance = serializer.save(
                created_by=request.user, sender=request.user, current_holder=hr_reciver)
            if data.get('edit-page') is  None:
                second_last = FileTransferHistory.objects.all().order_by('-send_at')[1]
                first = FileTransferHistory.objects.all().order_by('-send_at').first()
                if second_last.status in [0,6,7]:
                    if first.group.name=="HR Admin" :
                        group_instance = Group.objects.get(name="Super Admin")
                    elif file.group.name=="B2B Employee":
                        group_instance = Group.objects.get(name="HR Admin")
                    FileTransferHistory.objects.create(
                        file=instance,
                        group=group_instance,
                        sender=first.receiver,
                        receiver=first.sender
                    )
        documentType = {}
        documentFile = {}
        # Collect Document Type Selection
        for key, value in request.POST.items():
            if key.startswith('documentType['):
                idx = key.split('[')[1].split(']')[0]  # extract index number
                documentType[int(idx)] = value

        # Collect images
        for key, file in request.FILES.items():
            if key.startswith('documentFile['):
                idx = key.split('[')[1].split(']')[0]
                documentFile[int(idx)] = file

        # Combine by index
        combined_data = []

        for idx in sorted(documentType.keys()):
            combined_data.append({
                'claim': instance,
                'document_type': documentType.get(idx),
                'document': documentFile.get(idx)
            })
        filtered_document_list = [
            item for item in combined_data if item['document'] is not None]
        length = len(filtered_document_list)
        if length > 0:
            # create instances
            objs = [ClaimDocuments(**item) for item in filtered_document_list]
            ClaimDocuments.objects.bulk_create(objs)
    return Response({"status": "success"})


@api_view(["POST"])
def update_claim_status(request):
    if request.method == "POST":
        # Save Document
        print(request.data)
        data = request.data
        data._mutable = True
        id = data.get('id')
        status=int(data.get('status'))
        claim = ClaimInformation.objects.get(id=id)
        actor = request.user
        action = request.data.get('action')
        remarks = request.data.get('remarks', '')
        settled_amount = request.data.get('settled_amount',0)
        cost_items_raw = request.POST.get("cost_items",None)
    try:
        receiver_user =CustomUser.objects.get(pk=request.user.id)
        if claim.file_status== 7 :
            receiver_user = claim_hr_receiver(request)
            documentType = {}
            documentFile = {}
            # Collect Document Type Selection
            for key, value in request.POST.items():
                if key.startswith('documentType['):
                    idx = key.split('[')[1].split(']')[0]  # extract index number
                    documentType[int(idx)] = value

            # Collect images
            for key, file in request.FILES.items():
                if key.startswith('documentFile['):
                    idx = key.split('[')[1].split(']')[0]
                    documentFile[int(idx)] = file

            # Combine by index
            combined_data = []

            for idx in sorted(documentType.keys()):
                combined_data.append({
                    'claim': claim,
                    'document_type': documentType.get(idx),
                    'document': documentFile.get(idx)
                })
            filtered_document_list = [
                item for item in combined_data if item['document'] is not None]
            length = len(filtered_document_list)
            if length > 0:
                # create instances
                objs = [ClaimDocuments(**item) for item in filtered_document_list]
                ClaimDocuments.objects.bulk_create(objs)
        process_claim_action(claim, status,actor, remarks, settled_amount,receiver_user,cost_items_raw)
        return Response({"success": True, "message": f"Action '{action}' processed successfully"})
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=400)
        # claim = ClaimInformation.objects.filter(id=id).first()
        # claim_data = {
        #     "file_status": 4,
        #     "sender": request.user,
        #     'current_holder': request.user
        # }
        # if  status in [0, 1, 7]:  
        #     claim_data["sender"] = claim.current_holder  
        #     claim_data["current_holder"] = claim.sender  
        # claim = ClaimInformation.objects.filter(id=id).update(**claim_data)
        # if claim:
        #     file = FileTransferHistory.objects.filter(
        #         file_id=id).order_by('-id').first()
        #     if file:
        #         print("file.group.name",id )
        #         # Update fields
        #         groupname = file.group.name if file and file.group else None
        #         file.status = data.get('status')
        #         file.remarks = data.get('remarks')
        #         file.received_at = datetime.now()
        #         file.save()   
        #         if  status in [1,2]:    
        #             group_instance = None  
        #             if groupname.upper()=="":      
        #                 group_instance, _ = Group.objects.get_or_create(name="Waada")
        #             elif groupname.upper()=="Waada": 
        #                 group_instance, _ = Group.objects.get_or_create(name="Insurer Claim Officer")
        #             elif groupname.upper()=="Insurer Claim Officer": 
        #                 group_instance, _= Group.objects.get_or_create(name="Insurer Audit Officer")     
                    
        #             FileTransferHistory.objects.create(
        #                 file_id=id,
        #                 group=group_instance,
        #                 status=4,
        #                 sender=request.user,
        #                 receiver=superadmin
        #             )
        #             return Response({"status": True, 'message': 'claim status  updated'})
        #         else:
        #             if groupname.upper()=="ORGANIZATION HR": 
        #                 group_instance, created = Group.objects.get_or_create(name="B2B Employee")
        #             elif groupname.upper()=="Waada":
        #                 group_instance, created = Group.objects.get_or_create(name="ORGANIZATION HR")
        #             FileTransferHistory.objects.create(
        #                 file_id=id,
        #                 group=group_instance,
        #                 status=4,
        #                 sender=file.receiver,
        #                 receiver=file.sender
        #             )
        #         return Response({"status": True, 'message': 'claim status  updated'})
        #     return Response({"status": True, 'message': 'claim status  updated'})
        # return Response({"status": False, 'message': 'claim status not updated'})


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
def accept_claim(request):
    if request.method == "POST":
        # Save Document
       
        data = request.data
        data=request.data.copy()
        id = data.get('id')
        
        status=int(data.get('status'))
        claim = ClaimInformation.objects.get(id=id)
        actor = request.user
        action = request.data.get('action')
        remarks = request.data.get('remarks', '')
        settled_amount = request.data.get('settled_amount',0)
        cost_items_raw = request.POST.get("cost_items",None)
    try:
        receiver_user =CustomUser.objects.get(pk=request.user.id)
        if claim.file_status== 7 :
            receiver_user = claim_hr_receiver(request)
            documentType = {}
            documentFile = {}
            # Collect Document Type Selection
            for key, value in request.POST.items():
                if key.startswith('documentType['):
                    idx = key.split('[')[1].split(']')[0]  # extract index number
                    documentType[int(idx)] = value

            # Collect images
            for key, file in request.FILES.items():
                if key.startswith('documentFile['):
                    idx = key.split('[')[1].split(']')[0]
                    documentFile[int(idx)] = file

            # Combine by index
            combined_data = []

            for idx in sorted(documentType.keys()):
                combined_data.append({
                    'claim': claim,
                    'document_type': documentType.get(idx),
                    'document': documentFile.get(idx)
                })
            filtered_document_list = [
                item for item in combined_data if item['document'] is not None]
            length = len(filtered_document_list)
            if length > 0:
                # create instances
                objs = [ClaimDocuments(**item) for item in filtered_document_list]
                ClaimDocuments.objects.bulk_create(objs)
        process_claim_action(claim, status,actor, remarks, settled_amount,receiver_user,cost_items_raw)
        return Response({"success": True, "message": f"Claim received successfully"})
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=400)
        # claim = ClaimInformation.objects.filter(id=id).first()
        # claim_data = {
        #     "file_status": 4,
        #     "sender": request.user,
        #     'current_holder': request.user
        # }
        # if  status in [0, 1, 7]:  
        #     claim_data["sender"] = claim.current_holder  
        #     claim_data["current_holder"] = claim.sender  
        # claim = ClaimInformation.objects.filter(id=id).update(**claim_data)
        # if claim:
        #     file = FileTransferHistory.objects.filter(
        #         file_id=id).order_by('-id').first()
        #     if file:
        #         print("file.group.name",id )
        #         # Update fields
        #         groupname = file.group.name if file and file.group else None
        #         file.status = data.get('status')
        #         file.remarks = data.get('remarks')
        #         file.received_at = datetime.now()
        #         file.save()   
        #         if  status in [1,2]:    
        #             group_instance = None  
        #             if groupname.upper()=="":      
        #                 group_instance, _ = Group.objects.get_or_create(name="Waada")
        #             elif groupname.upper()=="Waada": 
        #                 group_instance, _ = Group.objects.get_or_create(name="Insurer Claim Officer")
        #             elif groupname.upper()=="Insurer Claim Officer": 
        #                 group_instance, _= Group.objects.get_or_create(name="Insurer Audit Officer")     
                    
        #             FileTransferHistory.objects.create(
        #                 file_id=id,
        #                 group=group_instance,
        #                 status=4,
        #                 sender=request.user,
        #                 receiver=superadmin
        #             )
        #             return Response({"status": True, 'message': 'claim status  updated'})
        #         else:
        #             if groupname.upper()=="ORGANIZATION HR": 
        #                 group_instance, created = Group.objects.get_or_create(name="B2B Employee")
        #             elif groupname.upper()=="Waada":
        #                 group_instance, created = Group.objects.get_or_create(name="ORGANIZATION HR")
        #             FileTransferHistory.objects.create(
        #                 file_id=id,
        #                 group=group_instance,
        #                 status=4,
        #                 sender=file.receiver,
        #                 receiver=file.sender
        #             )
        #         return Response({"status": True, 'message': 'claim status  updated'})
        #     return Response({"status": True, 'message': 'claim status  updated'})
        # return Response({"status": False, 'message': 'claim status not updated'})


# Claim FIle Delete
@api_view(["POST"])
def delete_claim_document(request):
    if request.method == "POST":
        doc_id = request.POST.get('doc_id')
        try:
            doc = ClaimDocuments.objects.get(id=doc_id)
            doc.document.delete(save=False)  # physically delete the file
            doc.delete()  # delete db row
            return JsonResponse({'status': 'ok'})
        except ClaimDocuments.DoesNotExist:
            return JsonResponse({'status': 'not_found'})
    return JsonResponse({'status': 'error'})


class FileTransferWithHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        # Grabing data with Search value

        queryset = ClaimInformation.objects.prefetch_related(
            'claim_history').all()
        if request.user.is_superuser:
            queryset = queryset
        else:
            # Normal user sees only own created data
            queryset.filter(
                Q(created_by=request.user) 
                |
                Q(claim_history__sender=request.user
                  )
            ).distinct()
        total_count = queryset.count()
        status = request.GET.get('status')
        if status:
            queryset = queryset.filter(file_status=status)
        if search_value:
            queryset = queryset.filter(
                Q(bank__name__icontains=search_value) | Q(
                    employee__employee_id__icontains=search_value)
                | Q(employee__member_id__icontains=search_value)
            )
        filtered_records = queryset.count()
        claims = queryset[start:start+length]
        serializer = ClaimInformationFileSerializer(claims, many=True)
        data = serializer.data
        for item in data:
            item['is_super_user'] = request.user.is_superuser
        return Response({
            "draw": draw,
            "recordsTotal": total_count,
            "recordsFiltered": filtered_records,
            "data": data
        })


class FileReceiveWithHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = ClaimInformation.objects.prefetch_related(
            'claim_history').all()
        user = request.user
        if user.is_superuser:
            pass  # superuser sees all
        else:
            user_groups = user.groups.values_list('name', flat=True)
            # Normal user sees only own created data
           
            if "Organization HR" in user_groups:
                queryset = queryset.filter(current_group__name="Organization HR")

            elif "Shield Operation" in user_groups:
                queryset = queryset.filter(current_group__name="Shield Operation")
            
            elif "Claim Supervisor" in user_groups:
                queryset = queryset.filter(current_group__name="Claim Supervisor")
            
            elif "Insurer Audit Officer" in user_groups:
                queryset = queryset.filter(current_group__name="Insurer Audit Officer")

            elif "Insurer Claim Officer" in user_groups:
                queryset = queryset.filter(current_group__name="Insurer Claim Officer")
            
            elif "B2B Employee" in user_groups:
                queryset = queryset.filter(current_group__name="B2B Employee") 
               
            else:
                # fallback → user sees only what they hold
                queryset = queryset.filter(current_holder=user)
        total_count = queryset.count()
        serializer = ClaimInformationFileSerializer(queryset, many=True)
        data = serializer.data
        for item in data:
            # item['is_super_user'] = request.user.is_superuser or  request.user.groups.filter(name__in=["ORGANIZATION HR","Insurer Claim Officer", "Waada","Insurer Audit Officer"]).exists()
            item['is_super_user'] =  request.user.is_superuser
        return Response({
            "draw": 0,
            "recordsTotal": total_count,
            "recordsFiltered": 0,
            "data": data
        })


class EmployeeListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,policy_id):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        status = request.GET.get('status')
        queryset = EmployeeInformation.objects.all()
        org_policy= OrganizationPolicy.objects.get(id=policy_id)
        if org_policy:
            queryset = queryset.filter(organization_emp_policy_id=policy_id,contract_no=org_policy.organization_contract_no)
            total_count = queryset.count()
            if start_date:
                queryset = queryset.filter(
                    membership_date__gte=datetime.strptime(start_date, '%Y-%m-%d'))
            if end_date:
                queryset = queryset.filter(
                    membership_date__lte=datetime.strptime(end_date, '%Y-%m-%d'))
            if status:
                queryset = queryset.filter(status=status)
            if search_value:
                queryset = queryset.filter(
                    Q(member_id__icontains=search_value) |
                    Q(mobile_number__icontains=search_value) |
                    Q(employee_email__icontains=search_value) |
                    Q(hr_type__icontains=search_value)
                 
                )
            # Count after filtering
            filtered_count = queryset.count()
            # Pagination
            queryset = queryset[start:start+length]
            serializer = EmployeeListSerializer(queryset, many=True)
        return Response({
            "draw": draw,
            "recordsTotal": total_count,
            "recordsFiltered": filtered_count,
            "data": serializer.data
        })
    
    def post(self,request):
        data=request.POST.copy()   
        group_name = "B2B Employee"  # or get from request.POST
        hr_group_name = "HR Admin"  # or get from request.POST
        group, created = Group.objects.get_or_create(name=group_name)
        hr_group, created = Group.objects.get_or_create(name=hr_group_name)
        org_id =data.get('organization')
        org_contract_id=data.get('org_contract_id')
        employee_id=data.get('employee_id')
        if data.get('dob'):
            data['dob'] = datetime.strptime(
                    data.get('dob'), "%d-%m-%Y").date()
        else:
            data['dob'] =None
        
        if data.get('membership_date'):
            data['membership_date'] = datetime.strptime(
                    data.get('membership_date'), "%d-%m-%Y").date()
        else:
            data['membership_date'] =None
        employee = EmployeeInformation.objects.filter(employee_id=employee_id).first()
        if employee:
            return Response({"success": False, 'message': 'Employee ID is already Exists'})
          
        org_policy = OrganizationPolicy.objects.filter(organization__id=org_id,organization_contract_no=org_contract_id).first()
        if org_policy:
            org_id=org_policy.id        
        else:
            org_policy = OrganizationPolicy.objects.create(organization_id=org_id,organization_contract_no=org_contract_id)
            org_id=org_policy.id
        data['organization_emp_policy']=org_policy.id
        data['designation']=data.get('emp_designation')
        data['contract_no']=org_contract_id
        data['department']=data.get('emp_department')
        data['mobile_number']=data.get('emp_mobile_no')
        data['employee_email']=data.get('emp_email')
        data['bank']=data.get('emp_bank')
        data['account_name']=data.get('emp_account_name')
        data['branch_name']=data.get('emp_branch_name')
        data['branch_code']=data.get('emp_branch_code')
        data['routing_number']=data.get('emp_routing_number')
        data['account_number']=data.get('emp_account_number')
        data['plan']=data.get('emp_plan')
        hr_admin=data.get('hr_type')
        if str(hr_admin).strip() in ['Yes','y','YES']:
            groups=[group,hr_group]    
        else:
            groups=[group]    
        serializer=EmployeeInformationSerializer(data=data)
        if serializer.is_valid():
            user_obj=CustomUser.objects.filter(email=data.get('emp_email')).first()
            if not user_obj:
                user_obj=CustomUser(
                    username=data.get('member_name'),
                    email=data.get('emp_email'),
                    system_generate='Y',
                    password=make_password('123456'),  # hash password
                    is_staff=True,
                    is_active=True,
                    is_status=True,
                )
                user_obj.save()
                user_obj.groups.set(groups)
            serializer.save(user_id=user_obj.id, created_by=request.user)
            return Response({"success": True, 'message': 'Employee data inserted successfully'})
        return Response({"success": False, 'message': "Employee data failed to save"})

class AllEmployeeList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        status = request.GET.get('status')
        queryset = EmployeeInformation.objects.all()
        total_count = queryset.count()
        if start_date:
            queryset = queryset.filter(
                membership_date__gte=datetime.strptime(start_date, '%Y-%m-%d'))
        if end_date:
            queryset = queryset.filter(
                membership_date__lte=datetime.strptime(end_date, '%Y-%m-%d'))
        if status:
            queryset = queryset.filter(status=status)
        if search_value:
            queryset = queryset.filter(
                Q(member_id__icontains=search_value) |
                Q(mobile_number__icontains=search_value) |
                Q(employee_email__icontains=search_value) |
                Q(hr_type__icontains=search_value)
                
            )
        # Count after filtering
        filtered_count = queryset.count()
        # Pagination
        queryset = queryset[start:start+length]
        serializer = EmployeeListSerializer(queryset, many=True)
        return Response({
            "draw": draw,
            "recordsTotal": total_count,
            "recordsFiltered": filtered_count,
            "data": serializer.data
        })
    
class ClaimDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [TokenAuthentication]  # Require token
    def get(self, request, pk):
        # Retrieve object or return 404 if not found
        obj = get_object_or_404(
            ClaimInformation.objects.prefetch_related('claim_history'),
            pk=pk
        )
        data = None
        serializer = ClaimInformationFileSerializer(obj)
        data=serializer.data
        # if request.headers.get('Content-Type') == 'application/json' or request.accepts('application/json'):
        #     return Response({
        #         "status": True,
        #         "message": "Company Plan fetched successfully",
        #         "data": serializer.data,
        #     }, status=status.HTTP_200_OK)
        context = {
            "claim_view": data,
        }
        template_name = 'claim/claim-view.html'
        return render(request, template_name, context)

class ClaimDetailsListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]  # Require token
    def get(self, request, pk):
        # Retrieve object or return 404 if not found
        obj = get_object_or_404(
            ClaimInformation.objects.prefetch_related('claim_history'),
            pk=pk
        )
        data = None
        serializer = ClaimInformationListSerializer(obj)
        return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)

class ClaimListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]  # Require token
    def get(self, request):
        search = request.GET.get("search")
        # Retrieve object or return 404 if not found
        
        
        
        queryset = ClaimInformation.objects.prefetch_related(
            'claim_history').all()
        queryset.filter(
                Q(created_by=request.user) |
                Q(claim_history__sender=request.user)
            ).distinct()
        
        if search:
            queryset = queryset.filter(
                Q(file_status__icontains=search) |
                Q(claim_for__icontains=search) |
                Q(beneficiary_name__icontains=search)
            )

        
        paginator = StandardResultsSetPagination()
        paginated_qs = paginator.paginate_queryset(queryset, request)
        serializer = ClaimInformationListSerializer(paginated_qs, many=True)
        return paginator.get_paginated_response({
            "success": True,
            "data": serializer.data
        })



class EmployeeDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk):
        # Retrieve object or return 404 if not found
        obj =EmployeeInformation.objects.get(id=pk) 
        data = None
        serializer = EmployeeInformationSerializer(obj)
        designations=Designation.objects.all()
        departments=Department.objects.filter(status=1)
        plans=Plan.objects.all()
        banks=Bank.objects.all()
        insurers=Insurer.objects.filter(status=1)
        data=serializer.data
        # if request.headers.get('Content-Type') == 'application/json' or request.accepts('application/json'):
        #     return Response({
        #         "status": True,
        #         "message": "Company Plan fetched successfully",
        #         "data": serializer.data,
        #     }, status=status.HTTP_200_OK)
        
        context = {
            "insurers":insurers,
            "employee": data,
            "plans":plans,
            "banks":banks,
            "designations":designations,
            "departments":departments
        }
        template_name = 'claim/update-employee.html'
        return render(request, template_name, context)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def claim_action(request, claim_id):
    claim = ClaimInformation.objects.get(id=claim_id)
    actor = request.data.get('actor')
    action = request.data.get('action')
    remarks = request.data.get('remarks', '')
    settled_amount = request.data.get('settled_amount')

    try:
        process_claim_action(claim, actor, action, remarks, settled_amount,request)
        return Response({"success": True, "message": f"Action '{action}' processed successfully"})
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=400)


@csrf_exempt
@login_required
def update_claim_item(request):
    if request.method == "POST":
        item_id = request.POST.get("id")
        field = request.POST.get("field")
        value = request.POST.get("value")
        try:
            item = ClaimCostItem.objects.get(id=item_id)
            # Limit editing by group
            group_name = request.user.groups.first().name.upper() if request.user.groups.exists() else ""
            allowed_fields = []
            if group_name == "Insurer Claim Officer":
                allowed_fields = ["claims_operation_settled", "claims_operation_deduction", "remarks_claims_operation"]
            elif group_name == "Insurer Audit Officer":
                allowed_fields = ["audit_settled", "audit_deduction", "remarks_audit"]

            if field in allowed_fields:
                setattr(item, field, value)
                item.save()
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "error": "Not allowed"})
        except ClaimCostItem.DoesNotExist:
            return JsonResponse({"success": False, "error": "Not found"})


def test_send_email(request):
    group = Group.objects.get(name="Insurer Claim Officer")
    user = CustomUser.objects.get(username="zia_uddin")

    # Context placeholders in the message body
    context = {
        "username": user.username,
        "group_name": group.name,
        "support_email": "support@example.com",
    }

    send_dynamic_email(
        to_email="ziauddinsc2016@gmail.com",
        template_type="group",
        group=group,
        context=context
    )

def currencyeView(request):
    template_name = 'claim/currency-list.html'
    return render(request, template_name=template_name)

def getCurrencyList(request):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        queryset=Currency.objects.all().order_by('-id')      
        # Grabing data with Search value        
        if search_value:
            queryset =  queryset.filter(
                Q(name__icontains=search_value) |
                Q(code__icontains=search_value) 
            )
        # counting All records           
        total_records = Currency.objects.count()
        #Count Filetred Data
        filtered_records = queryset.count()
        # Range query data
        banks=queryset[start:start+length]
        #Paginate Query data
        # Serilization by Data        
        serializer = CurrencySerializer(banks, many=True)
        # Response Data
        return JsonResponse({
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': serializer.data
        })

class CurrencyListView(APIView,PageNumberPagination):
    queryset = Currency.objects.all()
    authentication_classes = [TokenAuthentication]  # Require token
    pagination_class = BasicPagination
    serializer_class = CurrencySerializer
    def get(self, request):
        try:
            currencies = Currency.objects.all() #Sertalize single item
            serializer = CurrencySerializer(currencies,many=True)
            return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)

        except Currency.DoesNotExist:
            return Response({"success":False,"error": "Item not found"},status=status.HTTP_404_NOT_FOUND)
    

class CurrencyView(APIView,PageNumberPagination):
    queryset = Currency.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = BasicPagination
    serializer_class = CurrencySerializer
    def get(self, request):
        try:
            currencies = Currency.objects.all() #Sertalize single item
            serializer = CurrencySerializer(currencies,many=True)
            return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)

        except Currency.DoesNotExist:
            return Response({"success":False,"error": "Item not found"},status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        # Request Data
        serializer = CurrencySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({'success':True,"message":'Currency has been saved',"data":serializer.data})
        else:           
            return Response({'success':False,"message":'Currency has not been saved',"data":serializer.errors})

    def put(self, request, pk):
        try:
          currency = Currency.objects.get(id=pk) 
        except Currency.DeesNotExist:
            return Response({"error": "Currency not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CurrencySerializer(currency, data=request.data) 
        if serializer.is_valid():
            currency = serializer.save(updated_by=request.user)
            return Response({
                "message": "Currency information has been updated",
                "success":True,
                "data":serializer.data
                })  
        return Response({
            "message": "Currency didn't update",
            "success":False,
            "data":serializer.errors
            })


    def delete(self, request, pk):
        try:
          #Retrieve Iten by ID
          currency = Currency.objects.get(id=pk)

        except Currency.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        #Delete the organization from the database 
        currency.delete()
        #Return a 284 response
        return Response({"error": False,"message":'Currency has been deleted'})
    
class CurrencySigleList(APIView):
    def get(self, request,item_id):
        try:
            #Query a single tee by ID
            currency = Currency.objects.get(id=item_id) #Sertalize single item
            serializer = CurrencySerializer(currency)
            return Response({"success":True,"data":serializer.data}, status=status.HTTP_200_OK)
        except Currency.DoesNotExist:
                return Response({"success":False,"error": "Item not found"},status=status.HTTP_404_NOT_FOUND)



class EmployeeCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        obj = EmployeeInformation.objects.get(id=pk)
        serializer = EmployeeInformationSerializer(obj)

        context = {
            "employee": serializer.data,
            "plans": Plan.objects.all(),
            "designations": Designation.objects.all(),
            "departments": Department.objects.filter(status=1)
        }
        return render(request, "claim/update-employee.html", context)

    def post(self, request, pk):
        print(request.data)
        obj = EmployeeInformation.objects.get(id=pk)
        serializer = EmployeeInformationSerializer(
            obj,
            data=request.data,     # <-- jQuery send goes here
            partial=True           # <-- allow partial update
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Employee updated successfully",
                "data": serializer.data
            })
        return Response({
            "status": False,
            "errors": serializer.errors
        }, status=400)



class CompnayDetailProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        # Retrieve object or return 404 if not found
        employee = EmployeeInformation.objects.select_related(
                    'organization_emp_policy__organization'
            ).filter(user=request.user).first()
        if employee:
            serializer = EmployeeInformationOrgSerializer(employee, context={'request': request, 'employee': employee})
            context = {
                "company_profile": serializer.data,
            }
            template_name = 'claim/my-family.html'
            return render(request, template_name, context)
        else:
            template_name = 'claim/my-family.html'
            return render(request, template_name)

