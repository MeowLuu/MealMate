from django import forms
from .models import UserProfile
from .models import MealEvent
from datetime import datetime
from .models import MealEvent, Payment, UserProfile
from .models import Bill


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'dietary_preferences', 'contact_info'
        ]


class CustomPaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['user', 'amount']


class MealEventForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
   

    class Meta:
        model = MealEvent
        fields = ['title', 'description', 'location', 'latitude', 'longitude',
                  'max_participants', 'privacy']
        widgets = {
            'location': forms.TextInput(attrs={
                'id': 'autocomplete',
                'placeholder': 'Start typing an address...',
                'class': 'mt-1 block w-full border rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'latitude': forms.HiddenInput(attrs={'id': 'latitude'}),
            'longitude': forms.HiddenInput(attrs={'id': 'longitude'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        max_participants = cleaned_data.get('max_participants')
        if max_participants is not None and max_participants <= 0:
            self.add_error('max_participants', 'Participants must be greater than 0.')



    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        
        date = self.cleaned_data['date']
        time = self.cleaned_data['time']
        instance.date_time = datetime.combine(date, time)

        instance.latitude = self.cleaned_data.get('latitude')
        instance.longitude = self.cleaned_data.get('longitude')


        if user:
            instance.host = user
        if commit:
            instance.save()
            instance.participants.add(user)  
        return instance





class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['total_amount', 'is_split_equally']
        widgets = {
            'total_amount': forms.NumberInput(attrs={
                'step': '0.01',
                'class': 'mt-1 block w-full border rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'is_split_equally': forms.CheckboxInput()
        }

    def clean_total_amount(self):
        total_amount = self.cleaned_data.get('total_amount')
        if total_amount is None:
            raise forms.ValidationError("Total amount is required.")
        if total_amount <= 0:
            raise forms.ValidationError("Total amount must be greater than 0.")
        return total_amount

class BillUpdateForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['total_amount']
        widgets = {
            'total_amount': forms.NumberInput(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'step': '0.01'
            })
        }

    def clean_total_amount(self):
        total_amount = self.cleaned_data.get('total_amount')
        if total_amount is None:
            raise forms.ValidationError("Total amount is required.")
        if total_amount <= 0:
            raise forms.ValidationError("Total amount must be greater than 0.")
        return total_amount