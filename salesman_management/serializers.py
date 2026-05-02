from rest_framework import serializers
from django.db import transaction

from accounts.models import CustomUser

from .models import (
    SalesEmployee
)

class SalesEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesEmployee
        fields = '__all__' 


class SalesEmployeeCreateSerializer(
    serializers.ModelSerializer
):
    full_name = serializers.CharField(
        write_only=True
    )

    email = serializers.EmailField(
        write_only=True
    )

    password = serializers.CharField(
        write_only=True
    )

    date_of_birth = serializers.DateField(
        source='dob',
        required=False,
        allow_null=True
    )


    class Meta:
        model = SalesEmployee

        fields = [
            'full_name',
            'email',
            'password',

            'employee_code',
            'phone',

            'father_name',
            'mother_name',
            'date_of_birth',

            'channel',
            'department',
            'designation',
            'branch',
            'role',

            'manager',
            'line_manager',

            'status',
            'joining_date'
        ]


    def validate_email(self,value):
        if CustomUser.objects.filter(
            email=value
        ).exists():
            raise serializers.ValidationError(
                "Email already exists"
            )
        return value


    @transaction.atomic
    def create(self,validated_data):

        full_name = validated_data.pop(
            'full_name'
        )

        email = validated_data.pop(
            'email'
        )

        password = validated_data.pop(
            'password'
        )

        user = CustomUser.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=full_name
        )

        employee = SalesEmployee.objects.create(
            user=user,
            employee_name=full_name,
            **validated_data
        )

        return employee