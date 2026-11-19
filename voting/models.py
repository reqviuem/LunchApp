from django.db import models
from employees.models import Employee
from restaurants.models import Menu


class Vote(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='votes')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='votes')
    date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['employee', 'date'], name='unique_vote_per_employee_per_day')
        ]

    def __str__(self):
        return f"{self.employee.name} voted for {self.menu}"
