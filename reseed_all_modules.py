"""
Comprehensive Reseeding Script for BlkXchange Backend
Reseeds all modules from Phases 10-14A via API endpoints
"""
import requests
import json
from datetime import datetime

BASE_URL = "https://blkxchange-backend.onrender.com"

def test_endpoint(endpoint):
    """Test if an endpoint is accessible"""
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
        print(f"  {endpoint}: HTTP {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"  {endpoint}: ERROR - {e}")
        return False

def seed_wealth_hub():
    """Seed Wealth Hub modules"""
    print("\n📚 SEEDING WEALTH HUB MODULES")
    print("=" * 50)
    
    modules = [
        {
            "title": "Entrepreneurship Essentials",
            "category": "Business",
            "description": "Master the fundamentals of starting and scaling a successful Black-owned business. Learn business planning, market research, and customer acquisition strategies.",
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        },
        {
            "title": "Investing for Legacy",
            "category": "Finance",
            "description": "Build generational wealth through strategic investing. Explore stocks, real estate, and alternative investments tailored for the Black community.",
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        },
        {
            "title": "Mindset Mastery & Discipline",
            "category": "Personal Development",
            "description": "Develop the mental fortitude and discipline required for long-term success. Learn from successful Black entrepreneurs and thought leaders.",
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        }
    ]
    
    for module in modules:
        try:
            response = requests.post(f"{BASE_URL}/api/modules", json=module, timeout=10)
            if response.status_code in [200, 201]:
                print(f"  ✅ {module['title']}")
            else:
                print(f"  ❌ {module['title']}: {response.status_code} - {response.text[:100]}")
        except Exception as e:
            print(f"  ❌ {module['title']}: {e}")

def seed_legacy_wall():
    """Seed Legacy Wall tributes"""
    print("\n🏛️ SEEDING LEGACY WALL TRIBUTES")
    print("=" * 50)
    
    tributes = [
        {
            "name": "Madam C.J. Walker",
            "relation": "Pioneer",
            "biography": "America's first female self-made millionaire. Built a beauty empire and became a philanthropist supporting Black education and institutions.",
            "photo_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400",
            "era": "1867-1919"
        },
        {
            "name": "Dr. Martin Luther King Jr.",
            "relation": "Leader",
            "biography": "Civil rights icon who led the movement for racial equality through nonviolent resistance. His legacy continues to inspire generations.",
            "photo_url": "https://images.unsplash.com/photo-1573496774426-fe3db3dd1731?w=400",
            "era": "1929-1968"
        },
        {
            "name": "Harriet Tubman",
            "relation": "Freedom Fighter",
            "biography": "Escaped slavery and became a conductor on the Underground Railroad, leading hundreds to freedom. Later served as a spy for the Union Army.",
            "photo_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400",
            "era": "1822-1913"
        }
    ]
    
    for tribute in tributes:
        try:
            response = requests.post(f"{BASE_URL}/api/legacy", json=tribute, timeout=10)
            if response.status_code in [200, 201]:
                print(f"  ✅ {tribute['name']}")
            else:
                print(f"  ❌ {tribute['name']}: {response.status_code} - {response.text[:100]}")
        except Exception as e:
            print(f"  ❌ {tribute['name']}: {e}")

def seed_history_window():
    """Seed History Window 2.0 entries"""
    print("\n📜 SEEDING HISTORY WINDOW 2.0")
    print("=" * 50)
    
    entries = [
        {
            "title": "Tulsa Race Massacre",
            "year": 1921,
            "description": "The destruction of Black Wall Street in Tulsa, Oklahoma. A thriving Black community was attacked, resulting in hundreds of deaths and the destruction of 35 city blocks.",
            "image_url": "https://images.unsplash.com/photo-1541963463532-d68292c34b19?w=800"
        },
        {
            "title": "Brown v. Board of Education",
            "year": 1954,
            "description": "Landmark Supreme Court decision that declared racial segregation in public schools unconstitutional, overturning Plessy v. Ferguson.",
            "image_url": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=800"
        },
        {
            "title": "March on Washington",
            "year": 1963,
            "description": "Historic civil rights march where Dr. Martin Luther King Jr. delivered his iconic 'I Have a Dream' speech to over 250,000 people.",
            "image_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=800"
        }
    ]
    
    for entry in entries:
        try:
            response = requests.post(f"{BASE_URL}/api/history", json=entry, timeout=10)
            if response.status_code in [200, 201]:
                print(f"  ✅ {entry['title']}")
            else:
                print(f"  ❌ {entry['title']}: {response.status_code} - {response.text[:100]}")
        except Exception as e:
            print(f"  ❌ {entry['title']}: {e}")

def seed_community_hub():
    """Seed Community Hub events"""
    print("\n🎉 SEEDING COMMUNITY HUB EVENTS")
    print("=" * 50)
    
    events = [
        {
            "name": "Black Business Expo 2025",
            "description": "Annual showcase of Black-owned businesses, featuring networking, workshops, and vendor booths. Connect with entrepreneurs and discover new products.",
            "category": "Business",
            "date": "2025-12-15",
            "location": "Atlanta Convention Center"
        },
        {
            "name": "HBCU College Fair",
            "description": "Meet representatives from Historically Black Colleges and Universities. Learn about programs, scholarships, and campus life.",
            "category": "Education",
            "date": "2025-11-20",
            "location": "Virtual Event"
        }
    ]
    
    for event in events:
        try:
            response = requests.post(f"{BASE_URL}/api/events", json=event, timeout=10)
            if response.status_code in [200, 201]:
                print(f"  ✅ {event['name']}")
            else:
                print(f"  ❌ {event['name']}: {response.status_code} - {response.text[:100]}")
        except Exception as e:
            print(f"  ❌ {event['name']}: {e}")

def seed_private_groups():
    """Seed Private Groups"""
    print("\n👥 SEEDING PRIVATE GROUPS")
    print("=" * 50)
    
    groups = [
        {
            "name": "Black Tech Founders",
            "description": "Exclusive community for Black technology entrepreneurs. Share insights, collaborate on projects, and access mentorship.",
            "category": "Technology",
            "member_count": 0
        },
        {
            "name": "Real Estate Investors Circle",
            "description": "Private group for Black real estate investors. Discuss deals, share market insights, and build wealth through property.",
            "category": "Real Estate",
            "member_count": 0
        }
    ]
    
    for group in groups:
        try:
            response = requests.post(f"{BASE_URL}/api/groups", json=group, timeout=10)
            if response.status_code in [200, 201]:
                print(f"  ✅ {group['name']}")
            else:
                print(f"  ❌ {group['name']}: {response.status_code} - {response.text[:100]}")
        except Exception as e:
            print(f"  ❌ {group['name']}: {e}")

def seed_black_chronicle():
    """Seed additional Black Chronicle articles"""
    print("\n📰 SEEDING BLACK CHRONICLE ARTICLES")
    print("=" * 50)
    
    articles = [
        {
            "title": "The Economic Power of Black Dollars",
            "category": "Finance",
            "body": "Exploring how collective economic action in the Black community can drive systemic change and build generational wealth.",
            "author": "Dr. Aldric Marshall",
            "image_url": "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=800"
        },
        {
            "title": "HBCUs: Engines of Innovation",
            "category": "Education",
            "body": "How Historically Black Colleges and Universities continue to produce leaders, innovators, and change-makers across all industries.",
            "author": "Prof. Angela Williams",
            "image_url": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800"
        },
        {
            "title": "Black Women in Leadership",
            "category": "Business",
            "body": "Celebrating the achievements of Black women breaking barriers in corporate America and entrepreneurship.",
            "author": "Jasmine Clarke",
            "image_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=800"
        }
    ]
    
    for article in articles:
        try:
            response = requests.post(f"{BASE_URL}/api/articles", json=article, timeout=10)
            if response.status_code in [200, 201]:
                print(f"  ✅ {article['title']}")
            else:
                print(f"  ❌ {article['title']}: {response.status_code} - {response.text[:100]}")
        except Exception as e:
            print(f"  ❌ {article['title']}: {e}")

def verify_all_endpoints():
    """Verify all endpoints have data"""
    print("\n✅ VERIFYING ALL ENDPOINTS")
    print("=" * 50)
    
    endpoints = [
        "/api/modules",
        "/api/legacy",
        "/api/history",
        "/api/events",
        "/api/groups",
        "/api/articles"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                count = len(data) if isinstance(data, list) else "N/A"
                print(f"  ✅ {endpoint}: {count} records")
            else:
                print(f"  ❌ {endpoint}: HTTP {response.status_code}")
        except Exception as e:
            print(f"  ❌ {endpoint}: {e}")

if __name__ == "__main__":
    print("🚀 BLKXCHANGE FULL ECOSYSTEM RESTORE & RESEED")
    print("=" * 50)
    print(f"Target: {BASE_URL}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test connectivity first
    print("🔍 TESTING ENDPOINT CONNECTIVITY")
    print("=" * 50)
    test_endpoint("/api/modules")
    test_endpoint("/api/legacy")
    test_endpoint("/api/history")
    test_endpoint("/api/events")
    test_endpoint("/api/groups")
    test_endpoint("/api/articles")
    
    # Seed all modules
    seed_wealth_hub()
    seed_legacy_wall()
    seed_history_window()
    seed_community_hub()
    seed_private_groups()
    seed_black_chronicle()
    
    # Verify
    verify_all_endpoints()
    
    print()
    print("=" * 50)
    print(f"✅ RESEEDING COMPLETE!")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
