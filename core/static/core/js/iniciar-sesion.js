document.addEventListener('DOMContentLoaded', function() {
    console.log('🎬 FilmScoper - Login Form Loading...');
    
    // Obtener elementos del DOM
    const form = document.getElementById('formLogin');
    const usernameInput = document.getElementById('id_username');
    const passwordInput = document.getElementById('id_password');
    const togglePasswordBtn = document.getElementById('togglePassword');
    const eyeIcon = document.getElementById('eyeIcon');

    // Debug: Verificar elementos
    console.log('Form encontrado:', !!form);
    console.log('Username input:', !!usernameInput);
    console.log('Password input:', !!passwordInput);
    console.log('Toggle button:', !!togglePasswordBtn);
    console.log('Eye icon:', !!eyeIcon);

    // Configurar toggle de contraseña
    if (togglePasswordBtn && passwordInput && eyeIcon) {
        console.log('✅ Configurando toggle de contraseña');
        
        togglePasswordBtn.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('👁️ Toggle clicked');
            
            const currentType = passwordInput.getAttribute('type');
            const newType = currentType === 'password' ? 'text' : 'password';
            
            passwordInput.setAttribute('type', newType);
            eyeIcon.textContent = newType === 'password' ? 'Mostrar' : 'Ocultar';
            
            console.log(`Contraseña cambiada de ${currentType} a ${newType}`);
        });
    } else {
        console.error('❌ No se pudieron encontrar elementos para toggle');
        if (!togglePasswordBtn) console.error('- falta togglePasswordBtn');
        if (!passwordInput) console.error('- falta passwordInput');
        if (!eyeIcon) console.error('- falta eyeIcon');
    }

    // Validación robusta para username/email
    function validateUsernameOrEmail(value) {
        const trimmed = value.trim();
        if (trimmed.length === 0) return { valid: false, message: 'Este campo es obligatorio' };
        
        // Si contiene @, validar como email
        if (trimmed.includes('@')) {
            return validateEmail(trimmed);
        } else {
            return validateUsername(trimmed);
        }
    }

    // Validación específica de email
    function validateEmail(email) {
        const trimmedEmail = email.trim();
        
        // Verificaciones básicas
        if (trimmedEmail.length === 0) {
            return { valid: false, message: 'El email es obligatorio' };
        }
        
        if (trimmedEmail.length > 254) {
            return { valid: false, message: 'El email es demasiado largo (máx. 254 caracteres)' };
        }
        
        // Verificar que no empiece o termine con punto
        if (trimmedEmail.startsWith('.') || trimmedEmail.endsWith('.')) {
            return { valid: false, message: 'El email no puede empezar o terminar con punto' };
        }
        
        // Verificar que no tenga puntos consecutivos
        if (trimmedEmail.includes('..')) {
            return { valid: false, message: 'El email no puede tener puntos consecutivos' };
        }
        
        // Regex más estricta para email
        const emailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
        
        if (!emailRegex.test(trimmedEmail)) {
            return { valid: false, message: 'Formato de email inválido' };
        }
        
        return { valid: true, message: 'Email válido' };
    }

    // Validación específica de username
    function validateUsername(username) {
        const trimmed = username.trim();
        
        if (trimmed.length < 3) {
            return { valid: false, message: 'El nombre de usuario debe tener al menos 3 caracteres' };
        }
        
        if (trimmed.length > 150) {
            return { valid: false, message: 'El nombre de usuario es demasiado largo (máx. 150 caracteres)' };
        }
        
        // Solo letras, números y algunos símbolos permitidos
        const usernameRegex = /^[a-zA-Z0-9@.+_-]+$/;
        if (!usernameRegex.test(trimmed)) {
            return { valid: false, message: 'Solo se permiten letras, números y los símbolos @ . + _ -' };
        }
        
        return { valid: true, message: 'Nombre de usuario válido' };
    }

    // Validación robusta de contraseña para LOGIN
    function validatePasswordLogin(password) {
        // Para login, validación más permisiva (no revelar requisitos específicos por seguridad)
        if (password.length === 0) {
            return { valid: false, message: 'La contraseña es obligatoria' };
        }
        
        if (password.length < 6) {
            return { valid: false, message: 'La contraseña debe tener al menos 6 caracteres' };
        }
        
        return { valid: true, message: 'Contraseña válida' };
    }

    // Validación estricta de contraseña para REGISTRO
    function validatePasswordStrict(password) {
        const errors = [];
        
        if (password.length === 0) {
            return { valid: false, message: 'La contraseña es obligatoria' };
        }
        
        if (password.length < 8) {
            errors.push('al menos 8 caracteres');
        }
        
        if (!/[A-Z]/.test(password)) {
            errors.push('al menos una letra mayúscula');
        }
        
        if (!/[a-z]/.test(password)) {
            errors.push('al menos una letra minúscula');
        }
        
        if (!/\d/.test(password)) {
            errors.push('al menos un número');
        }
        
        if (!/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) {
            errors.push('al menos un símbolo especial');
        }
        
        // Verificar que no sea una contraseña común
        const commonPasswords = ['password', '123456', '12345678', 'qwerty', 'abc123', 'password123'];
        if (commonPasswords.includes(password.toLowerCase())) {
            errors.push('no puede ser una contraseña común');
        }
        
        if (errors.length > 0) {
            return { 
                valid: false, 
                message: `La contraseña debe tener: ${errors.join(', ')}` 
            };
        }
        
        return { valid: true, message: 'Contraseña segura' };
    }

    // Validación en tiempo real para username/email con mensajes
    if (usernameInput) {
        usernameInput.addEventListener('input', function() {
            const value = this.value;
            const validation = validateUsernameOrEmail(value);
            
            // Remover mensajes de error previos
            const existingFeedback = this.parentNode.querySelector('.validation-feedback');
            if (existingFeedback) {
                existingFeedback.remove();
            }
            
            if (value === '') {
                this.classList.remove('is-valid', 'is-invalid');
            } else if (validation.valid) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
                
                // Agregar mensaje de éxito
                const feedback = document.createElement('div');
                feedback.className = 'validation-feedback text-success small mt-1';
                feedback.textContent = validation.message;
                this.parentNode.appendChild(feedback);
            } else {
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
                
                // Agregar mensaje de error
                const feedback = document.createElement('div');
                feedback.className = 'validation-feedback text-danger small mt-1';
                feedback.textContent = validation.message;
                this.parentNode.appendChild(feedback);
            }
        });
    }

    // Validación en tiempo real para password con mensajes
    if (passwordInput) {
        passwordInput.addEventListener('input', function() {
            const value = this.value;
            // Para login usamos validación más permisiva
            const validation = validatePasswordLogin(value);
            
            // Remover mensajes de error previos
            const existingFeedback = this.parentNode.querySelector('.validation-feedback');
            if (existingFeedback) {
                existingFeedback.remove();
            }
            
            if (value === '') {
                this.classList.remove('is-valid', 'is-invalid');
            } else if (validation.valid) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
                
                // Mostrar fortaleza de la contraseña
                const strength = getPasswordStrength(value);
                const feedback = document.createElement('div');
                feedback.className = `validation-feedback text-${strength.color} small mt-1`;
                feedback.textContent = `Fortaleza: ${strength.level}`;
                this.parentNode.appendChild(feedback);
            } else {
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
                
                // Agregar mensaje de error
                const feedback = document.createElement('div');
                feedback.className = 'validation-feedback text-danger small mt-1';
                feedback.textContent = validation.message;
                this.parentNode.appendChild(feedback);
            }
        });
    }

    // Función para evaluar fortaleza de contraseña
    function getPasswordStrength(password) {
        let score = 0;
        
        // Longitud
        if (password.length >= 8) score += 1;
        if (password.length >= 12) score += 1;
        
        // Complejidad
        if (/[a-z]/.test(password)) score += 1;
        if (/[A-Z]/.test(password)) score += 1;
        if (/\d/.test(password)) score += 1;
        if (/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) score += 1;
        
        // Variedad
        const uniqueChars = new Set(password).size;
        if (uniqueChars >= password.length * 0.6) score += 1;
        
        if (score <= 2) {
            return { level: 'Débil', color: 'danger' };
        } else if (score <= 4) {
            return { level: 'Moderada', color: 'warning' };
        } else if (score <= 6) {
            return { level: 'Fuerte', color: 'success' };
        } else {
            return { level: 'Muy Fuerte', color: 'primary' };
        }
    }

    // Manejo del envío del formulario con validación completa
    if (form) {
        form.addEventListener('submit', function(e) {
            console.log('📨 Validando formulario antes del envío...');
            
            let isValid = true;
            const errors = [];
            
            // Validar username/email
            if (usernameInput) {
                const usernameValidation = validateUsernameOrEmail(usernameInput.value);
                if (!usernameValidation.valid) {
                    isValid = false;
                    errors.push(`Usuario/Email: ${usernameValidation.message}`);
                    usernameInput.classList.add('is-invalid');
                }
            }
            
            // Validar password
            if (passwordInput) {
                const passwordValidation = validatePasswordLogin(passwordInput.value);
                if (!passwordValidation.valid) {
                    isValid = false;
                    errors.push(`Contraseña: ${passwordValidation.message}`);
                    passwordInput.classList.add('is-invalid');
                }
            }
            
            // Si hay errores, prevenir envío y mostrar
            if (!isValid) {
                e.preventDefault();
                console.error('❌ Errores de validación:', errors);
                
                // Mostrar errores en un alert o en el DOM
                alert('Por favor corrige los siguientes errores:\n\n' + errors.join('\n'));
                return false;
            }
            
            console.log('✅ Formulario válido, enviando...');
            
            // Agregar loading al botón
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                const originalText = submitBtn.textContent;
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Iniciando sesión...';
                
                // Restaurar después de 5 segundos si hay error
                setTimeout(() => {
                    if (submitBtn.disabled) {
                        submitBtn.disabled = false;
                        submitBtn.textContent = originalText;
                    }
                }, 5000);
            }
            
            // Permitir que Django maneje el formulario
            return true;
        });
    }

    console.log('✅ Login form JavaScript configurado correctamente');
});