from PIL import Image
import os

def slice_logos():
    source_path = r"C:/Users/matar/.gemini/antigravity/brain/47be8269-e14b-495b-8901-9c35d941172e/uploaded_image_1764642987946.jpg"
    output_dir = r"c:\Users\matar\.gemini\antigravity\scratch\phone-recycle-site-premium"
    
    if not os.path.exists(source_path):
        print(f"Error: Source file not found at {source_path}")
        return

    try:
        img = Image.open(source_path)
    except Exception as e:
        print(f"Error opening image: {e}")
        return

    # The image has 6 logos horizontally. 
    # We'll do a simple equal width split first, as they look evenly spaced.
    # If that fails, we might need manual coordinates.
    
    width, height = img.size
    num_logos = 6
    logo_width = width // num_logos
    
    logos = [
        "logo-gov.png",
        "logo-police.png",
        "logo-samsung.png",
        "logo-apple.png",
        "logo-sk.png",
        "logo-himart.png"
    ]
    
    # Manual adjustments based on visual estimation if equal split is risky?
    # Let's try equal split first, it's usually a good starting point for these generated images.
    # Actually, looking at the image, there is whitespace. 
    # Let's try to find bounding boxes of non-white content.
    
    # Convert to grayscale and invert
    gray = img.convert('L')
    bw = gray.point(lambda x: 0 if x > 240 else 255, '1')
    
    # Find bounding box of all content
    bbox = bw.getbbox()
    if bbox:
        # Crop to content first
        img_cropped = img.crop(bbox)
        bw_cropped = bw.crop(bbox)
        width, height = img_cropped.size
    else:
        img_cropped = img
        bw_cropped = bw
        
    # Now try to split horizontally by finding vertical gaps
    # We project to 1D (x-axis)
    import numpy as np
    
    # Simple approach: Split into 6 equal parts after cropping whitespace
    # This is risky if they are not equal. 
    # Let's just do a hardcoded split based on the visual aspect ratio or just 6 equal chunks.
    # The user wants "pretty square boxes", so even if the crop isn't perfect, 
    # centering it in a box might work.
    
    # Let's try a smarter split: finding columns with no pixels.
    
    pixels = bw_cropped.load()
    
    empty_cols = []
    for x in range(width):
        is_empty = True
        for y in range(height):
            if pixels[x, y] > 0: # Content exists
                is_empty = False
                break
        if is_empty:
            empty_cols.append(x)
            
    # Find gaps
    gaps = []
    if empty_cols:
        current_gap = [empty_cols[0]]
        for i in range(1, len(empty_cols)):
            if empty_cols[i] == empty_cols[i-1] + 1:
                current_gap.append(empty_cols[i])
            else:
                if len(current_gap) > 10: # Minimum gap width
                    gaps.append(sum(current_gap) // len(current_gap))
                current_gap = [empty_cols[i]]
        if len(current_gap) > 10:
            gaps.append(sum(current_gap) // len(current_gap))
            
    # We expect 5 gaps for 6 items
    print(f"Found {len(gaps)} gaps.")
    
    # If detection fails, fallback to equal split
    boundaries = [0] + gaps + [width]
    
    # If we don't have enough boundaries, force equal split
    if len(boundaries) != 7:
        print("Gap detection failed or didn't match 6 items. Falling back to equal split.")
        boundaries = [i * (width // 6) for i in range(7)]
        
    for i in range(6):
        left = boundaries[i]
        right = boundaries[i+1]
        
        # Add some padding or just crop
        logo_slice = img_cropped.crop((left, 0, right, height))
        
        # Trim whitespace from the slice itself
        logo_bw = logo_slice.convert('L').point(lambda x: 0 if x > 240 else 255, '1')
        logo_bbox = logo_bw.getbbox()
        if logo_bbox:
            logo_slice = logo_slice.crop(logo_bbox)
            
        save_path = os.path.join(output_dir, logos[i])
        logo_slice.save(save_path)
        print(f"Saved {save_path}")

if __name__ == "__main__":
    slice_logos()
