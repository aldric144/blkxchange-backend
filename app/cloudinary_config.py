import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME", "demo"),
    api_key=os.getenv("CLOUDINARY_API_KEY", ""),
    api_secret=os.getenv("CLOUDINARY_API_SECRET", ""),
    secure=True
)

def upload_image_to_cloudinary(file_content, filename, folder="blkxchange"):
    """
    Upload an image to Cloudinary and return the secure URL
    
    Args:
        file_content: Binary file content
        filename: Original filename
        folder: Cloudinary folder to store the image
    
    Returns:
        dict: Upload result with secure_url
    """
    try:
        result = cloudinary.uploader.upload(
            file_content,
            folder=folder,
            resource_type="auto",
            public_id=filename.split('.')[0],
            overwrite=True,
            transformation=[
                {'width': 800, 'height': 800, 'crop': 'limit'},
                {'quality': 'auto:good'}
            ]
        )
        return {
            "success": True,
            "url": result['secure_url'],
            "public_id": result['public_id'],
            "format": result['format'],
            "width": result['width'],
            "height": result['height'],
            "bytes": result['bytes']
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def delete_image_from_cloudinary(public_id):
    """
    Delete an image from Cloudinary
    
    Args:
        public_id: Cloudinary public ID of the image
    
    Returns:
        dict: Deletion result
    """
    try:
        result = cloudinary.uploader.destroy(public_id)
        return {
            "success": result['result'] == 'ok',
            "result": result['result']
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
