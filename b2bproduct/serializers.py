from .models import Product,Policy
from rest_framework import serializers
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_name(self, value):
        if not value:
            return None
        if self.instance:
            # Exclude current instance from uniqueness check
            if Product.objects.filter(name=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("Product is already in use.")
        else:
            # If creating, just check if it exists
            if Product.objects.filter(name=value).exists():
                raise serializers.ValidationError("Product is already in use.")
        return value

class PolicyListSerializer(serializers.ModelSerializer):
    product=ProductSerializer()
    class Meta:
        model = Policy
        fields = '__all__'

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = '__all__'

    def validate_name(self, value):
        if not value:
            return None
        if self.instance:
            # Exclude current instance from uniqueness check
            if Policy.objects.filter(name=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("Policy is already in use.")
        else:
            # If creating, just check if it exists
            if Policy.objects.filter(name=value).exists():
                raise serializers.ValidationError("Policy is already in use.")
        return value