import os
import uuid
from django.db import models
from django.conf import settings 
from b2bmanagement.models import Designation,Bank,Department,Organization,Plan,OrganizationPolicy,District
from b2bproduct.models import Product,Policy
from accounts.models import CustomUser
from django.contrib.auth.models import Group
from django.utils import timezone
# Create your models here.


""" Document Type""" 
DOCUMENT_TYPE_CHOICES = [
        ('drc', 'DEATH REGISTRATION CERTIFICATE'),
        ('dcfh', 'DEATH CERTIFICATE FROM HOSPITAL'),
        ('cnnph', 'COPY OF NID OF NOMINEE & POLICY HOLDER'),
        ('hdc', 'HOSPITAL DISCHARGE CERTIFICATE'),
        ('dp', 'DOCTOR’S PRESCRIPTIONS'),
        ('dr', 'DIAGNOSIS REPORTS'),
        ('hb', 'HOSPITAL BILLS'),
        ('fad', 'FIR FOR ACCIDENTAL DEATH'),
        ('nbad', 'NOMINEE BANK ACCOUNT DETAILS'),
        ('gs/lt', 'GRAVEYARD SLIP / LOCAL TESTIMONIAL'),
        ('dl', 'DIVERSE LICENSE'),
        ('all', 'All Documents'),
        
    ]


""" Claim Status""" 
CLAIM_TYPE_CHOICES = [
        ('life', 'LIFE'),
        ('health', 'HEALTH'),
    ]



FILE_FROM_CHOICES = [
        (1, 'WEB'),
        (2, 'Mobile APP'),
    ]

""" Status""" 
CLAIM_BENIFICIARY_TYPE_CHOICES = [
        ('nd', 'NATURAL DEATH'),
        ('ad', 'ACCIDENTAL DEATH'),
        ('ptd', 'PERMANENT TOTAL DISABILITY'),
        ('pd', 'PARTIAL DISABILITY'),
        ('hipd', 'HEALTH - IPD'),
        ('hopd', 'HEALTH - OPD'),
        ('hm', 'HEALTH - MATERNITY'),
        ('hdc', 'HEALTH - DAYCARE'),
        ('hopdo', 'HEALTH - OPD - OPTICAL'),
        ('hopdd', 'HEALTH - OPD - DENTAL'),
        ('hci', 'CRTICAL ILLNESS'),
    ]


class AuditBaseModel(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True

class Currency(AuditBaseModel):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, unique=True)  # e.g., 'USD', 'BDT'
    symbol = models.CharField(max_length=5, blank=True, null=True)  # e.g., '$'
    exchange_rate = models.DecimalField(max_digits=12, decimal_places=4, default=1.0)    
    effective_date= models.DateField(blank=True,null=True)    
    class Meta:
        db_table = 'currency'  # This defines the database table name
        verbose_name_plural = "currencies"

    def __str__(self):
        return f"{self.name} ({self.code})"

class EmployeeInformation(AuditBaseModel):
    """Sex Status""" 
    SEX_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    """Marital Status"""    
    MARITAL_STATUS_CHOICES = (
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed')
    )
    """ ACCOUNT TYPE STATUS""" 
    ACCOUNT_TYPE_CHOICES = [
        ('bank', 'Bank'),
        ('mfs', 'Mobile Financial Service'),
    ]
     
    """Relation Status""" 
    RELATION_CHOICES = [
        ('self', 'Self'),
        ('wife', 'Wife'),
        ('child', 'Child-1'),
        ('child2', 'Child-2'),
        ('child3', 'Child-3'),
        ('child4', 'Child-4'),
        ('child5', 'Child-5'),  
        ('child6', 'Child-6'),
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('brother', 'Brother'),
        ('sister', 'Sister'),
        ('spouse', 'Spouse'),
        ('son', 'Son'),
        ('daughter', 'Daughter'),
        ('friend', 'Friend'),
        ('relative', 'Relative'),
        ('other', 'Other'),
    ]

    """BENIFICIARY _YPE Status""" 
    BENIFICIARY_TYPE_CHOICES = [
        ('sb', 'SINGLE BENIFIT'),
        ('fb', 'FAMILY BENIFIT'),
    ]

    """ Status""" 
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending'),
        ('deleted', 'Deleted'),
    ]

    """ NOMINEE TYPE STATUS""" 
    NOMINEE_TYPE_CHOICES = [
        ('y', 'YES'),
        ('n', 'No'),
    ]
    
    """ NOMINEE TYPE STATUS""" 
    HUMAN_RESOURCE_TYPE_CHOICES = [
        ('y', 'YES'),
        ('n', 'No'),
    ]

    organization_emp_policy = models.ForeignKey(OrganizationPolicy,blank=True,null=True, on_delete=models.CASCADE,related_name='emp_policy_organizations')
    employee_name = models.CharField(max_length=150,blank=True,null=True)
    contract_no = models.CharField(max_length=150,blank=True,null=True)
    employee_id = models.CharField(max_length=100,blank=True,null=True)
    member_id = models.CharField(max_length=100,blank=True,null=True)
    member_name = models.CharField(max_length=150,blank=True,null=True)
    designation = models.ForeignKey(Designation,blank=True,null=True, on_delete=models.CASCADE)
    department =models.ForeignKey(Department, on_delete=models.SET_NULL, null=True,blank=True)
    user =models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True,blank=True,related_name='users')
    nominee_name = models.CharField(max_length=150,blank=True,null=True)
    mobile_number = models.CharField(max_length=80,blank=True,null=True)   
    employee_email = models.CharField(max_length=100,blank=True,null=True)  
    dob = models.DateField(blank=True,null=True)
    number = models.SmallIntegerField(blank=True,null=True)
    age = models.CharField(max_length=20,blank=True,null=True)
    sex =  models.CharField(
        max_length=10,
        choices=SEX_CHOICES,
        default='male',
    )
    nominee_type =  models.CharField(
        max_length=5,
        choices=NOMINEE_TYPE_CHOICES,
        default='n',
    )
    marital_status = models.CharField(
        max_length=10,
        choices=MARITAL_STATUS_CHOICES,
        default='single',
    )
    hr_type =  models.CharField(
        max_length=5,
        choices=HUMAN_RESOURCE_TYPE_CHOICES,
        default='n',
    )
    ac_type =  models.CharField(
        max_length=10,
        choices=ACCOUNT_TYPE_CHOICES,
        default='mfs',
    )
    salary = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    relation = models.CharField(
        max_length=20,
        choices=RELATION_CHOICES,
        default='other',
    )
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True,blank=True)
    membership_date = models.DateField(blank=True,null=True)    
    sum_assured_life = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    bank = models.ForeignKey(Bank,blank=True,null=True, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=150,blank=True,null=True)  
    account_number = models.CharField(max_length=100,blank=True,null=True)    
    branch_name = models.CharField(max_length=150,blank=True,null=True)  
    routing_number = models.CharField(max_length=50,blank=True,null=True)   
    mat_status = models.CharField(max_length=255,blank=True,null=True)    
    mat_plan = models.CharField(max_length=255,blank=True,null=True)   
    benificiary_type = models.CharField(
        max_length=10,
        choices=BENIFICIARY_TYPE_CHOICES,
        default='sb',
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active',
    )
    
    def __str__(self):
        return f"{self.member_id}"
    
    class Meta:
        db_table = 'employee_information'
        ordering = ['-id']  # Orders by id in descending order




class ClaimInformation(AuditBaseModel):
    """ File Status""" 
    FILE_TYPE_CHOICES = [
        (0, 'DECLINED'),
        (1, 'APPROVED'),
        (2, 'SUBMITTED'),
        (3, 'SETTELED'),
        (4, 'Under Processing'),
        (5, 'PROCESSING'),
        (6, 'RETURN'),
        (7, 'DOCUMENT-WANTED') ,
        (8, 'INITIATED'), 
    ]

    """ CLAIM TYPE STATUS""" 
    CLAIM_TYPE_CHOICES = [
        (1, 'Meternity NVD/Normal delivery'),
        (2, 'Maternity LUCS Cesarean'),
        (3, 'Maternity Legal abortion'),
    ]
    employee =  models.ForeignKey(EmployeeInformation,blank=True,null=True, on_delete=models.CASCADE,related_name='employee_claim_files')
    beneficiary_name = models.CharField(max_length=150,blank=True,null=True)
    sender = models.ForeignKey(CustomUser, related_name='sent_files', on_delete=models.CASCADE,blank=True,null=True)
    current_holder = models.ForeignKey(CustomUser, related_name='holding_files', on_delete=models.CASCADE,blank=True,null=True)
    current_group =models.ForeignKey(Group, on_delete=models.SET_NULL,blank=True, null=True, related_name='current_group')
    claim_for = models.CharField(max_length=30,blank=True,null=True)
    product =models.ForeignKey(Product, on_delete=models.SET_NULL, null=True,blank=True)
    policy =models.ForeignKey(Policy, on_delete=models.SET_NULL, null=True,blank=True)
    currency =models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True,blank=True)
    exchange_rate = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    hospital_or_clinic_name = models.CharField(max_length=150,blank=True,null=True)  
    hospital_clinic_address = models.TextField(blank=True,null=True) 
    is_other_description = models.BooleanField(default=False,blank=True,null=True)  
    other_with_description = models.TextField(blank=True,null=True)     
    date_of_admission = models.DateTimeField(blank=True,null=True)  
    date_of_discharge = models.DateTimeField(blank=True,null=True)  
    date_of_treatment = models.DateTimeField(blank=True,null=True) 
    death_of_departure  = models.DateField(blank=True,null=True) 
    fir_date  = models.DateField(blank=True,null=True) 
    incident_date = models.DateTimeField(blank=True,null=True)  
    cause_of_admission = models.TextField(blank=True,null=True) 
    diagnosis = models.TextField(blank=True,null=True) 
    death_date = models.DateTimeField(blank=True,null=True)  
    death_cause = models.TextField(blank=True,null=True) 
    cause_of_treatment = models.TextField(blank=True,null=True) 
    incident_type = models.TextField(blank=True,null=True) 
    doctor_name = models.CharField(max_length=150,blank=True,null=True)  
    claim_type=models.PositiveBigIntegerField(CLAIM_TYPE_CHOICES,blank=True,null=True)
    issued_police_station=models.CharField(max_length=150,blank=True,null=True) 
    district=models.ForeignKey(District, related_name='claim_district', on_delete=models.CASCADE,blank=True,null=True) 
    bank = models.ForeignKey(Bank,blank=True,null=True, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=150,blank=True,null=True)  
    account_number = models.CharField(max_length=100,blank=True,null=True)
    branch_name = models.CharField(max_length=150,blank=True,null=True)  
    routing_number = models.CharField(max_length=50,blank=True,null=True)   
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_perchantage = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    file_status = models.PositiveBigIntegerField(default=4, choices=FILE_TYPE_CHOICES)   
    creation_from = models.PositiveBigIntegerField(default=1, choices=FILE_FROM_CHOICES)   
    is_edited_waada = models.BooleanField(default=False,blank=True,null=True)
    is_edited_claim_officer = models.BooleanField(default=False,blank=True,null=True)
    is_edited_audit_officer = models.BooleanField(default=False,blank=True,null=True)
    is_paid_by_claim = models.BooleanField(default=False,blank=True,null=True)
    is_edited_claim_supervisor = models.BooleanField(default=False,blank=True,null=True)

    def __str__(self):
        return f"{self.beneficiary_name}"
    
    class Meta:
        db_table = 'claim_information'
        ordering = ['-id']  # Orders by id in descending order

"""Claim Document File Path"""
def document_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('claim_documents/', filename)
    

class ClaimDocuments(AuditBaseModel):
    claim =  models.ForeignKey(ClaimInformation,blank=True,null=True, on_delete=models.CASCADE,related_name='documents')
    document_type = models.CharField(
        max_length=10,
        choices=DOCUMENT_TYPE_CHOICES,
        default='all',
        blank=True,
        null=True
    )
    document = models.FileField(upload_to=document_file_path,blank=True,null=True)  # You can also use ImageField    
    def __str__(self):
        return f"{self.document_type}"
    
    class Meta:
        db_table = 'claim_document'
        ordering = ['-id']  # Orders by id in descending order
        

class FileTransferHistory(models.Model):
    file = models.ForeignKey(ClaimInformation, on_delete=models.CASCADE, blank=True, null=True,related_name='claim_history')
    sender = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,blank=True, null=True, related_name='sent_transfers')
    receiver = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True,null=True, related_name='received_transfers')
    to_group = models.ForeignKey(Group, on_delete=models.SET_NULL,blank=True, null=True, related_name='received_group')
    from_group = models.ForeignKey(Group, on_delete=models.SET_NULL,blank=True, null=True, related_name='sent_group')
    from_department = models.ForeignKey(Department, on_delete=models.SET_NULL,blank=True, null=True, related_name='sent_from_dept')
    to_department = models.ForeignKey(Department, on_delete=models.SET_NULL,blank=True, null=True, related_name='sent_to_dept')
    sent_at = models.DateTimeField(auto_now_add=True)
    received_at = models.DateTimeField(null=True, blank=True)
    """ File Status""" 
    FILE_TYPE_CHOICES = [
        (0, 'DECLINED'),
        (1, 'APPROVED'),
        (2, 'SUBMITTED'),
        (3, 'SETTELED'),
        (4, 'PENDING'),
        (5, 'PROCESSING'),
        (6, 'RETURN'),
        (7, 'DOCUMENT-WANTED'),
        (8, 'INITIATED'), 
    ]
    status = models.PositiveBigIntegerField(default=4, choices=FILE_TYPE_CHOICES)   
    status_before = models.PositiveBigIntegerField(default=4, choices=FILE_TYPE_CHOICES)   
    status_after = models.PositiveBigIntegerField(default=4, choices=FILE_TYPE_CHOICES)   
    remarks = models.TextField(blank=True, null=True)
   
    class Meta:
        db_table = 'file_transfer_history'
        ordering = ['-id']  # Orders by id in descending order
        
    def time_spent(self):
        if self.received_at:
            return self.received_at - self.sent_at
        return None
    
    def elapsed_time(self):
        now = timezone.now()
        diff = now - self.received_at
        seconds = diff.total_seconds()

        if seconds < 60:
            return f"{int(seconds)} seconds "
        elif seconds < 3600:
            return f"{int(seconds // 60)} minutes "
        elif seconds < 86400:
            return f"{int(seconds // 3600)} hours "
        elif seconds < 31536000:
            return f"{int(seconds // 86400)} days "
        else:
            return f"{int(seconds // 31536000)} years "

    def __str__(self):
        return f"{self.file} from {self.from_group} to {self.to_group} - {self.status_after}"
    
    
class ClaimCostItem(models.Model):
    CLAIM_ITEM_CHOICES = [
        ('icu_or_ccu_or_nsu', 'ICU/CCU/NSU'),
        ('consultation_fee', 'Consultation fee'),
        ('medical_investigation', 'Medical Investigation'),
        ('investigation_fee', 'Investigation Fee'),
        ('ancillary', 'Ancillary'),
        ('medicine', 'Medicine'),
        ('other', 'Other'),
        ('others', 'others'),
        ('package_cost', 'Package Cost'),
        ('room_rent1', 'Room Rent1'),
        ('room_rent', 'Room Rent'),
        ('day_care_amount', 'Day Care Amount'),
        ('emergency_treatment',"Emergency Treatment"),
        ('physiotherapy_fee','Physiotherapy Fee'),
        ('outstanding_medical_bills', 'Outstanding Medical Bills'),
        ('funeral_expenses', 'Funeral Expenses'),
        ('surgery', 'Surgery'),
        
    ]
    claim = models.ForeignKey(ClaimInformation, on_delete=models.CASCADE, related_name='cost_items')
    key = models.CharField(max_length=50, choices=CLAIM_ITEM_CHOICES,null=True, blank=True)
    currency_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    claimed_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    claims_operation_settled = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    claims_operation_deduction = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    claim_supervisor_settled = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    claim_supervisor_deduction = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    audit_settled = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    audit_deduction = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    remarks_audit = models.TextField(blank=True, null=True)
    remarks_claims_operation = models.TextField(blank=True, null=True)
    remarks_claim_supervisor = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.key}-{self.claimed_amount}"

    class Meta:
        db_table = 'claim_cost_item'