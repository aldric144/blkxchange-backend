

CREATE TABLE IF NOT EXISTS vendors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    business_name TEXT NOT NULL,
    contact_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    address TEXT,
    website TEXT,
    category TEXT,
    description TEXT,
    price_range TEXT,
    fulfillment_method TEXT,
    image_urls JSONB DEFAULT '[]'::jsonb,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    agreement_accepted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS vendor_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vendor_id UUID REFERENCES vendors(id) ON DELETE CASCADE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'vendor',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vendor_id UUID REFERENCES vendors(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    quantity INTEGER DEFAULT 0,
    image_urls JSONB DEFAULT '[]'::jsonb,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS professionals_active (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    bio TEXT,
    credentials TEXT,
    rate TEXT,
    phone TEXT,
    email TEXT,
    image_url TEXT,
    rating NUMERIC(2, 1) DEFAULT 0.0,
    reviews_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS startup_applications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    business_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    website TEXT,
    funding_goal NUMERIC(12, 2),
    business_summary TEXT,
    pitch_deck_url TEXT,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS angel_investors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    company TEXT,
    accreditation_type TEXT,
    investment_range TEXT,
    interests JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS donations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    donor_name TEXT,
    email TEXT,
    amount NUMERIC(10, 2) NOT NULL,
    institution TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS black_banks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    description TEXT,
    location TEXT,
    affiliate_link TEXT
);

CREATE TABLE IF NOT EXISTS twofa (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT NOT NULL UNIQUE,
    method TEXT NOT NULL CHECK (method IN ('email_otp', 'totp')),
    secret_hash TEXT NOT NULL,
    recovery_codes JSONB DEFAULT '[]'::jsonb,
    enabled BOOLEAN DEFAULT TRUE,
    grace_period_expires TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT NOT NULL,
    event TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('success', 'fail')),
    ip_address TEXT,
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT NOT NULL,
    email TEXT NOT NULL,
    stripe_customer_id TEXT UNIQUE,
    stripe_subscription_id TEXT UNIQUE,
    plan_type TEXT NOT NULL CHECK (plan_type IN ('premium', 'elite')),
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'canceled', 'past_due', 'trialing')),
    current_period_start TIMESTAMP,
    current_period_end TIMESTAMP,
    cancel_at_period_end BOOLEAN DEFAULT FALSE,
    amount NUMERIC(10, 2) NOT NULL,
    currency TEXT DEFAULT 'usd',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS payouts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vendor_id UUID REFERENCES vendors(id) ON DELETE CASCADE,
    stripe_account_id TEXT,
    amount NUMERIC(10, 2) NOT NULL,
    currency TEXT DEFAULT 'usd',
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'paid', 'failed')),
    stripe_payout_id TEXT,
    failure_reason TEXT,
    arrival_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS affiliates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT NOT NULL,
    email TEXT NOT NULL,
    referral_code TEXT NOT NULL UNIQUE,
    referral_url TEXT NOT NULL,
    clicks INTEGER DEFAULT 0,
    conversions INTEGER DEFAULT 0,
    revenue_generated NUMERIC(10, 2) DEFAULT 0.00,
    commission_earned NUMERIC(10, 2) DEFAULT 0.00,
    commission_rate NUMERIC(5, 2) DEFAULT 10.00, -- 10% default
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'suspended')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS affiliate_clicks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    affiliate_id UUID REFERENCES affiliates(id) ON DELETE CASCADE,
    ip_address TEXT,
    user_agent TEXT,
    referrer TEXT,
    clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS affiliate_conversions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    affiliate_id UUID REFERENCES affiliates(id) ON DELETE CASCADE,
    user_id TEXT,
    order_id TEXT,
    order_amount NUMERIC(10, 2) NOT NULL,
    commission_amount NUMERIC(10, 2) NOT NULL,
    converted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ai_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    source TEXT, -- Wikipedia URL or other source
    category TEXT, -- e.g., 'black_wall_street', 'civil_rights', 'entrepreneurs'
    date_reference TEXT, -- Historical date reference
    image_url TEXT,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected', 'published')),
    admin_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    published_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ai_mentorship (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    mentee_id TEXT NOT NULL,
    mentee_email TEXT NOT NULL,
    mentee_skills JSONB DEFAULT '[]'::jsonb,
    mentee_interests JSONB DEFAULT '[]'::jsonb,
    mentee_industry TEXT,
    mentor_id TEXT,
    mentor_email TEXT,
    mentor_skills JSONB DEFAULT '[]'::jsonb,
    mentor_industry TEXT,
    match_score NUMERIC(5, 2), -- 0-100 similarity score
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected', 'active', 'completed')),
    admin_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    matched_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ai_content (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content_type TEXT NOT NULL CHECK (content_type IN ('wealth_hub_topic', 'business_insight', 'community_update')),
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    full_content TEXT,
    tags JSONB DEFAULT '[]'::jsonb,
    target_audience TEXT, -- e.g., 'entrepreneurs', 'investors', 'all'
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected', 'published')),
    admin_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    published_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS impact_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    metric_date DATE NOT NULL UNIQUE,
    total_revenue NUMERIC(12, 2) DEFAULT 0.00,
    subscription_revenue NUMERIC(12, 2) DEFAULT 0.00,
    vendor_revenue NUMERIC(12, 2) DEFAULT 0.00,
    donation_revenue NUMERIC(12, 2) DEFAULT 0.00,
    affiliate_revenue NUMERIC(12, 2) DEFAULT 0.00,
    active_subscriptions INTEGER DEFAULT 0,
    new_subscriptions INTEGER DEFAULT 0,
    canceled_subscriptions INTEGER DEFAULT 0,
    active_vendors INTEGER DEFAULT 0,
    new_vendors INTEGER DEFAULT 0,
    total_products INTEGER DEFAULT 0,
    new_products INTEGER DEFAULT 0,
    mentorship_matches INTEGER DEFAULT 0,
    ai_content_published INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS payment_metadata (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    stripe_payment_intent_id TEXT UNIQUE,
    stripe_charge_id TEXT,
    user_id TEXT,
    email TEXT,
    amount NUMERIC(10, 2) NOT NULL,
    currency TEXT DEFAULT 'usd',
    payment_type TEXT NOT NULL CHECK (payment_type IN ('subscription', 'donation', 'vendor_payment', 'affiliate_payout')),
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'succeeded', 'failed', 'refunded')),
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX IF NOT EXISTS idx_vendors_email ON vendors(email);
CREATE INDEX IF NOT EXISTS idx_vendors_status ON vendors(status);
CREATE INDEX IF NOT EXISTS idx_vendor_accounts_email ON vendor_accounts(email);
CREATE INDEX IF NOT EXISTS idx_products_vendor_id ON products(vendor_id);
CREATE INDEX IF NOT EXISTS idx_products_status ON products(status);
CREATE INDEX IF NOT EXISTS idx_professionals_category ON professionals_active(category);
CREATE INDEX IF NOT EXISTS idx_twofa_user_id ON twofa(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_timestamp ON audit_logs(timestamp);

CREATE INDEX IF NOT EXISTS idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_stripe_customer_id ON subscriptions(stripe_customer_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_status ON subscriptions(status);
CREATE INDEX IF NOT EXISTS idx_payouts_vendor_id ON payouts(vendor_id);
CREATE INDEX IF NOT EXISTS idx_payouts_status ON payouts(status);
CREATE INDEX IF NOT EXISTS idx_affiliates_user_id ON affiliates(user_id);
CREATE INDEX IF NOT EXISTS idx_affiliates_referral_code ON affiliates(referral_code);
CREATE INDEX IF NOT EXISTS idx_affiliate_clicks_affiliate_id ON affiliate_clicks(affiliate_id);
CREATE INDEX IF NOT EXISTS idx_affiliate_conversions_affiliate_id ON affiliate_conversions(affiliate_id);
CREATE INDEX IF NOT EXISTS idx_ai_history_status ON ai_history(status);
CREATE INDEX IF NOT EXISTS idx_ai_mentorship_mentee_id ON ai_mentorship(mentee_id);
CREATE INDEX IF NOT EXISTS idx_ai_mentorship_status ON ai_mentorship(status);
CREATE INDEX IF NOT EXISTS idx_ai_content_status ON ai_content(status);
CREATE INDEX IF NOT EXISTS idx_ai_content_content_type ON ai_content(content_type);
CREATE INDEX IF NOT EXISTS idx_impact_metrics_date ON impact_metrics(metric_date);
CREATE INDEX IF NOT EXISTS idx_payment_metadata_stripe_payment_intent_id ON payment_metadata(stripe_payment_intent_id);
CREATE INDEX IF NOT EXISTS idx_payment_metadata_user_id ON payment_metadata(user_id);


CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_vendors_updated_at BEFORE UPDATE ON vendors
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON products
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_subscriptions_updated_at BEFORE UPDATE ON subscriptions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_payouts_updated_at BEFORE UPDATE ON payouts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_affiliates_updated_at BEFORE UPDATE ON affiliates
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_payment_metadata_updated_at BEFORE UPDATE ON payment_metadata
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();


CREATE OR REPLACE VIEW active_subscriptions_view AS
SELECT 
    s.id,
    s.user_id,
    s.email,
    s.plan_type,
    s.amount,
    s.current_period_start,
    s.current_period_end,
    s.created_at
FROM subscriptions s
WHERE s.status = 'active';

CREATE OR REPLACE VIEW vendor_payout_summary AS
SELECT 
    v.id AS vendor_id,
    v.business_name,
    v.email,
    COUNT(p.id) AS total_payouts,
    SUM(CASE WHEN p.status = 'paid' THEN p.amount ELSE 0 END) AS total_paid,
    SUM(CASE WHEN p.status = 'pending' THEN p.amount ELSE 0 END) AS total_pending
FROM vendors v
LEFT JOIN payouts p ON v.id = p.vendor_id
GROUP BY v.id, v.business_name, v.email;

CREATE OR REPLACE VIEW affiliate_performance AS
SELECT 
    a.id,
    a.user_id,
    a.email,
    a.referral_code,
    a.clicks,
    a.conversions,
    a.revenue_generated,
    a.commission_earned,
    CASE 
        WHEN a.clicks > 0 THEN ROUND((a.conversions::NUMERIC / a.clicks::NUMERIC) * 100, 2)
        ELSE 0
    END AS conversion_rate
FROM affiliates a;

CREATE OR REPLACE VIEW ai_content_pending_approval AS
SELECT 
    id,
    content_type,
    title,
    summary,
    created_at
FROM ai_content
WHERE status = 'pending'
ORDER BY created_at DESC;
