from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_image():
    # Define image dimensions
    width, height = 800, 600
    
    # Create a new image with a gradient background
    image = Image.new('RGB', (width, height), color=(240, 240, 240))
    draw = ImageDraw.Draw(image)
    
    # Draw a gradient background
    for y in range(height):
        r = int(74 + (y / height) * 50)
        g = int(107 + (y / height) * 50)
        b = int(223 + (y / height) * 50)
        for x in range(width):
            draw.point((x, y), fill=(r, g, b))
    
    # Draw a waveform-like pattern
    for x in range(0, width, 4):
        amplitude = height / 4 + (height / 8) * (0.5 + 0.5 * ((x / 30) % 10) / 10)
        for i in range(60):
            y = height / 2 + amplitude * (i / 60) * (1 if i < 30 else -1)
            draw.point((x, int(y)), fill=(255, 255, 255, 180))
    
    # Draw a border for the image
    draw.rectangle([(0, 0), (width-1, height-1)], outline=(200, 200, 200), width=2)
    
    # Add text
    try:
        # You would need to provide a font file for this to work
        # font = ImageFont.truetype("arial.ttf", 48)
        # Using default font as fallback
        font = ImageFont.load_default()
        draw.text((width/2-100, height/2-30), "Audio Forensics", fill=(255, 255, 255), font=font)
    except Exception as e:
        print(f"Could not load font: {e}")
        # Just draw a rectangle instead
        draw.rectangle([(width/2-150, height/2-40), (width/2+150, height/2+40)], fill=(255, 255, 255, 180))
    
    # Save the image
    img_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "static", "img")
    os.makedirs(img_dir, exist_ok=True)
    image_path = os.path.join(img_dir, "audio-forensics.png")
    image.save(image_path)
    
    print(f"Created placeholder image at: {image_path}")
    
    # Create a small favicon
    favicon = Image.new('RGB', (32, 32), color=(74, 107, 223))
    favicon_draw = ImageDraw.Draw(favicon)
    favicon_draw.ellipse([(8, 8), (24, 24)], fill=(255, 255, 255))
    favicon_draw.ellipse([(12, 12), (20, 20)], fill=(74, 107, 223))
    
    favicon_path = os.path.join(img_dir, "favicon.ico")
    favicon.save(favicon_path)
    print(f"Created favicon at: {favicon_path}")

if __name__ == "__main__":
    create_placeholder_image()
