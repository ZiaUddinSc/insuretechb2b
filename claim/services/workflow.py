# services/workflow.py
import json
from django.contrib.auth.models import Group
from ..models import ClaimInformation, FileTransferHistory,ClaimCostItem
from accounts.models import CustomUser
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from core.utils import send_dynamic_email
from django.utils import timezone

def normalize_key(name: str) -> str:
    """
    Convert incoming item_name to DB key format:
    - lowercase
    - replace spaces or hyphens with underscores
    - strip leading/trailing whitespace
    """
    if not name:
        return ""
    return name.strip().lower().replace(" ", "_").replace("/", "_or_")

def process_claim_action(claim, action, actor_user, remarks="", settled_amount=None,receiver_user=None,cost_items_raw=None):
    """
    Handles approval, rejection, or document required at each step.
    """
    old_status = claim.file_status
    next_group = None
    new_status = None
    current_group =claim.current_group.name
    last_history = FileTransferHistory.objects.filter(file=claim).order_by('-id').first()
    claim_user = last_history.sender if last_history else None
    context = {
                "username": claim_user.username,
                "support_email": "support@example.com",
                "status":action,
            }
    # --- ORGANIZATION HR Actions ---
    if claim.current_group.name == "ORGANIZATION HR":
        if action == 1 : #APPROVED
            new_status  = 4 # Pending for New
            next_group  = Group.objects.get(name="Waada Operation")
        elif action == 7: # DOCUMENT_REQUIRED
            new_status = 7
            claim.current_holder=claim_user
            last_history.remarks=remarks
            next_group=Group.objects.get(name="B2B Employee")
            claim.current_group=next_group
            last_history.status_after=action
            group= Group.objects.get(name="ORGANIZATION HR") #Document Sending
            send_dynamic_email(
                to_email=claim_user.email,
                template_type="group",
                group=group,
                context=context
            )
        elif action == 0: #DECLINED
            new_status = 0
            last_history.remarks=remarks
            claim.current_holder=claim_user
            last_history.status_after=action
            next_group=Group.objects.get(name="B2B Employee")
            claim.current_group=next_group
            group= Group.objects.get(name="ORGANIZATION HR")
            send_dynamic_email(
                to_email=claim_user.email,
                template_type="group",
                group=group,
                context=context
            )

    # --- Waada Actions ---
    elif claim.current_group.name == "Waada Operation":
        if action == 1:
            new_status  = 4 # Pending for New
            claim.is_edited_waada=True
            next_group = Group.objects.get(name="Insurer Claim Officer")
        elif action == 7:
            new_status = 7
            claim.current_holder=claim_user
            next_group=Group.objects.get(name="B2B Employee")
            claim.current_group=next_group
            claim.is_edited_waada=False
            claim.is_edited_claim_officer=False
            claim.is_edited_audit_officer=False
            claim.is_edited_claim_supervisor=False
            group= Group.objects.get(name="Waada Operation")
            send_dynamic_email(
                to_email=claim_user.email,
                template_type="group",
                group=group,
                context=context
            )

        elif action == 0:
            new_status  = 4 # Pending for New
            claim.current_holder=claim_user
            next_group=Group.objects.get(name="B2B Employee")
            claim.current_group=next_group
            claim.is_edited_waada=False
            claim.is_edited_claim_officer=False
            claim.is_edited_audit_officer=False
            group= Group.objects.get(name="Waada Operation")
            
            send_dynamic_email(
                to_email=claim_user.email,
                template_type="group",
                group=group,
                context=context
            )

    # --- Insurer Claim Officer Actions ---
    elif claim.current_group.name == "Insurer Claim Officer":
        if action == 1:
            new_status  = 4 # Pending for New
            claim.is_edited_claim_officer=True
            group = Group.objects.get(name="Insurer Claim Officer")
            send_dynamic_email(
                to_email=claim_user.email,
                template_type="group",
                group=group,
                context=context
            )
            next_group = Group.objects.get(name="Claim Supervisor")
            claim.settled_amount = settled_amount
        elif action == 7:
            new_status = 7
            claim.current_holder=claim_user
            next_group=Group.objects.get(name="B2B Employee")
            claim.current_group=next_group
            claim.is_edited_waada=False
            claim.is_edited_claim_officer=False
            claim.is_edited_audit_officer=False
            claim.is_edited_claim_supervisor=False
            group= Group.objects.get(name="Claim Supervisor")
            send_dynamic_email(
                to_email=claim_user.email,
                template_type="group",
                group=group,
                context=context
            )
        elif action == 0:
            new_status = 0
            claim.current_holder=claim_user
            next_group=Group.objects.get(name="B2B Employee")
            claim.current_group=next_group
            claim.is_edited_waada=False
            claim.is_edited_claim_officer=False
            claim.is_edited_audit_officer=False
            claim.is_edited_claim_supervisor=False
            group= Group.objects.get(name="Insurer Claim Officer")
            send_dynamic_email(
                to_email=claim_user.email,
                template_type="group",
                group=group,
                context=context
            )

    
    elif claim.current_group.name == "Claim Supervisor":
        if action == 1:
            new_status  = 4 # Pending for New
            claim.is_edited_claim_supervisor=True
            group = Group.objects.get(name="Claim Supervisor")
            send_dynamic_email(
                to_email=claim_user.email,
                template_type="group",
                group=group,
                context=context
            )
            next_group = Group.objects.get(name="Insurer Audit Officer")
            claim.settled_amount = settled_amount
        elif action == 7:
            new_status = 7
            claim.current_holder=claim_user
            next_group=Group.objects.get(name="B2B Employee")
            claim.current_group=next_group
            claim.is_edited_waada=False
            claim.is_edited_claim_officer=False
            claim.is_edited_audit_officer=False
            claim.is_edited_claim_supervisor=False
            group= Group.objects.get(name="Claim Supervisor")
            send_dynamic_email(
                to_email=claim_user.email,
                template_type="group",
                group=group,
                context=context
            )
        elif action == 0:
            new_status = 0
            claim.current_holder=claim_user
            next_group=Group.objects.get(name="B2B Employee")
            claim.current_group=next_group
            claim.is_edited_waada=False
            claim.is_edited_claim_officer=False
            claim.is_edited_audit_officer=False
            claim.is_edited_claim_supervisor=False
            group= Group.objects.get(name="Insurer Claim Officer")
            send_dynamic_email(
                to_email=claim_user.email,
                template_type="group",
                group=group,
                context=context
            )


    # --- Insurer Audit Officer Actions ---
    elif claim.current_group.name == "Insurer Audit Officer":
        if action == 1:
            claim.is_edited_audit_officer=True
            group = Group.objects.get(name="Insurer Audit Officer")
            next_group = Group.objects.get(name="Insurer Finance")
            send_dynamic_email(
                to_email=claim_user.email,
                template_type="group",
                group=group,
                context=context
            )
            new_status = 3 # Final Settlement
        elif action == 7:
            new_status = 7
            claim.current_holder=claim_user
            next_group=Group.objects.get(name="ORGANIZATION HR")
            claim.current_group=next_group
            claim.is_edited_waada=False
            claim.is_edited_claim_officer=False
            claim.is_edited_audit_officer=False
            claim.is_edited_claim_supervisor=False
            group= Group.objects.get(name="Insurer Audit Officer")
            send_dynamic_email(
                to_email=claim_user.email,
                template_type="group",
                group=group,
                context=context
            )
        elif action == 0:
            new_status = 0
            claim.current_holder=claim_user
            next_group=Group.objects.get(name="ORGANIZATION HR")
            claim.current_group=next_group
            claim.is_edited_waada=False
            claim.is_edited_claim_officer=False
            claim.is_edited_audit_officer=False
            claim.is_edited_claim_supervisor=False
            group= Group.objects.get(name="Insurer Audit Officer")
            send_dynamic_email(
                to_email=claim_user.email,
                template_type="group",
                group=group,
                context=context
            )
    # Save claim changes
    elif claim.current_group.name == "B2B Employee":
        new_status = action  
        next_group = Group.objects.get(name="ORGANIZATION HR")               
    if new_status == 1:
        claim.file_status = 4
    else:
        claim.file_status = new_status            
    claim.remarks = remarks
    if action not in [0, 7]:
        claim.current_group = next_group
         # Receiver user must be provided when approving
        if not receiver_user:
            return Response(
                {"error": "Receiver user must be specified when approving the claim."},
                status=status.HTTP_400_BAD_REQUEST
            )
        claim.current_holder    =   receiver_user 
    last_history.status_after   =   action
    last_history.remarks        =   remarks
    last_history.save()
    claim.save()
    if action == 1 and cost_items_raw:
        try:
            cost_items = json.loads(cost_items_raw)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON in cost_items"}, status=400)

        # Clear existing cost items for the claim
        # print(claim.current_group.name)
        # Create for all 3 approval groups
        approval_groups = ["Insurer Claim Officer", "Insurer Audit Officer","Claim Supervisor"]
        created_count = 0
        if current_group in approval_groups:
            existing_items = {c.key: c for c in ClaimCostItem.objects.filter(claim=claim)}
            ClaimCostItem.objects.filter(claim=claim).delete()
            for item in cost_items:
                raw_name = item.get("item_name", "").strip()
                
                key = normalize_key(raw_name)# must match one of CLAIM_ITEM_CHOICES
                if key not in dict(ClaimCostItem.CLAIM_ITEM_CHOICES):
                    continue  # skip invalid keys
                if key in existing_items:
                    obj = existing_items[key]
                    # print(key,item)
                  # ✅ KEEP OLD REMARK if new value is "", None, or not provided
                    new_sup_remark = item.get("remarks_claim_supervisor")
                    # print(new_sup_remark)
                    if new_sup_remark  in [None, "", "null"]:
                        new_sup_remark = obj.remarks_claim_supervisor

                    # Same logic for other remarks if you want
                    new_claims_remark = item.get("remarks")
                    if new_claims_remark  in [None, "", "null"]:
                        new_claims_remark = obj.remarks_claims_operation

                    new_audit_remark = item.get("audit_remarks")
                    if new_audit_remark  in [None, "", "null"]:
                        new_audit_remark = obj.remarks_audit
                    # print(new_audit_remark)
                    # print(new_claims_remark)
                    # print(new_sup_remark)
                    ClaimCostItem.objects.create(
                        claim=claim,
                        key=key,  # use key field, not item_name
                        currency_amount=item.get("currency_amount", 0) or 0,
                        claimed_amount=item.get("claimed_amount", 0) or 0,
                        claims_operation_settled=item.get("settled_amount", 0) or 0,
                        claims_operation_deduction=item.get("deduction", 0) or 0,
                        claim_supervisor_settled=item.get("claim_supervisor_settled", 0) or 0,
                        claim_supervisor_deduction=item.get("claim_supervisor_deduction", 0) or 0,
                        audit_settled=item.get("audit_settled", 0) or 0,
                        audit_deduction=item.get("audit_deduction", 0) or 0,
                        remarks_audit=new_audit_remark,
                        remarks_claim_supervisor=new_sup_remark,
                        remarks_claims_operation=new_claims_remark
                    )
                    created_count += 1
    reciever=None
    if action==1:
        reciever=actor_user
    if action in [0,7]:
        reciever=claim_user         
    # Record history
    FileTransferHistory.objects.create(
        file=claim,
        sender=actor_user,
        receiver=reciever,
        from_group=actor_user.groups.first(),
        to_group=next_group,
        status_before=old_status,
        status_after=new_status,
        received_at=timezone.now(),
        # remarks=remarks,
        remarks=""
    )
    # ✅ Allow only superadmin to forward the claim


    # Notifications
    # if next_group:
    #     send_group_notification(
    #         next_group.name,
    #         title=f"New Claim Action",
    #         body=f"Claim #{claim.id} moved to {next_group.name}."
    #     )

    return claim
