import socket
import json
import time

def send_ipc(action, data):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 19222))
        request = {"requestId": 1, "action": action, "provider": "grok", "data": data}
        s.sendall((json.dumps(request) + '\n').encode('utf-8'))
        resp_bytes = b""
        while True:
            chunk = s.recv(4096)
            if not chunk: break
            resp_bytes += chunk
            if b'\n' in chunk: break
        s.close()
        return json.loads(resp_bytes.decode('utf-8'))
    except:
        return None

prompts = [
    "Intense 1990s Japanese sports anime style (Slam Dunk aesthetic). A young basketball player with fiery red spiky hair, screaming with determination, jumping high in the air for a powerful two-handed slam dunk. Ink-brushed shadows, sweat drops glistening, high-contrast cinematic court lighting. Hand-drawn cell animation look.",
    "Stoic ace basketball player with black hair in 90s anime style. Close-up mid-air jump shot, focused eyes, ball leaving the hand with perfect form. Sweating skin, dramatic spotlights. Sharp lines, vibrant but classic colors, cinematic framing, 35mm film grain.",
    "A team of 5 basketball players in red uniforms standing on a basketball court, determined expressions. Volumetric sunset light rays filtering through large gym windows, golden hour glow. Iconic 90s sports anime aesthetic, hand-painted painterly background, epic cinematic atmosphere."
]

def generate_and_animate():
    for i, prompt in enumerate(prompts):
        print(f"--- Scene {i+1} Start ---")
        
        # [Step 0] Reset Imagine UI
        send_ipc("executeScript", {"script": "const m = Array.from(document.querySelectorAll('a, div[role=\\\"button\\\"]')).find(el => (el.textContent || '').includes('Imagine')); if(m) m.click();"})
        time.sleep(5)
        
        # [Step 1] Inject prompt and FORCE ENTER
        print(f"Injecting Prompt and Pressing ENTER for Scene {i+1}...")
        script = f"""
        (function() {{
            const editor = document.querySelector('.tiptap');
            if(editor) {{
                editor.focus();
                // Clear and insert text via execCommand for better compatibility
                document.execCommand('selectAll', false, null);
                document.execCommand('delete', false, null);
                document.execCommand('insertText', false, {json.dumps(prompt)});
                
                // Try clicking the button first (most reliable)
                const buttons = Array.from(document.querySelectorAll('button'));
                const submitBtn = buttons.find(b => 
                    b.innerHTML.includes('생성') || b.innerHTML.includes('Generate') || 
                    b.getAttribute('aria-label') === '제출' || b.getAttribute('aria-label') === 'Submit' ||
                    b.getAttribute('aria-label') === '제작' || b.className.includes('primary')
                );
                
                if(submitBtn) {{
                    submitBtn.focus();
                    submitBtn.click();
                    return 'Clicked Submit Button';
                }} else {{
                    // Fallback: Dispatch multiple types of Enter events
                    const events = ['keydown', 'keypress', 'keyup'];
                    events.forEach(type => {{
                        const ev = new KeyboardEvent(type, {{
                            key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true, cancelable: true
                        }});
                        editor.dispatchEvent(ev);
                    }});
                    return 'Dispatched Enter Events';
                }}
            }}
            return 'Editor not found';
        }})()
        """
        send_ipc("executeScript", {"script": script})
        
        # [Step 2] Polling for the Animate button
        print(f"Waiting for image and Animate button...")
        found = False
        for attempt in range(12): 
            time.sleep(5)
            anim_script = """
            (function() {
                const buttons = Array.from(document.querySelectorAll('button[aria-label*="동영상"], button[aria-label*="video"], button[aria-label*="Animate"]'));
                if(buttons.length > 0) {
                    buttons[buttons.length - 1].click();
                    return 'Clicked Animate';
                }
                return 'Not found';
            })()
            """
            res = send_ipc("executeScript", {"script": anim_script})
            if res and res.get('result') != 'Not found':
                print(f"Success: {res.get('result')}")
                found = True
                break
            print(f"Attempt {attempt+1}: Still waiting...")
            
        print(f"Scene {i+1} finished.\n")
        time.sleep(3)

if __name__ == "__main__":
    generate_and_animate()
