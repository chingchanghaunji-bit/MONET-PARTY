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
        // Remove all non-digit characters
        let cleaned = value.replace(/\D/g, '');
        
        // Remove leading 91 (India country code) if user types it
        if (cleaned.startsWith('91') && cleaned.length > 10) {
            cleaned = cleaned.substring(2);
        }
        
        // Limit to 10 digits (Indian mobile number length)
        if (cleaned.length > 10) {
            cleaned = cleaned.slice(0, 10);
        }
        
        // Format as Indian number: +91 XXXXX XXXXX
        if (cleaned.length === 0) return '';
        if (cleaned.length <= 5) return `+91 ${cleaned}`;
        return `+91 ${cleaned.slice(0, 5)} ${cleaned.slice(5)}`;
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

    // Enhanced phone number formatting - Indian format
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = this.value;
            // Allow user to type digits, spaces, +, and -
            if (value.length > 0) {
                this.value = Utils.formatPhone(value);
            }
        });
        
        input.addEventListener('focus', function() {
            this.style.borderColor = 'var(--primary-color)';
            // Auto-format on focus if empty
            if (!this.value) {
                this.value = '+91 ';
            }
        });
        
        input.addEventListener('blur', function() {
            const digitsOnly = this.value.replace(/\D/g, '');
            // Remove leading 91 if present
            const phoneDigits = digitsOnly.startsWith('91') && digitsOnly.length > 10 
                ? digitsOnly.substring(2) 
                : digitsOnly;
            
            if (phoneDigits.length !== 10 && this.value.length > 0) {
                this.style.borderColor = 'var(--danger-color)';
                Utils.showToast('Please enter a valid 10-digit Indian mobile number', 'error');
            } else {
                this.style.borderColor = 'var(--border-color)';
                // Ensure proper formatting
                if (phoneDigits.length === 10) {
                    this.value = Utils.formatPhone(phoneDigits);
                }
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

// Enhanced Cursor Trail Effect with 3D Glow
(function() {
    // Check for reduced motion preference
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReducedMotion) return;
    
    // Check device capability (disable on mobile for performance)
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    if (isMobile) return;
    
    const trailContainer = document.createElement('div');
    trailContainer.id = 'cursor-trail';
    document.body.appendChild(trailContainer);
    
    const trail = [];
    const trailLength = 25; // Increased for more visible trail
    let mouseX = 0;
    let mouseY = 0;
    let lastMouseX = 0;
    let lastMouseY = 0;
    
    // Create enhanced trail particles with 3D glow
    for (let i = 0; i < trailLength; i++) {
        const particle = document.createElement('div');
        particle.className = 'cursor-trail-particle';
        const size = Math.max(6, 12 - i * 0.2);
        const opacity = Math.max(0.4, 1 - i * 0.04);
        const blur = Math.max(0, 3 - i * 0.1);
        
        // Alternate colors for visual variety
        const color1 = i % 3 === 0 ? '0, 212, 255' : (i % 3 === 1 ? '157, 78, 221' : '255, 0, 0');
        const color2 = i % 3 === 0 ? '157, 78, 221' : (i % 3 === 1 ? '255, 0, 0' : '0, 212, 255');
        
        particle.style.cssText = `
            position: fixed;
            width: ${size}px;
            height: ${size}px;
            border-radius: 50%;
            background: radial-gradient(circle, 
                rgba(${color1}, ${opacity * 0.9}) 0%,
                rgba(${color2}, ${opacity * 0.7}) 40%,
                rgba(${color1}, ${opacity * 0.3}) 70%,
                transparent 100%
            );
            pointer-events: none;
            z-index: 9999;
            box-shadow: 
                0 0 ${10 + i * 0.5}px rgba(${color1}, ${opacity * 0.8}),
                0 0 ${20 + i}px rgba(${color2}, ${opacity * 0.6}),
                0 0 ${30 + i * 1.5}px rgba(${color1}, ${opacity * 0.4}),
                inset 0 0 ${5 + i * 0.3}px rgba(255, 255, 255, ${opacity * 0.3});
            opacity: ${opacity};
            transform: translate3d(0, 0, ${i * 2}px);
            filter: blur(${blur}px);
            mix-blend-mode: screen;
            will-change: transform, opacity;
            transition: opacity 0.1s ease-out;
        `;
        trail.push({
            element: particle,
            x: 0,
            y: 0,
            vx: 0,
            vy: 0
        });
        trailContainer.appendChild(particle);
    }
    
    // Update trail on mouse move with velocity
    let rafId = null;
    document.addEventListener('mousemove', (e) => {
        const dx = e.clientX - lastMouseX;
        const dy = e.clientY - lastMouseY;
        
        mouseX = e.clientX;
        mouseY = e.clientY;
        
        // Calculate velocity for trail spread
        trail.forEach((particle, index) => {
            if (index === 0) {
                particle.vx = dx * 0.1;
                particle.vy = dy * 0.1;
            } else {
                particle.vx *= 0.9;
                particle.vy *= 0.9;
            }
        });
        
        lastMouseX = e.clientX;
        lastMouseY = e.clientY;
        
        // Update CSS variable for background glow
        document.documentElement.style.setProperty('--mouse-x', `${(e.clientX / window.innerWidth) * 100}%`);
        document.documentElement.style.setProperty('--mouse-y', `${(e.clientY / window.innerHeight) * 100}%`);
        
        if (!rafId) {
            rafId = requestAnimationFrame(animateTrail);
        }
    }, { passive: true });
    
    // Enhanced trail animation with 3D effects
    function animateTrail() {
        rafId = null;
        let currentX = mouseX;
        let currentY = mouseY;
        
        trail.forEach((particle, index) => {
            if (index === 0) {
                particle.x = currentX;
                particle.y = currentY;
            } else {
                const prevParticle = trail[index - 1];
                const lerp = 0.25 + (index * 0.02);
                particle.x += (prevParticle.x - particle.x) * lerp;
                particle.y += (prevParticle.y - particle.y) * lerp;
                
                // Add velocity spread
                particle.x += particle.vx;
                particle.y += particle.vy;
            }
            
            // 3D transform with depth
            const depth = index * 3;
            const scale = 1 - (index * 0.02);
            particle.element.style.transform = `translate3d(${particle.x - particle.element.offsetWidth / 2}px, ${particle.y - particle.element.offsetHeight / 2}px, ${depth}px) scale(${scale})`;
            
            // Pulsing glow effect
            const pulse = Math.sin(Date.now() * 0.003 + index * 0.5) * 0.2 + 0.8;
            particle.element.style.opacity = `${Math.max(0.2, (1 - index * 0.04) * pulse)}`;
        });
        
        requestAnimationFrame(animateTrail);
    }
    
    animateTrail();
    
    // Hide trail when mouse leaves window
    document.addEventListener('mouseleave', () => {
        trail.forEach(particle => {
            particle.element.style.opacity = '0';
            particle.element.style.transition = 'opacity 0.3s ease-out';
        });
    }, { passive: true });
    
    document.addEventListener('mouseenter', () => {
        trail.forEach((particle, index) => {
            particle.element.style.transition = 'opacity 0.1s ease-out';
            particle.element.style.opacity = `${Math.max(0.4, 1 - index * 0.04)}`;
        });
    }, { passive: true });
})();

