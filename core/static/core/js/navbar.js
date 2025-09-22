// Navbar functionality for FilmScoper
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap dropdowns
    const dropdownToggleList = document.querySelectorAll('.dropdown-toggle');
    const dropdownList = [...dropdownToggleList].map(dropdownToggleEl => new bootstrap.Dropdown(dropdownToggleEl));
    
    // Handle navbar toggler
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener('click', function() {
            const isExpanded = navbarToggler.getAttribute('aria-expanded') === 'true';
            navbarToggler.setAttribute('aria-expanded', !isExpanded);
        });
    }
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(event) {
        const dropdowns = document.querySelectorAll('.dropdown-menu.show');
        dropdowns.forEach(function(dropdown) {
            const dropdownToggle = dropdown.previousElementSibling;
            if (!dropdown.contains(event.target) && !dropdownToggle.contains(event.target)) {
                const bsDropdown = bootstrap.Dropdown.getInstance(dropdownToggle);
                if (bsDropdown) {
                    bsDropdown.hide();
                }
            }
        });
    });
});