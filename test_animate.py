import socket
import json

def test_animate():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 19222))
        print("Connected to Agent Hub IPC port 19222")
        
        request = {
            "requestId": 1,
            "action": "grokAnimate",
            "provider": "grok",
            "data": {}
        }
        
        s.sendall((json.dumps(request) + '\n').encode('utf-8'))
        
        response = s.recv(4096)
        print("Received response:", response.decode('utf-8'))
        s.close()
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_animate()
