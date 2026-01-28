import os
import uuid
from django.db import models
from decimal import Decimal
from django.conf import settings
from core.models import CommonBaseModel
from b2bproduct.models import Product,Policy
from django.utils import timezone
# Create your models here.
STATUS_CHOICES = [
        (1, 'Active'),
        (2, 'Inactive'),
        ]

BANK_TYPE_CHOICES = [
        ('bank', 'Bank'),
        ('mfs', 'MOBILE FINANCIAL SERVICE'),
        ]

COMPANY_TYPE_CHOICES = [
        (1, 'Life'),
        (2, 'Non-Life'),
        ]


"""Compnay Plan File Path"""
def compnay_logo_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('company_logo/', filename)

"""Compnay Plan File Path"""
def hospital_logo_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('hospital_logo/', filename)

"""Compnay Plan File Path"""
def compnay_plan_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('company_plan_files/', filename)

"""Organization Tin File Path"""
def tin_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('tin_files/', filename)

"""Organization Bin File Path"""
def bin_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('bin_files/', filename)


"""Organization Document File Path"""
def document_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('org_document_files/', filename)

""" Document File Path"""
def insuert_policy_document_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('insurer_policy_document_files/', filename)

""" Document File Path"""
def organization_policy_document_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('organization_policy_document_files/', filename)

def advice_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('organization_policy_document_files/', filename)

class Bank(CommonBaseModel):
    """Custom User Information"""
    BANK_STATUS_CHOICES = [
        (1, 'Active'),
        (2, 'Inactive'),
        ]
    name = models.CharField(max_length=255,unique=True, blank=True,null=True)
    short_name = models.CharField(max_length=255,unique=True, blank=True,null=True)
    status = models.PositiveSmallIntegerField(choices=BANK_STATUS_CHOICES, default=1)
    account_type = models.CharField(
            max_length=10,
            choices=BANK_TYPE_CHOICES,
            default='bank',
        )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
       related_name="%(class)s_related",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
    )
    class Meta:
        db_table = 'Bank'
        ordering = ('id',)
    
    def __str__(self):
        return str(self.name)
        
class Designation(CommonBaseModel):
    """Custom User Information"""
    title = models.CharField(max_length=255,unique=True, blank=True,null=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
       related_name="%(class)s_related",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
    )
    class Meta:
        db_table = 'designation'
        ordering = ('id',)
    
    def __str__(self):
     return str(self.title)

class Department(CommonBaseModel):
    """Custom User Information"""
    name = models.CharField(max_length=255,unique=True, blank=True,null=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
       related_name="%(class)s_related",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
    )
    class Meta:
        db_table = 'department'
        ordering = ('id',)
    
    def __str__(self):
     return str(self.name)   


class CompanyType(CommonBaseModel):
    """Company Type Information"""
    name = models.CharField(max_length=255,unique=True, blank=True,null=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
       related_name="%(class)s_related",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
    )
    class Meta:
        db_table = 'company_type'
        ordering = ('id',)

class District(CommonBaseModel):
    name = models.CharField(max_length=120, unique=True)
    code = models.CharField(max_length=20, blank=True, null=True, db_index=True)  # e.g. "CHT-01"
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "district"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code or 'no-code'})"

class SalaryRange(CommonBaseModel):
    """Custom User Information"""
    initial_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    final_amount =  models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
       related_name="%(class)s_related",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
    )
    
    class Meta:
        db_table = 'salaryRange'
        ordering = ('id',)
    
        
    def __str__(self):
     return str(self.initial_amount)+'-'+str(self.final_amount)
 


class Plan(CommonBaseModel):
    """Plan Information"""
    name = models.CharField(max_length=255,unique=True, blank=True,null=True)
    salary_range =  models.ForeignKey(
        SalaryRange,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
       related_name="%(class)s_related",
    )
    designation =  models.ForeignKey(
        Designation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
       related_name="%(class)s_related",
    )
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
       related_name="%(class)s_related",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
    )
    
    class Meta:
        db_table = 'plan'
        ordering = ('name',)
    
        
    def __str__(self):
     return str(self.name)


class HospitalInformation(CommonBaseModel):
    """Hospital Information"""
    HOSPITAL_STATUS_CHOICES = [
        (1, 'Active'),
        (2, 'Inactive'),
        ]
    hospital_name = models.CharField(max_length=255, blank=True,null=True)
    address = models.TextField(blank=True)
    website = models.CharField(max_length=250, blank=True,null=True)
    district=models.ForeignKey(District,blank=True,null=True, on_delete=models.SET_NULL,)
    hospital_logo = models.FileField(upload_to=hospital_logo_path,blank=True,null=True)  
    tin_number = models.CharField(max_length=100, blank=True,null=True)
    tin_file = models.FileField(upload_to=tin_file_path,blank=True,null=True)  # You can also use ImageField
    bin_number = models.CharField(max_length=100, blank=True,null=True)
    bin_file = models.FileField(upload_to=bin_file_path,blank=True,null=True)  # You can also use ImageField
    bank=models.ForeignKey(Bank,blank=True,null=True, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=100, blank=True,null=True)
    account_number = models.CharField(max_length=100, blank=True,null=True)
    branch_name = models.CharField(max_length=100, blank=True,null=True)
    routing_number = models.CharField(max_length=100, blank=True,null=True)
    status = models.PositiveSmallIntegerField(choices=HOSPITAL_STATUS_CHOICES, default=1)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
       related_name="%(class)s_related",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
    )
    
    class Meta:
        db_table = 'hospital'
        ordering = ('id',)
    
        
    def __str__(self):
     return str(self.hospital_name)

class HospitalContact(models.Model):
    """Hospital Contact Information"""
    CONTACT_STATUS_CHOICES = [
        (1, 'Active'),
        (2, 'Inactive'),
        ]
    hospital = models.ForeignKey(HospitalInformation, on_delete=models.CASCADE, related_name='hospital_contacts')
    name = models.CharField(max_length=150, blank=True,null=True)
    designation = models.ForeignKey(Designation,blank=True,null=True, on_delete=models.CASCADE, related_name='hospital_designations')
    mobile_no = models.CharField(max_length=150, blank=True,null=True)
    email = models.EmailField(max_length=150, blank=True,null=True)
    status = models.PositiveSmallIntegerField(choices=CONTACT_STATUS_CHOICES, default=1)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
       related_name="%(class)s_related",
    )
    updated_by = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name="%(class)s_updated",
        )
    
    class Meta:
        db_table = 'hospital_contacts'
        ordering = ['-id']  # Orders by id in descending order
    
    def __str__(self):
        return f"Hospital Contact for {self.hospital}"


class Insurer(CommonBaseModel):
    """Insurer Information"""
    INSURER_STATUS_CHOICES = [
        (1, 'Active'),
        (2, 'Inactive'),
        ]
    INSURER_TYPE_CHOICES = [
        (1, 'Life'),
        (2, 'Non Life'),
        ]
    insurer_name = models.CharField(max_length=255, blank=True,null=True)
    insurer_code = models.CharField(max_length=255, blank=True,null=True)
    address = models.TextField(blank=True)
    website = models.CharField(max_length=250, blank=True,null=True)
    trade_license_no = models.CharField(max_length=100, blank=True,null=True)
    company_logo = models.FileField(upload_to=compnay_logo_path,blank=True,null=True)  
    trade_license_file = models.FileField(upload_to=tin_file_path,blank=True,null=True)  # You can also use ImageField
    bin_number = models.CharField(max_length=100, blank=True,null=True)
    bin_file = models.FileField(upload_to=bin_file_path,blank=True,null=True)  # You can also use ImageField
    bank=models.ForeignKey(Bank,blank=True,null=True, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=100, blank=True,null=True)
    account_number = models.CharField(max_length=100, blank=True,null=True)
    branch_name = models.CharField(max_length=100, blank=True,null=True)
    branch_code = models.CharField(max_length=100, blank=True,null=True)
    routing_number = models.CharField(max_length=100, blank=True,null=True)
    insurer_type = models.PositiveSmallIntegerField(choices=INSURER_TYPE_CHOICES, default=1)
    status = models.PositiveSmallIntegerField(choices=INSURER_STATUS_CHOICES, default=1)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
       related_name="%(class)s_related",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
    )
    
    class Meta:
        db_table = 'insurer'
        ordering = ('id',)
    
        
    def __str__(self):
     return str(self.insurer_name)

class InsurerContact(models.Model):
    """Insuer Contact Information"""
    CONTACT_STATUS_CHOICES = [
        (1, 'Active'),
        (2, 'Inactive'),
        ]
    insurer = models.ForeignKey(Insurer, on_delete=models.CASCADE, related_name='insurer_contacts')
    name = models.CharField(max_length=150, blank=True,null=True)
    designation = models.ForeignKey(Designation,blank=True,null=True, on_delete=models.CASCADE, related_name='insurer_designations')
    mobile_no = models.CharField(max_length=150, blank=True,null=True)
    email = models.EmailField(max_length=150, blank=True,null=True)
    status = models.PositiveSmallIntegerField(choices=CONTACT_STATUS_CHOICES, default=1)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
       related_name="%(class)s_related",
    )
    updated_by = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name="%(class)s_updated",
        )
    
    class Meta:
        db_table = 'insurer_contacts'
        ordering = ['-id']  # Orders by id in descending order
    
    def __str__(self):
        return f"Insuer Contact for {self.insurer.insurer_name}"

class InsurerPolicy(models.Model):
    """Insuer Policy Information"""
    INSURER_POLICY_STATUS_CHOICES = [
        (1, 'FAMILY FLOTTER'),
        (2, 'PER DISABILITY'),
        (3, 'PER YEAR'),
        (4, 'PER DECEASE'),
        ]
    insurer = models.ForeignKey(Insurer, on_delete=models.CASCADE, related_name='insurer_policies')
    insurer_contract_no = models.CharField(max_length=255,unique=True, blank=True,null=True)
    contract_title = models.CharField(max_length=150, blank=True,null=True)
    policy_type = models.ForeignKey(Product,blank=True,null=True, on_delete=models.CASCADE)
    remarks = models.TextField(blank=True,null=True)
    end_date = models.DateField(blank=True,null=True,)    
    enrollment_date = models.DateField(blank=True,null=True)
    policy_mode = models.PositiveSmallIntegerField(choices=INSURER_POLICY_STATUS_CHOICES, default=1)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
       related_name="%(class)s_related",
    )
    updated_by = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name="%(class)s_updated",
        )
    def __str__(self):
        return f"Insuer Contact for {self.contract_title}"
    
    def update_status(self):
        today = timezone.now().date()
        if self.enrollment_date <= today <= self.end_date:
            self.status = 1
        else:
            self.status = 0
        self.save()
    
    class Meta:
        db_table = 'insurer_policy'
        ordering = ['-id']  # Orders by id in descending order

class InsurerPolicyDocuments(CommonBaseModel):
    insurer_policy =  models.ForeignKey(InsurerPolicy,blank=True,null=True, on_delete=models.CASCADE,related_name='insurer_policy_documents')
    document = models.FileField(upload_to=insuert_policy_document_file_path,blank=True,null=True)  # You can also use ImageField    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
       related_name="%(class)s_related",
    )
    updated_by = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name="%(class)s_updated",
        )
    def __str__(self):
        return f"{self.insurer_policy}"
    
    class Meta:
        db_table = 'insurer_policy_document'
        ordering = ['-id']  # Orders by id in descending order
        


        

class Organization(CommonBaseModel):
    """Organization Information"""
    ORGANIZATION_STATUS_CHOICES = [
        (1, 'Active'),
        (2, 'Inactive'),
        ]
    organization_code = models.CharField(max_length=150,unique=True, blank=True,null=True)
    organization_name = models.CharField(max_length=150, blank=True,null=True)
    organization_address = models.TextField(blank=True)
    website = models.CharField(max_length=250,blank=True,null=True)
    company_logo = models.FileField(upload_to=compnay_logo_path,blank=True,null=True)  
    trade_license_file = models.FileField(upload_to=tin_file_path,blank=True,null=True)  # You can also use ImageField
    trade_license_no = models.CharField(max_length=100, blank=True,null=True)
    trade_license_file = models.FileField(upload_to=tin_file_path,blank=True,null=True)  # You can also use ImageField
    bin_number = models.CharField(max_length=100, blank=True,null=True)
    bin_file = models.FileField(upload_to=bin_file_path,blank=True,null=True)  # You can also use ImageField
    bank=models.ForeignKey(Bank,blank=True,null=True, on_delete=models.DO_NOTHING)
    account_name = models.CharField(max_length=100, blank=True,null=True)
    account_number = models.CharField(max_length=100, blank=True,null=True)
    branch_name = models.CharField(max_length=100, blank=True,null=True)
    branch_code = models.CharField(max_length=100, blank=True,null=True)
    routing_number = models.CharField(max_length=100, blank=True,null=True)
    company_type = models.ForeignKey(
    CompanyType,
    blank=True,
    null=True,
    on_delete=models.DO_NOTHING
    )
    status = models.PositiveSmallIntegerField(choices=ORGANIZATION_STATUS_CHOICES, default=1)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
       related_name="%(class)s_related",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
    )

    REQUIRED_FIELDS = [organization_code,organization_name]
    class Meta:
        db_table = 'organization'
        ordering = ('-id',)
    
    def __str__(self):
     return str(self.organization_code)
 
 
 
class OrganizationContact(models.Model):
    """Organization Contact Information"""
    CONTACT_STATUS_CHOICES = [
        (1, 'Active'),
        (2, 'Inactive'),
        ]
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='contacts')  
    name = models.CharField(max_length=150, blank=True,null=True)
    designation = models.ForeignKey(Designation, blank=True,null=True, on_delete=models.CASCADE, related_name='organization_designations')
    mobile_no = models.CharField(max_length=150, blank=True,null=True)
    email = models.EmailField(max_length=150, blank=True,null=True)
    status = models.PositiveSmallIntegerField(choices=CONTACT_STATUS_CHOICES, default=1)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
       related_name="%(class)s_related",
    )
    updated_by = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name="%(class)s_updated",
        )
    class Meta:
        db_table = 'organization_contacts'
        ordering = ['-id']  # Orders by id in descending order
    
    def __str__(self):
        return f"Organzation Contact for {self.organization.organization_name}"

class OrganizationPolicy(models.Model):
    """Insuer Policy Information"""
    ORGANIZATION_POLICY_STATUS_CHOICES = [
        (1, 'FAMILY FLOTTER'),
        (2, 'PER DISABILITY'),
        (3, 'PER YEAR'),
        (4, 'PER DECEASE')
        ]
    insurer = models.ForeignKey(Insurer, on_delete=models.CASCADE,blank=True,null=True, related_name='organization_insurers')  
    organization_contract_no = models.CharField(max_length=150, blank=True,null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,blank=True,null=True, related_name='organization_policies')  
    contract_title = models.CharField(max_length=150, blank=True,null=True)
    policy_type = models.ForeignKey(Product,blank=True,null=True, on_delete=models.CASCADE)
    remarks = models.TextField(blank=True,null=True)
    end_date = models.DateField(blank=True,null=True,)    
    enrollment_date = models.DateField(blank=True,null=True)
    policy_mode = models.PositiveSmallIntegerField(choices=ORGANIZATION_POLICY_STATUS_CHOICES, blank=True,null=True,default=1)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
       related_name="%(class)s_related",
    )
    updated_by = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name="%(class)s_updated",
        )
    def __str__(self):
        return f"Organization Policy for {self.organization_contract_no}"
    class Meta:
        db_table = 'organization_policy'
        ordering = ['id']  # Orders by id in descending order
    
class OrganizationPolicyDocuments(CommonBaseModel):
    organization_policy =  models.ForeignKey(OrganizationPolicy,blank=True,null=True, on_delete=models.CASCADE,related_name='org_policy_documents')
    document = models.FileField(upload_to=organization_policy_document_file_path,blank=True,null=True)  # You can also use ImageField    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
       related_name="%(class)s_related",
    )
    updated_by = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name="%(class)s_updated",
        )
    def __str__(self):
        return f"{self.organization_policy}"
    
    class Meta:
        db_table = 'organization_policy_document'
        ordering = ['-id']  # Orders by id in descending order

class CompanyPlan(CommonBaseModel):
    organization_policy= models.ForeignKey(OrganizationPolicy, blank=True,null=True,on_delete=models.CASCADE, related_name='org_plan_policies')
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
       related_name="%(class)s_related",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
    )
    class Meta:
        db_table = 'company_plans'
        ordering = ['-id']  # Orders by id in descending order    

    # def __str__(self):
    #     return f"{self.organization.organization_name}"
    
class CompanyPlanDocument(CommonBaseModel):
    companyplan = models.ForeignKey(CompanyPlan, on_delete=models.CASCADE, blank=True,null=True,related_name='company_plan_documents')
    plan = models.ForeignKey(Plan,blank=True,null=True, on_delete=models.CASCADE, related_name='plan_types')
    company_plan_doc = models.FileField(upload_to=compnay_plan_file_path,blank=True,null=True)  # You can also use ImageField
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
       related_name="%(class)s_related",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
    )
    class Meta:
        db_table = 'company_plan_document'
        ordering = ['id']  # Orders by id in descending order    

    # def __str__(self):
    #     return f"{self.plan.name}"
    
class CompanyPlanItem(CommonBaseModel):
    company_document = models.ForeignKey(CompanyPlanDocument,blank=True,null=True, on_delete=models.CASCADE, related_name='company_plan_items')
    policy_type = models.ForeignKey(Product,blank=True,null=True, on_delete=models.CASCADE, related_name='plan_policies')
    coverage_type = models.ForeignKey(Policy,blank=True,null=True, on_delete=models.CASCADE, related_name='plan_coverage_types')
    coverage_amount = models.DecimalField(max_digits=12,blank=True,null=True, decimal_places=2)
    premium_rate = models.DecimalField(max_digits=5,blank=True,null=True, decimal_places=2)
    premium_amount = models.DecimalField(max_digits=12,blank=True,null=True, decimal_places=2)
    insured_beneficiary_no = models.DecimalField(max_digits=12,blank=True,null=True, decimal_places=2)
    total = models.DecimalField(max_digits=15,blank=True,null=True, decimal_places=2)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
       related_name="%(class)s_related",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
    )
    class Meta:
        db_table = 'company_plan_items'
        ordering = ['-id']  # Orders by id in descending order    

    # def __str__(self):
    #     return f"{self.coverage_type.name}"


class GopInformation(models.Model):
    STATUS_CHOICES = [
        (1, 'Pending'),
        (2, 'Completed'),
        ]
    hospital = models.ForeignKey(HospitalInformation, on_delete=models.CASCADE, related_name='hospitals')
    bed_cabin_word_no = models.CharField(max_length=30, blank=True,null=True)
    date_of_admission = models.DateField(blank=True,null=True)  
    attendant_name =  models.CharField(max_length=50, blank=True,null=True)
    document = models.FileField(upload_to=advice_file_path,blank=True,null=True)  # You can also use ImageField    
    attendant_mobile =  models.CharField(max_length=30, blank=True,null=True)
    diagnosis =  models.CharField(max_length=150, blank=True,null=True)
    attendant_relation =  models.CharField(max_length=50, blank=True,null=True)
    gop =  models.CharField(max_length=50, blank=True,null=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
       related_name="%(class)s_related",
    )
    updated_by = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name="%(class)s_updated",
        )
    def __str__(self):
        return f"GOP Information for {self.attendant_name}"
    
   
    class Meta:
        db_table = 'gop_information'
        ordering = ['-id']  # Orders by id in descending order
