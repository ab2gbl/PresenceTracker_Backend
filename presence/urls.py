from django.urls import path

from .views import *

urlpatterns = [
    path('companies/', CompanyRegistrationView.as_view(), name='company_registration'),
    path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company_detail'),
    path('employees/', EmployeeRegistrationView.as_view(), name='employee_registration'),
    path('companies/<int:company_id>/employees/', GetCompanyEmployeesView.as_view(), name='get_company_employees'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee_detail'),
    path('attendance/', AttendanceRecordView.as_view(), name='attendance_record'),
    path('attendance/<int:pk>/', AttendanceDetailsView.as_view(), name='attendance_details'),
    path('attendance/list/', AttendanceListView.as_view(), name='attendance_list'),
    #path('presence/', include('presence.urls')),


]
