import socket
import json

def test_script():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 19222))
        
        script = """
        (function() {
            const images = document.querySelectorAll('img');
            const data = [];
            for (const img of images) {
                // look for interactive elements near the image (parent's children, etc)
                const container = img.closest('.prose') || img.parentElement;
                if (!container) continue;
                
                const buttons = container.querySelectorAll('button, [role="button"], a');
                const btnData = Array.from(buttons).map(b => ({
                    text: b.textContent.trim(),
                    ariaLabel: b.getAttribute('aria-label'),
                    className: b.className
                }));
                
                data.push({
                    imgSrc: img.src.substring(0, 50),
                    nearbyButtons: btnData
                });
            }
            return data;
        })()
        """
        
        request = {
            "requestId": 1,
            "action": "executeScript",
            "provider": "grok",
            "data": { "script": script }
        }
        
        s.sendall((json.dumps(request) + '\n').encode('utf-8'))
        
        response_bytes = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response_bytes += chunk
            if b'\n' in chunk:
                break
                
        resp = json.loads(response_bytes.decode('utf-8'))
        print(json.dumps(resp, indent=2))
        s.close()
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_script()
