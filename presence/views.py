from rest_framework import generics
from .models import Company, Employee, AttendanceRecord
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .permissions import *
from rest_framework.views import APIView
from rest_framework.response import Response

# Companies
class CompanyRegistrationView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsOwnerOrStaff]

# Employees
class EmployeeRegistrationView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

class GetCompanyEmployeesView(generics.ListAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [IsCompanyOwner]

    def get_queryset(self):
        company_id = self.kwargs['company_id']
        return Employee.objects.filter(company__id=company_id)
    
class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsCompanyOwner]

# AttendanceRecord
class AttendanceRecordView(generics.CreateAPIView):
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer
    permission_classes = [IsAttendanceOwner]

class AttendanceDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer
    permission_classes = [IsAttendanceOwner]

class AttendanceListView(APIView):
    permission_classes = [IsAttendanceOwner]

    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if not start_date or not end_date:
            return Response({"detail": "Start date and end date are required"}, status=400)
        company_id = request.query_params.get('company_id')
        employee_id = request.query_params.get('employee_id')
        if not company_id and not employee_id:
            return Response({"detail": "Company ID or Employee ID are required"}, status=400)
        
        if company_id:
            records = AttendanceRecord.objects.filter(employee__company__id=company_id, date__range=[start_date, end_date])
        elif employee_id:
            records = AttendanceRecord.objects.filter(employee__id=employee_id, date__range=[start_date, end_date])
        
        serializer = AttendanceRecordSerializer(records, many=True)
        return Response(serializer.data)