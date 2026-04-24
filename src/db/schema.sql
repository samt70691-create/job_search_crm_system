PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS job_offers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    source_job_id TEXT,
    url TEXT,
    title TEXT NOT NULL,
    company TEXT,
    location TEXT,
    country TEXT DEFAULT 'France',
    job_type TEXT,
    remote_type TEXT,
    salary_min REAL,
    salary_max REAL,
    currency TEXT DEFAULT 'EUR',
    description_raw TEXT,
    description_clean TEXT,
    date_posted TEXT,
    date_scraped TEXT,
    keywords_detected TEXT,
    score REAL DEFAULT 0,
    priority_level TEXT DEFAULT 'medium',
    status TEXT DEFAULT 'new',
    is_duplicate INTEGER DEFAULT 0,
    duplicate_of INTEGER,
    ai_summary TEXT,
    ai_fit_reason TEXT,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source, source_job_id),
    UNIQUE(url)
);

CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_offer_id INTEGER NOT NULL,
    application_date TEXT,
    application_channel TEXT,
    application_status TEXT DEFAULT 'draft',
    next_followup_date TEXT,
    last_followup_date TEXT,
    cv_version TEXT,
    cover_letter_version TEXT,
    custom_message TEXT,
    response_date TEXT,
    outcome TEXT,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(job_offer_id) REFERENCES job_offers(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_offer_id INTEGER,
    company TEXT,
    full_name TEXT,
    role TEXT,
    email TEXT,
    linkedin_url TEXT,
    phone TEXT,
    contact_type TEXT,
    source TEXT,
    confidence_score REAL DEFAULT 0,
    notes TEXT,
    date_found TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(job_offer_id) REFERENCES job_offers(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS masters_programs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,
    url TEXT,
    program_name TEXT NOT NULL,
    institution TEXT,
    city TEXT,
    country TEXT DEFAULT 'France',
    program_type TEXT,
    domain TEXT,
    deadline TEXT,
    start_date TEXT,
    description TEXT,
    status TEXT DEFAULT 'new',
    score REAL DEFAULT 0,
    notes TEXT,
    date_scraped TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(url)
);

CREATE TABLE IF NOT EXISTS activity_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_type TEXT NOT NULL,
    entity_id INTEGER NOT NULL,
    action_type TEXT NOT NULL,
    action_date TEXT DEFAULT CURRENT_TIMESTAMP,
    details TEXT
);

CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT NOT NULL UNIQUE,
    value TEXT
);

CREATE INDEX IF NOT EXISTS idx_job_offers_status ON job_offers(status);
CREATE INDEX IF NOT EXISTS idx_job_offers_score ON job_offers(score DESC);
CREATE INDEX IF NOT EXISTS idx_applications_status ON applications(application_status);
CREATE INDEX IF NOT EXISTS idx_applications_followup ON applications(next_followup_date);
