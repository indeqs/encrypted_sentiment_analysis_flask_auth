document.addEventListener('DOMContentLoaded', function () {
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const emailInput = document.getElementById('email');
    const signupButton = document.getElementById('signupButton');
    const passwordStrength = document.getElementById('passwordStrength');
    const signupForm = document.getElementById('signupForm');

    // Form validation states
    let validations = {
        username: false,
        email: false,
        password: false
    };

    // Update signup button state
    function updateSignupButton() {
        signupButton.disabled = !(validations.username && validations.email && validations.password);
    }

    // Username validation
    usernameInput.addEventListener('input', function () {
        const username = this.value.trim();
        const usernameRegex = /^[a-zA-Z0-9_]{3,}$/;

        if (usernameRegex.test(username)) {
            // Check if username is available via API
            fetch('/api/check-username', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username: username }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.available) {
                        usernameInput.classList.remove('is-invalid');
                        usernameInput.classList.add('is-valid');
                        validations.username = true;
                    } else {
                        usernameInput.classList.remove('is-valid');
                        usernameInput.classList.add('is-invalid');
                        document.getElementById('usernameHelp').textContent = 'Username already taken';
                        validations.username = false;
                    }
                    updateSignupButton();
                });
        } else {
            usernameInput.classList.remove('is-valid');
            usernameInput.classList.add('is-invalid');
            document.getElementById('usernameHelp').textContent = 'Username must be at least 3 characters and contain only letters, numbers, and underscores.';
            validations.username = false;
            updateSignupButton();
        }
    });

    // Email validation
    emailInput.addEventListener('input', function () {
        const email = this.value.trim();
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$/;

        if (emailRegex.test(email)) {
            emailInput.classList.remove('is-invalid');
            emailInput.classList.add('is-valid');
            validations.email = true;
        } else {
            emailInput.classList.remove('is-valid');
            emailInput.classList.add('is-invalid');
            validations.email = false;
        }
        updateSignupButton();
    });

    // Password strength validation
    passwordInput.addEventListener('input', function () {
        const password = this.value;
        let strength = 0;

        // Password complexity criteria
        if (password.length >= 8) strength += 25;
        if (password.match(/[A-Z]/)) strength += 25;
        if (password.match(/[a-z]/)) strength += 25;
        if (password.match(/[0-9]/)) strength += 12.5;
        if (password.match(/[^A-Za-z0-9]/)) strength += 12.5;

        // Update progress bar
        passwordStrength.style.width = strength + '%';

        // Set progress bar color based on strength
        if (strength < 50) {
            passwordStrength.className = 'progress-bar bg-danger';
        } else if (strength < 75) {
            passwordStrength.className = 'progress-bar bg-warning';
        } else {
            passwordStrength.className = 'progress-bar bg-success';
        }

        // Check if password meets minimum requirements
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
        if (passwordRegex.test(password)) {
            passwordInput.classList.remove('is-invalid');
            passwordInput.classList.add('is-valid');
            validations.password = true;
        } else {
            passwordInput.classList.remove('is-valid');
            passwordInput.classList.add('is-invalid');
            validations.password = false;
        }
        updateSignupButton();
    });

    // Form submission validation
    signupForm.addEventListener('submit', function (event) {
        // Double check all validations before submitting
        if (!(validations.username && validations.email && validations.password)) {
            event.preventDefault();
            alert('Please fix all form errors before submitting.');
        }
    });
});