from django.contrib import admin
from .models import (
    Channel,
    Branch,
    SalesRole,
    SalesEmployee,
    SalesGroup,
    GroupMember,
    SalesTarget,
    SalesProduct,
    # PolicySale,
    Achievement,
    CommissionRule,
    CommissionLedger,
    OverrideCommission,
    VATLedger,
    CommissionPayout,
    Approval,
    AuditLog,
    PremiumCollection
)

# -------------------------
# SIMPLE MODELS
# -------------------------
admin.site.register(Channel)
admin.site.register(SalesRole)
admin.site.register(SalesGroup)
admin.site.register(GroupMember)
admin.site.register(SalesProduct)
admin.site.register(CommissionRule)
admin.site.register(VATLedger)
admin.site.register(CommissionPayout)
admin.site.register(Branch)
admin.site.register(AuditLog)


# -------------------------
# SALES EMPLOYEE
# -------------------------
@admin.register(SalesEmployee)
class SalesEmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'employee_code',
        'user',
        'role',
        'branch',
        'status',
        'manager'
    )
    list_filter = ('status', 'role', 'branch')
    search_fields = ('employee_code', 'phone', 'user__username')


# -------------------------
# SALES TARGET
# -------------------------
@admin.register(SalesTarget)
class SalesTargetAdmin(admin.ModelAdmin):
    list_display = (
        'scope',
        'employee',
        'group',
        'designation',
        'target_amount',
        'month',
        'year',
        'assigned_by'
    )
    list_filter = ('scope', 'month', 'year')


# -------------------------
# POLICY SALE
# -------------------------
# @admin.register(PolicySale)
class PolicySaleAdmin(admin.ModelAdmin):
    list_display = (
        # 'policy_no',
        'sales_person',
        'product',
        'premium',
        'vat_amount',
        'net_amount',
        'status',
        'issue_date'
    )
    list_filter = ('status', 'issue_date')
    # search_fields = ('policy_no',)

# -------------------------
# ACHIEVEMENT
# -------------------------
@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = (
        'employee',
        'month',
        'year',
        'target',
        'achieved',
        'percent'
    )
    list_filter = ('month', 'year')


# -------------------------
# COMMISSION LEDGER
# -------------------------
@admin.register(CommissionLedger)
class CommissionLedgerAdmin(admin.ModelAdmin):
    list_display = (
        'employee',
        # 'policy',
        'gross_commission',
        'vat_deduction',
        'tax_deduction',
        'net_commission'
    )


# -------------------------
# OVERRIDE COMMISSION
# -------------------------
@admin.register(OverrideCommission)
class OverrideCommissionAdmin(admin.ModelAdmin):
    list_display = (
        # 'policy',
        'upline',
        'level',
        'override_percent',
        'amount'
    )


# -------------------------
# APPROVAL FLOW
# -------------------------
@admin.register(Approval)
class ApprovalAdmin(admin.ModelAdmin):
    list_display = (
        # 'sale',
        'approver',
        'level',
        'status'
    )
    list_filter = ('status', 'level')

admin.site.register(PremiumCollection)
    