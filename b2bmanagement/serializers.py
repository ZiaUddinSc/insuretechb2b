from rest_framework import serializers
from rest_framework import generics, status
from django.db.models import Sum
from rest_framework.response import Response
from .models import (District,Organization,CompanyType,SalaryRange,Bank,Designation,Plan,
                     Insurer,InsurerContact,InsurerPolicy,InsurerPolicyDocuments,
                     OrganizationContact,OrganizationPolicy,OrganizationPolicyDocuments,CompanyPlan,
                     CompanyPlanItem,CompanyPlanDocument,Department,HospitalInformation,HospitalContact,GopInformation
                     )
from b2bproduct.serializers import ProductSerializer,PolicySerializer


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__' 

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__' 

class OrganizationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__' 

    def validate_organization_code(self, value):
        if not value:
            return None
        if self.instance:
            # Exclude current instance from uniqueness check
            if Organization.objects.filter(organization_code=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("This Organization Code is already in use.")
        else:
            # If creating, just check if it exists
            if Organization.objects.filter(organization_code=value).exists():
                raise serializers.ValidationError("This Organization Code is already in use.")
        return value
        
    def validate_organization_name(self, value):
        if not value:
            return None
        if self.instance:
            # Exclude current instance from uniqueness check
            if Organization.objects.filter(organization_name=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("This Organization Name is already in use.")
        else:
            # If creating, just check if it exists
            if Organization.objects.filter(organization_name=value).exists():
                raise serializers.ValidationError("This Organization Name is already in use.")
        
        return value

    def validate_email(self, value):
        if not value:
            return None
        if self.instance:
            # Exclude current instance from uniqueness check
            if Organization.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("This email is already in use.")
        else:
            # If creating, just check if it exists
            if Organization.objects.filter(email=value).exists():
                raise serializers.ValidationError("email already exists")
        return value


class CompanyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyType
        fields = '__all__' 
 

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__' 

    def validate_name(self, value):
        if not value:
            return None
        if self.instance:
            # Exclude current instance from uniqueness check
            if Organization.objects.filter(organization_code=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("This Bank Name is already in use.")
        else:
            # If creating, just check if it exists
            if Organization.objects.filter(organization_code=value).exists():
                raise serializers.ValidationError("This Bank Name Code is already in use.")
        return value
        
    def validate_short_name(self, value):
        if not value:
            return None
        if self.instance:
            # Exclude current instance from uniqueness check
            if Organization.objects.filter(organization_name=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("This Bank Name is already in use.")
        else:
            # If creating, just check if it exists
            if Organization.objects.filter(organization_name=value).exists():
                raise serializers.ValidationError("This Bank Name is already in use.")
        
        return value


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__' 

    def validate_name(self, value):
        if not value:
            return None
        if self.instance:
            # Exclude current instance from uniqueness check
            if Organization.objects.filter(organization_code=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("This Bank Name is already in use.")
        else:
            # If creating, just check if it exists
            if Organization.objects.filter(organization_code=value).exists():
                raise serializers.ValidationError("This Bank Name Code is already in use.")
        return value
        
    def validate_short_name(self, value):
        if not value:
            return None
        if self.instance:
            # Exclude current instance from uniqueness check
            if Organization.objects.filter(organization_name=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("This Bank Name is already in use.")
        else:
            # If creating, just check if it exists
            if Organization.objects.filter(organization_name=value).exists():
                raise serializers.ValidationError("This Bank Name is already in use.")
        
        return value

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__' 

    def validate_title(self, value):
        if not value:
            return None
        if self.instance:
            # Exclude current instance from uniqueness check
            if Designation.objects.filter(title=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("This Designation Name is already in use.")
        else:
            # If creating, just check if it exists
            if Designation.objects.filter(title=value).exists():
                raise serializers.ValidationError("This Designation is already in use.")
        return value

class SalaryRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryRange
        fields = '__all__' 


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__' 

    def validate_name(self, value):
        if not value:
            return None
        if self.instance:
            # Exclude current instance from uniqueness check
            if Organization.objects.filter(organization_code=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("This Bank Name is already in use.")
        else:
            # If creating, just check if it exists
            if Organization.objects.filter(organization_code=value).exists():
                raise serializers.ValidationError("This Bank Name Code is already in use.")
        return value
        
    def validate_short_name(self, value):
        if not value:
            return None
        if self.instance:
            # Exclude current instance from uniqueness check
            if Organization.objects.filter(organization_name=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("This Bank Name is already in use.")
        else:
            # If creating, just check if it exists
            if Organization.objects.filter(organization_name=value).exists():
                raise serializers.ValidationError("This Bank Name is already in use.")
        
        return value

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__' 

    def validate_title(self, value):
        if not value:
            return None
        if self.instance:
            # Exclude current instance from uniqueness check
            if Designation.objects.filter(title=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("This Designation Name is already in use.")
        else:
            # If creating, just check if it exists
            if Designation.objects.filter(title=value).exists():
                raise serializers.ValidationError("This Designation is already in use.")
        return value

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__' 

    def validate_name(self, value):
        if not value:
            return None
        if self.instance:
            # Exclude current instance from uniqueness check
            if Organization.objects.filter(organization_code=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("This Bank Name is already in use.")
        else:
            # If creating, just check if it exists
            if Organization.objects.filter(organization_code=value).exists():
                raise serializers.ValidationError("This Bank Name Code is already in use.")
        return value
        
    def validate_short_name(self, value):
        if not value:
            return None
        if self.instance:
            # Exclude current instance from uniqueness check
            if Organization.objects.filter(organization_name=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("This Bank Name is already in use.")
        else:
            # If creating, just check if it exists
            if Organization.objects.filter(organization_name=value).exists():
                raise serializers.ValidationError("This Bank Name is already in use.")
        
        return value

#Plan Serializer

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

    def validate_name(self, value):
        if not value:
            return None
        if self.instance:
            # Exclude current instance from uniqueness check
            if Plan.objects.filter(name=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("This Plan is already in use.")
        else:
            # If creating, just check if it exists
            if Plan.objects.filter(name=value).exists():
                raise serializers.ValidationError("This Plan is already in use.")
        return value

class PlanListSerializer(serializers.ModelSerializer):
    salary_range = SalaryRangeSerializer()
    designation = DesignationSerializer()
    class Meta:
        model = Plan
        fields = '__all__' 

#Insurer Serializer

class InsurerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurer
        fields = '__all__' 

    # def validate_website(self, value):
    #     if not value:
    #         return None
    #     if self.instance:
    #         # Exclude current instance from uniqueness check
    #         if Insurer.objects.filter(website=value).exclude(pk=self.instance.pk).exists():
    #             raise serializers.ValidationError("This Website is already in use.")
    #     else:
    #         # If creating, just check if it exists
    #         if Insurer.objects.filter(website=value).exists():
    #             raise serializers.ValidationError("This Website is already in use.")
    #     return value
    
    # def validate_trade_license_no(self, value):
    #     if not value:
    #         return None
    #     if self.instance:
    #         # Exclude current instance from uniqueness check
    #         if Insurer.objects.filter(trade_license_no=value).exclude(pk=self.instance.pk).exists():
    #             raise serializers.ValidationError("Trade License No is already in use.")
    #     else:
    #         # If creating, just check if it exists
    #         if Insurer.objects.filter(trade_license_no=value).exists():
    #             raise serializers.ValidationError("Trade License No is already in use.")
    #     return value
    
    # def validate_bin_number(self, value):
        # if not value:
        #     return None
        # if self.instance:
        #     # Exclude current instance from uniqueness check
        #     if Insurer.objects.filter(bin_number=value).exclude(pk=self.instance.pk).exists():
        #         raise serializers.ValidationError("Bin Number is already in use.")
        # else:
        #     # If creating, just check if it exists
        #     if Insurer.objects.filter(bin_number=value).exists():
        #         raise serializers.ValidationError("Bin Number is already in use.")
        # return value

class InsurerContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsurerContact
        fields = '__all__' 
        extra_kwargs = {
            'insurer': {'required': False}   # <-- make optional
        }

class InsurerContactListSerializer(serializers.ModelSerializer):
    designation=DesignationSerializer()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    class Meta:
        model = InsurerContact
        fields = '__all__' 

class HospitalContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalContact
        fields = '__all__' 
        extra_kwargs = {
            'hospital': {'required': False}   # <-- make optional
        }

class HospitalSerializer(serializers.ModelSerializer):
    hospital_logo=serializers.FileField(required=False, allow_null=True)
    tin_file=serializers.FileField(required=False, allow_null=True)
    bin_file=serializers.FileField(required=False, allow_null=True)
    district_info = DistrictSerializer(source='district', read_only=True)
    bank_info = DistrictSerializer(source='bank', read_only=True)
    hospital_contacts = HospitalContactSerializer(many=True, read_only=True)

    class Meta:
        model = HospitalInformation
        fields = '__all__' 
     
    def validate_hospital_name(self, value):
        if not value:
            return None
        if self.instance:
            # Exclude current instance from uniqueness check
            if HospitalInformation.objects.filter(hospital_name=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("This Hospital Name is already in use.")
        return value
    
    # def get_hospital_logo(self, obj):
    #     request = self.context.get("request")
    #     if obj.hospital_logo:
    #         return request.build_absolute_uri(obj.hospital_logo.url)
    #     return None
    
class GOPListSerializer(serializers.ModelSerializer):
    document=serializers.FileField(required=False, allow_null=True)
    hospital = HospitalSerializer()
    date_of_admission = serializers.DateField(
    input_formats=["%d-%m-%Y"],
    format="%d-%m-%Y",
    required=False
    )
    class Meta:
        model = GopInformation
        fields = '__all__' 
     

class GOPSerializer(serializers.ModelSerializer):
    document=serializers.FileField(required=False, allow_null=True)
    # hospital = HospitalSerializer(many=True, read_only=True)
    date_of_admission = serializers.DateField(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y'],  required=False,
        allow_null=True)
    class Meta:
        model = GopInformation
        fields = '__all__' 
     



    
class InsurerPolicySerializer(serializers.ModelSerializer):
    enrollment_date = serializers.DateField(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y'],  required=False,
        allow_null=True)
    end_date = serializers.DateField(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y'],  required=False,
        allow_null=True)
    class Meta:
        model = InsurerPolicy
        fields = '__all__' 

class InsurerPolicyDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsurerPolicyDocuments
        fields = '__all__' 
        
class InsurerPolicyListSerializer(serializers.ModelSerializer):
    policy_type=ProductSerializer()
    policy_mode_display = serializers.CharField(source='get_policy_mode_display', read_only=True)
    enrollment_date_full = serializers.DateField(
        source="enrollment_date",   # original model field
        format="%d %B, %Y",
        required=False,
        allow_null=True
    )
    end_date_full = serializers.DateField(
        source="end_date",   # original model field
        format="%d %B, %Y",
        required=False,
        allow_null=True
    )
    insurer_policy_documents=InsurerPolicyDocumentsSerializer(many=True)
    days_count = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    def get_days_count(self, obj):
        # Ensure both dates exist
        if obj.enrollment_date and obj.end_date:
            delta = obj.end_date - obj.enrollment_date
            return delta.days
        return None  # or 0 if you prefer
    class Meta:
        model = InsurerPolicy
        fields = '__all__' 



class HospitalListSerializer(serializers.ModelSerializer):
    bank=BankSerializer()
    # hospital_contacts=InsurerContactListSerializer(many=True)
    # insurer_policies=InsurerPolicyListSerializer(many=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    insurer_type_display = serializers.CharField(source='get_insurer_type_display', read_only=True)
    class Meta:
        model = HospitalInformation
        fields = '__all__'      


class InsurerListSerializer(serializers.ModelSerializer):
    bank=BankSerializer()
    insurer_contacts=InsurerContactListSerializer(many=True)
    insurer_policies=InsurerPolicyListSerializer(many=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    insurer_type_display = serializers.CharField(source='get_insurer_type_display', read_only=True)
    class Meta:
        model = Insurer
        fields = '__all__' 



class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__' 

    

class OrganizationContactListSerializer(serializers.ModelSerializer):
    designation=DesignationSerializer()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    class Meta:
        model = OrganizationContact
        fields = '__all__' 


class OrganizationContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationContact
        fields = '__all__' 
        extra_kwargs = {
            'organization': {'required': False}   # <-- make optional
        }

    
class OrganizationPolicySerializer(serializers.ModelSerializer):
    enrollment_date = serializers.DateField(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y'],  required=False,
        allow_null=True)
    end_date = serializers.DateField(input_formats=['%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y'],  required=False,
        allow_null=True)
    class Meta:
        model = OrganizationPolicy
        fields = '__all__' 





class OrganizationPolicyDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationPolicyDocuments
        fields = '__all__' 

class OrganizationPolicyDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationPolicyDocuments
        fields = '__all__'         






class CompanyPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyPlan
        fields = '__all__' 

class CompanyPlanItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyPlanItem
        fields = '__all__' 
 
   

class CompanyPlanDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyPlanDocument
        fields = '__all__'        

 
        
        

        
        

class CompanyPlanItemListSerializer(serializers.ModelSerializer):
    policy_type=ProductSerializer()
    coverage_type=PolicySerializer() 
    class Meta:
        model = CompanyPlanItem
        fields = '__all__'

class CompanyPlanDocumentListSerializer(serializers.ModelSerializer):
    company_plan_items = CompanyPlanItemListSerializer(many=True, read_only=True)
    plan =PlanListSerializer()
    total_sum = serializers.SerializerMethodField()
    class Meta:
        model = CompanyPlanDocument
        fields = '__all__'
        
    def get_total_sum(self, obj):
        return obj.company_plan_items.aggregate(total=Sum('total'))['total'] or 0
    
class CompanyPlanListSerializer(serializers.ModelSerializer):
    company_plan_documents=CompanyPlanDocumentListSerializer(many=True)
    class Meta:
        model = CompanyPlan
        fields = '__all__'
        
class OrganizationPolicyListSerializer(serializers.ModelSerializer):
    enrollment_date_full = serializers.DateField(
        source="enrollment_date",   # original model field
        format="%d %B, %Y",
        required=False,
        allow_null=True
    )
    end_date_full = serializers.DateField(
        source="end_date",   # original model field
        format="%d %B, %Y",
        required=False,
        allow_null=True
    )
    org_plan_policy = serializers.SerializerMethodField() 
    org_policy_documents=OrganizationPolicyDocumentsSerializer(many=True)
    policy_type=ProductSerializer()
    policy_mode_display = serializers.CharField(source='get_policy_mode_display', read_only=True)
    insurer=InsurerSerializer()
    days_count = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    def get_org_plan_policy(self, obj):
        first_plan = obj.org_plan_policies.first()  # get first related object
        if first_plan:
            return CompanyPlanListSerializer(first_plan).data
        return None
    
    def get_days_count(self, obj):
        # Ensure both dates exist
        if obj.enrollment_date and obj.end_date:
            delta = obj.end_date - obj.enrollment_date
            return delta.days
        return None  # or 0 if you prefer
    
    class Meta:
        model = OrganizationPolicy
        fields = '__all__' 

class OrganizationListSerializer(serializers.ModelSerializer):
    bank=BankSerializer()
    organization_policies=OrganizationPolicyListSerializer(many=True)
    class Meta:
        model = Organization
        fields = '__all__' 



class OrgnaizationListSerializer(serializers.ModelSerializer):
    bank=BankSerializer()
    contacts=OrganizationContactListSerializer(many=True)
    organization_policies=OrganizationPolicyListSerializer(many=True)
    # # insurer_policies=InsurerPolicyListSerializer(many=True)
    # status_display = serializers.CharField(source='get_status_display', read_only=True)
    company_type_display = serializers.CharField(source='get_company_type_display', read_only=True)
    class Meta:
        model = Organization
        fields = '__all__' 