// Funcionalidad del formulario de registro de FilmScoper
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('formRegister');
    const password = document.getElementById('regPassword');
    const confirmPassword = document.getElementById('regConfirm');
    const birthdate = document.getElementById('regBirthdate');
    const nameInput = document.getElementById('regName');
    const usernameInput = document.getElementById('regUsername');
    const emailInput = document.getElementById('regEmail');

    // Validación de contraseña con 4 reglas de seguridad
    function validatePassword(passwordValue) {
        const rules = {
            length: passwordValue.length >= 8,
            uppercase: /[A-Z]/.test(passwordValue),
            lowercase: /[a-z]/.test(passwordValue),
            numbers: /\d/.test(passwordValue),
            special: /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(passwordValue)
        };

        const passedRules = Object.values(rules).filter(Boolean).length;
        return { rules, passedRules, isValid: passedRules >= 4 };
    }

    // Mostrar feedback visual de la contraseña
    function updatePasswordFeedback(passwordValue) {
        const validation = validatePassword(passwordValue);
        let feedbackHTML = '<div class="password-rules mt-2">';
        
        feedbackHTML += `<small class="${validation.rules.length ? 'text-success' : 'text-danger'}">
            ${validation.rules.length ? '✓' : '✗'} Mínimo 8 caracteres
        </small><br>`;
        
        feedbackHTML += `<small class="${validation.rules.uppercase ? 'text-success' : 'text-danger'}">
            ${validation.rules.uppercase ? '✓' : '✗'} Al menos una mayúscula
        </small><br>`;
        
        feedbackHTML += `<small class="${validation.rules.lowercase ? 'text-success' : 'text-danger'}">
            ${validation.rules.lowercase ? '✓' : '✗'} Al menos una minúscula
        </small><br>`;
        
        feedbackHTML += `<small class="${validation.rules.numbers ? 'text-success' : 'text-danger'}">
            ${validation.rules.numbers ? '✓' : '✗'} Al menos un número
        </small><br>`;
        
        feedbackHTML += `<small class="${validation.rules.special ? 'text-success' : 'text-danger'}">
            ${validation.rules.special ? '✓' : '✗'} Al menos un carácter especial (!@#$%^&*)
        </small>`;
        
        feedbackHTML += '</div>';

        let feedbackDiv = password.parentNode.querySelector('.password-rules');
        if (feedbackDiv) {
            feedbackDiv.remove();
        }
        
        if (passwordValue.length > 0) {
            password.parentNode.insertAdjacentHTML('beforeend', feedbackHTML);
        }

        return validation.isValid;
    }

    // Validación de email
    function validateEmail(emailValue) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(emailValue);
    }

    // Validación de nombre (solo letras y espacios)
    function validateName(nameValue) {
        const nameRegex = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/;
        return nameValue.length >= 2 && nameRegex.test(nameValue);
    }

    // Validación de username (alfanumérico, guiones bajos)
    function validateUsername(usernameValue) {
        const usernameRegex = /^[a-zA-Z0-9_]+$/;
        return usernameValue.length >= 3 && usernameRegex.test(usernameValue);
    }

    // Eventos de validación en tiempo real
    password.addEventListener('input', function() {
        const isValid = updatePasswordFeedback(this.value);
        
        if (this.value === '') {
            this.setCustomValidity('');
        } else if (!isValid) {
            this.setCustomValidity('La contraseña debe cumplir al menos 4 de las reglas de seguridad.');
        } else {
            this.setCustomValidity('');
        }

        // Revalidar confirmación si ya tiene contenido
        if (confirmPassword.value) {
            confirmPassword.dispatchEvent(new Event('input'));
        }
    });

    // Validación de nombre en tiempo real
    nameInput.addEventListener('input', function() {
        if (this.value === '') {
            this.setCustomValidity('');
        } else if (!validateName(this.value)) {
            this.setCustomValidity('El nombre solo puede contener letras y espacios.');
        } else {
            this.setCustomValidity('');
        }
    });

    // Validación de username en tiempo real
    usernameInput.addEventListener('input', function() {
        if (this.value === '') {
            this.setCustomValidity('');
        } else if (!validateUsername(this.value)) {
            this.setCustomValidity('El usuario solo puede contener letras, números y guiones bajos.');
        } else {
            this.setCustomValidity('');
        }
    });

    // Validación de email en tiempo real
    emailInput.addEventListener('input', function() {
        if (this.value === '') {
            this.setCustomValidity('');
        } else if (!validateEmail(this.value)) {
            this.setCustomValidity('Ingresa un email válido.');
        } else {
            this.setCustomValidity('');
        }
    });

    // Validar edad mínima (13 años)
    birthdate.addEventListener('change', function() {
        const today = new Date();
        const birthDate = new Date(this.value);
        const age = today.getFullYear() - birthDate.getFullYear();
        const monthDiff = today.getMonth() - birthDate.getMonth();
        
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
            age--;
        }
        
        if (age < 13) {
            this.setCustomValidity('Debes tener al menos 13 años para registrarte.');
        } else {
            this.setCustomValidity('');
        }
    });

    // Validar confirmación de contraseña
    confirmPassword.addEventListener('input', function() {
        if (this.value !== password.value) {
            this.setCustomValidity('Las contraseñas deben coincidir.');
        } else {
            this.setCustomValidity('');
        }
    });

    // Manejar envío del formulario
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (this.checkValidity()) {
            // Obtener géneros seleccionados
            const selectedGenres = [];
            const genreCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
            genreCheckboxes.forEach(checkbox => {
                selectedGenres.push(checkbox.nextElementSibling.textContent);
            });
            
            // Simular registro exitoso
            let message = '¡Registro exitoso! Bienvenido a FilmScoper';
            if (selectedGenres.length > 0) {
                message += `\n\nTus géneros favoritos: ${selectedGenres.join(', ')}`;
            }
            alert(message);
            this.reset();
            // Limpiar preview de foto
            const photoPreview = document.getElementById('photoPreview');
            const photoLabel = document.getElementById('photoLabel');
            if (photoPreview) photoPreview.innerHTML = '';
            if (photoLabel) photoLabel.textContent = 'Seleccionar imagen';
        } else {
            // Mostrar errores de validación
            this.classList.add('was-validated');
        }
    });

    // Limpiar validaciones al resetear
    form.addEventListener('reset', function() {
        this.classList.remove('was-validated');
        // Limpiar validaciones personalizadas
        const inputs = this.querySelectorAll('input');
        inputs.forEach(input => input.setCustomValidity(''));
    });
});

// Función para previsualizar la foto seleccionada
function previewPhoto(input) {
    const file = input.files[0];
    const previewContainer = document.getElementById('photoPreview');
    const label = document.getElementById('photoLabel');
    
    if (file) {
        // Validar tamaño (5MB máximo)
        if (file.size > 5 * 1024 * 1024) {
            alert('La imagen es demasiado grande. Por favor selecciona una imagen menor a 5MB.');
            input.value = '';
            return;
        }
        
        // Validar tipo de archivo
        if (!file.type.startsWith('image/')) {
            alert('Por favor selecciona un archivo de imagen válido.');
            input.value = '';
            return;
        }
        
        const reader = new FileReader();
        reader.onload = function(e) {
            previewContainer.innerHTML = `
                <img src="${e.target.result}" alt="Preview" class="photo-preview">
                <div class="mt-2">
                    <small class="text-muted">${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)</small>
                </div>
            `;
            label.textContent = 'Cambiar imagen';
        };
        reader.readAsDataURL(file);
    } else {
        previewContainer.innerHTML = '';
        label.textContent = 'Seleccionar imagen';
    }
}