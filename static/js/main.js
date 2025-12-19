// Party Entry System - Enhanced JavaScript

// Utility Functions
const Utils = {
    showToast: (message, type = 'info') => {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            z-index: 10000;
            animation: slideIn 0.3s ease;
        `;
        document.body.appendChild(toast);
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transition = 'opacity 0.3s';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    },
    
    formatPhone: (value) => {
        const cleaned = value.replace(/\D/g, '');
        if (cleaned.length <= 3) return cleaned;
        if (cleaned.length <= 6) return `(${cleaned.slice(0, 3)}) ${cleaned.slice(3)}`;
        return `(${cleaned.slice(0, 3)}) ${cleaned.slice(3, 6)}-${cleaned.slice(6, 10)}`;
    },
    
    validateEmail: (email) => {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }
};

// Form validation and enhancements
document.addEventListener('DOMContentLoaded', function() {
    // Auto-uppercase ticket IDs
    const ticketInputs = document.querySelectorAll('input[name="ticket_id"]');
    ticketInputs.forEach(input => {
        input.addEventListener('input', function() {
            this.value = this.value.toUpperCase().replace(/[^A-Z0-9]/g, '');
        });
    });

    // Enhanced phone number formatting
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = this.value.replace(/\D/g, '');
            if (value.length > 10) value = value.slice(0, 10);
            if (value.length > 0) {
                this.value = Utils.formatPhone(value);
            }
        });
        
        input.addEventListener('focus', function() {
            this.style.borderColor = 'var(--primary-color)';
        });
        
        input.addEventListener('blur', function() {
            if (this.value.replace(/\D/g, '').length < 10 && this.value.length > 0) {
                this.style.borderColor = 'var(--danger-color)';
                Utils.showToast('Please enter a valid phone number', 'error');
            } else {
                this.style.borderColor = 'var(--border-color)';
            }
        });
    });

    // Enhanced email validation with real-time feedback
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.addEventListener('input', function() {
            if (this.value.length > 0) {
                if (Utils.validateEmail(this.value)) {
                    this.style.borderColor = 'var(--success-color)';
                } else {
                    this.style.borderColor = 'var(--warning-color)';
                }
            }
        });
        
        input.addEventListener('blur', function() {
            const email = this.value;
            if (email && !Utils.validateEmail(email)) {
                this.style.borderColor = 'var(--danger-color)';
                Utils.showToast('Please enter a valid email address', 'error');
            } else if (email) {
                this.style.borderColor = 'var(--success-color)';
            } else {
                this.style.borderColor = 'var(--border-color)';
            }
        });
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Copy ticket ID to clipboard
    const copyButtons = document.querySelectorAll('.copy-ticket');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const ticketId = this.getAttribute('data-ticket');
            navigator.clipboard.writeText(ticketId).then(() => {
                const originalText = this.textContent;
                this.textContent = 'Copied!';
                this.style.background = 'var(--success-color)';
                setTimeout(() => {
                    this.textContent = originalText;
                    this.style.background = '';
                }, 2000);
            });
        });
    });

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
    
    // Form submission enhancements
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = submitBtn.textContent.includes('Loading') 
                    ? submitBtn.textContent 
                    : 'Loading...';
            }
        });
    });
    
    // Add loading states to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.addEventListener('click', function() {
            if (this.type === 'submit' || this.closest('form')) {
                this.style.opacity = '0.7';
                this.style.cursor = 'wait';
            }
        });
    });
    
    // Animate stats cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.6s ease';
                entry.target.style.opacity = '1';
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.stat-card, .feature-card').forEach(card => {
        card.style.opacity = '0';
        observer.observe(card);
    });
    
    // Real-time search in admin dashboard
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.toLowerCase();
            searchTimeout = setTimeout(() => {
                const rows = document.querySelectorAll('#users-table tbody tr');
                let visibleCount = 0;
                rows.forEach(row => {
                    const text = row.textContent.toLowerCase();
                    if (text.includes(query)) {
                        row.style.display = '';
                        visibleCount++;
                    } else {
                        row.style.display = 'none';
                    }
                });
                
                // Show "no results" message if needed
                let noResults = document.getElementById('no-results');
                if (query && visibleCount === 0) {
                    if (!noResults) {
                        noResults = document.createElement('tr');
                        noResults.id = 'no-results';
                        noResults.innerHTML = `<td colspan="8" style="text-align: center; padding: 2rem; color: var(--text-secondary);">No users found matching "${query}"</td>`;
                        document.querySelector('#users-table tbody').appendChild(noResults);
                    }
                } else if (noResults) {
                    noResults.remove();
                }
            }, 300);
        });
    }
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);

// Print ticket function
function printTicket() {
    window.print();
}

// Download QR code
function downloadQR(ticketId) {
    const link = document.createElement('a');
    link.href = `/static/qrcodes/${ticketId}.png`;
    link.download = `ticket-${ticketId}.png`;
    link.click();
}

// Cursor Trail Effect
(function() {
    const trailContainer = document.createElement('div');
    trailContainer.id = 'cursor-trail';
    document.body.appendChild(trailContainer);
    
    const trail = [];
    const trailLength = 20;
    let mouseX = 0;
    let mouseY = 0;
    let lastX = 0;
    let lastY = 0;
    
    // Create trail particles
    for (let i = 0; i < trailLength; i++) {
        const particle = document.createElement('div');
        particle.style.cssText = `
            position: fixed;
            width: ${8 - i * 0.3}px;
            height: ${8 - i * 0.3}px;
            border-radius: 50%;
            background: radial-gradient(circle, 
                rgba(${157 - i * 5}, ${0 + i * 2}, ${255 - i * 3}, ${1 - i * 0.04}) 0%,
                rgba(${0 + i * 3}, ${153 - i * 5}, ${255 - i * 2}, ${0.8 - i * 0.03}) 50%,
                transparent 100%
            );
            pointer-events: none;
            z-index: 9997;
            box-shadow: 
                0 0 ${10 + i * 2}px rgba(157, 0, 255, ${0.8 - i * 0.03}),
                0 0 ${20 + i * 3}px rgba(0, 153, 255, ${0.6 - i * 0.02});
            transition: transform 0.1s ease-out, opacity 0.1s ease-out;
            opacity: ${1 - i * 0.05};
        `;
        trail.push({
            element: particle,
            x: 0,
            y: 0
        });
        trailContainer.appendChild(particle);
    }
    
    // Update trail on mouse move
    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });
    
    // Animate trail
    function animateTrail() {
        let currentX = mouseX;
        let currentY = mouseY;
        
        trail.forEach((particle, index) => {
            const nextIndex = index === 0 ? 0 : index - 1;
            const nextParticle = trail[nextIndex];
            
            if (index === 0) {
                particle.x = currentX;
                particle.y = currentY;
            } else {
                const dx = nextParticle.x - particle.x;
                const dy = nextParticle.y - particle.y;
                particle.x += dx * 0.3;
                particle.y += dy * 0.3;
            }
            
            particle.element.style.transform = `translate(${particle.x - particle.element.offsetWidth / 2}px, ${particle.y - particle.element.offsetHeight / 2}px)`;
        });
        
        requestAnimationFrame(animateTrail);
    }
    
    animateTrail();
    
    // Hide trail when mouse leaves window
    document.addEventListener('mouseleave', () => {
        trail.forEach(particle => {
            particle.element.style.opacity = '0';
        });
    });
    
    document.addEventListener('mouseenter', () => {
        trail.forEach((particle, index) => {
            particle.element.style.opacity = `${1 - index * 0.05}`;
        });
    });
})();

