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
        
        # [Step 0] Reset Imagine UI by clicking Imagine menu
        print("Resetting Imagine UI...")
        reset_script = """
        (function() {
            const menus = document.querySelectorAll('a, div[role="button"]');
            for (const m of menus) {
                if ((m.textContent || '').includes('Imagine')) {
                    m.click();
                    return 'Clicked Imagine Reset';
                }
            }
            return 'Imagine menu not found';
        })()
        """
        send_ipc("executeScript", {"script": reset_script})
        time.sleep(2) # Wait for UI to settle
        
        # [Step 1] Inject prompt and submit
        print(f"Injecting Prompt for Scene {i+1}...")
        script = f"""
        (function() {{
            const editor = document.querySelector('.tiptap');
            if(editor) {{
                editor.textContent = {json.dumps(prompt)};
                const submitBtn = Array.from(document.querySelectorAll('button')).find(b => 
                    b.innerHTML.includes('생성') || b.innerHTML.includes('Generate') || 
                    b.getAttribute('aria-label') === '제출' || b.getAttribute('aria-label') === 'Submit' ||
                    b.getAttribute('aria-label') === '제작'
                );
                if(submitBtn) {{
                    submitBtn.click();
                    return 'Submitted via button';
                }}
                editor.dispatchEvent(new KeyboardEvent('keydown', {{'key': 'Enter', 'code': 'Enter', 'bubbles': true}}));
                return 'Submitted via Enter';
            }}
            return 'Editor not found';
        }})()
        """
        send_ipc("executeScript", {"script": script})
        
        print("Waiting 25 seconds for image to generate...")
        time.sleep(25)
        
        # [Step 2] Click Animate
        print("Clicking Animate/Make Video button...")
        anim_script = """
        (function() {
            const buttons = Array.from(document.querySelectorAll('button[aria-label*="동영상"], button[aria-label*="video"], button[aria-label*="Animate"]'));
            if(buttons.length > 0) {
                buttons[buttons.length - 1].click();
                return 'Clicked Animate: ' + buttons.length;
            }
            return 'No animate button found';
        })()
        """
        res = send_ipc("executeScript", {"script": anim_script})
        print(f"Animate Result: {res}")
        
        print(f"Scene {i+1} process complete. Waiting 5s for next session.\n")
        time.sleep(5)

if __name__ == "__main__":
    generate_and_animate()
