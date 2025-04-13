import os
from PIL import Image, ImageDraw, ImageFont

def create_favicon():
    """Generate a simple favicon for Piga Kura"""
    # Create directories if they don't exist
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', 'static')
    images_dir = os.path.join(static_dir, 'images')
    
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
        print(f"Created directory: {images_dir}")
    
    # Create a 32x32 white image with a blue "PK" text
    img = Image.new('RGB', (32, 32), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    
    try:
        # Try to use a default font, if available
        font = ImageFont.truetype("arial.ttf", 16)
    except IOError:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Draw "PK" in blue
    d.text((8, 8), "PK", fill=(0, 123, 255), font=font)
    
    # Save as favicon.ico
    favicon_path = os.path.join(images_dir, 'favicon.ico')
    img.save(favicon_path)
    print(f"Created favicon at: {favicon_path}")
    
    # Create a larger version for Apple devices
    img_apple = Image.new('RGB', (180, 180), color=(255, 255, 255))
    d_apple = ImageDraw.Draw(img_apple)
    
    try:
        # Try to use a default font, if available
        font_apple = ImageFont.truetype("arial.ttf", 80)
    except IOError:
        # Fallback to default font, but scale it up
        font_apple = ImageFont.load_default()
    
    # Draw "PK" in blue
    d_apple.text((40, 50), "PK", fill=(0, 123, 255), font=font_apple)
    
    # Save as apple-touch-icon.png
    apple_icon_path = os.path.join(images_dir, 'apple-touch-icon.png')
    img_apple.save(apple_icon_path)
    print(f"Created Apple Touch icon at: {apple_icon_path}")

if __name__ == "__main__":
    create_favicon()
    print("\nFavicon added successfully!")
    print("Please make sure PIL/Pillow is installed (pip install pillow) to run this script.")
    print("The favicon and Apple Touch icon have been added to your static/images directory.")
    print("The base.html template has been updated to include the favicon references.")
