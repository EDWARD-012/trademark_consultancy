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