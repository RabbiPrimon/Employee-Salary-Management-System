# Employee Salary Management System

A Django-based web application for managing employee data and calculating salaries based on designations and allowances.

## Features

- **Employee Management**: Store and manage employee details including name, contact, overtime hours, and designation.
- **Designation-Based Salaries**: Link employees to designations with predefined salary components (basic salary, HRA, DA, TA, bonus).
- **Automatic Salary Calculations**:
  - HRA = (hra_percent / 100) × basic_salary
  - DA = (da_percent / 100) × basic_salary
  - TA = (ta_percent / 100) × basic_salary
  - Overtime = overtime_hours × 100
  - Gross Salary = Basic Salary + HRA + DA + TA + Bonus + Overtime
- **Salary Report**: View a comprehensive table of all employees with their salary breakdowns.
- **Filtering**: Filter employees by designation in the salary report.
- **Responsive UI**: Bootstrap-styled interface with navigation.

## Project Structure

```
Employee Salary Management System/
├── myProject/                 # Main Django project directory
│   ├── myProject/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py        # Django settings
│   │   ├── urls.py            # Main URL configuration
│   │   ├── wsgi.py
│   ├── myApp/                 # Django app
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py          # Database models
│   │   ├── tests.py
│   │   ├── urls.py            # App URL configuration
│   │   ├── views.py           # Views and logic
│   │   └── migrations/        # Database migrations
│   ├── templates/             # HTML templates
│   │   ├── base.html          # Base template
│   │   ├── employee_form.html # Add employee form
│   │   ├── navbar.html        # Navigation bar
│   │   └── salary_report.html # Salary report table
│   ├── db.sqlite3             # SQLite database
│   └── manage.py              # Django management script
└── README.md                  # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Django 5.2.6
- Virtual environment (recommended)

### Setup

1. **Clone or download the project**:
   ```
   cd /path/to/Employee Salary Management System
   ```

2. **Create and activate a virtual environment**:
   ```
   python -m venv myEnv
   myEnv\Scripts\activate  # On Windows
   # source myEnv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**:
   ```
   pip install django
   ```

4. **Navigate to the project directory**:
   ```
   cd myProject
   ```

5. **Run migrations**:
   ```
   python manage.py migrate
   ```

6. **Create a superuser (optional, for admin access)**:
   ```
   python manage.py createsuperuser
   ```

7. **Run the development server**:
   ```
   python manage.py runserver
   ```

8. **Access the application**:
   - Salary Report: http://127.0.0.1:8000/
   - Add Employee: http://127.0.0.1:8000/form/
   - Admin (if superuser created): http://127.0.0.1:8000/admin/

## Usage

### Adding Designations

Before adding employees, create designations via Django admin or programmatically:

```python
from myApp.models import Designation

# Create a sample designation
designation = Designation.objects.create(
    name="Software Engineer",
    basic_salary=50000,
    hra_percent=20,
    da_percent=10,
    ta_percent=5,
    bonus=5000
)
```

### Adding Employees

1. Navigate to http://127.0.0.1:8000/form/
2. Fill in the form:
   - Name: Employee's full name
   - Contact: Contact information
   - Overtime Hours: Number of overtime hours worked
   - Designation: Select from available designations
3. Click "Submit"

### Viewing Salary Report

1. Navigate to http://127.0.0.0.1:8000/ (root URL)
2. View the table showing all employees with their salary components
3. Use the designation filter to narrow down results

## Models

### Designation Model

```python
class Designation(models.Model):
    name = models.CharField(max_length=100, null=True)
    basic_salary = models.DecimalField(max_digits=10, null=True, decimal_places=2)
    hra_percent = models.DecimalField(max_digits=5, null=True, decimal_places=2, default=0)
    da_percent = models.DecimalField(max_digits=5, null=True, decimal_places=2, default=0)
    ta_percent = models.DecimalField(max_digits=5, null=True, decimal_places=2, default=0)
    bonus = models.DecimalField(max_digits=10, null=True, decimal_places=2, default=0)

    def __str__(self):
        return str(self.name)
```

### Employee Model

```python
class Employee(models.Model):
    name = models.CharField(max_length=100, null=True)
    overtime_hours = models.IntegerField(default=0, null=True)
    contact = models.CharField(max_length=100, null=True)
    designation = models.ForeignKey("Designation", on_delete=models.PROTECT, null=True)

    def hra(self):
        if self.designation and self.designation.hra_percent and self.designation.basic_salary:
            return (self.designation.hra_percent / 100) * self.designation.basic_salary
        return 0

    def da(self):
        if self.designation and self.designation.da_percent and self.designation.basic_salary:
            return (self.designation.da_percent / 100) * self.designation.basic_salary
        return 0

    def ta(self):
        if self.designation and self.designation.ta_percent and self.designation.basic_salary:
            return (self.designation.ta_percent / 100) * self.designation.basic_salary
        return 0

    def overtime(self):
        return self.overtime_hours * 100

    def gross_salary(self):
        if not self.designation:
            return 0
        return (
            self.designation.basic_salary
            + self.hra()
            + self.da()
            + self.ta()
            + (self.designation.bonus or 0)
            + self.overtime()
        )

    def __str__(self):
        return str(self.name)
```

## Views

### add_employee(request)

Handles employee creation form. Validates input, creates Employee instance, and redirects to salary report.

### salary_report(request)

Displays all employees in a table format. Supports filtering by designation via GET parameter.

## Templates

- **base.html**: Base template with Bootstrap CSS/JS, navigation bar, and block structure.
- **employee_form.html**: Form for adding new employees.
- **salary_report.html**: Table displaying employee salary information with filter dropdown.
- **navbar.html**: Navigation bar with links to add employee and salary report.

## URLs

### myProject/urls.py

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myApp.urls')),
]
```

### myApp/urls.py

```python
urlpatterns = [
    path('form/', add_employee, name='form'),
    path('', salary_report, name='table'),
]
```

## Requirements

- Django==5.2.6
- Python 3.8+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues, please open an issue on the project's repository or contact the development team.
email- rabbiprimon00000@gmail.com
