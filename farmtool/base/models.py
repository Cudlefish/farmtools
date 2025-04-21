from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class FarmTool(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    available = models.BooleanField(default=True)
    tool_image = models.ImageField(null='True',blank=True, upload_to='images')

    def __str__(self):
        return self.name
    
class ToolTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tool = models.ForeignKey(FarmTool, on_delete=models.CASCADE)
    check_out_date = models.DateTimeField(null=True, blank=True)
    check_in_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=100, choices=[('Checked Out', 'Checked Out'), ('Checked In', 'Checked In')])
    transaction_id = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return f"{self.user.username} - {self.tool.name} ({self.status})"
    
class MaintenanceSchedule(models.Model):
    tool = models.ForeignKey(FarmTool, on_delete=models.CASCADE)
    scheduled_date = models.DateField()
    status = models.CharField(
        max_length=15,
        choices=[('Pending', 'Pending'), ('Completed', 'Completed')],
        default='Pending'
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.tool.name} - {self.scheduled_date} ({self.status})"
