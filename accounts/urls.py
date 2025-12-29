from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-account/', views.create_account, name='create_account'),
    path('switch-account/<int:account_id>/', views.switch_account, name='switch_account'),
    path('verify-pin/', views.verify_pin, name='verify_pin'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('transfer/', views.transfer, name='transfer'),
    path('transaction-history/', views.transaction_history, name='transaction_history'),
    path('transaction/<int:transaction_id>/', views.transaction_receipt, name='transaction_receipt'),
    path('balance/', views.balance_inquiry, name='balance_inquiry'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
]
