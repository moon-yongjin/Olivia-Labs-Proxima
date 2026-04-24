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
    except Exception as e:
        print(f"IPC Error: {e}")
        return None

prompts = [
    "Intense 1990s Japanese sports anime style (Slam Dunk aesthetic). A young basketball player with fiery red spiky hair, screaming with determination, jumping high in the air for a powerful two-handed slam dunk. Ink-brushed shadows, sweat drops glistening, high-contrast cinematic court lighting. Hand-drawn cell animation look.",
    "Stoic ace basketball player with black hair in 90s anime style. Close-up mid-air jump shot, focused eyes, ball leaving the hand with perfect form. Sweating skin, dramatic spotlights. Sharp lines, vibrant classic colors, cinematic framing, 35mm film grain.",
    "A team of 5 basketball players in red uniforms standing on a basketball court, determined expressions. Volumetric sunset light rays filtering through large gym windows, golden hour glow. Iconic 90s sports anime aesthetic, hand-painted background, epic cinematic atmosphere."
]

def wait_for_animate_button(max_tries=12):
    """Poll until '동영상 만들기' button appears, then click it."""
    for attempt in range(max_tries):
        time.sleep(5)
        res = send_ipc("executeScript", {"script": """
            (function() {
                const buttons = Array.from(document.querySelectorAll('button[aria-label*="동영상"], button[aria-label*="Animate"], button[aria-label*="video"]'));
                if(buttons.length > 0) {
                    buttons[buttons.length - 1].click();
                    return 'Clicked: ' + buttons[buttons.length - 1].getAttribute('aria-label');
                }
                return 'Not found';
            })()
        """})
        result = res.get('result', 'Not found') if res else 'Error'
        print(f"  Animate check {attempt+1}/12: {result}")
        if result != 'Not found' and result != 'Error':
            return True
    return False

def run():
    for i, prompt in enumerate(prompts):
        print(f"\n{'='*40}")
        print(f"Scene {i+1}/3 starting...")
        print(f"{'='*40}")

        # Use the new sendToImagine handler — OS-level input, guaranteed Enter
        print("Sending prompt via sendToImagine (OS-level Enter)...")
        res = send_ipc("sendToImagine", {"prompt": prompt})
        print(f"Submit result: {res}")

        if not res or not res.get('success'):
            print(f"Scene {i+1} submission failed, skipping.")
            continue

        print("Waiting for image generation + Animate button...")
        found = wait_for_animate_button()

        if found:
            print(f"Scene {i+1} animated successfully!")
        else:
            print(f"Scene {i+1}: Animate button never appeared after 60s.")

        print(f"Cooldown 5s before next scene...")
        time.sleep(5)

    print("\nAll 3 scenes done!")

if __name__ == "__main__":
    run()
