from rest_framework import serializers
from .models import Company, Employee, AttendanceRecord

class CompanySerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Company
        fields = ['name', 'address', 'phone', 'email', 'website', 'date_created', 'owner']
        extra_kwargs = {
            'owner': {'read_only': True}
        }

    def get_owner(self, obj):
        return obj.owner.username if obj.owner else None

    def create(self, validated_data):
        owner = self.context['request'].user
        company = Company.objects.create(owner=owner, **validated_data)
        return company
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)
        instance.website = validated_data.get('website', instance.website)
        instance.save()
        return instance
    
    
class EmployeeSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Employee
        fields = '__all__'
    
    def create(self, validated_data):
        company = validated_data.get('company')
        
        # Check if the requesting user owns the company
        print(company.owner)
        if self.context['request'].user != company.owner:
            raise serializers.ValidationError("You do not own this company")
        
        employee = Employee.objects.create(**validated_data)
        return employee
    

class AttendanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecord
        fields = '__all__'
    
    def create(self, validated_data):
        employee = validated_data.get('employee')
        
        # Check if the requesting user owns the employee's company
        if self.context['request'].user != employee.company.owner:
            raise serializers.ValidationError("You do not own this company")
        
        attendance_record = AttendanceRecord.objects.create(**validated_data)
        return attendance_record