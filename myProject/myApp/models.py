from django.db import models

class Designation(models.Model): 
    name = models.CharField(max_length=100,null=True)

    basic_salary = models.DecimalField(max_digits=10,null=True, decimal_places=2)

    hra_percent = models.DecimalField(max_digits=5,null=True, decimal_places=2, default=0)    

    da_percent = models.DecimalField(max_digits=5,null=True, decimal_places=2, default=0) 

    ta_percent = models.DecimalField(max_digits=5,null=True, decimal_places=2, default=0)   

    bonus = models.DecimalField(max_digits=10,null=True, decimal_places=2, default=0)

    def __str__(self):
        return str(self.name)


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
        return self.overtime_hours * 100  # or your overtime rate

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
