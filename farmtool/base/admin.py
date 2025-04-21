from django.contrib import admin
from .models import FarmTool, ToolTransaction, MaintenanceSchedule

@admin.register(FarmTool)
class FarmToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'available')
    search_fields = ('name',)

@admin.register(ToolTransaction)
class ToolTransactionAdmin(admin.ModelAdmin):
    list_display = ('tool', 'user', 'check_out_date', 'check_in_date', 'status')
    list_filter = ('status',)
    search_fields = ('tool__name', 'user__username')

@admin.register(MaintenanceSchedule)
class MaintenanceScheduleAdmin(admin.ModelAdmin):
    list_display = ('tool', 'scheduled_date', 'status')
    list_filter = ('status',)
    search_fields = ('tool__name', 'notes')


# Register your models here.
