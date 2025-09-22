document.addEventListener('DOMContentLoaded', function() {
    const stepOneForm = document.getElementById('stepOneForm');
    const stepTwoForm = document.getElementById('stepTwoForm');
    const successMessage = document.getElementById('successMessage');
    const emailInput = document.getElementById('recoveryEmail');
    const codeInput = document.getElementById('verificationCode');
    const newPasswordInput = document.getElementById('newPassword');
    const confirmPasswordInput = document.getElementById('confirmPassword');
    
    // Referencias para feedback visual de contraseña
    const passwordRulesContainer = document.createElement('div');
    passwordRulesContainer.className = 'password-rules mt-2';
    passwordRulesContainer.innerHTML = `
        <small class="text-muted">La contraseña debe cumplir con:</small>
        <div class="password-rule" data-rule="length">
            <span class="rule-icon">✗</span> Al menos 8 caracteres
        </div>
        <div class="password-rule" data-rule="uppercase">
            <span class="rule-icon">✗</span> Una letra mayúscula
        </div>
        <div class="password-rule" data-rule="lowercase">
            <span class="rule-icon">✗</span> Una letra minúscula
        </div>
        <div class="password-rule" data-rule="number">
            <span class="rule-icon">✗</span> Un número
        </div>
        <div class="password-rule" data-rule="special">
            <span class="rule-icon">✗</span> Un carácter especial (!@#$%^&*(),.?":{}|<>)
        </div>
    `;

    // Insertar reglas después del campo de nueva contraseña
    if (newPasswordInput && newPasswordInput.parentNode) {
        newPasswordInput.parentNode.insertBefore(passwordRulesContainer, newPasswordInput.nextSibling);
    }

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

    // Validación de contraseña con 4 reglas de seguridad
    function validatePasswordRules(password) {
        const rules = {
            length: password.length >= 8,
            uppercase: /[A-Z]/.test(password),
            lowercase: /[a-z]/.test(password),
            number: /\d/.test(password),
            special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
        };

        // Actualizar feedback visual
        updatePasswordFeedback(rules);

        // Retornar si al menos 4 de 5 reglas se cumplen
        const validRules = Object.values(rules).filter(Boolean).length;
        return validRules >= 4;
    }

    // Actualizar feedback visual de las reglas
    function updatePasswordFeedback(rules) {
        Object.keys(rules).forEach(rule => {
            const ruleElement = passwordRulesContainer.querySelector(`[data-rule="${rule}"]`);
            if (ruleElement) {
                const icon = ruleElement.querySelector('.rule-icon');
                if (rules[rule]) {
                    icon.textContent = '✓';
                    icon.style.color = 'green';
                    ruleElement.style.color = 'green';
                } else {
                    icon.textContent = '✗';
                    icon.style.color = 'red';
                    ruleElement.style.color = 'red';
                }
            }
        });
    }

    // Validación de código
    function validateCode(code) {
        // El código debe ser de 6 dígitos
        return /^\d{6}$/.test(code);
    }

    // Real-time email validation
    if (emailInput) {
        emailInput.addEventListener('input', function() {
            if (this.value === '') {
                this.setCustomValidity('');
                this.classList.remove('is-valid', 'is-invalid');
            } else if (!validateEmail(this.value)) {
                this.setCustomValidity('Ingresa un email válido.');
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
    }

    // Real-time code validation
    if (codeInput) {
        codeInput.addEventListener('input', function() {
            // Solo permitir números
            this.value = this.value.replace(/\D/g, '');
            
            if (this.value === '') {
                this.setCustomValidity('');
                this.classList.remove('is-valid', 'is-invalid');
            } else if (!validateCode(this.value)) {
                this.setCustomValidity('El código debe tener 6 dígitos.');
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
            } else {
                this.setCustomValidity('');
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            }
        });
    }

    // Real-time password validation
    if (newPasswordInput) {
        newPasswordInput.addEventListener('input', function() {
            if (this.value === '') {
                this.setCustomValidity('');
                this.classList.remove('is-valid', 'is-invalid');
                // Resetear feedback visual
                updatePasswordFeedback({
                    length: false,
                    uppercase: false,
                    lowercase: false,
                    number: false,
                    special: false
                });
            } else if (!validatePasswordRules(this.value)) {
                this.setCustomValidity('La contraseña debe cumplir con al menos 4 de las 5 reglas de seguridad.');
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
            } else {
                this.setCustomValidity('');
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            }

            // Validar confirmación si ya tiene valor
            if (confirmPasswordInput && confirmPasswordInput.value) {
                validatePasswordMatch();
            }
        });
    }

    // Validación de confirmación de contraseña
    function validatePasswordMatch() {
        if (newPasswordInput && confirmPasswordInput) {
            if (confirmPasswordInput.value === '') {
                confirmPasswordInput.setCustomValidity('');
                confirmPasswordInput.classList.remove('is-valid', 'is-invalid');
                return false;
            } else if (newPasswordInput.value !== confirmPasswordInput.value) {
                confirmPasswordInput.setCustomValidity('Las contraseñas no coinciden.');
                confirmPasswordInput.classList.remove('is-valid');
                confirmPasswordInput.classList.add('is-invalid');
                return false;
            } else {
                confirmPasswordInput.setCustomValidity('');
                confirmPasswordInput.classList.remove('is-invalid');
                confirmPasswordInput.classList.add('is-valid');
                return true;
            }
        }
        return false;
    }

    // Real-time password confirmation validation
    if (confirmPasswordInput) {
        confirmPasswordInput.addEventListener('input', validatePasswordMatch);
    }

    // Step 1: Email verification
    if (stepOneForm) {
        stepOneForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            if (validateEmail(emailInput.value)) {
                const submitBtn = this.querySelector('button[type="submit"]');
                const originalText = submitBtn.textContent;
                
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Enviando código...';

                // Simulate API call delay
                setTimeout(() => {
                    // Hide step 1 and show step 2
                    stepOneForm.style.display = 'none';
                    stepTwoForm.style.display = 'block';
                    
                    // Focus on code input
                    codeInput.focus();
                    
                    // Reset button
                    submitBtn.disabled = false;
                    submitBtn.textContent = originalText;
                }, 2000);
            } else {
                this.classList.add('was-validated');
            }
        });
    }

    // Step 2: Code verification and password reset
    if (stepTwoForm) {
        stepTwoForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            const isCodeValid = validateCode(codeInput.value);
            const isPasswordValid = validatePasswordRules(newPasswordInput.value);
            const isPasswordMatchValid = validatePasswordMatch();

            if (isCodeValid && isPasswordValid && isPasswordMatchValid) {
                const submitBtn = this.querySelector('button[type="submit"]');
                const originalText = submitBtn.textContent;
                
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Actualizando contraseña...';

                // Simulate API call delay
                setTimeout(() => {
                    // Hide step 2 and show success message
                    stepTwoForm.style.display = 'none';
                    successMessage.style.display = 'block';
                    
                    // Auto redirect after 3 seconds
                    setTimeout(() => {
                        window.location.href = 'iniciar-sesion.html';
                    }, 3000);
                }, 2000);
            } else {
                this.classList.add('was-validated');
            }
        });
    }

    // Botón para volver al paso anterior
    const backButton = document.getElementById('backToStep1');
    if (backButton) {
        backButton.addEventListener('click', function() {
            stepTwoForm.style.display = 'none';
            stepOneForm.style.display = 'block';
            emailInput.focus();
        });
    }

    // Toggle password visibility
    const toggleButtons = document.querySelectorAll('.toggle-password');
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const targetInput = document.getElementById(targetId);
            const eyeIcon = this.querySelector('i') || this;
            
            if (targetInput) {
                const type = targetInput.getAttribute('type') === 'password' ? 'text' : 'password';
                targetInput.setAttribute('type', type);
                eyeIcon.textContent = type === 'password' ? '👁️' : '👁️‍🗨️';
            }
        });
    });
});
