from django import forms

class StatusCheckForm(forms.Form):
    application_no = forms.CharField(
        max_length=20, 
        label="Trademark Application No.",
        widget=forms.TextInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5',
            'placeholder': 'Enter Application No. (e.g., 5678901)'
        })
    )

from core.models import TrademarkApplication

class NewTrademarkForm(forms.ModelForm):
    class Meta:
        model = TrademarkApplication
        # Fields list mein naye fields add karo
        fields = ['applicant_type', 'applicant_name', 'company_name', 'trademark_name', 'trademark_class']
        
        widgets = {
            'applicant_type': forms.Select(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary py-3 px-4'}),
            'applicant_name': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary py-3 px-4', 'placeholder': 'Full Name of Applicant'}),
            'company_name': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary py-3 px-4', 'placeholder': 'Company Name (Optional for Individuals)'}),
            'trademark_name': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary py-3 px-4', 'placeholder': 'e.g. Nike, Tata'}),
            'trademark_class': forms.NumberInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary py-3 px-4', 'placeholder': 'e.g. 35'}),
        }