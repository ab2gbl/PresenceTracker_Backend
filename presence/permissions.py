from rest_framework import permissions

class IsOwnerOrStaff(permissions.BasePermission):
    """
    Allows update only to owner or stuff.
    """

    def has_object_permission(self, request, view, obj):
       
        if request.method in permissions.SAFE_METHODS and (request.user and request.user.is_authenticated):
          
            return True
        return request.user == obj.owner or request.user.is_staff
    
class IsCompanyOwner(permissions.BasePermission):
    """
    Allows access only to the owner of the company.
    """
    def has_permission(self, request, view):
        """
        Check if user has permission to access the view.
        For GetCompanyEmployeesView, check if user owns the company.
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        # If this is a staff user, allow access
        if request.user.is_staff:
            return True
            
        # For views that have company_id in URL kwargs
        if hasattr(view, 'kwargs') and 'company_id' in view.kwargs:
            from .models import Company
            try:
                company_id = view.kwargs['company_id']
                company = Company.objects.get(id=company_id)
                return request.user == company.owner
            except Company.DoesNotExist:
                return False
        
        return True  # Let has_object_permission handle individual objects
    
    def has_object_permission(self, request, view, obj):
        return request.user == obj.company.owner or request.user.is_staff
    
class IsAttendanceOwner(permissions.BasePermission):
    """
    Allows access only to the owner of the attendance record's company.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # If this is a staff user, allow access
        if request.user.is_staff:
            return True
        
        # For views that have attendance record in URL kwargs (detail views)
        if hasattr(view, 'kwargs') and 'pk' in view.kwargs:
            from .models import AttendanceRecord
            try:
                attendance_record = AttendanceRecord.objects.get(pk=view.kwargs['pk'])
                return request.user == attendance_record.employee.company.owner
            except AttendanceRecord.DoesNotExist:
                return False
        
        # For AttendanceListView that uses query parameters
        if hasattr(request, 'query_params'):
            company_id = request.query_params.get('company_id')
            employee_id = request.query_params.get('employee_id')
            
            if company_id:
                # Check if user owns the company
                from .models import Company
                try:
                    company = Company.objects.get(id=company_id)
                    return request.user == company.owner
                except Company.DoesNotExist:
                    return False
            
            elif employee_id:
                # Check if user owns the company that the employee works for
                from .models import Employee
                try:
                    employee = Employee.objects.get(id=employee_id)
                    return request.user == employee.company.owner
                except Employee.DoesNotExist:
                    return False

        return True  # Let has_object_permission handle individual objects
    
    def has_object_permission(self, request, view, obj):
        
        return request.user == obj.employee.company.owner or request.user.is_staff
  