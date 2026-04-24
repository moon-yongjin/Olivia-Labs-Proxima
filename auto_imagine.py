import socket
import json
import time

def send_ipc(action, data):
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
    try:
        return json.loads(resp_bytes.decode('utf-8'))
    except:
        return None

prompts = [
    "Part 1: Classic hand-drawn Tom and Jerry animation style. Tom (gray cat) is mid-run with a giant wooden mallet raised high, Jerry (brown mouse) is a blur of motion diving into a small mousehole in a white baseboard. 1940s vintage living room with a checked rug. High-key cartoon lighting, vibrant Technicolor palette, 35mm classic cartoon aesthetic, high quality clean lines.",
    "Part 2: Classic hand-drawn 1940s Tom and Jerry animation style. Close-up of Tom's furry gray foot hovering inches above a comically large red mousetrap on a black and white tiled kitchen floor. Jerry (brown mouse) is peeking from behind a green flowerpot in the corner, holding his hand over his mouth to giggle. Dramatic lighting.",
    "Part 3: Classic 1940s Tom and Jerry hand-drawn animation style. Tom is comically flattened against a yellow kitchen wall like paper, with dazed yellow stars circling his head. Jerry is sitting happily on the kitchen counter, eating a large wedge of Swiss cheese and winking at the camera. Bright morning light."
]

def generate_and_animate():
    for i, prompt in enumerate(prompts):
        print(f"Generating Part {i+1}...")
        
        # 1. Inject prompt and submit
        script = f"""
        (function() {{
            const editor = document.querySelector('.tiptap');
            if(editor) {{
                editor.textContent = {json.dumps(prompt)};
                // Find and click the submit/generate button next to it
                const submitBtn = Array.from(document.querySelectorAll('button')).find(b => 
                    b.innerHTML.includes('생성') || b.innerHTML.includes('Generate') || 
                    b.getAttribute('aria-label') === '제출' || b.getAttribute('aria-label') === 'Submit'
                );
                if(submitBtn) {{
                    submitBtn.click();
                    return 'Submitted via button';
                }} else {{
                    // Try to dispatch Enter key
                    editor.dispatchEvent(new KeyboardEvent('keydown', {{'key': 'Enter', 'code': 'Enter', 'bubbles': true}}));
                    return 'Submitted via Enter';
                }}
            }}
            return 'Editor not found';
        }})()
        """
        res = send_ipc("executeScript", {"script": script})
        print(f"Submission status: {res}")
        
        # Wait for generation (usually takes 15-20s)
        print("Waiting 25 seconds for image to generate...")
        time.sleep(25)
        
        # 2. Find the newest "동영상 만들기" button and click it
        anim_script = """
        (function() {
            const buttons = Array.from(document.querySelectorAll('button[aria-label*="동영상"], button[aria-label*="video"], button[aria-label*="Animate"]'));
            if(buttons.length > 0) {
                // The newest one is likely the last one in the DOM
                buttons[buttons.length - 1].click();
                return 'Clicked Animate: ' + buttons.length;
            }
            return 'No animate button found';
        })()
        """
        res = send_ipc("executeScript", {"script": anim_script})
        print(f"Animate status: {res}")
        
        print(f"Part {i+1} done. Waiting 5s before next.\n")
        time.sleep(5)

if __name__ == "__main__":
    generate_and_animate()
