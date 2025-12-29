from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction as db_transaction
from django.http import JsonResponse
from decimal import Decimal
from .models import User, Account, Transaction, Card
from .forms import (UserRegistrationForm, AccountCreationForm, PINVerificationForm,
                    DepositForm, WithdrawalForm, TransferForm)
from datetime import datetime, timedelta


def home(request):
    """Home page view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Please create an account.')
            return redirect('create_account')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'registration/login.html')


@login_required
def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def create_account(request):
    """Create a new bank account"""
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            
            # Create a card for the account
            expiry_date = datetime.now() + timedelta(days=365*3)  # 3 years validity
            Card.objects.create(
                account=account,
                expiry_date=expiry_date.date()
            )
            
            messages.success(request, f'Account created successfully! Account Number: {account.account_number}')
            return redirect('dashboard')
    else:
        form = AccountCreationForm()
    
    return render(request, 'accounts/create_account.html', {'form': form})


@login_required
def dashboard(request):
    """Dashboard view"""
    accounts = Account.objects.filter(user=request.user)
    
    # Get the active account from session or use the first account
    account_id = request.session.get('active_account_id')
    if account_id:
        try:
            active_account = Account.objects.get(id=account_id, user=request.user)
        except Account.DoesNotExist:
            active_account = accounts.first() if accounts.exists() else None
    else:
        active_account = accounts.first() if accounts.exists() else None
    
    # Store active account in session
    if active_account:
        request.session['active_account_id'] = active_account.id
    
    # Get recent transactions
    recent_transactions = []
    if active_account:
        recent_transactions = Transaction.objects.filter(account=active_account)[:10]
    
    context = {
        'accounts': accounts,
        'active_account': active_account,
        'recent_transactions': recent_transactions,
    }
    
    return render(request, 'accounts/dashboard.html', context)


@login_required
def switch_account(request, account_id):
    """Switch active account"""
    account = get_object_or_404(Account, id=account_id, user=request.user)
    request.session['active_account_id'] = account.id
    messages.success(request, f'Switched to account: {account.account_number}')
    return redirect('dashboard')


@login_required
def verify_pin(request):
    """Verify PIN before transactions"""
    if request.method == 'POST':
        form = PINVerificationForm(request.POST)
        if form.is_valid():
            pin = form.cleaned_data['pin']
            account_id = request.session.get('active_account_id')
            
            if account_id:
                account = get_object_or_404(Account, id=account_id, user=request.user)
                if account.pin == pin:
                    request.session['pin_verified'] = True
                    request.session['pin_verified_at'] = datetime.now().isoformat()
                    next_url = request.GET.get('next', 'dashboard')
                    return redirect(next_url)
                else:
                    messages.error(request, 'Invalid PIN. Please try again.')
            else:
                messages.error(request, 'No active account found.')
    else:
        form = PINVerificationForm()
    
    return render(request, 'accounts/verify_pin.html', {'form': form})


def check_pin_verification(request):
    """Check if PIN is verified and not expired"""
    if not request.session.get('pin_verified'):
        return False
    
    verified_at = request.session.get('pin_verified_at')
    if verified_at:
        verified_time = datetime.fromisoformat(verified_at)
        if datetime.now() - verified_time > timedelta(minutes=10):  # PIN valid for 10 minutes
            request.session['pin_verified'] = False
            return False
    
    return True


@login_required
def deposit(request):
    """Deposit money"""
    if not check_pin_verification(request):
        return redirect(f'/verify-pin/?next={request.path}')
    
    account_id = request.session.get('active_account_id')
    account = get_object_or_404(Account, id=account_id, user=request.user)
    
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            description = form.cleaned_data.get('description', 'Deposit')
            
            with db_transaction.atomic():
                balance_before = account.balance
                account.balance += amount
                account.save()
                
                Transaction.objects.create(
                    account=account,
                    transaction_type='DEPOSIT',
                    amount=amount,
                    balance_before=balance_before,
                    balance_after=account.balance,
                    description=description,
                    status='SUCCESS'
                )
            
            messages.success(request, f'Successfully deposited ₹{amount}. New balance: ₹{account.balance}')
            return redirect('dashboard')
    else:
        form = DepositForm()
    
    return render(request, 'accounts/deposit.html', {'form': form, 'account': account})


@login_required
def withdraw(request):
    """Withdraw money"""
    if not check_pin_verification(request):
        return redirect(f'/verify-pin/?next={request.path}')
    
    account_id = request.session.get('active_account_id')
    account = get_object_or_404(Account, id=account_id, user=request.user)
    
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            description = form.cleaned_data.get('description', 'Withdrawal')
            
            if amount > account.balance:
                messages.error(request, 'Insufficient balance.')
            else:
                with db_transaction.atomic():
                    balance_before = account.balance
                    account.balance -= amount
                    account.save()
                    
                    Transaction.objects.create(
                        account=account,
                        transaction_type='WITHDRAWAL',
                        amount=amount,
                        balance_before=balance_before,
                        balance_after=account.balance,
                        description=description,
                        status='SUCCESS'
                    )
                
                messages.success(request, f'Successfully withdrew ₹{amount}. New balance: ₹{account.balance}')
                return redirect('dashboard')
    else:
        form = WithdrawalForm()
    
    return render(request, 'accounts/withdraw.html', {'form': form, 'account': account})


@login_required
def transfer(request):
    """Transfer money to another account"""
    if not check_pin_verification(request):
        return redirect(f'/verify-pin/?next={request.path}')
    
    account_id = request.session.get('active_account_id')
    account = get_object_or_404(Account, id=account_id, user=request.user)
    
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            recipient_account_number = form.cleaned_data['recipient_account']
            amount = form.cleaned_data['amount']
            description = form.cleaned_data.get('description', 'Transfer')
            
            recipient_account = Account.objects.get(account_number=recipient_account_number)
            
            if recipient_account.id == account.id:
                messages.error(request, 'Cannot transfer to the same account.')
            elif amount > account.balance:
                messages.error(request, 'Insufficient balance.')
            else:
                with db_transaction.atomic():
                    # Debit sender
                    sender_balance_before = account.balance
                    account.balance -= amount
                    account.save()
                    
                    Transaction.objects.create(
                        account=account,
                        transaction_type='TRANSFER',
                        amount=amount,
                        balance_before=sender_balance_before,
                        balance_after=account.balance,
                        description=f'Transfer to {recipient_account_number}: {description}',
                        recipient_account=recipient_account,
                        status='SUCCESS'
                    )
                    
                    # Credit recipient
                    recipient_balance_before = recipient_account.balance
                    recipient_account.balance += amount
                    recipient_account.save()
                    
                    Transaction.objects.create(
                        account=recipient_account,
                        transaction_type='TRANSFER',
                        amount=amount,
                        balance_before=recipient_balance_before,
                        balance_after=recipient_account.balance,
                        description=f'Transfer from {account.account_number}: {description}',
                        status='SUCCESS'
                    )
                
                messages.success(request, f'Successfully transferred ₹{amount} to {recipient_account_number}')
                return redirect('dashboard')
    else:
        form = TransferForm()
    
    return render(request, 'accounts/transfer.html', {'form': form, 'account': account})


@login_required
def transaction_history(request):
    """View transaction history"""
    account_id = request.session.get('active_account_id')
    account = get_object_or_404(Account, id=account_id, user=request.user)
    
    transactions = Transaction.objects.filter(account=account)
    
    # Filter by transaction type
    transaction_type = request.GET.get('type')
    if transaction_type:
        transactions = transactions.filter(transaction_type=transaction_type)
    
    context = {
        'account': account,
        'transactions': transactions,
    }
    
    return render(request, 'accounts/transaction_history.html', context)


@login_required
def balance_inquiry(request):
    """Check account balance"""
    account_id = request.session.get('active_account_id')
    account = get_object_or_404(Account, id=account_id, user=request.user)
    
    # Create balance inquiry transaction
    Transaction.objects.create(
        account=account,
        transaction_type='BALANCE_INQUIRY',
        amount=Decimal('0.00'),
        balance_before=account.balance,
        balance_after=account.balance,
        description='Balance Inquiry',
        status='SUCCESS'
    )
    
    return render(request, 'accounts/balance_inquiry.html', {'account': account})


@login_required
def profile(request):
    """User profile view"""
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'accounts/profile.html', {'accounts': accounts})


@login_required
def edit_profile(request):
    """Edit user profile"""
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.email = request.POST.get('email', request.user.email)
        request.user.phone_number = request.POST.get('phone_number', request.user.phone_number)
        request.user.address = request.POST.get('address', request.user.address)
        request.user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'accounts/edit_profile.html')


@login_required
def change_password(request):
    """Change user password"""
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
        elif new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
        elif len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        else:
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, 'Password changed successfully! Please login again.')
            return redirect('login')
    
    return render(request, 'accounts/change_password.html')


@login_required
def transaction_receipt(request, transaction_id):
    """View transaction receipt"""
    transaction = get_object_or_404(Transaction, id=transaction_id, account__user=request.user)
    return render(request, 'accounts/transaction_receipt.html', {'transaction': transaction})
