let lastSelectedText = '';

// Handle text selection
document.addEventListener('mouseup', function(event) {
    const selectedText = window.getSelection().toString().trim();
    
    if (selectedText && selectedText !== lastSelectedText) {
        lastSelectedText = selectedText;
        
        // Send message to background script
        chrome.runtime.sendMessage({
            type: 'textSelected',
            text: selectedText
        });
    }
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
                
                // Send message to background script
                chrome.runtime.sendMessage({
                    type: 'textSelected',
                    text: selectedText
                });
            }
        }
    }
}); 