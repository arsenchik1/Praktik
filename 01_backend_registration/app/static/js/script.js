document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registrationForm');
    const errorContainer = document.getElementById('errorContainer');
    const successContainer = document.getElementById('successContainer');
    const submitBtn = document.getElementById('submitBtn');
    
    function validateForm(data) {
        const errors = [];
        const emailError = document.getElementById('emailError');
        const passwordError = document.getElementById('passwordError');
        
        emailError.textContent = '';
        passwordError.textContent = '';
        
        if (!data.email.includes('@')) {
            errors.push('Email должен содержать символ @');
            emailError.textContent = 'Email должен содержать символ @';
        }
        
        if (data.password !== data.confirmPassword) {
            errors.push('Пароли не совпадают');
            passwordError.textContent = 'Пароли не совпадают';
        }
        
        if (data.password.length < 6) {
            errors.push('Пароль должен быть не менее 6 символов');
            passwordError.textContent = 'Пароль должен быть не менее 6 символов';
        }
        
        return errors;
    }
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        errorContainer.classList.add('d-none');
        errorContainer.innerHTML = '';
        
        submitBtn.disabled = true;
        submitBtn.textContent = 'Отправка...';
        
        const formData = {
            firstName: document.getElementById('firstName').value,
            lastName: document.getElementById('lastName').value,
            email: document.getElementById('email').value,
            password: document.getElementById('password').value,
            confirmPassword: document.getElementById('confirmPassword').value
        };
        
        const clientErrors = validateForm(formData);
        if (clientErrors.length > 0) {
            errorContainer.innerHTML = clientErrors.join('<br>');
            errorContainer.classList.remove('d-none');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Зарегистрироваться';
            return;
        }
        
        try {
            const csrfToken = document.querySelector('input[name="csrf_token"]').value;
            
            const response = await fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (response.ok && result.success) {
                form.style.display = 'none';
                errorContainer.classList.add('d-none');
                
                successContainer.classList.remove('d-none');
                successContainer.innerHTML = `
                    <div class="success-message">
                        <h4>${result.message}</h4>
                        <p class="mt-3">Спасибо за регистрацию!</p>
                    </div>
                `;
            } else {
                errorContainer.innerHTML = result.errors.join('<br>');
                errorContainer.classList.remove('d-none');
            }
        } catch (error) {
            errorContainer.innerHTML = 'Ошибка при отправке формы. Попробуйте позже.';
            errorContainer.classList.remove('d-none');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Зарегистрироваться';
        }
    });
});