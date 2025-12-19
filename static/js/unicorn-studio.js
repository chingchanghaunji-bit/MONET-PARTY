// Unicorn Studio Integration
// Project ID: JETgWpEpJYLpUm9USYby

(function() {
    'use strict';
    
    const projectId = 'JETgWpEpJYLpUm9USYby';
    const containerId = 'unicorn-studio-background';
    
    // Load Unicorn Studio SDK
    function initUnicornStudio() {
        const container = document.getElementById(containerId);
        if (!container) {
            console.warn('Unicorn Studio container not found');
            return;
        }
        
        // Create script tag to load Unicorn Studio SDK
        const script = document.createElement('script');
        script.src = 'https://cdn.unicorn.studio/unicornStudio.umd.js';
        script.async = true;
        
        script.onload = function() {
            if (window.UnicornStudio) {
                // Initialize Unicorn Studio
                window.UnicornStudio.init({
                    projectId: projectId,
                    container: container
                }).then(scenes => {
                    console.log('Unicorn Studio scenes loaded:', scenes);
                }).catch((err) => {
                    console.error('Unicorn Studio initialization error:', err);
                    // Fallback: use iframe embed
                    fallbackEmbed(container);
                });
            } else {
                console.error('Unicorn Studio SDK not loaded');
                fallbackEmbed(container);
            }
        };
        
        script.onerror = function() {
            console.error('Failed to load Unicorn Studio SDK');
            fallbackEmbed(container);
        };
        
        document.head.appendChild(script);
    }
    
    // Fallback to iframe embed if SDK fails
    function fallbackEmbed(container) {
        const iframe = document.createElement('iframe');
        iframe.src = `https://www.unicorn.studio/embed/${projectId}`;
        iframe.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
            pointer-events: none;
        `;
        container.appendChild(iframe);
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initUnicornStudio);
    } else {
        initUnicornStudio();
    }
    
    // Cleanup function
    window.cleanupUnicornStudio = function() {
        if (window.UnicornStudio && window.UnicornStudio.destroy) {
            window.UnicornStudio.destroy();
        }
    };
})();

