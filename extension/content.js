let lastSelectedText = '';
let selectionTimeout;

// Handle text selection
document.addEventListener('mouseup', function(event) {
    // Clear any existing timeout
    clearTimeout(selectionTimeout);
    
    // Wait a brief moment to ensure selection is complete
    selectionTimeout = setTimeout(() => {
        const selectedText = window.getSelection().toString().trim();
        
        // Only proceed if we have new selected text
        if (selectedText && selectedText !== lastSelectedText) {
            lastSelectedText = selectedText;
            
            // Send message to background script with coordinates
            chrome.runtime.sendMessage({
                type: 'textSelected',
                text: selectedText,
                x: event.clientX,
                y: event.clientY
            });
        }
    }, 200); // Small delay to ensure selection is complete
});

// Reset last selected text when mouse is pressed
document.addEventListener('mousedown', function() {
    lastSelectedText = '';
});

// Handle single word click
document.addEventListener('click', function(event) {
    if (event.target.nodeType === Node.TEXT_NODE || 
        event.target.tagName === 'P' || 
        event.target.tagName === 'SPAN' || 
        event.target.tagName === 'DIV') {
        
        const range = document.caretRangeFromPoint(event.clientX, event.clientY);
        if (range) {
            range.expand('word');
            const selectedText = range.toString().trim();
            
            if (selectedText && selectedText !== lastSelectedText) {
                lastSelectedText = selectedText;
                
                // Send message to background script with coordinates
                chrome.runtime.sendMessage({
                    type: 'textSelected',
                    text: selectedText,
                    x: event.clientX,
                    y: event.clientY
                });
            }
        }
    }
}); 