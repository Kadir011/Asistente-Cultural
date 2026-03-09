document.addEventListener('DOMContentLoaded', function() {
    // Form validation enhancement
    const form = document.querySelector('form');
    const submitBtn = document.querySelector('button[type="submit"]');
    const inputs = form.querySelectorAll('input, textarea');

    // Real-time validation feedback
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });

        input.addEventListener('input', function() {
            if (this.classList.contains('border-red-300')) {
                validateField(this);
            }
        });
    });

    function validateField(field) {
        const value = field.value.trim();
        const fieldName = field.name;
        let isValid = true;
        let errorMessage = '';

        // Remove existing error styling
        field.classList.remove('border-red-300', 'border-green-300');
        
        // Basic validation
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            errorMessage = 'Este campo es obligatorio';
        } else if (fieldName === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                isValid = false;
                errorMessage = 'Ingresa un email válido';
            }
        }

        // Apply styling based on validation
        if (!isValid) {
            field.classList.add('border-red-300');
            showFieldError(field, errorMessage);
        } else if (value) {
            field.classList.add('border-green-300');
            removeFieldError(field);
        }

        return isValid;
    }

    function showFieldError(field, message) {
        removeFieldError(field); // Remove any existing error
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error mt-1 text-sm text-red-600';
        errorDiv.textContent = message;
        
        field.parentNode.appendChild(errorDiv);
    }

    function removeFieldError(field) {
        const existingError = field.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }
    }

    // Form submission handling
    form.addEventListener('submit', function(e) {
        let isFormValid = true;
        
        inputs.forEach(input => {
            if (!validateField(input)) {
                isFormValid = false;
            }
        });

        if (isFormValid) {
            // Show loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Enviando...';
        }
    });

    // Auto-resize textarea
    const textarea = document.querySelector('textarea');
    if (textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    }

    // Smooth scroll for anchor links
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
});

// FAQ toggle functionality
function toggleFAQ(element) {
    const content = element.nextElementSibling;
    const icon = element.querySelector('i');
    
    if (content.style.display === 'none' || !content.style.display) {
        content.style.display = 'block';
        icon.classList.remove('fa-plus');
        icon.classList.add('fa-minus');
    } else {
        content.style.display = 'none';
        icon.classList.remove('fa-minus');
        icon.classList.add('fa-plus');
    }
}

// Copy email to clipboard functionality
function copyEmail(email) {
    navigator.clipboard.writeText(email).then(function() {
        // Show success notification
        const notification = document.createElement('div');
        notification.className = 'fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50';
        notification.innerHTML = '<i class="fas fa-check mr-2"></i>Email copiado al portapapeles';
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    });
}