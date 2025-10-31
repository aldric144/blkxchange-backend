# BlkXchange™ API Documentation

Base URL (Local): `http://localhost:8000`
Base URL (Production): `https://your-app.fly.dev`

## Table of Contents
- [Authentication](#authentication)
- [Vendors](#vendors)
- [Products](#products)
- [Professionals](#professionals)
- [Orders](#orders)
- [Impact Stats](#impact-stats)

## Authentication

Currently, the API does not require authentication for MVP. In production, implement JWT-based authentication using Supabase Auth.

## Vendors

### Create Vendor
Create a new vendor account.

**Endpoint**: `POST /api/vendors`

**Request Body**:
```json
{
  "email": "vendor@example.com",
  "name": "John Doe",
  "business_name": "Doe's Boutique",
  "business_description": "Premium handcrafted goods",
  "phone": "555-0123",
  "stripe_account_id": null
}
```

**Response**: `201 Created`
```json
{
  "id": "uuid-here",
  "email": "vendor@example.com",
  "name": "John Doe",
  "business_name": "Doe's Boutique",
  "business_description": "Premium handcrafted goods",
  "phone": "555-0123",
  "stripe_account_id": null,
  "verified": false,
  "total_sales": 0.0,
  "community_contribution": 0.0,
  "created_at": "2025-10-19T12:00:00"
}
```

### Get All Vendors
Retrieve a list of all vendors.

**Endpoint**: `GET /api/vendors`

**Response**: `200 OK`
```json
[
  {
    "id": "uuid-here",
    "email": "vendor@example.com",
    "name": "John Doe",
    "business_name": "Doe's Boutique",
    "business_description": "Premium handcrafted goods",
    "phone": "555-0123",
    "stripe_account_id": null,
    "verified": false,
    "total_sales": 0.0,
    "community_contribution": 0.0,
    "created_at": "2025-10-19T12:00:00"
  }
]
```

### Get Vendor by ID
Retrieve a specific vendor by ID.

**Endpoint**: `GET /api/vendors/{vendor_id}`

**Response**: `200 OK` (same structure as Create Vendor response)

**Error**: `404 Not Found` if vendor doesn't exist

## Products

### Create Product
Create a new product for a vendor.

**Endpoint**: `POST /api/vendors/{vendor_id}/products`

**Request Body**:
```json
{
  "name": "Handmade Scarf",
  "description": "Beautiful handwoven scarf made with organic materials",
  "price": 45.99,
  "category": "apparel",
  "image_url": "https://example.com/image.jpg",
  "stock": 20
}
```

**Categories**: `apparel`, `beauty`, `books`, `art`, `tech`, `food`, `wellness`, `home`, `jewelry`, `other`

**Response**: `201 Created`
```json
{
  "id": "uuid-here",
  "vendor_id": "vendor-uuid",
  "name": "Handmade Scarf",
  "description": "Beautiful handwoven scarf made with organic materials",
  "price": 45.99,
  "category": "apparel",
  "image_url": "https://example.com/image.jpg",
  "stock": 20,
  "rating": 0.0,
  "reviews_count": 0,
  "created_at": "2025-10-19T12:00:00"
}
```

### Get All Products
Retrieve all products with optional filtering.

**Endpoint**: `GET /api/products`

**Query Parameters**:
- `category` (optional): Filter by product category
- `vendor_id` (optional): Filter by vendor ID

**Examples**:
- All products: `GET /api/products`
- Beauty products: `GET /api/products?category=beauty`
- Vendor's products: `GET /api/products?vendor_id=uuid-here`

**Response**: `200 OK`
```json
[
  {
    "id": "uuid-here",
    "vendor_id": "vendor-uuid",
    "name": "Handmade Scarf",
    "description": "Beautiful handwoven scarf made with organic materials",
    "price": 45.99,
    "category": "apparel",
    "image_url": "https://example.com/image.jpg",
    "stock": 20,
    "rating": 0.0,
    "reviews_count": 0,
    "created_at": "2025-10-19T12:00:00"
  }
]
```

### Get Product by ID
Retrieve a specific product.

**Endpoint**: `GET /api/products/{product_id}`

**Response**: `200 OK` (same structure as Create Product response)

**Error**: `404 Not Found` if product doesn't exist

### Update Product
Update an existing product.

**Endpoint**: `PUT /api/products/{product_id}`

**Request Body**: Same as Create Product

**Response**: `200 OK` (updated product)

**Error**: `404 Not Found` if product doesn't exist

### Delete Product
Delete a product.

**Endpoint**: `DELETE /api/products/{product_id}`

**Response**: `200 OK`
```json
{
  "message": "Product deleted successfully"
}
```

**Error**: `404 Not Found` if product doesn't exist

## Professionals

### Create Professional
Register a new professional.

**Endpoint**: `POST /api/professionals`

**Request Body**:
```json
{
  "email": "doctor@example.com",
  "name": "Dr. Jane Smith",
  "title": "Family Medicine Physician",
  "category": "health",
  "bio": "Board-certified physician with 10 years experience",
  "credentials": "MD, Board Certified",
  "hourly_rate": 200.0,
  "phone": "555-0456",
  "image_url": "https://example.com/photo.jpg"
}
```

**Categories**: `health`, `legal`, `finance`, `coaching`, `consulting`, `education`, `other`

**Response**: `201 Created`
```json
{
  "id": "uuid-here",
  "email": "doctor@example.com",
  "name": "Dr. Jane Smith",
  "title": "Family Medicine Physician",
  "category": "health",
  "bio": "Board-certified physician with 10 years experience",
  "credentials": "MD, Board Certified",
  "hourly_rate": 200.0,
  "phone": "555-0456",
  "image_url": "https://example.com/photo.jpg",
  "verified": false,
  "rating": 0.0,
  "reviews_count": 0,
  "created_at": "2025-10-19T12:00:00"
}
```

### Get All Professionals
Retrieve all professionals with optional filtering.

**Endpoint**: `GET /api/professionals`

**Query Parameters**:
- `category` (optional): Filter by professional category

**Examples**:
- All professionals: `GET /api/professionals`
- Health professionals: `GET /api/professionals?category=health`

**Response**: `200 OK` (array of professionals)

### Get Professional by ID
Retrieve a specific professional.

**Endpoint**: `GET /api/professionals/{professional_id}`

**Response**: `200 OK` (same structure as Create Professional response)

**Error**: `404 Not Found` if professional doesn't exist

## Orders

### Create Order
Create a new order.

**Endpoint**: `POST /api/orders`

**Request Body**:
```json
{
  "customer_email": "customer@example.com",
  "customer_name": "Alice Johnson",
  "items": [
    {
      "product_id": "product-uuid-1",
      "quantity": 2
    },
    {
      "product_id": "product-uuid-2",
      "quantity": 1
    }
  ],
  "shipping_address": "123 Main St, City, State 12345"
}
```

**Response**: `201 Created`
```json
{
  "id": "uuid-here",
  "customer_email": "customer@example.com",
  "customer_name": "Alice Johnson",
  "items": [
    {
      "product_id": "product-uuid-1",
      "product_name": "Handmade Scarf",
      "quantity": 2,
      "price": 45.99,
      "vendor_id": "vendor-uuid"
    }
  ],
  "total_amount": 91.98,
  "vendor_amount": 82.78,
  "platform_amount": 6.44,
  "community_amount": 2.76,
  "shipping_address": "123 Main St, City, State 12345",
  "status": "pending",
  "created_at": "2025-10-19T12:00:00"
}
```

**Revenue Split**:
- `vendor_amount`: 90% of total
- `platform_amount`: 7% of total
- `community_amount`: 3% of total (distributed to HBCUs, scholarships, nonprofits)

### Get All Orders
Retrieve all orders.

**Endpoint**: `GET /api/orders`

**Response**: `200 OK` (array of orders)

### Get Order by ID
Retrieve a specific order.

**Endpoint**: `GET /api/orders/{order_id}`

**Response**: `200 OK` (same structure as Create Order response)

**Error**: `404 Not Found` if order doesn't exist

## Impact Stats

### Get Impact Statistics
Retrieve community impact statistics.

**Endpoint**: `GET /api/impact`

**Response**: `200 OK`
```json
{
  "total_donations": 150.50,
  "total_orders": 45,
  "total_vendors": 12,
  "total_professionals": 8,
  "hbcu_donations": 75.25,
  "scholarship_donations": 45.15,
  "nonprofit_donations": 30.10
}
```

**Breakdown**:
- `total_donations`: Total amount donated to community (3% of all sales)
- `hbcu_donations`: 50% of community donations
- `scholarship_donations`: 30% of community donations
- `nonprofit_donations`: 20% of community donations

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
Invalid request body or parameters.
```json
{
  "detail": "Validation error message"
}
```

### 404 Not Found
Resource not found.
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
Server error.
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

Currently no rate limiting is implemented. For production, implement rate limiting to prevent abuse.

## CORS

CORS is configured to allow all origins for development. For production, restrict to your frontend domain only.

## Testing the API

### Using cURL

```bash
# Get all products
curl http://localhost:8000/api/products

# Get products by category
curl http://localhost:8000/api/products?category=beauty

# Create a vendor
curl -X POST http://localhost:8000/api/vendors \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "name": "Test Vendor",
    "business_name": "Test Business",
    "business_description": "A test business"
  }'

# Get impact stats
curl http://localhost:8000/api/impact
```

### Using the Frontend

The frontend application provides a user-friendly interface to interact with all API endpoints.

## Future Enhancements

- JWT authentication
- Pagination for list endpoints
- Advanced filtering and search
- File upload for images
- Webhook support for Stripe
- Real-time updates via WebSockets
- GraphQL API option
