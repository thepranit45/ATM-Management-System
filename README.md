# ATM Management System

A modern ATM (Automated Teller Machine) Management System built with Django, Python, SQLite, HTML5, CSS3, and JavaScript. This application provides a complete banking experience with secure authentication, transaction management, and an intuitive user interface.

## Features

### User Management
- **User Registration**: Create new user accounts with personal details
- **User Authentication**: Secure login/logout system
- **User Profile**: View and manage personal information
- **Multiple Accounts**: Support for multiple bank accounts per user

### Account Management
- **Create Accounts**: Open new bank accounts (Savings, Checking, Current)
- **Account Types**: Different account types with unique features
- **PIN Security**: 4-digit PIN protection for transactions
- **Account Status**: Active, Inactive, and Blocked status management
- **Auto-generated Account Numbers**: Unique 16-digit account numbers
- **Card Management**: Automatic ATM card generation with expiry dates

### Transaction Operations
- **Deposit**: Add money to your account
- **Withdrawal**: Withdraw money with balance validation
- **Transfer**: Send money to other accounts instantly
- **Balance Inquiry**: Check current account balance
- **Transaction History**: View complete transaction records with filters

### Security Features
- **PIN Verification**: Required before any transaction
- **Session Management**: Auto-logout after inactivity
- **PIN Timeout**: PIN verification expires after 10 minutes
- **Secure Password Storage**: Django's built-in password hashing
- **CSRF Protection**: Cross-Site Request Forgery protection

### Modern UI/UX
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern Card-Based Layout**: Clean and intuitive interface
- **Real-time Alerts**: Success and error messages
- **Smooth Animations**: CSS animations for better UX
- **Dashboard**: Overview of accounts and recent transactions
- **Quick Actions**: Easy access to common operations

## Technology Stack

### Backend
- **Framework**: Django 5.0
- **Language**: Python 3.8+
- **Database**: SQLite (default, easily switchable to PostgreSQL/MySQL)
- **ORM**: Django ORM

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS Grid and Flexbox
- **JavaScript**: Vanilla JS for interactivity
- **Responsive**: Mobile-first design approach

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step-by-Step Setup

1. **Clone or Navigate to the Project Directory**
   ```bash
   cd d:\ATM
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Apply Database Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a Superuser (Admin)**
   ```bash
   python manage.py createsuperuser
   ```
   
   Follow the prompts to create an admin account.

7. **Collect Static Files (if needed)**
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

9. **Access the Application**
   
   Open your browser and navigate to:
   - **Main Site**: http://127.0.0.1:8000/
   - **Admin Panel**: http://127.0.0.1:8000/admin/

## Usage Guide

### Getting Started

1. **Register a New Account**
   - Navigate to the homepage
   - Click "Register" and fill in your details
   - Submit the registration form

2. **Create a Bank Account**
   - After registration, you'll be prompted to create a bank account
   - Choose account type (Savings, Checking, or Current)
   - Set a 4-digit PIN for security
   - Your account will be created with a unique account number

3. **Access Dashboard**
   - After login, you'll see your dashboard
   - View account balance and recent transactions
   - Access quick action buttons for operations

### Performing Transactions

#### Making a Deposit
1. Click "Deposit" from the dashboard or navigation menu
2. Enter PIN for verification
3. Enter the deposit amount
4. Add optional description
5. Confirm the transaction

#### Withdrawing Money
1. Click "Withdraw" from the menu
2. Verify your PIN
3. Enter the withdrawal amount (must not exceed balance)
4. Submit the transaction

#### Transferring Money
1. Click "Transfer"
2. Enter PIN verification
3. Enter recipient's account number
4. Enter transfer amount
5. Add optional description
6. Confirm transfer

#### Checking Balance
1. Click "Balance" from quick actions
2. View current balance and account details

#### Viewing Transaction History
1. Navigate to "History" in the menu
2. Filter transactions by type if needed
3. View detailed transaction records

### Admin Panel

Access the admin panel at http://127.0.0.1:8000/admin/ to:
- Manage users and accounts
- View all transactions
- Monitor system activity
- Update account statuses
- Generate reports

## Project Structure

```
ATM/
├── atm_system/              # Main project configuration
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── accounts/                # Main application
│   ├── migrations/          # Database migrations
│   ├── __init__.py
│   ├── admin.py             # Admin panel configuration
│   ├── apps.py
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── urls.py              # App URL routing
│   └── forms.py             # Form definitions
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   ├── home.html            # Homepage
│   ├── registration/        # Auth templates
│   │   ├── login.html
│   │   └── register.html
│   └── accounts/            # Account templates
│       ├── dashboard.html
│       ├── deposit.html
│       ├── withdraw.html
│       ├── transfer.html
│       ├── balance_inquiry.html
│       ├── transaction_history.html
│       └── profile.html
├── static/                  # Static files
│   ├── css/
│   │   └── style.css        # Main stylesheet
│   └── js/
│       └── script.js        # JavaScript functions
├── .github/
│   └── copilot-instructions.md
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Database Models

### User Model
- Extended Django's AbstractUser
- Additional fields: phone_number, date_of_birth, address

### Account Model
- account_number (unique, auto-generated)
- account_type (Savings, Checking, Current)
- balance
- pin (4-digit)
- status (Active, Inactive, Blocked)

### Card Model
- card_number (unique, auto-generated)
- card_type (Debit, Credit)
- cvv (auto-generated)
- expiry_date
- status

### Transaction Model
- transaction_id (unique, auto-generated)
- transaction_type (Deposit, Withdrawal, Transfer, Balance Inquiry)
- amount
- balance_before
- balance_after
- description
- status (Success, Failed, Pending)

## Security Considerations

### For Development
- Default SECRET_KEY is included (change in production)
- DEBUG mode is enabled
- ALLOWED_HOSTS includes '*' for easy testing

### For Production
Before deploying to production:

1. **Generate a new SECRET_KEY**
   ```python
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```

2. **Update settings.py**
   ```python
   SECRET_KEY = 'your-new-secret-key'
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   ```

3. **Use HTTPS**
   - Enable SSL/TLS certificates
   - Update security middleware settings

4. **Database**
   - Switch to PostgreSQL or MySQL
   - Use environment variables for credentials

5. **Static Files**
   - Configure proper static file serving
   - Use a CDN for better performance

## Customization

### Changing Colors
Edit `static/css/style.css` and modify the CSS variables:
```css
:root {
    --primary-color: #2563eb;
    --secondary-color: #64748b;
    /* ... other colors */
}
```

### Adding New Features
1. Update models in `accounts/models.py`
2. Create migrations: `python manage.py makemigrations`
3. Apply migrations: `python manage.py migrate`
4. Add views in `accounts/views.py`
5. Create templates in `templates/accounts/`
6. Update URLs in `accounts/urls.py`

### Session Timeout
Modify in `atm_system/settings.py`:
```python
SESSION_COOKIE_AGE = 1800  # 30 minutes (in seconds)
```

## Troubleshooting

### Common Issues

**Issue**: "No module named 'django'"
**Solution**: Activate virtual environment and install requirements
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

**Issue**: "Table doesn't exist"
**Solution**: Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

**Issue**: Static files not loading
**Solution**: Run collectstatic
```bash
python manage.py collectstatic --noinput
```

**Issue**: Port already in use
**Solution**: Use a different port
```bash
python manage.py runserver 8080
```

## Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is created for educational purposes. Feel free to use and modify as needed.

## Support

For issues, questions, or suggestions:
- Create an issue in the repository
- Review the documentation
- Check the troubleshooting section

## Future Enhancements

Potential features for future versions:
- Email notifications for transactions
- SMS alerts
- Two-factor authentication
- Bill payments
- Loan management
- Investment accounts
- Mobile app integration
- QR code payments
- Biometric authentication
- Export transaction statements (PDF)
- Multi-language support
- Dark mode theme

## Acknowledgments

- Django Documentation
- Bootstrap concepts for responsive design
- Modern UI/UX best practices

---

**Version**: 1.0.0  
**Last Updated**: December 28, 2025  
**Author**: ATM Management System Team
#   A T M - M a n a g e m e n t - S y s t e m  
 