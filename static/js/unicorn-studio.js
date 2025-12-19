// Unicorn Studio Integration
// Project ID: JETgWpEpJYLpUm9USYby
// Embed URL: https://www.unicorn.studio/embed/JETgWpEpJYLpUm9USYby

(function() {
    'use strict';
    
    const projectId = 'JETgWpEpJYLpUm9USYby';
    const containerId = 'unicorn-studio-background';
    const embedUrl = `https://www.unicorn.studio/embed/${projectId}`;
    
    function initUnicornStudio() {
        const container = document.getElementById(containerId);
        if (!container) {
            console.warn('Unicorn Studio container not found');
            return;
        }
        
        // Try to load Unicorn Studio SDK first
        const script = document.createElement('script');
        script.src = 'https://www.unicorn.studio/sdk/unicornStudio.umd.js';
        script.async = true;
        
        script.onload = function() {
            // Check if SDK loaded successfully
            if (window.UnicornStudio && typeof window.UnicornStudio.init === 'function') {
                // Use JavaScript API
                window.UnicornStudio.init({
                    projectId: projectId,
                    container: container
                }).then(scenes => {
                    console.log('Unicorn Studio initialized successfully:', scenes);
                }).catch((err) => {
                    console.warn('Unicorn Studio SDK init failed, using iframe fallback:', err);
                    createIframeEmbed(container);
                });
            } else {
                // SDK not available, use iframe embed
                createIframeEmbed(container);
            }
        };
        
        script.onerror = function() {
            // SDK failed to load, use iframe embed
            console.log('Unicorn Studio SDK not available, using iframe embed');
            createIframeEmbed(container);
        };
        
        // Try loading SDK, but don't wait too long
        document.head.appendChild(script);
        
        // Fallback timeout - use iframe if SDK doesn't load quickly
        setTimeout(() => {
            if (!container.querySelector('iframe') && !container.querySelector('canvas')) {
                createIframeEmbed(container);
            }
        }, 2000);
    }
    
    // Create iframe embed (reliable fallback)
    function createIframeEmbed(container) {
        // Remove any existing content
        container.innerHTML = '';
        
        const iframe = document.createElement('iframe');
        iframe.src = embedUrl;
        iframe.allow = 'autoplay; fullscreen';
        iframe.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
            pointer-events: none;
            z-index: -1;
        `;
        iframe.setAttribute('loading', 'eager');
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
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = '';
        }
        if (window.UnicornStudio && typeof window.UnicornStudio.destroy === 'function') {
            window.UnicornStudio.destroy();
        }
    };
})();

