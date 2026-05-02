from django.db import models
from django.conf import settings
from b2bmanagement.models import Designation,Branch,Department,Organization,Bank
from accounts.models import CustomUser
# Create your models here.

class Channel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SalesRole(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    hierarchy_level = models.PositiveIntegerField(
        help_text="""
            1=National Head
            2=Regional Manager
            3=Zonal Manager
            4=Area Manager
            5=Branch Manager
            6=Sales Officer
            7=Agent
            """
    )

    def __str__(self):
        return self.name

class SalesEmployee(models.Model):
    STATUS=(
        (1,'ACTIVE'),
        (2,'INACTIVE')
    )

    user=models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='employee_profile'
    )
    employee_code=models.CharField(max_length=30,unique=True)
    employee_name=models.CharField(max_length=150,null=True, blank=True)
    phone=models.CharField(max_length=30)
      # NEW FIELDS
    father_name = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )

    mother_name = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )

    dob = models.DateField(
        null=True,
        blank=True
    )
    channel = models.ForeignKey(Channel, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    designation=models.ForeignKey(
        Designation,
        on_delete=models.SET_NULL,
        null=True
    )

    branch=models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True
    )
    role = models.ForeignKey(
        SalesRole,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    manager=models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='subordinates'
    )
    
    line_manager=models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='line_reports',
        on_delete=models.SET_NULL
    )

    status = models.IntegerField(
            choices=STATUS,
            default=1
    )
    joining_date=models.DateField(null=True,blank=True)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.employee_code

class SalesGroup(models.Model):
    name=models.CharField(
        max_length=100
    )
    manager=models.ForeignKey(
        SalesEmployee,
        on_delete=models.CASCADE
    )

    parent_group=models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )


class GroupMember(models.Model):
    group=models.ForeignKey(
        SalesGroup,
        on_delete=models.CASCADE
    )

    employee=models.ForeignKey(
        SalesEmployee,
        on_delete=models.CASCADE
    )


class PremiumCollection(models.Model):

    STATUS = (
        ('partial', 'Partial'),
        ('full', 'Full')
    )

    PAYMENT_TYPE = (
        ('bank', 'Bank'),
        ('cash', 'Cash'),
        ('mfs', 'MFS'),
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='collections',
        null=True,
        blank=True
    )

    collected_by = models.ForeignKey(
        'salesman_management.SalesEmployee',
        on_delete=models.SET_NULL,
        related_name='collections',
        null=True,
        blank=True
    )

    # =========================
    # AMOUNT
    # =========================
    premium_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    collected_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    due_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    # =========================
    # STATUS
    # =========================
    status = models.CharField(max_length=10, choices=STATUS)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE,null=True,blank=True)

    # =========================
    # COMMISSION
    # =========================
    commission_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    commission_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    # =========================
    # DATE
    # =========================
    collection_date = models.DateField()

    # =========================
    # BANK (ONLY NAME FROM BANK MODEL)
    # =========================
    bank = models.ForeignKey(
        Bank,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='collections'
    )

    account_name = models.CharField(max_length=255, null=True, blank=True)
    account_number = models.CharField(max_length=100, null=True, blank=True)
    bank_image = models.ImageField(upload_to='bank_slips/', null=True, blank=True)

    # =========================
    # MFS (MANUAL DETAILS)
    # =========================
    transaction_id = models.CharField(max_length=100, null=True, blank=True)

    # =========================
    # CASH
    # =========================
    cash_received_by = models.CharField(max_length=255, null=True, blank=True)
    cash_note = models.TextField(null=True, blank=True)

    # =========================
    # SYSTEM
    # =========================
    created_at = models.DateTimeField(auto_now_add=True)
    
    

class SalesTarget(models.Model):

    SCOPE=(
      ('designation','Designation'),
      ('group','Group'),
      ('individual','Individual')
    )

    scope = models.CharField(
        max_length=20,
        choices=SCOPE,
        null=True,
        blank=True
    )

    designation=models.ForeignKey(
        Designation,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    group=models.ForeignKey(
        SalesGroup,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    employee=models.ForeignKey(
        SalesEmployee,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    assigned_by=models.ForeignKey(
        SalesEmployee,
        related_name='targets_given',
        null=True,
        on_delete=models.SET_NULL
    )

    target_amount=models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )

    month = models.IntegerField(null=True, blank=True)
    year = models.IntegerField(
        null=True,
        blank=True
    )


class SalesProduct(models.Model):
    name=models.CharField(
        max_length=100
    )

    commission_percent=models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    vat_percent=models.DecimalField(
        max_digits=5,
        decimal_places=2
    )


# class PolicySale(models.Model):

#     STATUS=(
#       ('pending','Pending'),
#       ('approved','Approved'),
#       ('rejected','Rejected')
#     )

#     sales_person=models.ForeignKey(
#         SalesEmployee,
#         on_delete=models.CASCADE,
#         related_name='sales_policies'   # FIX
#     )

#     product=models.ForeignKey(
#         SalesProduct,
#         on_delete=models.PROTECT
#     )

#     policy_no=models.CharField(
#         max_length=50,
#         unique=True
#     )

#     premium=models.DecimalField(
#         max_digits=15,
#         decimal_places=2
#     )

#     vat_amount=models.DecimalField(
#         max_digits=15,
#         decimal_places=2,
#         default=0
#     )

#     net_amount=models.DecimalField(
#         max_digits=15,
#         decimal_places=2,
#         default=0
#     )

#     issue_date=models.DateField()

#     status=models.CharField(
#         max_length=20,
#         choices=STATUS
#     )

#     approved_by=models.ForeignKey(
#         SalesEmployee,
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL
#     )

#     def save(self,*args,**kwargs):
#         self.vat_amount=(
#             self.premium*
#             self.product.vat_percent
#         )/100

#         self.net_amount=(
#             self.premium-
#             self.vat_amount
#         )

#         super().save(*args,**kwargs)
    
class Achievement(models.Model):

    employee=models.ForeignKey(
        SalesEmployee,
        on_delete=models.CASCADE
    )

    month = models.IntegerField(null=True, blank=True)
    year = models.IntegerField(
        null=True,
        blank=True
    )

    target=models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    achieved=models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    @property
    def percent(self):
        return (
            self.achieved /
            self.target
        )*100 if self.target else 0


class CommissionRule(models.Model):

    designation=models.ForeignKey(
        Designation,
        on_delete=models.CASCADE
    )

    min_achievement=models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    commission_rate=models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    override_rate=models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )


class CommissionLedger(models.Model):

    employee=models.ForeignKey(
        SalesEmployee,
        on_delete=models.CASCADE
    )

    # policy=models.ForeignKey(
    #     PolicySale,
    #     on_delete=models.CASCADE
    # )

    gross_commission=models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    vat_deduction=models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    tax_deduction=models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    net_commission=models.DecimalField(
        max_digits=15,
        decimal_places=2
    )


class OverrideCommission(models.Model):

    # policy=models.ForeignKey(
    #     PolicySale,
    #     on_delete=models.CASCADE
    # )

    upline=models.ForeignKey(
        SalesEmployee,
        on_delete=models.CASCADE
    )

    level=models.IntegerField()

    override_percent=models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    amount=models.DecimalField(
        max_digits=15,
        decimal_places=2
    )


class VATLedger(models.Model):
    # policy=models.ForeignKey(
    #     PolicySale,
    #     on_delete=models.CASCADE
    # )

    vat_amount=models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    tax_period=models.CharField(
        max_length=20
    )

class CommissionPayout(models.Model):

    employee=models.ForeignKey(
        SalesEmployee,
        on_delete=models.CASCADE
    )

    amount=models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    payout_date=models.DateField()

    paid=models.BooleanField(
        default=False
    )


class Approval(models.Model):

    # sale=models.ForeignKey(
    #     PolicySale,
    #     on_delete=models.CASCADE
    # )

    approver=models.ForeignKey(
        SalesEmployee,
        on_delete=models.CASCADE
    )

    level=models.IntegerField()

    status=models.CharField(
        max_length=30
    )

    remarks=models.TextField(
        blank=True
    )

class AuditLog(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True)
    action=models.CharField(max_length=255)
    model_name=models.CharField(max_length=100)
    record_id=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)