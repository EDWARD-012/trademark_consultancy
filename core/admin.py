from django.contrib import admin
from .models import Service, Lead, TrademarkApplication, ApplicationDocument

# 1. Documents ko Application ke andar dikhane ke liye Inline
class DocumentInline(admin.TabularInline):
    model = ApplicationDocument
    extra = 0 # Extra empty fields nahi dikhenge
    readonly_fields = ('uploaded_at',)

# 2. Trademark Application Admin
@admin.register(TrademarkApplication)
class TrademarkApplicationAdmin(admin.ModelAdmin):
    list_display = ('application_number', 'applicant_name', 'trademark_name', 'status', 'filing_date')
    list_filter = ('status', 'trademark_class')
    search_fields = ('application_number', 'trademark_name', 'applicant_name')
    inlines = [DocumentInline] # 🔥 Ye magic line hai (Docs yahi dikhenge)

# 3. Lead/Enquiry Admin
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'service_interested', 'created_at')
    list_filter = ('service_interested', 'created_at')
    search_fields = ('name', 'phone', 'email')

# 4. Service Admin
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price_estimate', 'is_active')
    list_filter = ('category', 'is_active')
    prepopulated_fields = {'slug': ('title',)}