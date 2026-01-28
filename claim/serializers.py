from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import ClaimInformation,ClaimDocuments,FileTransferHistory,EmployeeInformation,ClaimCostItem,Currency
from accounts.models import CustomUser
from b2bmanagement.serializers import DesignationSerializer,DepartmentSerializer, DistrictSerializer,BankSerializer,OrgnaizationListSerializer,OrganizationPolicySerializer
from django.utils import timezone
from b2bproduct.serializers import ProductSerializer,PolicySerializer
from decimal import Decimal, ROUND_HALF_UP

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class ClaimInformationSerializer(serializers.ModelSerializer):
    fir_date =  date_of_admission = serializers.DateField(
        required=False,
        allow_null=True,
        input_formats=['%d-%m-%Y'],   # Accept DD-MM-YYYY
        format='%d-%m-%Y'             # Return DD-MM-YYYY
    )
    incident_date = serializers.DateField(
        required=False,
        allow_null=True,
        input_formats=['%d-%m-%Y'],   # Accept DD-MM-YYYY
        format='%d-%m-%Y'             # Return DD-MM-YYYY
    )
    date_of_admission = serializers.DateField(
        required=False,
        allow_null=True,
        input_formats=['%d-%m-%Y'],   # Accept DD-MM-YYYY
        format='%d-%m-%Y'             # Return DD-MM-YYYY
    )
    date_of_discharge = serializers.DateField(
        required=False,
        allow_null=True,
        input_formats=['%d-%m-%Y'],   # Accept DD-MM-YYYY
        format='%d-%m-%Y'             # Return DD-MM-YYYY
    )
    death_of_departure = serializers.DateField(
        required=False,
        allow_null=True,
        input_formats=['%d-%m-%Y'],   # Accept DD-MM-YYYY
        format='%d-%m-%Y'             # Return DD-MM-YYYY
    )
    
    date_of_treatment = serializers.DateField(
        required=False,
        allow_null=True,
        input_formats=['%d-%m-%Y'],   # Accept DD-MM-YYYY
        format='%d-%m-%Y'             # Return DD-MM-YYYY
    )
    class Meta:
        model = ClaimInformation
        fields = '__all__'
        
class ClaimDocumentsSerializer(serializers.ModelSerializer):
    document_type_display = serializers.CharField(source='get_document_type_display', read_only=True)
    
    class Meta:
        model = ClaimDocuments
        fields = ['id', 'document_type', 'document','document_type_display']
  
class ClaimCostItemSerializer(serializers.ModelSerializer):
    claimed_amount_bdt = serializers.SerializerMethodField()
    settled_bdt = serializers.SerializerMethodField()
    deduction_bdt = serializers.SerializerMethodField()
    
    class Meta:
        model = ClaimCostItem
        fields = '__all__'
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email','phone_number',"groups"]

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class EmployeeInformationSerializer(serializers.ModelSerializer):
    dob = serializers.DateField(
        required=False,
        allow_null=True,
        input_formats=['%d-%m-%Y'],   # Accept DD-MM-YYYY
        format='%d-%m-%Y'             # Return DD-MM-YYYY
    )
    membership_date = serializers.DateField(
        required=False,
        allow_null=True,
        input_formats=['%d-%m-%Y'],   # Accept DD-MM-YYYY
        format='%d-%m-%Y'             # Return DD-MM-YYYY
    )
    
    class Meta:
        model = EmployeeInformation
        fields = '__all__'
    


class FileTransferHistorySerializer(serializers.ModelSerializer):
    # elapsed_time = serializers.SerializerMethodField()
    time_spent = serializers.SerializerMethodField()
    to_group=GroupSerializer()
    from_group=GroupSerializer()
    sender=UserSerializer()
    receiver=UserSerializer()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    status_before_display = serializers.CharField(source='get_status_before_display', read_only=True)
    status_after_display = serializers.CharField(source='get_status_after_display', read_only=True)
    received_at = serializers.DateTimeField(format="%d-%m-%Y", read_only=True)
    class Meta:
        model = FileTransferHistory
        fields = '__all__'   
    
    def get_time_spent(self,obj):
        request = self.context.get("request")
        if request and request.user.is_superuser:
            if not obj.received_at:
                return "Not received yet"
            diff = obj.received_at - obj.sent_at
            days = diff.days
            seconds = diff.seconds

            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            sec = seconds % 60

            parts = []
            if days > 0:
                parts.append(f"{days} days")
            if hours > 0:
                parts.append(f"{hours} hours")
            if minutes > 0:
                parts.append(f"{minutes} minutes")
            if sec > 0:
                parts.append(f"{sec} seconds")

            return ", ".join(parts) if parts else "0 seconds"
        return None   # hide for normal users

    
    # def get_elapsed_time(self, obj):
    #     now = timezone.now()
    #     diff = now - obj.sent_at
    #     seconds = diff.total_seconds()

    #     if seconds < 60:
    #         return f"{int(seconds)} seconds "
    #     elif seconds < 3600:
    #         return f"{int(seconds // 60)} minutes "
    #     elif seconds < 86400:
    #         return f"{int(seconds // 3600)} hours "
    #     elif seconds < 31536000:
    #         return f"{int(seconds // 86400)} days "
    #     else:
    #         return f"{int(seconds // 31536000)} years "

class ClaimCostItemSerializer(serializers.ModelSerializer):
    currency_code = serializers.SerializerMethodField()
    exchange_rate = serializers.SerializerMethodField()
    claimed_amount_bdt = serializers.SerializerMethodField()
    settled_bdt = serializers.SerializerMethodField()
    deduction_bdt = serializers.SerializerMethodField()
    
    class Meta:
        model = ClaimCostItem
        fields = '__all__'
    
    def get_currency_code(self, obj):
        return obj.claim.currency.code if obj.claim and obj.claim.currency else None

    def get_exchange_rate(self, obj):
        return obj.claim.exchange_rate if obj.claim and obj.claim.currency else None
    
    def _to_2_decimal(self, value):
        """Helper to round Decimal values to 2 digits"""
        if value is None:
            return Decimal('0.00')
        return value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    # --- calculated fields ---
    def get_claimed_amount_bdt(self, obj):
        if obj.claim and obj.claim.currency:
            rate = obj.claim.exchange_rate
            return  self._to_2_decimal(obj.claimed_amount * rate)
        return  self._to_2_decimal(obj.claimed_amount)

    def get_settled_bdt(self, obj):
        if obj.claim and obj.claim.currency and obj.claims_operation_settled:
            rate = obj.claim.exchange_rate
            return obj.claims_operation_settled * rate
        return obj.claims_operation_settled or 0

    def get_deduction_bdt(self, obj):
        if obj.claim and obj.claim.currency and obj.claims_operation_deduction:
            rate = obj.claim.exchange_rate
            return obj.claims_operation_deduction * rate
        return obj.claims_operation_deduction or 0

class ClaimInformationFileSerializer(serializers.ModelSerializer):
    claim_history = FileTransferHistorySerializer(many=True, read_only=True)  
    cost_items = ClaimCostItemSerializer(many=True, read_only=True)
    documents = ClaimDocumentsSerializer(many=True, read_only=True)  
    sender=UserSerializer()
    product=ProductSerializer()
    policy=PolicySerializer()
    current_holder=UserSerializer()
    current_group=GroupSerializer()
    bank = BankSerializer()
    employee=EmployeeInformationSerializer()
    currency=CurrencySerializer()
    district=DistrictSerializer()
    file_status_display = serializers.CharField(source='get_file_status_display', read_only=True)
    creation_from_display = serializers.CharField(source='get_creation_from_display', read_only=True)
    claim_type_display = serializers.CharField(source='get_claim_type_display', read_only=True)
    beneficiary_type_display = serializers.CharField(source='get_beneficiary_type_display', read_only=True)
    death_date = serializers.DateTimeField(format="%d-%m-%Y", required=False)
    fir_date = serializers.DateField(format="%d-%m-%Y", required=False)
    death_of_departure = serializers.DateField(
    input_formats=["%d-%m-%Y"],
    format="%d-%m-%Y",
    required=False
    )
    incident_date = serializers.DateTimeField(format="%d-%m-%Y", required=False)
    date_of_admission= serializers.DateTimeField(format="%d-%m-%Y", required=False)
    date_of_discharge = serializers.DateTimeField(format="%d-%m-%Y", required=False)
    date_of_treatment = serializers.DateTimeField(format="%d-%m-%Y", required=False)
    created_at = serializers.DateTimeField(format="%d-%m-%Y", required=False)
    current_holder_groups = serializers.SerializerMethodField()
    is_user_in_current_group = serializers.SerializerMethodField()
    is_edited_enable = serializers.SerializerMethodField()
    total_amount_bdt = serializers.SerializerMethodField()
    discount_bdt = serializers.SerializerMethodField()
    class Meta:
        model = ClaimInformation
        fields = '__all__'
    def _to_2_decimal(self, value):
        """Helper to round Decimal values to 2 digits"""
        if value is None:
            return Decimal('0.00')
        return value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    def get_total_amount_bdt(self, obj):
        if obj.exchange_rate:
            rate = obj.exchange_rate
            return self._to_2_decimal(obj.total_amount * rate)
        return self._to_2_decimal(obj.total_amount) or 0
    
    def get_discount_bdt(self, obj):
        if obj.exchange_rate:
            rate = obj.exchange_rate
            return self._to_2_decimal(obj.discount * rate)
        return self._to_2_decimal(obj.discount) or 0
    
    def get_current_holder_groups(self, obj):
        if obj.current_holder:
            return list(obj.current_holder.groups.values_list('name', flat=True))
        return []
    
    def get_is_user_in_current_group(self, obj):
        # """Check if the current logged-in user belongs to the same group as current_group"""
        # # return True
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False

        current_group = obj.current_group
        if not current_group:
            return False
        user_group_ids = request.user.groups.values_list('id', flat=True)
        
        return current_group.id in user_group_ids
    
    def get_is_edited_enable(self, obj):
        # """Check if the current logged-in user belongs to the same group as current_group"""
        # # return True
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        current_group = obj.current_group
        if not current_group:
            return False
        enable_edit=True
        groups=request.user.groups.values_list('name', flat=True)
        if "Insurer Claim Officer" in groups:
            enable_edit=obj.is_edited_claim_officer
        elif "Waada Operation" in groups:
            enable_edit=obj.is_edited_waada
        elif "Claim Supervisor" in groups:
            enable_edit=obj.is_edited_claim_supervisor
        elif "Insurer Audit Officer" in groups:
            enable_edit=obj.is_edited_audit_officer
        elif "ORGANIZATION HR" in groups:
            enable_edit=False
        elif "B2B Employee" in groups:
            enable_edit=False
        return enable_edit
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # convert cost_items list into dict keyed by 'key'
        rep['cost_items'] = {item['key']: item for item in rep['cost_items']}
        total_claims_operation_settled = 0
        total_audit_settled = 0
        total_clamed_amount=0
        total_claimed_amount_bdt=0
        
        # Loop through all items and accumulate totals
        for item in rep['cost_items'].values():
            # Claims operation settled total
            claim_val = item.get('claimed_amount')
            if claim_val not in (None, ''):
                try:
                    total_claimed_amount_bdt += float(claim_val)
                except (ValueError, TypeError):
                    pass  # skip non-numeric values
            claims_val = item.get('claims_operation_settled')
            claims_super_val = item.get('claim_supervisor_settled')
            if claims_val not in (None, ''):
                try:
                    total_claims_operation_settled += float(claims_val)
                except (ValueError, TypeError):
                    pass  # skip non-numeric values
            
            claims_amount =  item.get('currency_amount')
            
            if claims_amount not in (None, ''):
                try:
                    total_clamed_amount += float(claims_amount)
                except (ValueError, TypeError):
                    pass  # skip non-numeric values
            # Audit settled total
            audit_val = item.get('audit_settled')
            if audit_val not in (None, ''):
                try:
                    total_audit_settled += float(audit_val)
                except (ValueError, TypeError):
                    pass  # skip non-numeric values

            claims_ded = float(item.get('claims_operation_deduction') or 0)
            supervisor_ded = float(item.get('claim_supervisor_deduction') or 0)
            audit_ded = float(item.get('audit_deduction') or 0)

            # Create a set of non-zero deductions
            deductions = [claims_ded, supervisor_ded, audit_ded]

            # Only count duplicates once
            unique_deductions = set(deductions)

            # Sum of unique non-zero values
            row_total_deduction = sum(unique_deductions)

            item['total_deduction'] = f"{row_total_deduction:.2f}"
        rate=1       
        discount=float(rep["discount"])   
        if rep['exchange_rate']: 
            if float(rep['exchange_rate']) > 0:
                rate=float(rep['exchange_rate'])
            discount=discount*float(rate)  
        if  total_claimed_amount_bdt == 0:
            total_clamed_amount = float(rep.get('total_amount') or 0)
            total_claimed_amount_bdt = float(rep.get('total_amount') or 0) * rate
        total_ampunt =float(total_claimed_amount_bdt)-discount
        # Add totals to final output
        rep['total_currency_amount'] = f"{total_clamed_amount:.2f}"
        rep['total_claimed_after_discount'] = f"{total_ampunt:.2f}"
        rep['total_claimed_amount'] = f"{total_ampunt:.2f}"
        rep['total_claims_operation_settled'] = f"{max(total_claims_operation_settled - discount, 0):.2f}"
        rep['total_audit_settled'] = f"{max(total_audit_settled - discount, 0):.2f}"
        return rep


class ClaimInformationListSerializer(serializers.ModelSerializer):
    claim_history = FileTransferHistorySerializer(many=True, read_only=True)  
    cost_items = ClaimCostItemSerializer(many=True, read_only=True)
    documents = ClaimDocumentsSerializer(many=True, read_only=True)  
    sender=UserSerializer()
    product=ProductSerializer()
    policy=PolicySerializer()
    current_holder=UserSerializer()
    current_group=GroupSerializer()
    bank = BankSerializer()
    employee=EmployeeInformationSerializer()
    currency=CurrencySerializer()
    district=DistrictSerializer()
    file_status_display = serializers.CharField(source='get_file_status_display', read_only=True)
    creation_from_display = serializers.CharField(source='get_creation_from_display', read_only=True)
    claim_type_display = serializers.CharField(source='get_claim_type_display', read_only=True)
    beneficiary_type_display = serializers.CharField(source='get_beneficiary_type_display', read_only=True)
    death_date = serializers.DateTimeField(format="%d-%m-%Y", required=False)
    fir_date = serializers.DateField(format="%d-%m-%Y", required=False)
    death_of_departure = serializers.DateField(
    input_formats=["%d-%m-%Y"],
    format="%d-%m-%Y",
    required=False
    )
    incident_date = serializers.DateTimeField(format="%d-%m-%Y", required=False)
    date_of_admission= serializers.DateTimeField(format="%d-%m-%Y", required=False)
    date_of_discharge = serializers.DateTimeField(format="%d-%m-%Y", required=False)
    date_of_treatment = serializers.DateTimeField(format="%d-%m-%Y", required=False)
    current_holder_groups = serializers.SerializerMethodField()
    is_user_in_current_group = serializers.SerializerMethodField()
    is_edited_enable = serializers.SerializerMethodField()
    total_amount_bdt = serializers.SerializerMethodField()
    discount_bdt = serializers.SerializerMethodField()
    class Meta:
        model = ClaimInformation
        fields = '__all__'
    def _to_2_decimal(self, value):
        """Helper to round Decimal values to 2 digits"""
        if value is None:
            return Decimal('0.00')
        return value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    def get_total_amount_bdt(self, obj):
        if obj.exchange_rate:
            rate = obj.exchange_rate
            return self._to_2_decimal(obj.total_amount * rate)
        return self._to_2_decimal(obj.total_amount) or 0
    
    def get_discount_bdt(self, obj):
        if obj.exchange_rate:
            rate = obj.exchange_rate
            return self._to_2_decimal(obj.discount * rate)
        return self._to_2_decimal(obj.discount) or 0
    
    def get_current_holder_groups(self, obj):
        if obj.current_holder:
            return list(obj.current_holder.groups.values_list('name', flat=True))
        return []
    
    def get_is_user_in_current_group(self, obj):
        # """Check if the current logged-in user belongs to the same group as current_group"""
        # # return True
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        print("current_group")

        current_group = obj.current_group
        if not current_group:
            return False
        user_group_ids = request.user.groups.values_list('id', flat=True)
        
        return current_group.id in user_group_ids
    
    def get_is_edited_enable(self, obj):
        # """Check if the current logged-in user belongs to the same group as current_group"""
        # # return True
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        current_group = obj.current_group
        if not current_group:
            return False
        enable_edit=True
        groups=request.user.groups.values_list('name', flat=True)
        if "Insurer Claim Officer" in groups:
            enable_edit=obj.is_edited_claim_officer
        elif "Waada Operation" in groups:
            enable_edit=obj.is_edited_waada
        elif "Claim Supervisor" in groups:
            enable_edit=obj.is_edited_claim_supervisor
        elif "Insurer Audit Officer" in groups:
            enable_edit=obj.is_edited_audit_officer
        elif "ORGANIZATION HR" in groups:
            enable_edit=False
        elif "B2B Employee" in groups:
            enable_edit=False
        return enable_edit
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        choices = dict(ClaimCostItem.CLAIM_ITEM_CHOICES)
        total_claims_operation_settled = 0
        total_audit_settled = 0
        total_claimed_amount_bdt = 0
        total_currency_amount = 0

        items = rep['cost_items']   # keep as array

        for item in items:
            # claimed amount BDT
            claim_val = item.get('claimed_amount')
            if claim_val not in (None, ''):
                try:
                    total_claimed_amount_bdt += float(claim_val)
                except:
                    pass

            # claims operation settled
            claims_val = item.get('claims_operation_settled')
            if claims_val not in (None, ''):
                try:
                    total_claims_operation_settled += float(claims_val)
                except:
                    pass

            # currency amount
            currency_val = item.get('currency_amount')
            if currency_val not in (None, ''):
                try:
                    total_currency_amount += float(currency_val)
                except:
                    pass

            # audit settled
            audit_val = item.get('audit_settled')
            if audit_val not in (None, ''):
                try:
                    total_audit_settled += float(audit_val)
                except:
                    pass

            # deductions
            claims_ded = float(item.get('claims_operation_deduction') or 0)
            supervisor_ded = float(item.get('claim_supervisor_deduction') or 0)
            audit_ded = float(item.get('audit_deduction') or 0)

            unique_deductions = {claims_ded, supervisor_ded, audit_ded}
            row_total_deduction = sum(unique_deductions)
            item["key_label"] = choices.get(item["key"], item["key"].replace("_", " ").title())
            item['total_deduction'] = f"{row_total_deduction:.2f}"

        # exchange rate / discount handling
        rate = 1
        discount = float(rep["discount"])

        if rep.get('exchange_rate') and float(rep['exchange_rate']) > 0:
            rate = float(rep['exchange_rate'])
            discount = discount * rate
        
        if not total_claimed_amount_bdt:
            total_currency_amount = float(rep.get('total_amount') or 0)
            total_claimed_amount_bdt = float(rep.get('total_amount') or 0)
        # final totals
        rep['total_currency_amount'] = f"{total_currency_amount:.2f}"
        rep['total_claimed_amount'] = f"{float(total_claimed_amount_bdt) * rate:.2f}"
        rep['total_claims_operation_settled'] = f"{max(total_claims_operation_settled - discount, 0):.2f}"
        rep['total_audit_settled'] = f"{max(total_audit_settled - discount, 0):.2f}"

        # KEEP ARRAY FORMAT
        rep['cost_items'] = items

        return rep

     

class EmployeeInformationSerializer(serializers.ModelSerializer):
    relation_name = serializers.SerializerMethodField()
    sex_name = serializers.CharField(source='get_sex_display', read_only=True)
    status_name = serializers.CharField(source='get_status_display', read_only=True)
    benificiary_type_name = serializers.CharField(source='get_benificiary_type_display', read_only=True)
    nominee_type_name = serializers.CharField(source='get_nominee_type_display', read_only=True)

    class Meta:
        model = EmployeeInformation
        fields = "__all__"   # ✅ GETS ALL MODEL FIELDS + custom fields above

    def get_relation_name(self, obj):
        if obj.relation and obj.member_id:
            return f"{obj.get_relation_display()}-{obj.member_id.split('-')[-1]}"
        return ""


class EmployeeInformationOrgSerializer(serializers.ModelSerializer):
    organization = serializers.SerializerMethodField()
    relation_name = serializers.SerializerMethodField()
    beneficiaries = serializers.SerializerMethodField()
    designation=DesignationSerializer()
    department=DepartmentSerializer()
    sex_name = serializers.CharField(source='get_sex_display', read_only=True)
    class Meta:
        model = EmployeeInformation
        fields = "__all__"

    

    def get_organization(self, obj):
        if obj.organization_emp_policy and obj.organization_emp_policy.organization:
            return OrgnaizationListSerializer(
                obj.organization_emp_policy.organization,
                context=self.context
            ).data
        return None

    def get_relation_name(self, obj):
        return f"{obj.relation.capitalize()}-{obj.member_id.split('-')[-1]}" if obj.relation else ''

    def get_beneficiaries(self, obj):
        request = self.context.get('request')
        employee = self.context.get('employee')

        if request and request.user.is_superuser:
            qs = EmployeeInformation.objects.all().order_by('id')
        elif employee:
            member_id = employee.member_id
            new_member_id = member_id[:-1]
            qs = EmployeeInformation.objects.filter(
                member_id__startswith=new_member_id).order_by('id')
        else:
            qs = EmployeeInformation.objects.none()

        return EmployeeInformationSerializer(qs, many=True, context=self.context).data


class EmployeeListSerializer(serializers.ModelSerializer):
    organization_emp_policy = OrganizationPolicySerializer()  
    bank = BankSerializer()
    nominee_type_display = serializers.CharField(source='get_nominee_type_display', read_only=True)
    class Meta:
        model = EmployeeInformation
        fields = '__all__'
        
