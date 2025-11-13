/**
 * Jodit Editor Initialization Script for Django
 * 
 * This script initializes Jodit editor instances for textareas
 * that have been marked with jodit configuration data.
 * 
 * Supports automatic dark theme detection from:
 * - Django admin dark mode (data-theme="dark")
 * - System prefers-color-scheme
 * - Custom theme settings
 */

(function() {
    'use strict';

    /**
     * Detect if dark theme should be used
     * Compatible with Django admin's dark mode
     */
    function isDarkTheme() {
        // Check Django admin dark mode (Django 3.2+)
        const htmlElement = document.documentElement;
        const adminTheme = htmlElement.getAttribute('data-theme');
        if (adminTheme === 'dark') {
            return true;
        } else if (adminTheme === 'auto') {
            // Check system preference
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                return true;
            }
        }
        
        // Check for dark mode class (some admin themes)
        if (document.body.classList.contains('theme-dark') || 
            document.body.classList.contains('dark-mode') ||
            htmlElement.classList.contains('dark-mode')) {
            return true;
        }
        
        return false;
    }

    /**
     * Initialize a single Jodit editor instance
     */
    function initJoditEditor(textarea) {
        // Skip if already processed
        if (textarea.getAttribute('data-processed') === '1') {
            return;
        }

        // Get configuration from data attribute
        const configData = textarea.getAttribute('data-jodit-config');
        let config = {};
        
        if (configData) {
            try {
                config = JSON.parse(configData);
            } catch (e) {
                console.error('Failed to parse Jodit config:', e);
            }
        }

        // Handle theme configuration
        // If theme is 'auto' or not specified, detect automatically
        if (!config.theme || config.theme === 'auto') {
            config.theme = isDarkTheme() ? 'dark' : 'default';
        }

        // Initialize Jodit editor
        try {
            const editor = Jodit.make(textarea, config);
            textarea.setAttribute('data-processed', '1');
            
            // Store editor instance for potential future access
            textarea.joditEditor = editor;
            
            // Watch for theme changes (Django admin theme switcher)
            observeThemeChanges(editor, config);
        } catch (e) {
            console.error('Failed to initialize Jodit editor:', e);
        }
    }

    /**
     * Observe theme changes and update editor accordingly
     */
    function observeThemeChanges(editor, originalConfig) {
        // Watch for changes to data-theme attribute on html element
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.attributeName === 'data-theme') {
                    const newTheme = isDarkTheme() ? 'dark' : 'default';
                    if (editor.options && editor.options.theme !== newTheme) {
                        // Update theme if it changed
                        editor.options.theme = newTheme;
                        // Recreate editor with new theme
                        const textarea = editor.element;
                        editor.destruct();
                        textarea.setAttribute('data-processed', '0');
                        initJoditEditor(textarea);
                    }
                }
            });
        });

        // Observe html element for theme changes
        observer.observe(document.documentElement, {
            attributes: true,
            attributeFilter: ['data-theme']
        });

        // Also listen for prefers-color-scheme changes
        if (window.matchMedia) {
            const darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');
            darkModeQuery.addEventListener('change', function(e) {
                if (!originalConfig.theme || originalConfig.theme === 'auto') {
                    const newTheme = e.matches ? 'dark' : 'default';
                    if (editor.options && editor.options.theme !== newTheme) {
                        editor.options.theme = newTheme;
                        const textarea = editor.element;
                        editor.destruct();
                        textarea.setAttribute('data-processed', '0');
                        initJoditEditor(textarea);
                    }
                }
            });
        }
    }

    /**
     * Initialize all Jodit editors on the page
     */
    function initAllJoditEditors() {
        const textareas = document.querySelectorAll('textarea[data-jodit-config][data-processed="0"]');
        textareas.forEach(initJoditEditor);
    }

    /**
     * Wait for Jodit library to be loaded
     */
    function waitForJodit() {
        if (typeof Jodit !== 'undefined') {
            initAllJoditEditors();
        } else {
            setTimeout(waitForJodit, 50);
        }
    }

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', waitForJodit);
    } else {
        waitForJodit();
    }

    // Support for Django admin inline forms (dynamically added forms)
    if (typeof django !== 'undefined' && django.jQuery) {
        django.jQuery(document).on('formset:added', function(event, row) {
            const textareas = row.find('textarea[data-jodit-config][data-processed="0"]');
            textareas.each(function() {
                initJoditEditor(this);
            });
        });
    }

    // Expose initialization function globally for manual initialization
    window.initJoditEditor = initJoditEditor;
    window.initAllJoditEditors = initAllJoditEditors;
})();
