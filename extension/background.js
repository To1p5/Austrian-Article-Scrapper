let currentPopup = null;

// Handle messages from content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'textSelected') {
        const selectedText = message.text;
        
        // Close existing popup if any
        if (currentPopup) {
            chrome.windows.remove(currentPopup);
            currentPopup = null;
        }
        
        // Convert text to speech
        fetch('http://localhost:5000/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: selectedText
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.filename) {
                chrome.storage.local.set({
                    'lastAudio': `http://localhost:5000/audio/${data.filename}`,
                    'lastText': data.text
                });
                
                // Create new popup
                chrome.windows.create({
                    url: 'player.html',
                    type: 'popup',
                    width: 300,
                    height: 150,
                    left: 100,
                    top: 100
                }, (window) => {
                    currentPopup = window.id;
                });
            }
        })
        .catch(error => console.error('Error:', error));
    }
});

// Keep the context menu for right-click functionality
chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
        id: "convertToSpeech",
        title: "Listen with TTS",
        contexts: ["selection"]
    });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === "convertToSpeech") {
        const selectedText = info.selectionText;
        
        // Use the same conversion logic as above
        fetch('http://localhost:5000/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: selectedText
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.filename) {
                chrome.storage.local.set({
                    'lastAudio': `http://localhost:5000/audio/${data.filename}`,
                    'lastText': data.text
                });
                
                if (currentPopup) {
                    chrome.windows.remove(currentPopup);
                }
                
                chrome.windows.create({
                    url: 'player.html',
                    type: 'popup',
                    width: 300,
                    height: 150,
                    left: 100,
                    top: 100
                }, (window) => {
                    currentPopup = window.id;
                });
            }
        })
        .catch(error => console.error('Error:', error));
    }
});

// Add a context menu item to stop audio
chrome.contextMenus.create({
  id: "stopSpeech",
  title: "Stop Speech",
  contexts: ["all"]
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "stopSpeech" && currentAudio) {
    currentAudio.pause();
    currentAudio = null;
  }
}); 