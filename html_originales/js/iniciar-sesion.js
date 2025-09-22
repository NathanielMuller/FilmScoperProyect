document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('formLogin');
    const emailInput = document.getElementById('loginEmail');
    const passwordInput = document.getElementById('loginPassword');
    const togglePasswordBtn = document.getElementById('togglePassword');
    const eyeIcon = document.getElementById('eyeIcon');

    // Toggle password visibility
    togglePasswordBtn.addEventListener('click', function() {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        eyeIcon.textContent = type === 'password' ? 'Mostrar' : 'Ocultar';
    });

    // Validación de email más robusta
    function validateEmail(emailValue) {
        const emailValue_trimmed = emailValue.trim();
        // Regex más estricto para email
        const emailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
        
        // Verificaciones adicionales
        if (emailValue_trimmed.length === 0) return false;
        if (emailValue_trimmed.length > 254) return false;
        if (emailValue_trimmed.startsWith('.') || emailValue_trimmed.endsWith('.')) return false;
        if (emailValue_trimmed.includes('..')) return false;
        
        return emailRegex.test(emailValue_trimmed);
    }

    // Validación de contraseña para login (solo longitud mínima por seguridad)
    function validatePasswordValue(passwordValue) {
        // Solo validar longitud mínima para no dar pistas sobre formato
        return passwordValue.length >= 6;
    }

    // Real-time email validation
    emailInput.addEventListener('input', function() {
        if (this.value === '') {
            this.setCustomValidity('');
            this.classList.remove('is-valid', 'is-invalid');
        } else if (!validateEmail(this.value)) {
            this.setCustomValidity('Ingresa un email con formato válido (ejemplo@dominio.com).');
            this.classList.remove('is-valid');
            this.classList.add('is-invalid');
        } else {
            this.setCustomValidity('');
            this.classList.remove('is-invalid');
            this.classList.add('is-valid');
        }
    });

    // Real-time password validation
    passwordInput.addEventListener('input', function() {
        if (this.value === '') {
            this.setCustomValidity('');
            this.classList.remove('is-valid', 'is-invalid');
        } else if (!validatePasswordValue(this.value)) {
            this.setCustomValidity('La contraseña debe tener al menos 6 caracteres.');
            this.classList.remove('is-valid');
            this.classList.add('is-invalid');
        } else {
            this.setCustomValidity('');
            this.classList.remove('is-invalid');
            this.classList.add('is-valid');
        }
    });

    // Prevenir espacios en email
    emailInput.addEventListener('keypress', function(e) {
        if (e.key === ' ') {
            e.preventDefault();
        }
    });

    // Form submission
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        const isEmailValid = validateEmail(emailInput.value);
        const isPasswordValid = validatePasswordValue(passwordInput.value);

        if (isEmailValid && isPasswordValid) {
            // Simulate login process
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Iniciando sesión...';

            // Simulate API call delay
            setTimeout(() => {
                // Here you would normally make an API call to your backend
                alert('¡Inicio de sesión exitoso! (Simulación)');
                
                // Reset button
                submitBtn.disabled = false;
                submitBtn.textContent = originalText;
                
                // Redirect to main page
                window.location.href = 'index.html';
            }, 2000);
        } else {
            // Show validation errors
            form.classList.add('was-validated');
            
            // Mostrar errores específicos
            if (!validateEmail(emailInput.value)) {
                showError(emailInput, 'Por favor ingresa un correo válido con formato correcto (ejemplo@dominio.com).');
            }
            if (!validatePasswordValue(passwordInput.value)) {
                showError(passwordInput, 'La contraseña debe tener al menos 6 caracteres.');
            }
        }
    });

    // Password validation function
    function validatePassword(input) {
        const password = input.value;
        
        if (password === '') {
            showError(input, 'La contraseña es requerida.');
            return false;
        } else if (!validatePasswordValue(password)) {
            showError(input, 'La contraseña debe tener al menos 6 caracteres.');
            return false;
        } else {
            showValid(input);
            return true;
        }
    }

    // Show error state
    function showError(input, message) {
        input.classList.remove('is-valid');
        input.classList.add('is-invalid');
        
        const feedback = input.nextElementSibling;
        if (feedback && feedback.classList.contains('invalid-feedback')) {
            feedback.textContent = message;
        }
    }

    // Show valid state
    function showValid(input) {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
    }

    // Handle "Remember me" functionality
    const rememberCheckbox = document.getElementById('rememberMe');
    
    // Load saved email if "remember me" was checked
    const savedEmail = localStorage.getItem('rememberedEmail');
    if (savedEmail) {
        emailInput.value = savedEmail;
        rememberCheckbox.checked = true;
    }

    // Save/remove email based on checkbox
    rememberCheckbox.addEventListener('change', function() {
        if (this.checked && emailInput.value.trim()) {
            localStorage.setItem('rememberedEmail', emailInput.value.trim());
        } else {
            localStorage.removeItem('rememberedEmail');
        }
    });

    // Update saved email when email changes
    emailInput.addEventListener('change', function() {
        if (rememberCheckbox.checked) {
            localStorage.setItem('rememberedEmail', this.value.trim());
        }
    });
});
