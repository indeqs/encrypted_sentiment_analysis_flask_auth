document.addEventListener('DOMContentLoaded', function () {
    // Auto-close alerts after 3 seconds, except on verify page
    if (!window.location.pathname.includes('/verify')) {
        setTimeout(function () {
            const alerts = document.querySelectorAll('.alert');
            alerts.forEach(function (alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            });
        }, 3000);
    }

    // Toggle password visibility
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('password');

    if (togglePassword && passwordInput) {
        togglePassword.addEventListener('click', function () {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            this.querySelector('i').classList.toggle('fa-eye');
            this.querySelector('i').classList.toggle('fa-eye-slash');
        });
    }

    // Example chart initialization (would be replaced with real data)
    const chartElement = document.getElementById('sentimentChart');
    if (chartElement) {
        // This is a placeholder for chart initialization
        console.log('Chart element found, would initialize chart here in a real implementation');
    }
});