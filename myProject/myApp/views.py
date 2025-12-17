from django.shortcuts import render, redirect
from .models import Employee, Designation 

def add_employee(request):
    designations = Designation.objects.all()

    if request.method == 'POST':
        try:
            designation_id = request.POST.get('designation')
            if not designation_id:
                raise ValueError("Designation is required")

            designation = Designation.objects.get(id=designation_id)

            overtime_hours_str = request.POST.get('overtime_hours', '0')
            overtime_hours = int(overtime_hours_str) if overtime_hours_str.isdigit() else 0

            Employee.objects.create(
                name=request.POST.get('name'),
                contact=request.POST.get('contact'),
                overtime_hours=overtime_hours,
                designation=designation
            )
            return redirect('table')  # Redirect after saving
        except (ValueError, Designation.DoesNotExist):
            # Handle errors, perhaps add error message
            pass  # For now, just pass, can add messages later

    context = {
        'designations': designations
    }
    return render(request, "employee_form.html", context)

def salary_report(request):
    employees = Employee.objects.all()
    designations = Designation.objects.all()
    # Filter
    designation_filter = request.GET.get("designation")
    if designation_filter:
        employees = employees.filter(designation__id=designation_filter)

    context = {
        'employees': employees,
        'designations': designations,
    }

    return render(request, "salary_report.html", context)

 
 