from django.contrib import admin
from .models import TrademarkApplication

@admin.register(TrademarkApplication)
class TrademarkAdmin(admin.ModelAdmin):
    list_display = ('application_number', 'trademark_name', 'applicant_name', 'status', 'filing_date')
    search_fields = ('application_number', 'trademark_name', 'applicant_name')
    list_filter = ('status', 'trademark_class')
    ordering = ('-updated_at',)