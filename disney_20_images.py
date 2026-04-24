import subprocess
import time

prompt1 = """Generate exactly 10 separate images in a single response, sequentially telling a story. 
Style: 1950s classic Disney hand-drawn 2D cell animation, vintage colors, magical forest aesthetic, cinematic lighting. 
Sequential Story Part 1:
1) A brave little brown rabbit finds a glowing vintage map in the forest.
2) The rabbit packs a small bindle on a stick.
3) The rabbit meets a grumpy old owl wearing spectacles on a tree branch.
4) The owl points its wing toward a dark mountain in the distance.
5) The rabbit bravely crosses a sparkling stream by jumping on lily pads.
6) A mischievous squirrel drops an acorn on the rabbit's head, comical expression.
7) The rabbit discovers a hidden cave glowing with blue crystals.
8) Inside the cave, a tiny baby dragon is sleeping curled up.
9) The baby dragon wakes up and does a big cute yawn.
10) The dragon and the rabbit smile at each other, becoming friends."""

prompt2 = """Now generate exactly 10 more separate images to continue the story, keeping the exact same 1950s classic Disney hand-drawn animation style.
Sequential Story Part 2:
11) The baby dragon and rabbit flying out of the crystal cave together.
12) They soar high above fluffy white clouds.
13) They spot a beautiful glittering fairy castle on a floating island.
14) Landing in the castle courtyard full of giant sparkling magical flowers.
15) The elegant Fairy Queen greets them with a glowing star wand.
16) The Queen presents the rabbit with a shiny magical golden carrot.
17) A grand feast at a long wooden table with all the forest animals.
18) A breathtaking sunset over the floating island, painted sky.
19) The dragon and rabbit sleeping peacefully together under a starry night sky.
20) Close-up shot of the golden carrot glowing softly in the dark. End of story."""

def run():
    print("Starting 20-image Disney Storyboard Session...")
    
    print("\n[Batch 1/2] Sending Prompt 1 (Images 1-10)...")
    subprocess.run([
        "python3", 
        "/Users/a12/.gemini/antigravity/skills/proxima/scripts/proxima_helper.py", 
        "chat", prompt1, "--model", "grok"
    ])
    
    print("\nWaiting 180 seconds for Grok to render 10 images...")
    time.sleep(180)
    
    print("\n[Batch 2/2] Sending Prompt 2 (Images 11-20)...")
    subprocess.run([
        "python3", 
        "/Users/a12/.gemini/antigravity/skills/proxima/scripts/proxima_helper.py", 
        "chat", prompt2, "--model", "grok"
    ])
    
    print("\nSession complete! 20 images generated.")

if __name__ == "__main__":
    run()
