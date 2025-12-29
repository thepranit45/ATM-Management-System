from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Account, Transaction
from decimal import Decimal


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    first_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    phone_number = forms.CharField(
        max_length=15, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
    )
    date_of_birth = forms.DateField(
        required=True, 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}),
        required=True
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'address', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})


class AccountCreationForm(forms.ModelForm):
    pin = forms.CharField(
        max_length=4, 
        min_length=4, 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '4-digit PIN'}), 
        help_text="Enter a 4-digit PIN"
    )
    confirm_pin = forms.CharField(
        max_length=4, 
        min_length=4, 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm PIN'}), 
        label="Confirm PIN"
    )
    
    class Meta:
        model = Account
        fields = ['account_type', 'pin']
        widgets = {
            'account_type': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account_type'].widget.attrs.update({'class': 'form-control'})
    
    def clean(self):
        cleaned_data = super().clean()
        pin = cleaned_data.get('pin')
        confirm_pin = cleaned_data.get('confirm_pin')
        
        if pin and confirm_pin and pin != confirm_pin:
            raise forms.ValidationError("PINs do not match")
        
        if pin and not pin.isdigit():
            raise forms.ValidationError("PIN must contain only digits")
        
        return cleaned_data


class PINVerificationForm(forms.Form):
    pin = forms.CharField(
        max_length=4, 
        min_length=4, 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '4-digit PIN'}), 
        label="Enter PIN"
    )


class DepositForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        min_value=Decimal('0.01'), 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter amount'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional description'}), 
        required=False
    )


class WithdrawalForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        min_value=Decimal('0.01'),
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter amount'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional description'}), 
        required=False
    )


class TransferForm(forms.Form):
    recipient_account = forms.CharField(
        max_length=20, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter recipient account number'})
    )
    amount = forms.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        min_value=Decimal('0.01'),
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter amount'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional description'}), 
        required=False
    )
    
    def clean_recipient_account(self):
        account_number = self.cleaned_data['recipient_account']
        try:
            Account.objects.get(account_number=account_number, status='ACTIVE')
        except Account.DoesNotExist:
            raise forms.ValidationError("Invalid or inactive account number")
        return account_number
