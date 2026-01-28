# signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import EmployeeInformation,ClaimInformation
from  accounts.models import EditLog
from .middleware import get_current_user

@receiver(pre_save, sender=EmployeeInformation)
def log_employee_changes(sender, instance, **kwargs):
    # Skip logging for new records
    if not instance.pk:
        return
    
    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    user = get_current_user()

    for field in instance._meta.fields:
        field_name = field.name
        old_value = getattr(old_instance, field_name, None)
        new_value = getattr(instance, field_name, None)

        # Skip if both are None or equal
        if old_value == new_value:
            continue

        # Skip if both are empty strings (optional, for CharFields)
        if old_value in [None, ""] and new_value in [None, ""]:
            continue

        # Create edit log only for actual differences
        EditLog.objects.create(
            model_name=sender.__name__,
            object_id=instance.pk,
            field_name=field_name,
            old_value=old_value,
            new_value=new_value,
            user=user
        )



@receiver(pre_save, sender=ClaimInformation)
def log_claim_edits(sender, instance, **kwargs):
    # Skip if it's a new record (no old data yet)
    if not instance.pk:
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    user = get_current_user()

    # --- fields to IGNORE during 'file sending' ---
    # (since file sending changes only group/status/holder)
    TRANSFER_FIELDS = ['is_edited_waada','is_paid_by_claim','is_edited_audit_officer','is_edited_claim_officer','current_holder', 'current_group', 'sender', 'file_status']

    for field in instance._meta.fields:
        field_name = field.name

        # Skip irrelevant or transfer-related fields
        if field_name in TRANSFER_FIELDS:
            continue

        old_value = getattr(old_instance, field_name, None)
        new_value = getattr(instance, field_name, None)

        # Skip if both same or both null/blank
        if old_value == new_value:
            continue
        if old_value in [None, ""] and new_value in [None, ""]:
            continue

        # Convert FK values to readable strings
        if hasattr(field, 'remote_field') and field.remote_field:
            try:
                old_value = getattr(old_value, 'name', str(old_value)) if old_value else None
                new_value = getattr(new_value, 'name', str(new_value)) if new_value else None
            except Exception:
                pass

        # Create the edit log entry
        EditLog.objects.create(
            model_name=sender.__name__,
            object_id=instance.pk,
            field_name=field_name,
            old_value=old_value,
            new_value=new_value,
            user=user
        )