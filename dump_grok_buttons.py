import socket
import json

def test_script():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 19222))
        
        script = """
        (function() {
            return Array.from(document.querySelectorAll('button')).map(b => ({
                text: b.textContent.trim(),
                ariaLabel: b.getAttribute('aria-label'),
                className: b.className
            })).filter(b => b.text || b.ariaLabel);
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
        if 'result' in resp:
            for b in resp['result']:
                print(f"Text: '{b.get('text', '')}', Aria-Label: '{b.get('ariaLabel', '')}', Class: '{b.get('className', '')}'")
        else:
            print(resp)
        s.close()
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_script()
