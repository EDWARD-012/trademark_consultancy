from django import forms
# 🔥 CHANGE IS HERE: 'Lead' ab core.models se aayega, .models se nahi
from core.models import TrademarkApplication, Service, Lead , ApplicationDocument

# --- 1. Status Check Form ---
class StatusCheckForm(forms.Form):
    application_no = forms.CharField(
        max_length=20, 
        label="Trademark Application No.",
        widget=forms.TextInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5',
            'placeholder': 'Enter Application No. (e.g., 5678901)'
        })
    )

# --- 2. New Application Form ---
class NewTrademarkForm(forms.ModelForm):
    class Meta:
        model = TrademarkApplication
        fields = ['service_type', 'applicant_type', 'applicant_name', 'company_name', 'trademark_name', 'trademark_class']
        
        widgets = {
            'applicant_type': forms.Select(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary py-3 px-4'}),
            'applicant_name': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary py-3 px-4', 'placeholder': 'Full Name of Applicant'}),
            'company_name': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary py-3 px-4', 'placeholder': 'Company Name (Optional for Individuals)'}),
            'trademark_name': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary py-3 px-4', 'placeholder': 'Brand Name / Title of Work'}),
            'trademark_class': forms.NumberInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary py-3 px-4', 'placeholder': 'e.g. 35 (Enter 0 if not applicable)'}),
        }

    def __init__(self, *args, **kwargs):
        super(NewTrademarkForm, self).__init__(*args, **kwargs)

        if self.initial.get('service_type'):
            self.fields['service_type'].widget = forms.TextInput(attrs={
                'class': 'w-full rounded-md border-gray-300 bg-gray-200 shadow-sm focus:border-primary focus:ring-primary py-3 px-4 cursor-not-allowed font-bold text-gray-700',
                'readonly': 'readonly'
            })
        else:
            services = Service.objects.filter(is_active=True).values_list('title', 'title')
            self.fields['service_type'] = forms.ChoiceField(
                choices=[('', 'Select a Service...')] + list(services),
                widget=forms.Select(attrs={
                    'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary py-3 px-4'
                })
            )

# --- 3. Lead Form ---
class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'phone', 'email', 'service_interested', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-white/5 backdrop-blur-md border border-white/10 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-lovable-purple/60 transition', 'placeholder': 'Your Name'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-white/5 backdrop-blur-md border border-white/10 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-lovable-purple/60 transition', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-white/5 backdrop-blur-md border border-white/10 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-lovable-purple/60 transition', 'placeholder': 'Email Address'}),
            'service_interested': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-white/5 backdrop-blur-md border border-white/10 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-lovable-purple/60 transition', 'placeholder': 'Service (e.g. Trademark)'}),
            'message': forms.Textarea(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-white/5 backdrop-blur-md border border-white/10 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-lovable-purple/60 transition', 'placeholder': 'Tell us about your requirement...', 'rows': 4}),
        }

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = ApplicationDocument
        fields = ['doc_type', 'file']
        
        widgets = {
            'document_name': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-3 rounded-xl bg-gray/5 backdrop-blur-md border border-white/10 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-lovable-purple/60 transition',
                'placeholder': 'Document Name (e.g. PAN Card, Logo)'
            }),
            'file': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-primary file:text-white hover:file:bg-secondary cursor-pointer'
            })
        }