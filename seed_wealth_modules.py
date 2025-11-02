"""
Seed script for Wealth Hub modules
Run this to populate the wealth_modules table with sample educational content
"""
from app.db_models import SessionLocal
from app.db_models.models import WealthModule

def seed_wealth_modules():
    db = SessionLocal()
    
    existing_count = db.query(WealthModule).count()
    if existing_count > 0:
        print(f"✅ Wealth modules already seeded ({existing_count} modules exist)")
        db.close()
        return
    
    modules = [
        {
            "title": "Introduction to Generational Wealth",
            "description": "Learn the fundamentals of building wealth that lasts for generations",
            "content": "This module covers the basics of generational wealth, including asset accumulation, financial literacy, and long-term planning strategies.",
            "tier_required": "Free",
            "points_reward": 75,
            "duration_minutes": 15,
            "category": "Foundations",
            "order_index": 1
        },
        {
            "title": "Understanding Credit and Debt",
            "description": "Master the fundamentals of credit scores, debt management, and financial health",
            "content": "Learn how credit works, how to improve your credit score, and strategies for managing and eliminating debt effectively.",
            "tier_required": "Free",
            "points_reward": 75,
            "duration_minutes": 20,
            "category": "Foundations",
            "order_index": 2
        },
        {
            "title": "Budgeting Basics",
            "description": "Create a sustainable budget that works for your lifestyle and goals",
            "content": "Discover proven budgeting methods, expense tracking techniques, and how to allocate your income for maximum financial growth.",
            "tier_required": "Free",
            "points_reward": 75,
            "duration_minutes": 25,
            "category": "Foundations",
            "order_index": 3
        },
        {
            "title": "Emergency Fund Essentials",
            "description": "Build a financial safety net to protect against unexpected expenses",
            "content": "Learn why emergency funds are critical, how much to save, and the best places to keep your emergency savings.",
            "tier_required": "Free",
            "points_reward": 75,
            "duration_minutes": 15,
            "category": "Foundations",
            "order_index": 4
        },
        
        {
            "title": "Investment Fundamentals",
            "description": "Introduction to stocks, bonds, and investment strategies",
            "content": "Explore different investment vehicles, risk management, diversification strategies, and how to start building an investment portfolio.",
            "tier_required": "Premium",
            "points_reward": 100,
            "duration_minutes": 30,
            "category": "Investing",
            "order_index": 5
        },
        {
            "title": "Real Estate Investing 101",
            "description": "Learn how to build wealth through property investment",
            "content": "Discover real estate investment strategies, from rental properties to REITs, and how to evaluate property investment opportunities.",
            "tier_required": "Premium",
            "points_reward": 100,
            "duration_minutes": 35,
            "category": "Investing",
            "order_index": 6
        },
        {
            "title": "Retirement Planning Strategies",
            "description": "Plan for a secure and comfortable retirement",
            "content": "Learn about 401(k)s, IRAs, pension plans, and how to calculate how much you need to save for retirement.",
            "tier_required": "Premium",
            "points_reward": 100,
            "duration_minutes": 30,
            "category": "Planning",
            "order_index": 7
        },
        {
            "title": "Tax Optimization Strategies",
            "description": "Minimize your tax burden and maximize your wealth",
            "content": "Understand tax-advantaged accounts, deductions, credits, and strategies to legally reduce your tax liability.",
            "tier_required": "Premium",
            "points_reward": 100,
            "duration_minutes": 40,
            "category": "Planning",
            "order_index": 8
        },
        
        {
            "title": "Advanced Portfolio Management",
            "description": "Master sophisticated investment strategies and portfolio optimization",
            "content": "Learn advanced concepts like asset allocation, rebalancing, tax-loss harvesting, and modern portfolio theory.",
            "tier_required": "Investor",
            "points_reward": 150,
            "duration_minutes": 45,
            "category": "Advanced",
            "order_index": 9
        },
        {
            "title": "Business Ownership and Entrepreneurship",
            "description": "Build wealth through business ownership and entrepreneurship",
            "content": "Explore business structures, funding strategies, scaling techniques, and how to build a valuable business asset.",
            "tier_required": "Investor",
            "points_reward": 150,
            "duration_minutes": 50,
            "category": "Advanced",
            "order_index": 10
        },
        {
            "title": "Estate Planning and Wealth Transfer",
            "description": "Protect and transfer your wealth to future generations",
            "content": "Learn about wills, trusts, estate taxes, and strategies to efficiently transfer wealth to your heirs.",
            "tier_required": "Investor",
            "points_reward": 150,
            "duration_minutes": 40,
            "category": "Advanced",
            "order_index": 11
        },
        {
            "title": "Alternative Investments",
            "description": "Explore cryptocurrency, private equity, and other alternative assets",
            "content": "Discover alternative investment opportunities beyond traditional stocks and bonds, including crypto, private equity, and commodities.",
            "tier_required": "Investor",
            "points_reward": 150,
            "duration_minutes": 45,
            "category": "Advanced",
            "order_index": 12
        }
    ]
    
    for module_data in modules:
        module = WealthModule(**module_data)
        db.add(module)
    
    db.commit()
    print(f"✅ Successfully seeded {len(modules)} wealth modules")
    db.close()

if __name__ == "__main__":
    seed_wealth_modules()
