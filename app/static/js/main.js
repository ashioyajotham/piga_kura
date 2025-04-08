// Main JavaScript functions

// Enable Bootstrap tooltips
document.addEventListener('DOMContentLoaded', function() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Handle flash message dismissal
    const alertList = document.querySelectorAll('.alert-dismissible');
    alertList.forEach(function(alert) {
        const closeButton = alert.querySelector('.btn-close');
        closeButton?.addEventListener('click', function() {
            alert.remove();
        });
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            alert.classList.add('fade');
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
});
