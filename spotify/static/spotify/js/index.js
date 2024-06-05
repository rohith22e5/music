// cardClicks.js
document.addEventListener('DOMContentLoaded', () => {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.parentElement.classList.add('active');
        }
    });
        document.getElementById('prevPage').addEventListener('click', function(e) {
            e.preventDefault();
            window.history.back();
        });

        document.getElementById('nextPage').addEventListener('click', function(e) {
            e.preventDefault();
            window.history.forward();
        });

    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            const type = this.getAttribute('data-type');
            if (id && type) {
                window.location.href = `/${type}/${id}/`;
            } else {
                console.error('Card ID or type not found');
            }
        });
    });
});
