# BlkXchange™ Image Upload System Documentation

## Overview

The BlkXchange™ platform features a comprehensive image upload system with drag-and-drop functionality, automatic optimization, and auto-watermarking for verified vendors and professionals.

## Features

### 1. **Drag-and-Drop File Upload**
- Intuitive drag-and-drop interface
- Click to browse files alternative
- Visual feedback during drag operations
- Real-time preview after upload

### 2. **File Validation**
- **Supported formats**: JPG, PNG, WEBP
- **Maximum file size**: 2MB
- **Validation**: Client-side and server-side validation
- **Error handling**: Clear error messages for invalid files

### 3. **Automatic Image Optimization**
- **Logos**: Resized to 512×512px, compressed to ≤300KB
- **Products**: Resized to 800×800px, compressed to ≤400KB
- **Ads**: Resized to 1200×600px, compressed to ≤500KB
- **Profiles**: Resized to 512×512px, compressed to ≤300KB
- **Format conversion**: All images converted to JPEG for consistency
- **Quality optimization**: Adaptive quality adjustment to meet size targets

### 4. **Auto-Watermarking**
- **Verified vendors/professionals**: Automatic "BlkXchange™ Verified" watermark
- **Watermark styling**:
  - Color: Gold (#C5A14E) with 70% opacity
  - Font: DejaVu Sans Bold (scaled to image size)
  - Position: Bottom-right corner with padding
  - Background: Semi-transparent black rectangle for readability
- **Clean copies**: Original optimized images saved without watermark for internal use

### 5. **Test Mode Support**
- **Test Mode**: Files saved to `/uploads/test/{section}/`
- **Live Mode**: Files saved to `/uploads/live/{section}/`
- **Sections**: vendors, professionals, products, ads

## Architecture

### Backend (FastAPI + Python)

#### Image Processing Pipeline (`app/image_utils.py`)

```python
# 1. Validation
validate_image(file_content, filename)
  - Check file size (max 2MB)
  - Verify file format (JPG, PNG, WEBP)
  - Validate image integrity

# 2. Optimization
optimize_image(image_content, image_type)
  - Convert to RGB (handle transparency)
  - Resize to target dimensions
  - Compress with adaptive quality (95% → 20%)
  - Target file sizes based on image type

# 3. Watermarking
add_watermark(image_content, is_verified)
  - Add "BlkXchange™ Verified" text
  - Gold color with 70% opacity
  - Semi-transparent black background
  - Bottom-right positioning

# 4. Storage
save_image(image_content, section, test_mode)
  - Generate unique filename with timestamp
  - Save to appropriate directory
  - Return CDN-ready URL path
```

#### Upload Endpoint (`app/main.py`)

```python
@app.post("/api/upload-image")
async def upload_image(
    file: UploadFile,
    section: str,           # vendors, professionals, products, ads
    image_type: str,        # logo, product, ad, profile
    is_verified: bool,      # Add watermark if True
    test_mode: bool,        # Save to test directory if True
    admin: bool = Depends(require_admin)
)
```

**Request**: `multipart/form-data`
**Response**: 
```json
{
  "success": true,
  "url": "https://app-tcqwzext.fly.dev/uploads/live/vendors/vendors_1234567890_abc123.jpg",
  "path": "/uploads/live/vendors/vendors_1234567890_abc123.jpg"
}
```

### Frontend (React + TypeScript)

#### ImageUpload Component (`src/components/ImageUpload.tsx`)

**Props**:
```typescript
interface ImageUploadProps {
  section: 'vendors' | 'professionals' | 'products' | 'ads';
  imageType: 'logo' | 'product' | 'ad' | 'profile';
  isVerified?: boolean;        // Default: false
  testMode?: boolean;          // Default: false
  onUploadSuccess: (url: string) => void;
  onUploadError?: (error: string) => void;
  currentImage?: string;       // For edit modals
  label?: string;              // Default: 'Upload Image'
  maxSizeMB?: number;          // Default: 2
}
```

**Features**:
- Drag-and-drop zone with visual feedback
- File input fallback (click to browse)
- Real-time preview with thumbnail
- Delete and replace buttons
- Upload progress indicator
- Success/error notifications
- Watermark confirmation message for verified entities

**Usage Example**:
```tsx
<ImageUpload
  section="vendors"
  imageType="logo"
  isVerified={vendor.status === 'approved'}
  testMode={false}
  onUploadSuccess={(url) => setFormData({ ...formData, logo_url: url })}
  onUploadError={(error) => console.error(error)}
  currentImage={vendor.logo_url}
  label="Vendor Logo"
/>
```

## Integration Across Admin Sections

### 1. **Vendors** (`AddVendorModal.tsx`, `EditVendorModal.tsx`)
- **Field**: `logo_url`
- **Image Type**: `logo`
- **Dimensions**: 512×512px
- **Target Size**: ≤300KB
- **Watermark**: Applied if vendor is approved

### 2. **Professionals** (`AddProfessionalModal.tsx`, `EditProfessionalModal.tsx`)
- **Field**: `image_url`
- **Image Type**: `profile`
- **Dimensions**: 512×512px
- **Target Size**: ≤300KB
- **Watermark**: Applied if professional is approved

### 3. **Products** (`AddProductModal.tsx`, `EditProductModal.tsx`)
- **Field**: `image_urls` (array, up to 5 images)
- **Image Type**: `product`
- **Dimensions**: 800×800px
- **Target Size**: ≤400KB per image
- **Watermark**: Applied if product is approved

### 4. **Ads** (`AddAdModal.tsx`, `EditAdModal.tsx`)
- **Field**: `asset_url`
- **Image Type**: `ad`
- **Dimensions**: 1200×600px
- **Target Size**: ≤500KB
- **Watermark**: Applied if ad is approved

## File Storage Structure

```
/home/ubuntu/blkxchange/blkxchange-backend/uploads/
├── live/
│   ├── vendors/
│   │   ├── vendors_1234567890_abc123.jpg
│   │   └── vendors_1234567891_def456.jpg
│   ├── professionals/
│   │   └── professionals_1234567892_ghi789.jpg
│   ├── products/
│   │   └── products_1234567893_jkl012.jpg
│   └── ads/
│       └── ads_1234567894_mno345.jpg
└── test/
    ├── vendors/
    ├── professionals/
    ├── products/
    └── ads/
```

## Testing Checklist

### ✅ Backend Testing
- [x] Image validation (file type, size)
- [x] Image optimization (resize, compress)
- [x] Watermark generation (verified entities only)
- [x] File storage (test and live modes)
- [x] URL generation (CDN-ready paths)
- [x] Error handling (invalid files, processing failures)

### ✅ Frontend Testing
- [x] Drag-and-drop functionality
- [x] File input fallback (click to browse)
- [x] File validation (client-side)
- [x] Preview display
- [x] Delete/replace buttons
- [x] Upload progress indicator
- [x] Success/error notifications
- [x] Watermark confirmation message

### ✅ Integration Testing
- [x] Vendor logo upload (Add/Edit modals)
- [x] Professional profile image upload (Add/Edit modals)
- [x] Product images upload (Add/Edit modals, up to 5 images)
- [x] Ad asset upload (Add/Edit modals)
- [x] Test mode vs Live mode file storage
- [x] Verified vs non-verified watermarking

## API Endpoints

### Upload Image
**POST** `/api/upload-image`

**Headers**:
```
Authorization: Bearer <jwt_token>
```
OR
```
X-Admin-Secret: <admin_secret>
```

**Request Body** (`multipart/form-data`):
```
file: <image_file>
section: "vendors" | "professionals" | "products" | "ads"
image_type: "logo" | "product" | "ad" | "profile"
is_verified: true | false
test_mode: true | false
```

**Response** (200 OK):
```json
{
  "success": true,
  "url": "https://app-tcqwzext.fly.dev/uploads/live/vendors/vendors_1234567890_abc123.jpg",
  "path": "/uploads/live/vendors/vendors_1234567890_abc123.jpg"
}
```

**Error Response** (400 Bad Request):
```json
{
  "detail": "File exceeds 2MB limit"
}
```

**Error Response** (401 Unauthorized):
```json
{
  "detail": "Unauthorized: Invalid admin password"
}
```

## Environment Variables

### Backend
```bash
# Required
BACKEND_URL=https://app-tcqwzext.fly.dev

# Optional (for admin authentication)
ADMIN_SECRET_KEY=changeme
JWT_SECRET_KEY=your-secret-key-here
```

### Frontend
```bash
# Required
VITE_API_URL=https://app-tcqwzext.fly.dev
```

## Deployment

### Backend Deployment (Fly.io)
```bash
cd /home/ubuntu/blkxchange/blkxchange-backend
fly deploy
```

**Note**: Ensure the `/uploads` directory is mounted as a persistent volume in production for permanent file storage.

### Frontend Deployment (Devin Apps)
```bash
cd /home/ubuntu/blkxchange/blkxchange-frontend
npm run build
# Deploy dist/ folder
```

## Security Considerations

1. **Authentication**: All upload endpoints require admin authentication (JWT or admin secret)
2. **File Validation**: Server-side validation prevents malicious file uploads
3. **File Size Limits**: 2MB maximum to prevent DoS attacks
4. **File Type Restrictions**: Only image formats (JPG, PNG, WEBP) allowed
5. **Unique Filenames**: Timestamp + UUID prevents filename collisions and overwrites

## Future Enhancements

1. **Cloud Storage**: Migrate from local storage to AWS S3 or Supabase Storage
2. **CDN Integration**: Use CloudFront or Cloudflare for faster image delivery
3. **Image Variants**: Generate multiple sizes (thumbnail, medium, large) for responsive images
4. **Bulk Upload**: Support uploading multiple images at once
5. **Image Cropping**: Allow users to crop images before upload
6. **Progress Tracking**: Show detailed upload progress for large files
7. **Image Editing**: Basic editing tools (rotate, brightness, contrast)

## Troubleshooting

### Issue: "Upload failed: 401 Unauthorized"
**Solution**: Ensure you're logged in as an admin. Check that the JWT token or admin secret is correctly set in the request headers.

### Issue: "File exceeds 2MB limit"
**Solution**: Compress the image before uploading. Use tools like TinyPNG or ImageOptim.

### Issue: "Invalid file format"
**Solution**: Only JPG, PNG, and WEBP formats are supported. Convert your image to one of these formats.

### Issue: "Image processing failed"
**Solution**: The image file may be corrupted. Try re-saving the image or using a different file.

### Issue: Watermark not appearing
**Solution**: Watermarks are only added for verified vendors/professionals. Check that `is_verified=true` is set in the upload request.

### Issue: Images not displaying after upload
**Solution**: Check that the backend URL is correctly configured in the frontend `.env` file (`VITE_API_URL`).

## Support

For issues or questions about the image upload system, contact the development team or refer to the main project documentation.

---

**Last Updated**: 2025-10-19
**Version**: 1.0.0
**Author**: BlkXchange™ Development Team
