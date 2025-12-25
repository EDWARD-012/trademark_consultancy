from django.contrib import admin
from .models import Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'service', 'created_at')
    list_filter = ('service', 'created_at')