// Close alert messages
document.addEventListener('DOMContentLoaded', function() {
    // Auto-close alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.animation = 'fadeOut 0.3s';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });

    // Manual close alerts
    const closeButtons = document.querySelectorAll('.close-alert');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const alert = this.parentElement;
            alert.style.animation = 'fadeOut 0.3s';
            setTimeout(() => alert.remove(), 300);
        });
    });

    // Mobile menu toggle
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            this.classList.toggle('active');
        });
    }

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
            let isValid = true;
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.style.borderColor = 'var(--danger-color)';
                } else {
                    input.style.borderColor = 'var(--border-color)';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showMessage('Please fill in all required fields', 'error');
            }
        });
    });

    // Number input validation (only positive numbers)
    const numberInputs = document.querySelectorAll('input[type="number"]');
    numberInputs.forEach(input => {
        input.addEventListener('input', function() {
            if (this.value < 0) {
                this.value = 0;
            }
        });
    });

    // PIN input validation (only 4 digits)
    const pinInputs = document.querySelectorAll('input[name="pin"], input[name="confirm_pin"]');
    pinInputs.forEach(input => {
        input.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9]/g, '').slice(0, 4);
        });
    });

    // Confirm before dangerous actions
    const dangerousLinks = document.querySelectorAll('a[href*="logout"], a[href*="delete"]');
    dangerousLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to proceed?')) {
                e.preventDefault();
            }
        });
    });

    // Format account numbers
    const accountNumbers = document.querySelectorAll('.account-number');
    accountNumbers.forEach(element => {
        const number = element.textContent.trim();
        if (number.length === 16) {
            element.textContent = number.match(/.{1,4}/g).join(' ');
        }
    });

    // Smooth scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add loading state to buttons
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(button => {
        // Store original button text
        button.dataset.originalText = button.textContent;
        
        const form = button.closest('form');
        if (form) {
            form.addEventListener('submit', function() {
                button.disabled = true;
                button.innerHTML = '<span>Processing...</span>';
                
                // Re-enable after 5 seconds as a fallback
                setTimeout(() => {
                    button.disabled = false;
                    button.innerHTML = button.dataset.originalText || 'Submit';
                }, 5000);
            });
        }
    });
});

// Utility function to show messages
function showMessage(message, type = 'info') {
    const messagesContainer = document.querySelector('.messages-container') || createMessagesContainer();
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} fade-in`;
    alertDiv.innerHTML = `
        ${message}
        <button class="close-alert">&times;</button>
    `;
    
    messagesContainer.appendChild(alertDiv);
    
    // Auto close
    setTimeout(() => {
        alertDiv.style.animation = 'fadeOut 0.3s';
        setTimeout(() => alertDiv.remove(), 300);
    }, 5000);
    
    // Manual close
    alertDiv.querySelector('.close-alert').addEventListener('click', function() {
        alertDiv.style.animation = 'fadeOut 0.3s';
        setTimeout(() => alertDiv.remove(), 300);
    });
}

function createMessagesContainer() {
    const container = document.createElement('div');
    container.className = 'messages-container';
    document.body.appendChild(container);
    return container;
}

// Add fadeOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeOut {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100%);
        }
    }
    
    .nav-menu.active {
        display: flex !important;
        flex-direction: column;
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: var(--card-bg);
        box-shadow: var(--shadow);
        padding: 1rem;
    }
    
    .hamburger.active span:nth-child(1) {
        transform: rotate(45deg) translate(5px, 5px);
    }
    
    .hamburger.active span:nth-child(2) {
        opacity: 0;
    }
    
    .hamburger.active span:nth-child(3) {
        transform: rotate(-45deg) translate(7px, -6px);
    }
`;
document.head.appendChild(style);
