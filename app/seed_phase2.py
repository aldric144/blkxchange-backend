from datetime import datetime
from app.database import db
from app.models import (
    Blk360WealthModuleCreate, WealthModuleCategory, WealthModuleAccessLevel,
    Blk360LegacyEntryCreate, LegacyEntryCategory,
    Blk360HistoryEntryCreate, HistoryDecade, HistorySourceType,
    Blk360ForumPostCreate, Forum360Category
)

def seed_phase2_data():
    print("\n🚀 Seeding BlkXchange 360™ Phase 2 MVP Data...")
    
    print("📚 Creating 5 Wealth Hub modules...")
    module1 = db.create_blk360_wealth_module(Blk360WealthModuleCreate(
        title="Turning Passion into Profit",
        category=WealthModuleCategory.ENTREPRENEURSHIP,
        description="Learn how to transform your passion into a sustainable business. This module covers business planning, market research, and launching your first product or service.",
        video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        thumbnail_url="https://images.pexels.com/photos/3184292/pexels-photo-3184292.jpeg?w=400",
        access_level=WealthModuleAccessLevel.FREE,
        published=True
    ))
    
    module2 = db.create_blk360_wealth_module(Blk360WealthModuleCreate(
        title="Basics of Index Funds",
        category=WealthModuleCategory.INVESTING,
        description="Understand the fundamentals of index fund investing and how to build long-term wealth through diversified portfolios. Perfect for beginners.",
        video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        thumbnail_url="https://images.pexels.com/photos/6801648/pexels-photo-6801648.jpeg?w=400",
        access_level=WealthModuleAccessLevel.PREMIUM,
        published=True
    ))
    
    module3 = db.create_blk360_wealth_module(Blk360WealthModuleCreate(
        title="Servant Leadership in Action",
        category=WealthModuleCategory.LEADERSHIP,
        description="Discover the principles of servant leadership and how to lead with empathy, integrity, and purpose in your business and community.",
        video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        thumbnail_url="https://images.pexels.com/photos/3184338/pexels-photo-3184338.jpeg?w=400",
        access_level=WealthModuleAccessLevel.PREMIUM,
        published=True
    ))
    
    module4 = db.create_blk360_wealth_module(Blk360WealthModuleCreate(
        title="Budgeting for Stability",
        category=WealthModuleCategory.FINANCIAL_LITERACY,
        description="Master the art of budgeting with practical strategies to manage your income, reduce debt, and build an emergency fund.",
        video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        thumbnail_url="https://images.pexels.com/photos/6801642/pexels-photo-6801642.jpeg?w=400",
        access_level=WealthModuleAccessLevel.FREE,
        published=True
    ))
    
    module5 = db.create_blk360_wealth_module(Blk360WealthModuleCreate(
        title="Resilience and Faith in Business",
        category=WealthModuleCategory.MINDSET,
        description="Cultivate mental resilience and spiritual strength to overcome entrepreneurial challenges. Learn how faith and mindset drive success.",
        video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        thumbnail_url="https://images.pexels.com/photos/3184339/pexels-photo-3184339.jpeg?w=400",
        access_level=WealthModuleAccessLevel.ELITE,
        published=True
    ))
    
    print("🕊️ Creating 15 Legacy Wall sample stories...")
    legacy_stories = [
        {
            "title": "My Grandmother's Strength",
            "honoree_name": "Rosa Mae Johnson",
            "story": "My grandmother Rosa Mae Johnson was born in 1932 in rural Mississippi. Despite facing segregation and limited opportunities, she became a teacher and educated three generations of Black children in our community. She taught us that education is the key to freedom and that our heritage is our strength. Her legacy lives on through the hundreds of students she inspired.",
            "category": LegacyEntryCategory.FAMILY,
            "photo_url": "https://images.pexels.com/photos/3768894/pexels-photo-3768894.jpeg?w=400"
        },
        {
            "title": "A Pillar of Our Community",
            "honoree_name": "Reverend James Washington",
            "story": "Reverend Washington founded our church in 1965 and led the civil rights movement in our town. He organized peaceful protests, voter registration drives, and youth mentorship programs. His unwavering faith and commitment to justice changed our community forever. He showed us that faith without action is dead.",
            "category": LegacyEntryCategory.COMMUNITY,
            "photo_url": "https://images.pexels.com/photos/3768895/pexels-photo-3768895.jpeg?w=400"
        },
        {
            "title": "Building Black Wall Street",
            "honoree_name": "Marcus Thompson Sr.",
            "story": "My great-grandfather Marcus Thompson Sr. owned a successful grocery store in Tulsa's Greenwood District before the 1921 massacre. Though he lost everything, he rebuilt his business and taught us the importance of Black economic empowerment. His entrepreneurial spirit lives on in our family's businesses today.",
            "category": LegacyEntryCategory.BUSINESS,
            "photo_url": "https://images.pexels.com/photos/3768896/pexels-photo-3768896.jpeg?w=400"
        },
        {
            "title": "The Teacher Who Changed Lives",
            "honoree_name": "Dr. Sarah Mitchell",
            "story": "Dr. Mitchell was the first Black woman to earn a PhD in Mathematics from our state university in 1968. She returned to teach at our local HBCU and mentored countless students who went on to become engineers, scientists, and educators. She proved that excellence has no color barrier.",
            "category": LegacyEntryCategory.EDUCATION,
            "photo_url": "https://images.pexels.com/photos/3768897/pexels-photo-3768897.jpeg?w=400"
        },
        {
            "title": "Faith That Moved Mountains",
            "honoree_name": "Mother Evelyn Brown",
            "story": "Mother Brown was a prayer warrior who founded our church's intercessory prayer ministry. For 40 years, she prayed for families, businesses, and our community. Her faith was unshakeable, and countless testimonies of healing and breakthrough came through her prayers. She taught us that prayer changes everything.",
            "category": LegacyEntryCategory.FAITH,
            "photo_url": "https://images.pexels.com/photos/3768898/pexels-photo-3768898.jpeg?w=400"
        },
        {
            "title": "The Midwife Who Delivered Hope",
            "honoree_name": "Mama Josephine Carter",
            "story": "Mama Josephine was a midwife who delivered over 2,000 babies in our community from the 1940s to 1980s. When Black women couldn't access hospitals due to segregation, she was there. She saved countless lives with her skill, wisdom, and compassion. She was a true healer.",
            "category": LegacyEntryCategory.COMMUNITY,
            "photo_url": "https://images.pexels.com/photos/3768899/pexels-photo-3768899.jpeg?w=400"
        },
        {
            "title": "My Father's Sacrifice",
            "honoree_name": "William Davis",
            "story": "My father William Davis worked three jobs to send all five of his children to college. He never complained, never gave up, and always reminded us that education was the pathway to a better life. Because of his sacrifice, we all graduated and now serve our communities as doctors, teachers, and business owners.",
            "category": LegacyEntryCategory.FAMILY,
            "photo_url": "https://images.pexels.com/photos/3768900/pexels-photo-3768900.jpeg?w=400"
        },
        {
            "title": "The Barber Who Built Community",
            "honoree_name": "Mr. Charles 'Chuck' Robinson",
            "story": "Mr. Chuck's barbershop was more than a place for haircuts—it was a community hub where men gathered to discuss politics, mentor young boys, and support each other. For 50 years, he created a safe space for Black men to be themselves. His shop was a sanctuary.",
            "category": LegacyEntryCategory.BUSINESS,
            "photo_url": "https://images.pexels.com/photos/3768901/pexels-photo-3768901.jpeg?w=400"
        },
        {
            "title": "The Seamstress Who Dressed Dreams",
            "honoree_name": "Miss Dorothy Lee",
            "story": "Miss Dorothy was a master seamstress who made custom clothing for our community. She dressed brides, graduates, and church choirs with elegance and pride. She taught young girls the art of sewing and self-sufficiency. Her craftsmanship was her ministry.",
            "category": LegacyEntryCategory.BUSINESS,
            "photo_url": "https://images.pexels.com/photos/3768902/pexels-photo-3768902.jpeg?w=400"
        },
        {
            "title": "The Coach Who Built Champions",
            "honoree_name": "Coach Robert 'Big Rob' Williams",
            "story": "Coach Williams led our high school basketball team to five state championships, but his real legacy was teaching young men about discipline, teamwork, and character. Many of his players went on to college on scholarships. He built champions on and off the court.",
            "category": LegacyEntryCategory.EDUCATION,
            "photo_url": "https://images.pexels.com/photos/3768903/pexels-photo-3768903.jpeg?w=400"
        },
        {
            "title": "The Nurse Who Healed with Love",
            "honoree_name": "Nurse Betty Jackson",
            "story": "Nurse Betty worked at our community hospital for 45 years. She treated every patient with dignity and compassion, especially during the civil rights era when Black patients faced discrimination. She was an angel in scrubs who healed bodies and souls.",
            "category": LegacyEntryCategory.COMMUNITY,
            "photo_url": "https://images.pexels.com/photos/3768904/pexels-photo-3768904.jpeg?w=400"
        },
        {
            "title": "The Farmer Who Fed Generations",
            "honoree_name": "Mr. Henry 'Hank' Green",
            "story": "Mr. Hank owned 200 acres of farmland that he inherited from his grandfather, a freed slave. He grew vegetables and raised livestock, providing fresh food to our community for decades. He taught us the value of land ownership and self-sufficiency.",
            "category": LegacyEntryCategory.BUSINESS,
            "photo_url": "https://images.pexels.com/photos/3768905/pexels-photo-3768905.jpeg?w=400"
        },
        {
            "title": "The Librarian Who Opened Worlds",
            "honoree_name": "Mrs. Clara Jenkins",
            "story": "Mrs. Jenkins was our town's first Black librarian. She created a special section for African American literature and history when it was controversial to do so. She introduced countless children to books that reflected their heritage and inspired them to dream bigger.",
            "category": LegacyEntryCategory.EDUCATION,
            "photo_url": "https://images.pexels.com/photos/3768906/pexels-photo-3768906.jpeg?w=400"
        },
        {
            "title": "The Musician Who Preserved Our Sound",
            "honoree_name": "Professor James 'Jazz' Turner",
            "story": "Professor Turner taught music at our HBCU for 40 years and preserved the tradition of gospel, blues, and jazz. He mentored Grammy-winning artists and ensured that our musical heritage was passed down to future generations. His legacy is in every note we play.",
            "category": LegacyEntryCategory.EDUCATION,
            "photo_url": "https://images.pexels.com/photos/3768907/pexels-photo-3768907.jpeg?w=400"
        },
        {
            "title": "The Activist Who Never Quit",
            "honoree_name": "Mrs. Fannie Lou Harris",
            "story": "Mrs. Harris was a civil rights activist who organized voter registration drives, sit-ins, and protests throughout the 1960s. She was arrested multiple times but never stopped fighting for justice. She taught us that freedom is never free and that we must always stand up for what's right.",
            "category": LegacyEntryCategory.COMMUNITY,
            "photo_url": "https://images.pexels.com/photos/3768908/pexels-photo-3768908.jpeg?w=400"
        }
    ]
    
    for story_data in legacy_stories:
        db.create_blk360_legacy_entry(Blk360LegacyEntryCreate(
            user_email="demo@blkxchange.com",
            title=story_data["title"],
            honoree_name=story_data["honoree_name"],
            story=story_data["story"],
            category=story_data["category"],
            photo_url=story_data["photo_url"]
        ))
        from app.models import LegacyEntryStatus
        entries = db.get_all_blk360_legacy_entries(status=LegacyEntryStatus.PENDING)
        if entries:
            db.update_blk360_legacy_entry_status(entries[-1].id, LegacyEntryStatus.APPROVED, featured=(len(entries) <= 3))
    
    print("📜 Creating 30 History Window entries...")
    history_entries = [
        {"name": "Benjamin Banneker", "field": "Astronomy & Mathematics", "decade": HistoryDecade.PRE_1900, "biography": "Benjamin Banneker (1731-1806) was a self-taught mathematician, astronomer, and surveyor. He helped survey the boundaries of Washington D.C. and published almanacs that challenged racial stereotypes about Black intellectual capacity.", "photo_url": "https://images.pexels.com/photos/3768909/pexels-photo-3768909.jpeg?w=400", "source_url": "https://www.blackpast.org/african-american-history/banneker-benjamin-1731-1806/"},
        {"name": "Harriet Tubman", "field": "Abolitionist & Freedom Fighter", "decade": HistoryDecade.PRE_1900, "biography": "Harriet Tubman (1822-1913) escaped slavery and became a conductor on the Underground Railroad, leading over 300 enslaved people to freedom. She also served as a spy and scout for the Union Army during the Civil War.", "photo_url": "https://images.pexels.com/photos/3768910/pexels-photo-3768910.jpeg?w=400", "source_url": "https://www.blackpast.org/african-american-history/tubman-harriet-1820-1913/"},
        {"name": "Frederick Douglass", "field": "Abolitionist & Orator", "decade": HistoryDecade.PRE_1900, "biography": "Frederick Douglass (1818-1895) escaped slavery to become a leading abolitionist, orator, and writer. His autobiography 'Narrative of the Life of Frederick Douglass' became a powerful anti-slavery document.", "photo_url": "https://images.pexels.com/photos/3768911/pexels-photo-3768911.jpeg?w=400", "source_url": "https://www.blackpast.org/african-american-history/douglass-frederick-1818-1895/"},
        {"name": "Sojourner Truth", "field": "Abolitionist & Women's Rights Activist", "decade": HistoryDecade.PRE_1900, "biography": "Sojourner Truth (1797-1883) was an abolitionist and women's rights activist. Her famous 'Ain't I a Woman?' speech at the 1851 Women's Rights Convention challenged prevailing notions of racial and gender inequality.", "photo_url": "https://images.pexels.com/photos/3768912/pexels-photo-3768912.jpeg?w=400", "source_url": "https://www.blackpast.org/african-american-history/truth-sojourner-1797-1883/"},
        {"name": "Booker T. Washington", "field": "Educator & Author", "decade": HistoryDecade.PRE_1900, "biography": "Booker T. Washington (1856-1915) founded Tuskegee Institute and became a leading voice for Black education and economic advancement. His autobiography 'Up From Slavery' inspired millions.", "photo_url": "https://images.pexels.com/photos/3768913/pexels-photo-3768913.jpeg?w=400", "source_url": "https://www.blackpast.org/african-american-history/washington-booker-t-1856-1915/"},
        {"name": "George Washington Carver", "field": "Agricultural Scientist", "decade": HistoryDecade.DECADE_1900_1950, "biography": "George Washington Carver (1864-1943) was an agricultural scientist who developed hundreds of products from peanuts, sweet potatoes, and soybeans, revolutionizing Southern agriculture and helping poor farmers.", "photo_url": "https://images.pexels.com/photos/3768914/pexels-photo-3768914.jpeg?w=400", "source_url": "https://www.blackpast.org/african-american-history/carver-george-washington-1864-1943/"},
        {"name": "W.E.B. Du Bois", "field": "Sociologist & Civil Rights Activist", "decade": HistoryDecade.DECADE_1900_1950, "biography": "W.E.B. Du Bois (1868-1963) was the first African American to earn a PhD from Harvard. He co-founded the NAACP and wrote 'The Souls of Black Folk,' a seminal work on race in America.", "photo_url": "https://images.pexels.com/photos/3768915/pexels-photo-3768915.jpeg?w=400", "source_url": "https://www.blackpast.org/african-american-history/du-bois-w-e-b-1868-1963/"},
        {"name": "Madam C.J. Walker", "field": "Entrepreneur & Philanthropist", "decade": HistoryDecade.DECADE_1900_1950, "biography": "Madam C.J. Walker (1867-1919) became America's first female self-made millionaire by creating a line of beauty and hair products for Black women. She was also a philanthropist and activist.", "photo_url": "https://images.pexels.com/photos/3768916/pexels-photo-3768916.jpeg?w=400", "source_url": "https://www.blackpast.org/african-american-history/walker-madam-c-j-1867-1919/"},
        {"name": "Ida B. Wells", "field": "Journalist & Anti-Lynching Activist", "decade": HistoryDecade.DECADE_1900_1950, "biography": "Ida B. Wells (1862-1931) was an investigative journalist who documented lynching in America and co-founded the NAACP. Her fearless reporting exposed racial violence and sparked national outrage.", "photo_url": "https://images.pexels.com/photos/3768917/pexels-photo-3768917.jpeg?w=400", "source_url": "https://www.blackpast.org/african-american-history/wells-barnett-ida-b-1862-1931/"},
        {"name": "Langston Hughes", "field": "Poet & Writer", "decade": HistoryDecade.DECADE_1900_1950, "biography": "Langston Hughes (1902-1967) was a leading figure of the Harlem Renaissance. His poetry and prose celebrated Black life and culture, and his work continues to inspire generations.", "photo_url": "https://images.pexels.com/photos/3768918/pexels-photo-3768918.jpeg?w=400", "source_url": "https://www.blackpast.org/african-american-history/hughes-langston-1902-1967/"},
        {"name": "Zora Neale Hurston", "field": "Author & Anthropologist", "decade": HistoryDecade.DECADE_1900_1950, "biography": "Zora Neale Hurston (1891-1960) was a novelist, folklorist, and anthropologist. Her novel 'Their Eyes Were Watching God' is considered a masterpiece of African American literature.", "photo_url": "https://images.pexels.com/photos/3768919/pexels-photo-3768919.jpeg?w=400", "source_url": "https://www.blackpast.org/african-american-history/hurston-zora-neale-1891-1960/"},
        {"name": "Jackie Robinson", "field": "Baseball Player & Civil Rights Advocate", "decade": HistoryDecade.DECADE_1900_1950, "biography": "Jackie Robinson (1919-1972) broke baseball's color barrier in 1947, becoming the first Black player in Major League Baseball. His courage and excellence paved the way for integration in sports.", "photo_url": "https://images.pexels.com/photos/3768920/pexels-photo-3768920.jpeg?w=400", "source_url": "https://www.blackpast.org/african-american-history/robinson-jackie-1919-1972/"},
        {"name": "Rosa Parks", "field": "Civil Rights Activist", "decade": HistoryDecade.DECADE_1950_2000, "biography": "Rosa Parks (1913-2005) sparked the Montgomery Bus Boycott in 1955 when she refused to give up her seat to a white passenger. Her act of defiance became a catalyst for the Civil Rights Movement.", "photo_url": "https://images.pexels.com/photos/3768921/pexels-photo-3768921.jpeg?w=400", "source_url": "https://www.blackpast.org/african-american-history/parks-rosa-1913-2005/"},
        {"name": "Dr. Martin Luther King Jr.", "field": "Civil Rights Leader & Minister", "decade": HistoryDecade.DECADE_1950_2000, "biography": "Dr. Martin Luther King Jr. (1929-1968) led the Civil Rights Movement with nonviolent resistance. His 'I Have a Dream' speech and leadership helped end legal segregation in America.", "photo_url": "https://images.pexels.com/photos/3768922/pexels-photo-3768922.jpeg?w=400", "source_url": "https://www.blackpast.org/african-american-history/king-martin-luther-jr-1929-1968/"},
        {"name": "Malcolm X", "field": "Civil Rights Leader & Minister", "decade": HistoryDecade.DECADE_1950_2000, "biography": "Malcolm X (1925-1965) was a powerful orator and advocate for Black empowerment. His autobiography and speeches continue to inspire movements for racial justice worldwide.", "photo_url": "https://images.pexels.com/photos/3768923/pexels-photo-3768923.jpeg?w=400", "source_url": "https://www.blackpast.org/african-american-history/malcolm-x-1925-1965/"},
        {"name": "Maya Angelou", "field": "Poet & Author", "decade": HistoryDecade.DECADE_1950_2000, "biography": "Maya Angelou (1928-2014) was a poet, memoirist, and civil rights activist. Her autobiography 'I Know Why the Caged Bird Sings' is a classic of American literature.", "photo_url": "https://images.pexels.com/photos/3768924/pexels-photo-3768924.jpeg?w=400", "source_url": "https://www.blackpast.org/african-american-history/angelou-maya-1928-2014/"},
        {"name": "Thurgood Marshall", "field": "Supreme Court Justice", "decade": HistoryDecade.DECADE_1950_2000, "biography": "Thurgood Marshall (1908-1993) was the first African American Supreme Court Justice. As a lawyer, he argued the landmark Brown v. Board of Education case that ended school segregation.", "photo_url": "https://images.pexels.com/photos/3768925/pexels-photo-3768925.jpeg?w=400", "source_url": "https://www.blackpast.org/african-american-history/marshall-thurgood-1908-1993/"},
        {"name": "Shirley Chisholm", "field": "Politician & Educator", "decade": HistoryDecade.DECADE_1950_2000, "biography": "Shirley Chisholm (1924-2005) was the first Black woman elected to Congress and the first to run for president. Her motto was 'Unbought and Unbossed.'", "photo_url": "https://images.pexels.com/photos/3768926/pexels-photo-3768926.jpeg?w=400", "source_url": "https://www.blackpast.org/african-american-history/chisholm-shirley-1924-2005/"},
        {"name": "Toni Morrison", "field": "Novelist & Nobel Laureate", "decade": HistoryDecade.DECADE_1950_2000, "biography": "Toni Morrison (1931-2019) was a Nobel Prize-winning author whose novels explored the African American experience. Her works include 'Beloved,' 'Song of Solomon,' and 'The Bluest Eye.'", "photo_url": "https://images.pexels.com/photos/3768927/pexels-photo-3768927.jpeg?w=400", "source_url": "https://www.blackpast.org/african-american-history/morrison-toni-1931-2019/"},
        {"name": "Jesse Jackson", "field": "Civil Rights Leader & Minister", "decade": HistoryDecade.DECADE_1950_2000, "biography": "Reverend Jesse Jackson (1941-present) is a civil rights activist who worked with Dr. King and founded Operation PUSH and the Rainbow Coalition. He ran for president twice in the 1980s.", "photo_url": "https://images.pexels.com/photos/3768928/pexels-photo-3768928.jpeg?w=400", "source_url": "https://www.blackpast.org/african-american-history/jackson-jesse-1941/"},
        {"name": "Oprah Winfrey", "field": "Media Mogul & Philanthropist", "decade": HistoryDecade.DECADE_2000_TODAY, "biography": "Oprah Winfrey (1954-present) is a media executive, actress, and philanthropist. She became the first Black female billionaire and has used her platform to empower millions worldwide.", "photo_url": "https://images.pexels.com/photos/3768929/pexels-photo-3768929.jpeg?w=400", "source_url": "https://www.blackpast.org/african-american-history/winfrey-oprah-1954/"},
        {"name": "Barack Obama", "field": "44th President of the United States", "decade": HistoryDecade.DECADE_2000_TODAY, "biography": "Barack Obama (1961-present) became the first African American President of the United States in 2009. His presidency represented a historic milestone in American history.", "photo_url": "https://images.pexels.com/photos/3768930/pexels-photo-3768930.jpeg?w=400", "source_url": "https://www.blackpast.org/african-american-history/obama-barack-1961/"},
        {"name": "Kamala Harris", "field": "Vice President of the United States", "decade": HistoryDecade.DECADE_2000_TODAY, "biography": "Kamala Harris (1964-present) became the first woman, first Black woman, and first South Asian American to serve as Vice President of the United States in 2021.", "photo_url": "https://images.pexels.com/photos/3768931/pexels-photo-3768931.jpeg?w=400", "source_url": "https://www.blackpast.org/african-american-history/harris-kamala-1964/"},
        {"name": "LeBron James", "field": "Basketball Player & Activist", "decade": HistoryDecade.DECADE_2000_TODAY, "biography": "LeBron James (1984-present) is one of the greatest basketball players of all time. He has used his platform to advocate for social justice and opened the I PROMISE School for at-risk youth.", "photo_url": "https://images.pexels.com/photos/3768932/pexels-photo-3768932.jpeg?w=400", "source_url": "https://www.blackpast.org/african-american-history/james-lebron-1984/"},
        {"name": "Stacey Abrams", "field": "Politician & Voting Rights Activist", "decade": HistoryDecade.DECADE_2000_TODAY, "biography": "Stacey Abrams (1973-present) is a politician, lawyer, and voting rights activist. She founded Fair Fight Action to combat voter suppression and has been a leading voice for democracy.", "photo_url": "https://images.pexels.com/photos/3768933/pexels-photo-3768933.jpeg?w=400", "source_url": "https://www.blackpast.org/african-american-history/abrams-stacey-1973/"},
        {"name": "Ta-Nehisi Coates", "field": "Author & Journalist", "decade": HistoryDecade.DECADE_2000_TODAY, "biography": "Ta-Nehisi Coates (1975-present) is an author and journalist known for his powerful writing on race in America. His book 'Between the World and Me' won the National Book Award.", "photo_url": "https://images.pexels.com/photos/3768934/pexels-photo-3768934.jpeg?w=400", "source_url": "https://www.blackpast.org/african-american-history/coates-ta-nehisi-1975/"},
        {"name": "Ava DuVernay", "field": "Filmmaker & Director", "decade": HistoryDecade.DECADE_2000_TODAY, "biography": "Ava DuVernay (1972-present) is a filmmaker known for 'Selma,' '13th,' and 'When They See Us.' She is the first Black woman to direct a film nominated for Best Picture at the Oscars.", "photo_url": "https://images.pexels.com/photos/3768935/pexels-photo-3768935.jpeg?w=400", "source_url": "https://www.blackpast.org/african-american-history/duvernay-ava-1972/"},
        {"name": "Chadwick Boseman", "field": "Actor & Cultural Icon", "decade": HistoryDecade.DECADE_2000_TODAY, "biography": "Chadwick Boseman (1976-2020) was an actor who portrayed Black icons like Jackie Robinson, James Brown, and Black Panther. His legacy continues to inspire millions.", "photo_url": "https://images.pexels.com/photos/3768936/pexels-photo-3768936.jpeg?w=400", "source_url": "https://www.blackpast.org/african-american-history/boseman-chadwick-1976-2020/"},
        {"name": "Simone Biles", "field": "Olympic Gymnast", "decade": HistoryDecade.DECADE_2000_TODAY, "biography": "Simone Biles (1997-present) is the most decorated gymnast in history. She has won 32 Olympic and World Championship medals and is an advocate for mental health awareness.", "photo_url": "https://images.pexels.com/photos/3768937/pexels-photo-3768937.jpeg?w=400", "source_url": "https://www.blackpast.org/african-american-history/biles-simone-1997/"},
        {"name": "Amanda Gorman", "field": "Poet & Activist", "decade": HistoryDecade.DECADE_2000_TODAY, "biography": "Amanda Gorman (1998-present) became the youngest inaugural poet in U.S. history at President Biden's inauguration. Her poem 'The Hill We Climb' captivated the nation.", "photo_url": "https://images.pexels.com/photos/3768938/pexels-photo-3768938.jpeg?w=400", "source_url": "https://www.blackpast.org/african-american-history/gorman-amanda-1998/"}
    ]
    
    for entry_data in history_entries:
        db.create_blk360_history_entry(Blk360HistoryEntryCreate(
            name=entry_data["name"],
            field=entry_data["field"],
            decade=entry_data["decade"],
            biography=entry_data["biography"],
            photo_url=entry_data["photo_url"],
            source_url=entry_data["source_url"],
            source_type=HistorySourceType.MANUAL
        ))
    
    print("💬 Creating 5 Community Forum demo threads...")
    forum_posts = [
        {
            "title": "How are you investing in your community this year?",
            "content": "I'm curious to hear how everyone is giving back to their communities in 2025. Whether it's mentoring youth, supporting local businesses, or volunteering at nonprofits, let's share our stories and inspire each other!",
            "category": Forum360Category.BUSINESS,
            "author_name": "Marcus Johnson",
            "author_email": "marcus@example.com"
        },
        {
            "title": "Favorite Black-Owned Tech Brands",
            "content": "I'm looking to support more Black-owned tech companies. What are your favorite brands for electronics, software, or tech services? Drop your recommendations below!",
            "category": Forum360Category.TECH,
            "author_name": "Aisha Williams",
            "author_email": "aisha@example.com"
        },
        {
            "title": "Tips for Launching a Small Business with Limited Capital",
            "content": "I'm planning to launch my first business but have limited startup capital. What strategies worked for you? Looking for advice on bootstrapping, finding investors, and managing cash flow.",
            "category": Forum360Category.BUSINESS,
            "author_name": "James Davis",
            "author_email": "james@example.com"
        },
        {
            "title": "Mental Health Resources for Black Entrepreneurs",
            "content": "Entrepreneurship can be stressful, and mental health is so important. What resources, therapists, or practices have helped you maintain your mental wellness while building your business?",
            "category": Forum360Category.HEALTH,
            "author_name": "Keisha Brown",
            "author_email": "keisha@example.com"
        },
        {
            "title": "Faith and Business: How Do You Balance Both?",
            "content": "For those who are people of faith, how do you integrate your spiritual values into your business practices? I'd love to hear how faith guides your decision-making and leadership.",
            "category": Forum360Category.FAITH,
            "author_name": "Pastor Michael Thompson",
            "author_email": "michael@example.com"
        }
    ]
    
    for post_data in forum_posts:
        db.create_blk360_forum_post(Blk360ForumPostCreate(
            title=post_data["title"],
            content=post_data["content"],
            category=post_data["category"],
            author_name=post_data["author_name"],
            author_email=post_data["author_email"]
        ))
    
    print("✅ Phase 2 MVP seed data created successfully!")
    print(f"   - {len(db.get_all_blk360_wealth_modules())} Wealth Hub modules")
    print(f"   - {len(db.get_all_blk360_legacy_entries())} Legacy Wall entries")
    print(f"   - {len(db.get_all_blk360_history_entries())} History Window entries")
    print(f"   - {len(db.get_all_blk360_forum_posts())} Forum posts")
