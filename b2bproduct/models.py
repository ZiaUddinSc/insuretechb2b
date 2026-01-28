import os
import uuid
from django.conf import settings
from django.db import models
# Create your models here.

"""Common Use for all models"""
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


"""Organization Logo"""
def organization_logo_file_path(instance, filename):
    """Generate file path for new image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('organization_logo/', filename)


"""Trade License"""
def trade_license_file_path(instance, filename):
    """Generate file path for new image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('trade_license/', filename)


"""Tin Number"""
def tin_number_file_path(instance, filename):
    """Generate file path for new image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('tin_number/', filename)


"""NID Number"""
def nid_number_file_path(instance, filename):
    """Generate file path for new image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('nid_number/', filename)


ACTIVE=1
CLOSE=2
POLICY_TYPE = {
        ACTIVE: "Active",
        CLOSE: "Close",
        
    }

class OrganizationType(AuditBaseModel):
    type_name = models.CharField(max_length=255,blank=True,null=True)
    summary = models.TextField(blank=True,null=True)

    def __str__(self):
        return f"{self.type_name}"
    
    class Meta:
        db_table = 'organization_type'
        ordering = ['-id']  # Orders by id in descending order




class PolicyAssign(AuditBaseModel):
    policy = models.CharField(max_length=255,choices=POLICY_TYPE,blank=True,null=True)
    b2b_organization=models.CharField(max_length=255,blank=True,null=True)


    def __str__(self):
        return f"{self.policy}"
    

    class Meta:
        db_table = 'policy_assign'
        ordering = ['-id']  # Orders by id in descending order


class ProductType(AuditBaseModel):
    type_name = models.CharField(max_length=255,blank=True,null=True)
    description = models.TextField(blank=True,null=True)

    def __str__(self):
        return f"{self.type_name}"
    
    class Meta:
        db_table = 'product_type'
        ordering = ['-id']  # Orders by id in descending order



class Product(AuditBaseModel):
    name = models.CharField(max_length=255,blank=True,null=True)
 

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        db_table = 'product'
        ordering = ['-id']  # Orders by id in descending order
        

class Policy(AuditBaseModel):
    product =  models.ForeignKey(Product,blank=True,null=True, on_delete=models.CASCADE,related_name='products')
    name = models.CharField(max_length=255,blank=True,null=True)
 

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        db_table = 'policy'
        ordering = ['-id']  # Orders by id in descending order        





