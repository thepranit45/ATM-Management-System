from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import random


class User(AbstractUser):
    """Custom User model extending Django's AbstractUser"""
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.username} - {self.get_full_name()}"


class Account(models.Model):
    """Bank Account model"""
    ACCOUNT_TYPES = [
        ('SAVINGS', 'Savings Account'),
        ('CHECKING', 'Checking Account'),
        ('CURRENT', 'Current Account'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('BLOCKED', 'Blocked'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    account_number = models.CharField(max_length=20, unique=True, editable=False)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES, default='SAVINGS')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, validators=[MinValueValidator(Decimal('0.00'))])
    pin = models.CharField(max_length=4)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = self.generate_account_number()
        super().save(*args, **kwargs)
    
    def generate_account_number(self):
        """Generate a unique 16-digit account number"""
        while True:
            account_number = ''.join([str(random.randint(0, 9)) for _ in range(16)])
            if not Account.objects.filter(account_number=account_number).exists():
                return account_number
    
    def __str__(self):
        return f"{self.account_number} - {self.user.username} ({self.account_type})"
    
    class Meta:
        ordering = ['-created_at']


class Card(models.Model):
    """ATM Card model"""
    CARD_TYPES = [
        ('DEBIT', 'Debit Card'),
        ('CREDIT', 'Credit Card'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('BLOCKED', 'Blocked'),
        ('EXPIRED', 'Expired'),
    ]
    
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='cards')
    card_number = models.CharField(max_length=16, unique=True, editable=False)
    card_type = models.CharField(max_length=6, choices=CARD_TYPES, default='DEBIT')
    cvv = models.CharField(max_length=3, editable=False)
    expiry_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.card_number:
            self.card_number = self.generate_card_number()
        if not self.cvv:
            self.cvv = ''.join([str(random.randint(0, 9)) for _ in range(3)])
        super().save(*args, **kwargs)
    
    def generate_card_number(self):
        """Generate a unique 16-digit card number"""
        while True:
            card_number = ''.join([str(random.randint(0, 9)) for _ in range(16)])
            if not Card.objects.filter(card_number=card_number).exists():
                return card_number
    
    def __str__(self):
        return f"{self.card_number} - {self.account.account_number}"
    
    class Meta:
        ordering = ['-created_at']


class Transaction(models.Model):
    """Transaction model"""
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('TRANSFER', 'Transfer'),
        ('BALANCE_INQUIRY', 'Balance Inquiry'),
    ]
    
    STATUS_CHOICES = [
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('PENDING', 'Pending'),
    ]
    
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    balance_before = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    recipient_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_transactions')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='SUCCESS')
    transaction_id = models.CharField(max_length=20, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = self.generate_transaction_id()
        super().save(*args, **kwargs)
    
    def generate_transaction_id(self):
        """Generate a unique transaction ID"""
        import time
        timestamp = str(int(time.time()))
        random_num = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        return f"TXN{timestamp}{random_num}"
    
    def __str__(self):
        return f"{self.transaction_id} - {self.transaction_type} - {self.amount}"
    
    class Meta:
        ordering = ['-created_at']
