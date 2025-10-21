from app.database import db
from app.models import (
    VendorCreate, ProductCreate, ProfessionalCreate,
    ProductCategory, ProfessionalCategory
)

def seed_database():
    vendor1 = db.create_vendor(VendorCreate(
        email="maya@soulfulthreads.com",
        name="Maya Johnson",
        business_name="Soulful Threads",
        business_description="Authentic African-inspired apparel and accessories celebrating Black culture and heritage.",
        phone="555-0101"
    ))
    
    vendor2 = db.create_vendor(VendorCreate(
        email="james@naturalglow.com",
        name="James Williams",
        business_name="Natural Glow Beauty",
        business_description="Premium natural beauty products formulated for melanin-rich skin.",
        phone="555-0102"
    ))
    
    vendor3 = db.create_vendor(VendorCreate(
        email="aisha@blackbookshelf.com",
        name="Aisha Davis",
        business_name="The Black Bookshelf",
        business_description="Curated collection of books by Black authors across all genres.",
        phone="555-0103"
    ))
    
    vendor4 = db.create_vendor(VendorCreate(
        email="marcus@afroart.com",
        name="Marcus Brown",
        business_name="AfroArt Gallery",
        business_description="Contemporary African and African-American art pieces.",
        phone="555-0104"
    ))
    
    vendor5 = db.create_vendor(VendorCreate(
        email="info@harlemessence.com",
        name="Keisha Thompson",
        business_name="Harlem Essence",
        business_description="Luxury wellness products and home goods inspired by Harlem Renaissance elegance.",
        phone="555-0105"
    ))
    
    vendor6 = db.create_vendor(VendorCreate(
        email="contact@diasporathreads.com",
        name="Jamal Washington",
        business_name="Diaspora Threads",
        business_description="Contemporary streetwear celebrating the African diaspora and Black culture worldwide.",
        phone="555-0106"
    ))
    
    vendor7 = db.create_vendor(VendorCreate(
        email="hello@afrozenco.com",
        name="Nia Robinson",
        business_name="AfroZen Wellness Co.",
        business_description="Holistic wellness products rooted in African healing traditions and mindfulness.",
        phone="555-0107"
    ))
    
    vendor8 = db.create_vendor(VendorCreate(
        email="support@herrootsbeauty.com",
        name="Tasha Mitchell",
        business_name="Her Roots Beauty",
        business_description="Natural beauty and hair care products celebrating Black women's natural beauty.",
        phone="555-0108"
    ))
    
    vendor9 = db.create_vendor(VendorCreate(
        email="shop@panafricanprints.com",
        name="Kwame Osei",
        business_name="PanAfrican Prints",
        business_description="Authentic African art, jewelry, and home décor connecting the diaspora to the motherland.",
        phone="555-0109"
    ))
    
    vendor10 = db.create_vendor(VendorCreate(
        email="klove144@bellsouth.net",
        name="Dr. Aldric Marshall",
        business_name="Dr. Aldric Marshall Ministries",
        business_description="Empowering believers with divine revelation and Kingdom teaching through transformative books and resources.",
        phone="555-0110"
    ))
    
    db.create_product(vendor1.id, ProductCreate(
        name="Ankara Print Dress",
        description="Beautiful handmade dress featuring vibrant Ankara print fabric. Perfect for any occasion.",
        price=89.99,
        category=ProductCategory.APPAREL,
        image_url="https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=500",
        stock=15
    ))
    
    db.create_product(vendor1.id, ProductCreate(
        name="Kente Cloth Scarf",
        description="Authentic Kente cloth scarf handwoven in Ghana. A timeless accessory.",
        price=45.00,
        category=ProductCategory.APPAREL,
        image_url="https://images.unsplash.com/photo-1601924994987-69e26d50dc26?w=500",
        stock=25
    ))
    
    db.create_product(vendor1.id, ProductCreate(
        name="Dashiki Shirt",
        description="Classic dashiki shirt in bold colors. Comfortable and stylish.",
        price=39.99,
        category=ProductCategory.APPAREL,
        image_url="https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500",
        stock=30
    ))
    
    db.create_product(vendor2.id, ProductCreate(
        name="Shea Butter Body Cream",
        description="Rich, moisturizing body cream made with pure African shea butter.",
        price=24.99,
        category=ProductCategory.BEAUTY,
        image_url="https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=500",
        stock=50
    ))
    
    db.create_product(vendor2.id, ProductCreate(
        name="Natural Hair Growth Oil",
        description="Nourishing oil blend to promote healthy hair growth and shine.",
        price=18.99,
        category=ProductCategory.BEAUTY,
        image_url="https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?w=500",
        stock=40
    ))
    
    db.create_product(vendor2.id, ProductCreate(
        name="Melanin Glow Serum",
        description="Vitamin C serum designed to enhance and protect melanin-rich skin.",
        price=32.99,
        category=ProductCategory.BEAUTY,
        image_url="https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=500",
        stock=35
    ))
    
    db.create_product(vendor3.id, ProductCreate(
        name="The Bluest Eye by Toni Morrison",
        description="Classic novel exploring themes of beauty, race, and identity.",
        price=16.99,
        category=ProductCategory.BOOKS,
        image_url="https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500",
        stock=20
    ))
    
    db.create_product(vendor3.id, ProductCreate(
        name="Between the World and Me",
        description="Ta-Nehisi Coates' powerful meditation on race in America.",
        price=14.99,
        category=ProductCategory.BOOKS,
        image_url="https://images.unsplash.com/photo-1512820790803-83ca734da794?w=500",
        stock=18
    ))
    
    db.create_product(vendor3.id, ProductCreate(
        name="Homegoing by Yaa Gyasi",
        description="Epic novel tracing two branches of a family through generations.",
        price=17.99,
        category=ProductCategory.BOOKS,
        image_url="https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=500",
        stock=22
    ))
    
    db.create_product(vendor4.id, ProductCreate(
        name="African Mask Wall Art",
        description="Handcrafted wooden African mask, perfect for home decor.",
        price=125.00,
        category=ProductCategory.ART,
        image_url="https://images.unsplash.com/photo-1577083552431-6e5fd01988ec?w=500",
        stock=8
    ))
    
    db.create_product(vendor4.id, ProductCreate(
        name="Abstract Canvas Print",
        description="Contemporary abstract art celebrating Black excellence.",
        price=89.00,
        category=ProductCategory.ART,
        image_url="https://images.unsplash.com/photo-1549887534-1541e9326642?w=500",
        stock=12
    ))
    
    db.create_product(vendor6.id, ProductCreate(
        name="CrownCulture Streetwear Hoodie",
        description="Premium unisex hoodie with embroidered crown logo. Ethically made and designed by HBCU graduate.",
        price=75.00,
        category=ProductCategory.APPAREL,
        image_url="https://images.pexels.com/photos/8148577/pexels-photo-8148577.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=40
    ))
    
    db.create_product(vendor6.id, ProductCreate(
        name="HBCU Pride Collection Tee",
        description="Celebrate Black excellence with this premium cotton tee featuring iconic HBCU designs.",
        price=35.00,
        category=ProductCategory.APPAREL,
        image_url="https://images.pexels.com/photos/8148583/pexels-photo-8148583.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=60
    ))
    
    db.create_product(vendor8.id, ProductCreate(
        name="Loc & Twist Butter",
        description="Nourishing butter blend for locs, twists, and braids. Made with shea butter and essential oils.",
        price=22.99,
        category=ProductCategory.BEAUTY,
        image_url="https://images.pexels.com/photos/7428100/pexels-photo-7428100.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=45
    ))
    
    db.create_product(vendor8.id, ProductCreate(
        name="Beard Growth & Care Kit",
        description="Complete beard care system with oil, balm, and brush. Specially formulated for coarse hair.",
        price=45.00,
        category=ProductCategory.BEAUTY,
        image_url="https://images.pexels.com/photos/7428095/pexels-photo-7428095.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=30
    ))
    
    db.create_product(vendor3.id, ProductCreate(
        name="The New Jim Crow by Michelle Alexander",
        description="Groundbreaking work on mass incarceration and racial justice in America.",
        price=18.99,
        category=ProductCategory.BOOKS,
        image_url="https://images.pexels.com/photos/4866041/pexels-photo-4866041.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=25
    ))
    
    db.create_product(vendor3.id, ProductCreate(
        name="Black Entrepreneurship Guide",
        description="Comprehensive guide to building wealth and business success in the Black community.",
        price=24.99,
        category=ProductCategory.BOOKS,
        image_url="https://images.pexels.com/photos/4866043/pexels-photo-4866043.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=35
    ))
    
    db.create_product(vendor10.id, ProductCreate(
        name="Seven Trading Floors of Heaven: Confronting and Overcoming Ungodly Exchanges",
        description="A powerful and revelatory work that unveils how spiritual exchanges take place in the unseen realm — both godly and ungodly. Dr. Aldric Marshall draws from biblical insight and divine revelation to guide readers in reclaiming spiritual authority, breaking cycles of loss, and walking in heavenly alignment. This book helps believers understand how to position themselves on Heaven's trading floors to receive divine strategy, favor, and restoration.",
        price=24.99,
        category=ProductCategory.BOOKS,
        image_url="https://images.pexels.com/photos/4866045/pexels-photo-4866045.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=100
    ))
    
    db.create_product(vendor9.id, ProductCreate(
        name="Afrofuturist Canvas Print",
        description="Vibrant 24x36 canvas featuring Afrofuturist themes and Black excellence.",
        price=150.00,
        category=ProductCategory.ART,
        image_url="https://images.pexels.com/photos/1839919/pexels-photo-1839919.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=15
    ))
    
    db.create_product(vendor9.id, ProductCreate(
        name="Handcrafted Wooden Sculpture",
        description="Beautiful hand-carved African sculpture celebrating ancestral heritage.",
        price=200.00,
        category=ProductCategory.ART,
        image_url="https://images.pexels.com/photos/3004909/pexels-photo-3004909.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=8
    ))
    
    db.create_product(vendor4.id, ProductCreate(
        name="Black History Portrait Series",
        description="Limited edition print series featuring iconic Black leaders and changemakers.",
        price=95.00,
        category=ProductCategory.ART,
        image_url="https://images.pexels.com/photos/1839924/pexels-photo-1839924.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=20
    ))
    
    db.create_product(vendor5.id, ProductCreate(
        name="Melanin Tech Wireless Earbuds",
        description="Premium wireless earbuds from Black-owned tech startup. Superior sound quality and comfort.",
        price=89.99,
        category=ProductCategory.TECH,
        image_url="https://images.pexels.com/photos/3825517/pexels-photo-3825517.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=50
    ))
    
    db.create_product(vendor5.id, ProductCreate(
        name="Smart Home Hub - Onyx Edition",
        description="Voice-activated smart home controller designed by Black engineers. Compatible with all devices.",
        price=149.99,
        category=ProductCategory.TECH,
        image_url="https://images.pexels.com/photos/4219861/pexels-photo-4219861.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=30
    ))
    
    db.create_product(vendor5.id, ProductCreate(
        name="Digital Planner Pro",
        description="Comprehensive digital planner app subscription designed for Black entrepreneurs and creatives.",
        price=12.99,
        category=ProductCategory.TECH,
        image_url="https://images.pexels.com/photos/4219862/pexels-photo-4219862.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=999
    ))
    
    db.create_product(vendor5.id, ProductCreate(
        name="Portable Power Bank - 20000mAh",
        description="High-capacity power bank with fast charging. Perfect for entrepreneurs on the go.",
        price=45.00,
        category=ProductCategory.TECH,
        image_url="https://images.pexels.com/photos/4219863/pexels-photo-4219863.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=75
    ))
    
    db.create_product(vendor5.id, ProductCreate(
        name="Bluetooth Speaker - Heritage Series",
        description="Premium Bluetooth speaker with 360° sound. Designed and engineered by Black-owned tech company.",
        price=79.99,
        category=ProductCategory.TECH,
        image_url="https://images.pexels.com/photos/3825518/pexels-photo-3825518.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=40
    ))
    
    db.create_product(vendor7.id, ProductCreate(
        name="Soul Spice Blend Collection",
        description="Authentic Southern spice blends passed down through generations. Set of 5 premium seasonings.",
        price=35.00,
        category=ProductCategory.FOOD,
        image_url="https://images.pexels.com/photos/4198933/pexels-photo-4198933.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=60
    ))
    
    db.create_product(vendor7.id, ProductCreate(
        name="Gourmet Hot Sauce Trio",
        description="Award-winning hot sauce collection featuring Caribbean and African flavors.",
        price=28.00,
        category=ProductCategory.FOOD,
        image_url="https://images.pexels.com/photos/4198935/pexels-photo-4198935.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=45
    ))
    
    db.create_product(vendor7.id, ProductCreate(
        name="Artisan Coffee - Diaspora Blend",
        description="Small-batch roasted coffee beans sourced from Black-owned farms in Ethiopia and Jamaica.",
        price=18.99,
        category=ProductCategory.FOOD,
        image_url="https://images.pexels.com/photos/4198936/pexels-photo-4198936.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=80
    ))
    
    db.create_product(vendor7.id, ProductCreate(
        name="Herbal Tea Collection",
        description="Organic herbal tea blends inspired by African healing traditions. Set of 6 flavors.",
        price=24.99,
        category=ProductCategory.FOOD,
        image_url="https://images.pexels.com/photos/4198937/pexels-photo-4198937.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=55
    ))
    
    db.create_product(vendor7.id, ProductCreate(
        name="Gourmet Baking Mix Bundle",
        description="Premium baking mixes for sweet potato pie, cornbread, and biscuits. Family recipes.",
        price=32.00,
        category=ProductCategory.FOOD,
        image_url="https://images.pexels.com/photos/4198938/pexels-photo-4198938.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=40
    ))
    
    db.create_product(vendor7.id, ProductCreate(
        name="Meditation & Mindfulness Journal",
        description="Guided journal for Black mental wellness and self-care. 90-day transformation program.",
        price=29.99,
        category=ProductCategory.WELLNESS,
        image_url="https://images.pexels.com/photos/4498362/pexels-photo-4498362.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=70
    ))
    
    db.create_product(vendor7.id, ProductCreate(
        name="Aromatherapy Candle Set",
        description="Hand-poured soy candles with essential oils. Lavender, eucalyptus, and sandalwood scents.",
        price=45.00,
        category=ProductCategory.WELLNESS,
        image_url="https://images.pexels.com/photos/4498363/pexels-photo-4498363.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=50
    ))
    
    db.create_product(vendor7.id, ProductCreate(
        name="Luxury Bath Salt Collection",
        description="Mineral-rich bath salts infused with African botanicals. Perfect for relaxation and self-care.",
        price=32.00,
        category=ProductCategory.WELLNESS,
        image_url="https://images.pexels.com/photos/4498364/pexels-photo-4498364.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=60
    ))
    
    db.create_product(vendor7.id, ProductCreate(
        name="Yoga Mat - Melanin Magic",
        description="Premium non-slip yoga mat with inspirational affirmations. Eco-friendly materials.",
        price=55.00,
        category=ProductCategory.WELLNESS,
        image_url="https://images.pexels.com/photos/4498365/pexels-photo-4498365.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=35
    ))
    
    db.create_product(vendor7.id, ProductCreate(
        name="Essential Oil Diffuser Set",
        description="Ultrasonic diffuser with 10 essential oils. Create your perfect wellness sanctuary.",
        price=65.00,
        category=ProductCategory.WELLNESS,
        image_url="https://images.pexels.com/photos/4498366/pexels-photo-4498366.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=40
    ))
    
    db.create_product(vendor9.id, ProductCreate(
        name="Ankara Print Throw Pillows",
        description="Set of 4 decorative pillows featuring authentic Ankara fabric. Handmade with love.",
        price=85.00,
        category=ProductCategory.HOME,
        image_url="https://images.pexels.com/photos/6969831/pexels-photo-6969831.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=30
    ))
    
    db.create_product(vendor9.id, ProductCreate(
        name="Afrocentric Wall Tapestry",
        description="Large woven tapestry featuring African-inspired geometric patterns. 60x80 inches.",
        price=120.00,
        category=ProductCategory.HOME,
        image_url="https://images.pexels.com/photos/6969832/pexels-photo-6969832.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=20
    ))
    
    db.create_product(vendor9.id, ProductCreate(
        name="Handcrafted Ceramic Dinnerware Set",
        description="12-piece dinnerware set with African-inspired designs. Microwave and dishwasher safe.",
        price=180.00,
        category=ProductCategory.HOME,
        image_url="https://images.pexels.com/photos/6969833/pexels-photo-6969833.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=15
    ))
    
    db.create_product(vendor5.id, ProductCreate(
        name="Luxury Throw Blanket - Kente",
        description="Plush throw blanket featuring Kente cloth pattern. Perfect for cozy evenings.",
        price=95.00,
        category=ProductCategory.HOME,
        image_url="https://images.pexels.com/photos/6969834/pexels-photo-6969834.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=40
    ))
    
    db.create_product(vendor9.id, ProductCreate(
        name="African Basket Wall Décor Set",
        description="Set of 3 handwoven baskets from Rwanda. Beautiful wall art with cultural significance.",
        price=75.00,
        category=ProductCategory.HOME,
        image_url="https://images.pexels.com/photos/6969835/pexels-photo-6969835.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=25
    ))
    
    db.create_product(vendor9.id, ProductCreate(
        name="Ankh Pendant Necklace - Gold",
        description="18K gold-plated ankh pendant on 24-inch chain. Symbol of life and eternal wisdom.",
        price=65.00,
        category=ProductCategory.JEWELRY,
        image_url="https://images.pexels.com/photos/1191531/pexels-photo-1191531.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=50
    ))
    
    db.create_product(vendor9.id, ProductCreate(
        name="Beaded Bracelet Collection",
        description="Set of 3 handmade African beaded bracelets. Each tells a unique cultural story.",
        price=35.00,
        category=ProductCategory.JEWELRY,
        image_url="https://images.pexels.com/photos/1191532/pexels-photo-1191532.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=60
    ))
    
    db.create_product(vendor9.id, ProductCreate(
        name="Cowrie Shell Earrings",
        description="Elegant cowrie shell drop earrings. Handcrafted with sterling silver hooks.",
        price=42.00,
        category=ProductCategory.JEWELRY,
        image_url="https://images.pexels.com/photos/1191533/pexels-photo-1191533.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=45
    ))
    
    db.create_product(vendor9.id, ProductCreate(
        name="Custom Name Plate Necklace",
        description="Personalized gold name plate necklace. Classic style celebrating your identity.",
        price=89.00,
        category=ProductCategory.JEWELRY,
        image_url="https://images.pexels.com/photos/1191534/pexels-photo-1191534.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=100
    ))
    
    db.create_product(vendor9.id, ProductCreate(
        name="African Map Pendant - Sterling Silver",
        description="Detailed Africa continent pendant in sterling silver. Celebrate your roots with pride.",
        price=55.00,
        category=ProductCategory.JEWELRY,
        image_url="https://images.pexels.com/photos/1191535/pexels-photo-1191535.jpeg?auto=compress&cs=tinysrgb&w=500",
        stock=70
    ))
    
    db.create_professional(ProfessionalCreate(
        email="dr.thompson@healthclinic.com",
        name="Dr. Sarah Thompson",
        title="Family Medicine Physician",
        category=ProfessionalCategory.HEALTH,
        bio="Board-certified family medicine physician with 15 years of experience providing comprehensive care to diverse communities.",
        credentials="MD, Board Certified in Family Medicine",
        hourly_rate=200.00,
        phone="555-0201",
        image_url="https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="attorney.jackson@lawfirm.com",
        name="Attorney Michael Jackson",
        title="Civil Rights Attorney",
        category=ProfessionalCategory.LEGAL,
        bio="Dedicated civil rights attorney fighting for justice and equality. Specializing in employment discrimination and police misconduct cases.",
        credentials="JD, Licensed to practice in NY, NJ, and Federal Courts",
        hourly_rate=350.00,
        phone="555-0202",
        image_url="https://images.unsplash.com/photo-1556157382-97eda2d62296?w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="lisa@financialfreedom.com",
        name="Lisa Anderson",
        title="Financial Advisor",
        category=ProfessionalCategory.FINANCE,
        bio="Certified financial planner helping families build generational wealth through smart investing and financial planning.",
        credentials="CFP, MBA in Finance",
        hourly_rate=175.00,
        phone="555-0203",
        image_url="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="coach.roberts@empowerment.com",
        name="Coach David Roberts",
        title="Life & Business Coach",
        category=ProfessionalCategory.COACHING,
        bio="Empowering Black entrepreneurs to achieve their dreams through strategic coaching and mentorship.",
        credentials="ICF Certified Coach, 20+ years business experience",
        hourly_rate=150.00,
        phone="555-0204",
        image_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="dr.williams@consulting.com",
        name="Dr. Patricia Williams",
        title="Diversity & Inclusion Consultant",
        category=ProfessionalCategory.CONSULTING,
        bio="PhD in Organizational Psychology. Helping companies build inclusive cultures and equitable practices.",
        credentials="PhD in Organizational Psychology, SHRM-SCP",
        hourly_rate=300.00,
        phone="555-0205",
        image_url="https://images.unsplash.com/photo-1580489944761-15a19d654956?w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="dr.martinez@pediatrics.com",
        name="Dr. Carlos Martinez",
        title="Pediatrician",
        category=ProfessionalCategory.HEALTH,
        bio="Compassionate pediatrician dedicated to providing quality healthcare for children in underserved communities.",
        credentials="MD, Board Certified Pediatrics, FAAP",
        hourly_rate=225.00,
        phone="555-0301",
        image_url="https://images.pexels.com/photos/5215024/pexels-photo-5215024.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="dr.johnson@mentalhealth.com",
        name="Dr. Keisha Johnson",
        title="Clinical Psychologist",
        category=ProfessionalCategory.HEALTH,
        bio="Licensed clinical psychologist specializing in trauma therapy and culturally responsive mental health care.",
        credentials="PhD in Clinical Psychology, Licensed Psychologist",
        hourly_rate=180.00,
        phone="555-0302",
        image_url="https://images.pexels.com/photos/5215024/pexels-photo-5215024.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="dr.brown@dentistry.com",
        name="Dr. Marcus Brown",
        title="Dentist",
        category=ProfessionalCategory.HEALTH,
        bio="Family dentist committed to making dental care accessible and comfortable for all ages.",
        credentials="DDS, Member of National Dental Association",
        hourly_rate=195.00,
        phone="555-0303",
        image_url="https://images.pexels.com/photos/6303761/pexels-photo-6303761.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="nurse.davis@healthcare.com",
        name="Nurse Practitioner Angela Davis",
        title="Family Nurse Practitioner",
        category=ProfessionalCategory.HEALTH,
        bio="Experienced nurse practitioner providing primary care with a focus on preventive medicine and wellness.",
        credentials="MSN, FNP-C, 12 years experience",
        hourly_rate=150.00,
        phone="555-0304",
        image_url="https://images.pexels.com/photos/5327585/pexels-photo-5327585.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="attorney.washington@law.com",
        name="Attorney James Washington",
        title="Criminal Defense Attorney",
        category=ProfessionalCategory.LEGAL,
        bio="Aggressive criminal defense attorney protecting the rights of the accused with over 20 years of courtroom experience.",
        credentials="JD, Licensed in Multiple States",
        hourly_rate=400.00,
        phone="555-0305",
        image_url="https://images.pexels.com/photos/5668838/pexels-photo-5668838.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="attorney.harris@familylaw.com",
        name="Attorney Nicole Harris",
        title="Family Law Attorney",
        category=ProfessionalCategory.LEGAL,
        bio="Compassionate family law attorney specializing in divorce, custody, and adoption cases.",
        credentials="JD, Certified Family Law Specialist",
        hourly_rate=325.00,
        phone="555-0306",
        image_url="https://images.pexels.com/photos/5668858/pexels-photo-5668858.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="attorney.robinson@business.com",
        name="Attorney Terrence Robinson",
        title="Business Attorney",
        category=ProfessionalCategory.LEGAL,
        bio="Corporate attorney helping Black-owned businesses navigate contracts, compliance, and business formation.",
        credentials="JD, MBA, Business Law Specialist",
        hourly_rate=375.00,
        phone="555-0307",
        image_url="https://images.pexels.com/photos/8112199/pexels-photo-8112199.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="attorney.green@immigration.com",
        name="Attorney Fatima Green",
        title="Immigration Attorney",
        category=ProfessionalCategory.LEGAL,
        bio="Dedicated immigration attorney helping families reunite and achieve their American dream.",
        credentials="JD, AILA Member, Fluent in Spanish",
        hourly_rate=300.00,
        phone="555-0308",
        image_url="https://images.pexels.com/photos/7640443/pexels-photo-7640443.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="cpa.mitchell@accounting.com",
        name="CPA Robert Mitchell",
        title="Certified Public Accountant",
        category=ProfessionalCategory.FINANCE,
        bio="Experienced CPA specializing in tax planning and small business accounting for entrepreneurs.",
        credentials="CPA, MBA in Accounting",
        hourly_rate=165.00,
        phone="555-0309",
        image_url="https://images.pexels.com/photos/8112198/pexels-photo-8112198.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="advisor.lewis@wealth.com",
        name="Wealth Advisor Jasmine Lewis",
        title="Wealth Management Advisor",
        category=ProfessionalCategory.FINANCE,
        bio="Helping high-net-worth individuals and families preserve and grow wealth across generations.",
        credentials="CFP, CFA, Series 7 & 66",
        hourly_rate=250.00,
        phone="555-0310",
        image_url="https://images.pexels.com/photos/7640432/pexels-photo-7640432.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="planner.taylor@retirement.com",
        name="Retirement Planner Marcus Taylor",
        title="Retirement Planning Specialist",
        category=ProfessionalCategory.FINANCE,
        bio="Certified retirement counselor helping clients achieve financial security in their golden years.",
        credentials="CRPC, 15 years experience",
        hourly_rate=185.00,
        phone="555-0311",
        image_url="https://images.pexels.com/photos/5668882/pexels-photo-5668882.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="analyst.cooper@investment.com",
        name="Investment Analyst Shanice Cooper",
        title="Investment Analyst",
        category=ProfessionalCategory.FINANCE,
        bio="Data-driven investment analyst specializing in portfolio optimization and risk management.",
        credentials="CFA Level III, MS Finance",
        hourly_rate=200.00,
        phone="555-0312",
        image_url="https://images.pexels.com/photos/7640461/pexels-photo-7640461.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="coach.williams@executive.com",
        name="Executive Coach Denise Williams",
        title="Executive Leadership Coach",
        category=ProfessionalCategory.COACHING,
        bio="Empowering C-suite executives and emerging leaders to maximize their impact and influence.",
        credentials="PCC, MBA, 25 years corporate experience",
        hourly_rate=275.00,
        phone="555-0313",
        image_url="https://images.pexels.com/photos/8112180/pexels-photo-8112180.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="coach.jenkins@career.com",
        name="Career Coach Brandon Jenkins",
        title="Career Transition Coach",
        category=ProfessionalCategory.COACHING,
        bio="Helping professionals navigate career transitions and land their dream jobs with confidence.",
        credentials="CPCC, Former Fortune 500 Recruiter",
        hourly_rate=125.00,
        phone="555-0314",
        image_url="https://images.pexels.com/photos/7640450/pexels-photo-7640450.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="coach.parker@wellness.com",
        name="Wellness Coach Tanya Parker",
        title="Health & Wellness Coach",
        category=ProfessionalCategory.COACHING,
        bio="Certified wellness coach guiding clients toward holistic health through nutrition, fitness, and mindfulness.",
        credentials="NBC-HWC, Certified Nutritionist",
        hourly_rate=110.00,
        phone="555-0315",
        image_url="https://images.pexels.com/photos/5668772/pexels-photo-5668772.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="coach.henderson@relationship.com",
        name="Relationship Coach Dr. Kevin Henderson",
        title="Marriage & Relationship Coach",
        category=ProfessionalCategory.COACHING,
        bio="Licensed therapist and relationship coach helping couples build stronger, healthier partnerships.",
        credentials="PhD in Counseling Psychology, LMFT",
        hourly_rate=160.00,
        phone="555-0316",
        image_url="https://images.pexels.com/photos/7640424/pexels-photo-7640424.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="consultant.adams@strategy.com",
        name="Strategy Consultant Monica Adams",
        title="Business Strategy Consultant",
        category=ProfessionalCategory.CONSULTING,
        bio="Former McKinsey consultant helping businesses develop winning strategies and operational excellence.",
        credentials="MBA from Wharton, 18 years consulting",
        hourly_rate=350.00,
        phone="555-0317",
        image_url="https://images.pexels.com/photos/8112182/pexels-photo-8112182.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="consultant.foster@hr.com",
        name="HR Consultant Gerald Foster",
        title="Human Resources Consultant",
        category=ProfessionalCategory.CONSULTING,
        bio="HR expert specializing in talent acquisition, employee relations, and organizational development.",
        credentials="SPHR, SHRM-SCP, 20+ years HR leadership",
        hourly_rate=225.00,
        phone="555-0318",
        image_url="https://images.pexels.com/photos/7640427/pexels-photo-7640427.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="consultant.brooks@tech.com",
        name="IT Consultant Alicia Brooks",
        title="Technology Consultant",
        category=ProfessionalCategory.CONSULTING,
        bio="Technology strategist helping businesses leverage digital transformation and cybersecurity solutions.",
        credentials="CISSP, MS Computer Science",
        hourly_rate=275.00,
        phone="555-0319",
        image_url="https://images.pexels.com/photos/5668473/pexels-photo-5668473.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="consultant.reed@marketing.com",
        name="Marketing Consultant Isaiah Reed",
        title="Marketing Strategy Consultant",
        category=ProfessionalCategory.CONSULTING,
        bio="Award-winning marketing consultant specializing in brand development and digital marketing strategies.",
        credentials="MBA Marketing, Google Analytics Certified",
        hourly_rate=200.00,
        phone="555-0320",
        image_url="https://images.pexels.com/photos/7640456/pexels-photo-7640456.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="prof.carter@university.edu",
        name="Professor Vanessa Carter",
        title="College Professor & Academic Advisor",
        category=ProfessionalCategory.EDUCATION,
        bio="PhD professor and academic advisor helping students navigate higher education and career planning.",
        credentials="PhD in Education, 15 years teaching",
        hourly_rate=140.00,
        phone="555-0321",
        image_url="https://images.pexels.com/photos/8197543/pexels-photo-8197543.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="tutor.simmons@learning.com",
        name="Tutor Malcolm Simmons",
        title="STEM Tutor & Test Prep Specialist",
        category=ProfessionalCategory.EDUCATION,
        bio="Experienced tutor specializing in SAT/ACT prep, mathematics, and science for high school students.",
        credentials="MS Mathematics, Perfect SAT Score",
        hourly_rate=95.00,
        phone="555-0322",
        image_url="https://images.pexels.com/photos/8197527/pexels-photo-8197527.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="educator.bell@literacy.org",
        name="Literacy Specialist Tamika Bell",
        title="Reading & Literacy Specialist",
        category=ProfessionalCategory.EDUCATION,
        bio="Certified reading specialist helping children overcome learning challenges and develop strong literacy skills.",
        credentials="MEd Reading, Wilson Reading Certified",
        hourly_rate=105.00,
        phone="555-0323",
        image_url="https://images.pexels.com/photos/5212317/pexels-photo-5212317.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="counselor.hayes@guidance.edu",
        name="School Counselor Dr. Raymond Hayes",
        title="Educational Counselor",
        category=ProfessionalCategory.EDUCATION,
        bio="Licensed school counselor providing academic guidance, college planning, and social-emotional support.",
        credentials="EdD in Counseling, Licensed School Counselor",
        hourly_rate=120.00,
        phone="555-0324",
        image_url="https://images.pexels.com/photos/5212345/pexels-photo-5212345.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="instructor.freeman@training.com",
        name="Training Specialist Jasmine Freeman",
        title="Corporate Training Specialist",
        category=ProfessionalCategory.EDUCATION,
        bio="Professional development trainer designing and delivering engaging corporate training programs and workshops.",
        credentials="MEd Adult Education, CPTD Certified",
        hourly_rate=135.00,
        phone="555-0355",
        image_url="https://images.pexels.com/photos/8197539/pexels-photo-8197539.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="broker.patterson@realestate.com",
        name="Real Estate Broker Candace Patterson",
        title="Licensed Real Estate Broker",
        category=ProfessionalCategory.REAL_ESTATE,
        bio="Top-producing broker specializing in residential and commercial properties in urban markets.",
        credentials="Licensed Broker, 12 years experience",
        hourly_rate=175.00,
        phone="555-0325",
        image_url="https://images.pexels.com/photos/7640471/pexels-photo-7640471.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="advisor.coleman@wealth.com",
        name="Wealth Advisor Jerome Coleman",
        title="Private Wealth Advisor",
        category=ProfessionalCategory.REAL_ESTATE,
        bio="Certified wealth advisor helping clients build real estate portfolios and achieve financial independence.",
        credentials="CFP, Real Estate Investment Specialist",
        hourly_rate=225.00,
        phone="555-0326",
        image_url="https://images.pexels.com/photos/8112183/pexels-photo-8112183.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="agent.russell@homes.com",
        name="Real Estate Agent Kimberly Russell",
        title="Residential Real Estate Agent",
        category=ProfessionalCategory.REAL_ESTATE,
        bio="Dedicated agent helping first-time homebuyers and families find their dream homes.",
        credentials="Licensed Realtor, Accredited Buyer Representative",
        hourly_rate=150.00,
        phone="555-0327",
        image_url="https://images.pexels.com/photos/5668840/pexels-photo-5668840.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="investor.morgan@property.com",
        name="Property Investor Darius Morgan",
        title="Real Estate Investment Consultant",
        category=ProfessionalCategory.REAL_ESTATE,
        bio="Experienced investor teaching others how to build wealth through strategic real estate investments.",
        credentials="Licensed Broker, 50+ Properties Managed",
        hourly_rate=200.00,
        phone="555-0328",
        image_url="https://images.pexels.com/photos/7640438/pexels-photo-7640438.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="appraiser.dixon@valuation.com",
        name="Property Appraiser Latoya Dixon",
        title="Certified Real Estate Appraiser",
        category=ProfessionalCategory.REAL_ESTATE,
        bio="Licensed appraiser providing accurate property valuations for residential and commercial real estate.",
        credentials="Certified Residential Appraiser",
        hourly_rate=165.00,
        phone="555-0329",
        image_url="https://images.pexels.com/photos/5669617/pexels-photo-5669617.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="barber.thompson@cuts.com",
        name="Master Barber Jamal Thompson",
        title="Master Barber & Stylist",
        category=ProfessionalCategory.BARBERS_BEAUTY,
        bio="Award-winning master barber specializing in precision cuts, fades, and beard grooming.",
        credentials="Licensed Master Barber, 15 years experience",
        hourly_rate=85.00,
        phone="555-0330",
        image_url="https://images.pexels.com/photos/3992870/pexels-photo-3992870.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="stylist.washington@salon.com",
        name="Hair Stylist Ebony Washington",
        title="Natural Hair Specialist",
        category=ProfessionalCategory.BARBERS_BEAUTY,
        bio="Certified natural hair stylist specializing in locs, braids, and protective styles for all hair types.",
        credentials="Licensed Cosmetologist, Natural Hair Certified",
        hourly_rate=95.00,
        phone="555-0331",
        image_url="https://images.pexels.com/photos/3065209/pexels-photo-3065209.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="mua.jackson@beauty.com",
        name="Makeup Artist Destiny Jackson",
        title="Professional Makeup Artist",
        category=ProfessionalCategory.BARBERS_BEAUTY,
        bio="Professional makeup artist specializing in bridal, editorial, and special occasion makeup for melanin-rich skin.",
        credentials="Certified Makeup Artist, 10 years experience",
        hourly_rate=125.00,
        phone="555-0332",
        image_url="https://images.pexels.com/photos/3992871/pexels-photo-3992871.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="esthetician.moore@skincare.com",
        name="Esthetician Tiffany Moore",
        title="Licensed Esthetician",
        category=ProfessionalCategory.BARBERS_BEAUTY,
        bio="Licensed esthetician providing customized skincare treatments and facials for all skin types.",
        credentials="Licensed Esthetician, Skincare Specialist",
        hourly_rate=110.00,
        phone="555-0333",
        image_url="https://images.pexels.com/photos/3065171/pexels-photo-3065171.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="nail.tech@nails.com",
        name="Nail Technician Crystal Lee",
        title="Master Nail Technician",
        category=ProfessionalCategory.BARBERS_BEAUTY,
        bio="Master nail technician specializing in nail art, gel manicures, and pedicures with 12 years experience.",
        credentials="Licensed Nail Technician, Nail Art Specialist",
        hourly_rate=75.00,
        phone="555-0334",
        image_url="https://images.pexels.com/photos/3065210/pexels-photo-3065210.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="photographer.evans@studio.com",
        name="Photographer Marcus Evans",
        title="Portrait & Wedding Photographer",
        category=ProfessionalCategory.PHOTOGRAPHY_DESIGN,
        bio="Award-winning photographer capturing life's most precious moments with artistic vision and technical excellence.",
        credentials="Professional Photographer, 18 years experience",
        hourly_rate=200.00,
        phone="555-0335",
        image_url="https://images.pexels.com/photos/1264210/pexels-photo-1264210.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="designer.clark@creative.com",
        name="Graphic Designer Jasmine Clark",
        title="Brand & Graphic Designer",
        category=ProfessionalCategory.PHOTOGRAPHY_DESIGN,
        bio="Creative graphic designer specializing in brand identity, logo design, and marketing materials.",
        credentials="BFA Graphic Design, Adobe Certified Expert",
        hourly_rate=135.00,
        phone="555-0336",
        image_url="https://images.pexels.com/photos/3184418/pexels-photo-3184418.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="designer.walker@interiors.com",
        name="Interior Designer Natalie Walker",
        title="Interior Designer",
        category=ProfessionalCategory.PHOTOGRAPHY_DESIGN,
        bio="Licensed interior designer creating beautiful, functional spaces that reflect clients' unique personalities.",
        credentials="NCIDQ Certified, 14 years experience",
        hourly_rate=165.00,
        phone="555-0337",
        image_url="https://images.pexels.com/photos/1264210/pexels-photo-1264210.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="videographer.hill@media.com",
        name="Videographer Andre Hill",
        title="Commercial Videographer",
        category=ProfessionalCategory.PHOTOGRAPHY_DESIGN,
        bio="Professional videographer producing high-quality commercial videos, documentaries, and event coverage.",
        credentials="Film Production Degree, Emmy Nominated",
        hourly_rate=185.00,
        phone="555-0338",
        image_url="https://images.pexels.com/photos/3184611/pexels-photo-3184611.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="designer.scott@web.com",
        name="Web Designer Brittany Scott",
        title="UX/UI Designer",
        category=ProfessionalCategory.PHOTOGRAPHY_DESIGN,
        bio="User experience designer creating intuitive, beautiful digital experiences for web and mobile applications.",
        credentials="MS Human-Computer Interaction, Google UX Certified",
        hourly_rate=155.00,
        phone="555-0339",
        image_url="https://images.pexels.com/photos/3184465/pexels-photo-3184465.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="advisor.turner@auto.com",
        name="Auto Finance Advisor Derek Turner",
        title="Automotive Finance Specialist",
        category=ProfessionalCategory.AUTOMOTIVE_HOUSING,
        bio="Experienced auto finance specialist helping clients secure the best financing options for vehicle purchases.",
        credentials="Certified Automotive Finance Manager",
        hourly_rate=120.00,
        phone="555-0340",
        image_url="https://images.pexels.com/photos/7640469/pexels-photo-7640469.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="broker.phillips@mortgage.com",
        name="Mortgage Broker Sandra Phillips",
        title="Mortgage Loan Officer",
        category=ProfessionalCategory.AUTOMOTIVE_HOUSING,
        bio="Licensed mortgage broker specializing in first-time homebuyer programs and refinancing solutions.",
        credentials="NMLS Licensed, 16 years mortgage experience",
        hourly_rate=145.00,
        phone="555-0341",
        image_url="https://images.pexels.com/photos/8112184/pexels-photo-8112184.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="consultant.gray@housing.com",
        name="Housing Consultant Michael Gray",
        title="Affordable Housing Consultant",
        category=ProfessionalCategory.AUTOMOTIVE_HOUSING,
        bio="Housing consultant helping families navigate affordable housing programs and homeownership opportunities.",
        credentials="HUD Certified Housing Counselor",
        hourly_rate=110.00,
        phone="555-0342",
        image_url="https://images.pexels.com/photos/5668841/pexels-photo-5668841.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="advisor.bennett@credit.com",
        name="Credit Advisor Monique Bennett",
        title="Credit Repair Specialist",
        category=ProfessionalCategory.AUTOMOTIVE_HOUSING,
        bio="Credit repair specialist helping clients improve credit scores and qualify for better financing options.",
        credentials="Certified Credit Consultant, FICO Expert",
        hourly_rate=95.00,
        phone="555-0343",
        image_url="https://images.pexels.com/photos/7640435/pexels-photo-7640435.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="inspector.collins@home.com",
        name="Home Inspector Leonard Collins",
        title="Certified Home Inspector",
        category=ProfessionalCategory.AUTOMOTIVE_HOUSING,
        bio="Licensed home inspector providing thorough property inspections to protect homebuyers' investments.",
        credentials="ASHI Certified, 20 years construction experience",
        hourly_rate=130.00,
        phone="555-0344",
        image_url="https://images.pexels.com/photos/5669618/pexels-photo-5669618.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="strategist.price@media.com",
        name="Media Strategist Gabrielle Price",
        title="Digital Media Strategist",
        category=ProfessionalCategory.MEDIA_MARKETING,
        bio="Digital media strategist developing comprehensive campaigns that drive engagement and business growth.",
        credentials="MBA Marketing, Google Ads Certified",
        hourly_rate=175.00,
        phone="555-0345",
        image_url="https://images.pexels.com/photos/7640447/pexels-photo-7640447.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="manager.butler@social.com",
        name="Social Media Manager Tyrone Butler",
        title="Social Media Marketing Manager",
        category=ProfessionalCategory.MEDIA_MARKETING,
        bio="Social media expert helping brands build authentic connections and grow their online presence.",
        credentials="Certified Social Media Manager, 10 years experience",
        hourly_rate=140.00,
        phone="555-0346",
        image_url="https://images.pexels.com/photos/8112185/pexels-photo-8112185.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="specialist.rivera@pr.com",
        name="PR Specialist Carmen Rivera",
        title="Public Relations Specialist",
        category=ProfessionalCategory.MEDIA_MARKETING,
        bio="Public relations professional managing brand reputation and securing media coverage for clients.",
        credentials="APR Accreditation, Former Journalist",
        hourly_rate=160.00,
        phone="555-0347",
        image_url="https://images.pexels.com/photos/5668842/pexels-photo-5668842.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="writer.sanders@content.com",
        name="Content Writer Jordan Sanders",
        title="Content Marketing Writer",
        category=ProfessionalCategory.MEDIA_MARKETING,
        bio="Professional content writer creating compelling copy that converts readers into customers.",
        credentials="BA Journalism, SEO Certified",
        hourly_rate=115.00,
        phone="555-0348",
        image_url="https://images.pexels.com/photos/7640441/pexels-photo-7640441.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="producer.hughes@broadcast.com",
        name="Media Producer Vanessa Hughes",
        title="Broadcast Media Producer",
        category=ProfessionalCategory.MEDIA_MARKETING,
        bio="Award-winning media producer with experience in television, radio, and digital content production.",
        credentials="Emmy Award Winner, 15 years broadcasting",
        hourly_rate=195.00,
        phone="555-0349",
        image_url="https://images.pexels.com/photos/5669620/pexels-photo-5669620.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="director.powell@nonprofit.org",
        name="Nonprofit Director Angela Powell",
        title="Nonprofit Executive Director",
        category=ProfessionalCategory.NONPROFITS,
        bio="Experienced nonprofit leader with proven track record in fundraising, program development, and community impact.",
        credentials="MPA, 20 years nonprofit leadership",
        hourly_rate=185.00,
        phone="555-0350",
        image_url="https://images.pexels.com/photos/7640454/pexels-photo-7640454.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="coordinator.long@community.org",
        name="Community Organizer Marcus Long",
        title="Community Engagement Coordinator",
        category=ProfessionalCategory.NONPROFITS,
        bio="Grassroots organizer mobilizing communities for social justice and positive change.",
        credentials="MSW, 12 years community organizing",
        hourly_rate=125.00,
        phone="555-0351",
        image_url="https://images.pexels.com/photos/8112186/pexels-photo-8112186.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="manager.perry@grants.org",
        name="Grant Writer Stephanie Perry",
        title="Grant Writing Specialist",
        category=ProfessionalCategory.NONPROFITS,
        bio="Professional grant writer securing millions in funding for nonprofits and community organizations.",
        credentials="GPC Certified, $50M+ Grants Secured",
        hourly_rate=150.00,
        phone="555-0352",
        image_url="https://images.pexels.com/photos/5668843/pexels-photo-5668843.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="coordinator.jenkins@volunteer.org",
        name="Volunteer Coordinator Keith Jenkins",
        title="Volunteer Program Manager",
        category=ProfessionalCategory.NONPROFITS,
        bio="Volunteer coordinator building and managing effective volunteer programs that create lasting community impact.",
        credentials="CVA Certified, Nonprofit Management Certificate",
        hourly_rate=105.00,
        phone="555-0353",
        image_url="https://images.pexels.com/photos/7640448/pexels-photo-7640448.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    db.create_professional(ProfessionalCreate(
        email="advocate.barnes@social.org",
        name="Social Worker Dr. Michelle Barnes",
        title="Licensed Clinical Social Worker",
        category=ProfessionalCategory.NONPROFITS,
        bio="Licensed social worker providing counseling, advocacy, and support services to underserved communities.",
        credentials="LCSW, PhD in Social Work",
        hourly_rate=135.00,
        phone="555-0354",
        image_url="https://images.pexels.com/photos/5669621/pexels-photo-5669621.jpeg?auto=compress&cs=tinysrgb&w=500"
    ))
    
    print("Database seeded successfully!")
    print(f"Created {len(db.vendors)} vendors")
    print(f"Created {len(db.products)} products")
    print(f"Created {len(db.professionals)} professionals")
