-- Natilus Intelligence Dashboard Schema
-- Run this in your Supabase SQL Editor

-- 1. Competitor Job Postings
CREATE TABLE IF NOT EXISTS competitor_jobs (
    id SERIAL PRIMARY KEY,
    job_id VARCHAR(255) UNIQUE,
    company VARCHAR(255),
    title TEXT,
    location VARCHAR(255),
    description TEXT,
    posted_date TIMESTAMP,
    url TEXT,
    scraped_at TIMESTAMP DEFAULT NOW(),
    strategic_signal TEXT, -- e.g., "Manufacturing expansion", "Engineering scale-up"
    priority VARCHAR(50) -- "HIGH", "MEDIUM", "LOW"
);

-- 2. Patent Filings
CREATE TABLE IF NOT EXISTS patents (
    id SERIAL PRIMARY KEY,
    patent_number VARCHAR(100) UNIQUE,
    title TEXT,
    assignee VARCHAR(255),
    filing_date DATE,
    publication_date DATE,
    abstract TEXT,
    url TEXT,
    technology_area VARCHAR(255), -- "BWB", "Cargo", "Propulsion"
    competitive_threat VARCHAR(50), -- "HIGH", "MEDIUM", "LOW"
    scraped_at TIMESTAMP DEFAULT NOW()
);

-- 3. Talent Pipeline
CREATE TABLE IF NOT EXISTS talent_leads (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    current_company VARCHAR(255),
    current_title VARCHAR(255),
    linkedin_url TEXT UNIQUE,
    years_experience INT,
    skills TEXT[], -- Array of skills
    location VARCHAR(255),
    open_to_work BOOLEAN DEFAULT FALSE,
    last_profile_update TIMESTAMP,
    github_url TEXT,
    contact_status VARCHAR(50), -- "NOT_CONTACTED", "REACHED_OUT", "IN_PROCESS", "HIRED"
    priority VARCHAR(50), -- "CRITICAL", "HIGH", "MEDIUM", "LOW"
    notes TEXT,
    discovered_at TIMESTAMP DEFAULT NOW(),
    action_deadline DATE -- When to contact by
);

-- 4. News & Intelligence
CREATE TABLE IF NOT EXISTS intelligence_feed (
    id SERIAL PRIMARY KEY,
    source VARCHAR(255),
    headline TEXT,
    summary TEXT,
    url TEXT UNIQUE,
    published_date TIMESTAMP,
    category VARCHAR(100), -- "COMPETITOR", "SUPPLIER", "INDUSTRY", "REGULATORY"
    entities TEXT[], -- Companies/people mentioned
    sentiment VARCHAR(50), -- "POSITIVE", "NEGATIVE", "NEUTRAL"
    action_required BOOLEAN DEFAULT FALSE,
    scraped_at TIMESTAMP DEFAULT NOW()
);

-- 5. Supplier Health Monitoring
CREATE TABLE IF NOT EXISTS supplier_monitoring (
    id SERIAL PRIMARY KEY,
    supplier_name VARCHAR(255) UNIQUE,
    ticker_symbol VARCHAR(10),
    stock_price DECIMAL(10,2),
    price_change_percent DECIMAL(5,2),
    market_cap BIGINT,
    last_news_headline TEXT,
    financial_health_score INT, -- 1-100
    risk_level VARCHAR(50), -- "CRITICAL", "HIGH", "MEDIUM", "LOW"
    bankruptcy_risk BOOLEAN DEFAULT FALSE,
    last_updated TIMESTAMP DEFAULT NOW()
);

-- 6. VC Activity Tracking
CREATE TABLE IF NOT EXISTS vc_intelligence (
    id SERIAL PRIMARY KEY,
    vc_firm VARCHAR(255),
    portfolio_company VARCHAR(255),
    deal_size BIGINT,
    deal_date DATE,
    sector VARCHAR(255),
    stage VARCHAR(50), -- "SEED", "SERIES_A", "SERIES_B", etc.
    relevance_to_natilus VARCHAR(50), -- "HIGH", "MEDIUM", "LOW"
    notes TEXT,
    scraped_at TIMESTAMP DEFAULT NOW()
);

-- 7. Daily Action Items (Auto-generated from other tables)
CREATE TABLE IF NOT EXISTS action_items (
    id SERIAL PRIMARY KEY,
    item_type VARCHAR(50), -- "TALENT", "COMPETITOR", "SUPPLIER", "INVESTOR"
    priority VARCHAR(50), -- "URGENT", "HIGH", "MEDIUM", "LOW"
    title TEXT,
    description TEXT,
    deadline DATE,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    related_table VARCHAR(50),
    related_id INT
);

-- 8. Strategic Analysis (AI-generated insights)
CREATE TABLE IF NOT EXISTS strategic_analysis (
    id SERIAL PRIMARY KEY,
    analysis_date TIMESTAMP DEFAULT NOW(),
    executive_summary TEXT,
    critical_threats TEXT, -- JSON array
    opportunities TEXT, -- JSON array
    competitor_movements TEXT, -- JSON array
    talent_recommendations TEXT, -- JSON array
    supply_chain_risks TEXT, -- JSON array
    strategic_priorities TEXT -- JSON array
);

-- Create indexes for better query performance
CREATE INDEX idx_jobs_company ON competitor_jobs(company);
CREATE INDEX idx_jobs_posted_date ON competitor_jobs(posted_date);
CREATE INDEX idx_patents_assignee ON patents(assignee);
CREATE INDEX idx_talent_priority ON talent_leads(priority);
CREATE INDEX idx_talent_deadline ON talent_leads(action_deadline);
CREATE INDEX idx_news_category ON intelligence_feed(category);
CREATE INDEX idx_supplier_risk ON supplier_monitoring(risk_level);
CREATE INDEX idx_actions_priority ON action_items(priority);
CREATE INDEX idx_actions_deadline ON action_items(deadline);
CREATE INDEX idx_analysis_date ON strategic_analysis(analysis_date);
