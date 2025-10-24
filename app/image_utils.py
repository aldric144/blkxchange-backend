"""
Image processing utilities for BlkXchange™
Handles image upload, optimization, resizing, and watermarking
"""
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io

UPLOAD_DIR = Path("/home/ubuntu/blkxchange/blkxchange-backend/uploads")
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB (increased from 2MB)
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

IMAGE_SIZES = {
    "logo": (300, 300),
    "product": (600, 600),
    "ad": (600, 600),
    "profile": (300, 300),
}

COMPRESSION_TARGETS = {
    "logo": 200,
    "product": 400,
    "ad": 500,
    "profile": 200,
}


def ensure_upload_dirs():
    """Create upload directories if they don't exist"""
    for mode in ["live", "test"]:
        for section in ["vendors", "professionals", "products", "ads"]:
            dir_path = UPLOAD_DIR / mode / section
            dir_path.mkdir(parents=True, exist_ok=True)


def validate_image(file_content: bytes, filename: str) -> Tuple[bool, Optional[str]]:
    """
    Validate image file
    Returns: (is_valid, error_message)
    """
    if len(file_content) > MAX_FILE_SIZE:
        return False, "File exceeds 5MB limit"
    
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Invalid file format. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
    
    try:
        img = Image.open(io.BytesIO(file_content))
        img.verify()
        return True, None
    except Exception as e:
        return False, f"Invalid image file: {str(e)}"


def optimize_image(
    image_content: bytes,
    image_type: str,
    target_size: Optional[Tuple[int, int]] = None
) -> bytes:
    """
    Optimize and resize image with smart padding for aspect ratio mismatches
    
    Args:
        image_content: Raw image bytes
        image_type: Type of image (logo, product, ad, profile)
        target_size: Optional custom size, otherwise uses IMAGE_SIZES
    
    Returns:
        Optimized image bytes
    """
    img = Image.open(io.BytesIO(image_content))
    
    # Convert RGBA/LA/P to RGB with white background
    if img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = background
    
    if target_size is None:
        target_size = IMAGE_SIZES.get(image_type, (600, 600))
    
    img_aspect = img.width / img.height
    target_aspect = target_size[0] / target_size[1]
    
    if img_aspect > target_aspect:
        new_width = target_size[0]
        new_height = int(target_size[0] / img_aspect)
    else:
        new_height = target_size[1]
        new_width = int(target_size[1] * img_aspect)
    
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    final_img = Image.new('RGB', target_size, (255, 255, 255))
    paste_x = (target_size[0] - new_width) // 2
    paste_y = (target_size[1] - new_height) // 2
    final_img.paste(img, (paste_x, paste_y))
    
    target_kb = COMPRESSION_TARGETS.get(image_type, 400)
    quality = 85
    
    output = io.BytesIO()
    while quality > 20:
        output.seek(0)
        output.truncate()
        final_img.save(output, format='JPEG', quality=quality, optimize=True)
        size_kb = len(output.getvalue()) / 1024
        
        if size_kb <= target_kb:
            break
        quality -= 5
    
    return output.getvalue()


def add_watermark(
    image_content: bytes,
    is_verified: bool = True
) -> bytes:
    """
    Add BlkXchange™ Verified watermark to image
    
    Args:
        image_content: Optimized image bytes
        is_verified: Whether to add verified watermark
    
    Returns:
        Watermarked image bytes
    """
    if not is_verified:
        return image_content
    
    img = Image.open(io.BytesIO(image_content))
    
    draw = ImageDraw.Draw(img, 'RGBA')
    
    text = "BlkXchange™ Verified"
    
    try:
        font_size = max(16, int(img.height * 0.03))  # Scale with image size
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    padding = 10
    x = img.width - text_width - padding - 10
    y = img.height - text_height - padding - 10
    
    bg_padding = 5
    bg_rect = [
        x - bg_padding,
        y - bg_padding,
        x + text_width + bg_padding,
        y + text_height + bg_padding
    ]
    draw.rectangle(bg_rect, fill=(0, 0, 0, 128))  # Black with 50% opacity
    
    gold_color = (197, 161, 78, 179)  # #C5A14E with 70% opacity
    draw.text((x, y), text, font=font, fill=gold_color)
    
    output = io.BytesIO()
    img.save(output, format='JPEG', quality=95)
    return output.getvalue()


def save_image(
    image_content: bytes,
    section: str,
    test_mode: bool = False,
    original_filename: Optional[str] = None
) -> str:
    """
    Save image to disk and return URL path
    
    Args:
        image_content: Image bytes to save
        section: Section (vendors, professionals, products, ads)
        test_mode: Whether to save in test directory
        original_filename: Original filename for extension
    
    Returns:
        Relative URL path to saved image
    """
    ensure_upload_dirs()
    
    timestamp = int(datetime.now().timestamp())
    unique_id = str(uuid.uuid4())[:8]
    ext = Path(original_filename).suffix if original_filename else ".jpg"
    filename = f"{section}_{timestamp}_{unique_id}{ext}"
    
    mode = "test" if test_mode else "live"
    file_path = UPLOAD_DIR / mode / section / filename
    
    with open(file_path, 'wb') as f:
        f.write(image_content)
    
    return f"/uploads/{mode}/{section}/{filename}"


def process_and_save_image(
    file_content: bytes,
    filename: str,
    section: str,
    image_type: str,
    is_verified: bool = False,
    test_mode: bool = False
) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Complete image processing pipeline
    
    Args:
        file_content: Raw uploaded file bytes
        filename: Original filename
        section: Section (vendors, professionals, products, ads)
        image_type: Type for optimization (logo, product, ad, profile)
        is_verified: Whether to add verified watermark
        test_mode: Whether to save in test directory
    
    Returns:
        (success, url_path, error_message)
    """
    is_valid, error = validate_image(file_content, filename)
    if not is_valid:
        return False, None, error
    
    try:
        ensure_upload_dirs()
        
        optimized = optimize_image(file_content, image_type)
        
        final_image = add_watermark(optimized, is_verified)
        
        url_path = save_image(final_image, section, test_mode, filename)
        
        return True, url_path, None
        
    except Exception as e:
        return False, None, f"Image processing failed: {str(e)}"
