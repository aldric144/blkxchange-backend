# BlkXchange™ - The Internet's Black Wall Street

A comprehensive eCommerce and professional services marketplace empowering Black and BIPOC entrepreneurs.

## 🌟 Features

### Core Functionality
- **Multi-Vendor Marketplace**: Black-owned businesses can sell products without upfront fees
- **Professional Services Directory**: Connect with verified Black professionals (health, legal, finance, coaching, etc.)
- **Community Impact Tracking**: 3% of every sale automatically goes to HBCUs, scholarships, and nonprofits
- **Revenue Sharing Model**: 90% to vendors, 7% platform operations, 3% community impact

### Pages Implemented
1. **Landing Page**: Hero section, category grid, mission statement, impact stats
2. **Marketplace**: Product listings with category filtering, search functionality
3. **Professionals**: Directory of service providers with booking capabilities
4. **Impact Dashboard**: Real-time metrics of community contributions
5. **About Page**: Mission, vision, values, and platform story
6. **Vendor Registration**: Application form for new vendors

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: In-memory (PostgreSQL-ready for production)
- **API**: RESTful endpoints for vendors, products, professionals, orders, and impact stats
- **Deployment**: Fly.io ready

### Frontend
- **Framework**: React 18 + Vite
- **Styling**: Tailwind CSS with custom brand colors
- **UI Components**: shadcn/ui
- **Icons**: Lucide React
- **Routing**: React Router v6
- **Deployment**: Vercel ready

## 🎨 Design System

### Brand Colors
- **Jet Black**: #000000
- **Gold**: #C5A14E
- **Warm Ivory**: #F8F8F6
- **Deep Charcoal**: #1A1A1A

### Typography
- **Headings**: Playfair Display (elegant serif)
- **Body**: Inter (clean sans-serif)

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Node.js 18+
- Poetry (Python package manager)

### Backend Setup
```bash
cd blkxchange-backend
poetry install
poetry run fastapi dev app/main.py
```

Backend will run on http://localhost:8000

### Frontend Setup
```bash
cd blkxchange-frontend
npm install
npm run dev
```

Frontend will run on http://localhost:5173

## 📁 Project Structure

```
blkxchange/
├── blkxchange-backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app with all endpoints
│   │   ├── models.py        # Pydantic models
│   │   ├── database.py      # In-memory database
│   │   └── seed_data.py     # Sample data
│   └── pyproject.toml
├── blkxchange-frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navigation.tsx
│   │   │   └── ui/          # shadcn/ui components
│   │   ├── pages/
│   │   │   ├── Landing.tsx
│   │   │   ├── Marketplace.tsx
│   │   │   ├── Professionals.tsx
│   │   │   ├── Impact.tsx
│   │   │   ├── About.tsx
│   │   │   └── VendorRegister.tsx
│   │   ├── types.ts
│   │   ├── api.ts
│   │   └── App.tsx
│   ├── tailwind.config.js
│   └── package.json
└── README.md
```

## 🔌 API Endpoints

### Vendors
- `POST /api/vendors` - Create new vendor
- `GET /api/vendors` - List all vendors
- `GET /api/vendors/{id}` - Get vendor details

### Products
- `POST /api/vendors/{vendor_id}/products` - Create product
- `GET /api/products` - List all products (with optional category filter)
- `GET /api/products/{id}` - Get product details
- `PUT /api/products/{id}` - Update product
- `DELETE /api/products/{id}` - Delete product

### Professionals
- `POST /api/professionals` - Create professional profile
- `GET /api/professionals` - List all professionals (with optional category filter)
- `GET /api/professionals/{id}` - Get professional details

### Orders
- `POST /api/orders` - Create new order
- `GET /api/orders` - List all orders
- `GET /api/orders/{id}` - Get order details

### Impact
- `GET /api/impact` - Get community impact statistics

## 💰 Revenue Model

Every sale is automatically split:
- **90%** → Vendor (direct deposit via Stripe Connect)
- **7%** → Platform operations
- **3%** → Community impact fund
  - 50% → HBCUs
  - 30% → Scholarships
  - 20% → Nonprofit partners

## 🎯 Future Enhancements

### Phase 2
- Stripe Connect integration for real payments
- User authentication with Supabase
- Shopping cart and checkout flow
- Order management system
- Vendor dashboard with analytics
- Product reviews and ratings

### Phase 3
- Mobile app (React Native)
- AI-powered product recommendations
- Live chat support
- Advanced search with filters
- Vendor verification system
- Professional booking calendar integration

### Phase 4
- Global vendor onboarding
- Multi-language support
- Community social feed
- Live auction features
- Partnership integrations

## 📝 Notes

- **Database**: Currently using in-memory storage for MVP. Data resets on server restart.
- **Payments**: Stripe Connect integration ready but requires API keys for production.
- **Authentication**: Supabase Auth configured but not yet enforced on routes.
- **Images**: Using Unsplash placeholder images for seed data.

## 👨‍💻 Developer

Created by Dr. Aldric Marshall (@aldric144)

## 📄 License

© 2025 BlkXchange™. All rights reserved.

**Tagline**: Empower. Exchange. Elevate.
