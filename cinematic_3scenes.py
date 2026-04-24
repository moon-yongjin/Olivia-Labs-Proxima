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
    # Scene 1: Chrysler Reveal — Old man in skyscraper
    "The clouds are stagnant. Camera zooms quickly into the small window of the Chrysler Building, revealing an old bearded man in a black suit, full body, looking down at the city from a large dark conference room. Behind the cold glass, his expression is determined and serious. Cinematic hyperrealistic photography.",
    # Scene 2: Neon Tokyo Street — Cyberpunk rain
    "Aerial shot of a neon-drenched Tokyo alley at midnight, heavy rain, steam rising from the street. A lone figure in a black trench coat walks alone, back to camera, under a red lantern. Volumetric neon lighting, rim light, shallow depth of field, ultra-realistic cinematic photography, blade runner aesthetic.",
    # Scene 3: Ancient Samurai Temple — Golden hour
    "An aged samurai in full black armor kneeling at a stone temple altar at golden hour, hands resting on the hilt of his sword, cherry blossoms drifting through the air. Cinematic volumetric sunlight through ancient wooden beams, shallow depth of field, wide-angle shot, ultra-realistic photorealism."
]

def wait_for_animate_button(max_tries=12):
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
    scene_names = ["Chrysler Building Reveal", "Neon Tokyo Rain", "Ancient Samurai Temple"]
    for i, prompt in enumerate(prompts):
        print(f"\n{'='*45}")
        print(f"Scene {i+1}/3: {scene_names[i]}")
        print(f"{'='*45}")

        res = send_ipc("sendToImagine", {"prompt": prompt})
        print(f"Submit: {res}")

        print("Waiting for Animate button...")
        found = wait_for_animate_button()
        print(f"{'Animated!' if found else 'Animate button not found after 60s'}\n")

        time.sleep(5)

    print("All 3 scenes done!")

if __name__ == "__main__":
    run()
