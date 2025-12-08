# 🚀 Setup Guide

## Step-by-Step Installation (15 minutes)

### 1. Install Python

**Download:** https://www.python.org/downloads/

**Recommended:** Python 3.11 or 3.12  
**Works with:** Python 3.14 (but 3.11-3.12 more stable)

✅ During installation, check **"Add Python to PATH"**

### 2. Clone or Download

```bash
# Option A: Clone with Git
git clone https://github.com/yourusername/natilus-intelligence.git
cd natilus-intelligence

# Option B: Download ZIP
# Extract to folder, then:
cd natilus-intelligence
```

### 3. Create Virtual Environment

```bash
# Create venv
python -m venv .venv

# Activate
# On Windows:
.venv\Scripts\activate

# On Mac/Linux:
source .venv/bin/activate
```

You should see `(.venv)` in your terminal.

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

**If you get errors on Python 3.14:**
```bash
pip install sgmllib3k  # Fixes feedparser
pip install -r requirements.txt
```

### 5. Create Supabase Database

1. Go to https://supabase.com
2. Sign up (free)
3. Click **"New Project"**
   - Name: `natilus-intelligence`
   - Database password: (create strong password)
   - Region: Closest to you
4. Wait 2 minutes for project to initialize
5. Click **"SQL Editor"** → **"New Query"**
6. Copy contents of `natilus_schema.sql`
7. Paste and click **"Run"**
8. Should see: "Success"

### 6. Get API Credentials

#### Supabase (Required)
1. In Supabase, go to **Settings** → **API**
2. Copy **Project URL**
3. Copy **anon public** key

#### Anthropic (Optional - for AI analysis)
1. Go to https://console.anthropic.com
2. Sign up (get $5 free credit)
3. Go to **API Keys**
4. Create new key
5. Copy it

#### Alpha Vantage (Optional - for stock data)
1. Go to https://www.alphavantage.co/support/#api-key
2. Enter email
3. Get key instantly

#### Serper (Optional - for LinkedIn)
1. Go to https://serper.dev
2. Sign up with Google
3. Copy API key from dashboard

### 7. Configure Environment

```bash
# Copy template
cp .env.example .env

# Edit file
# On Windows:
notepad .env

# On Mac/Linux:
nano .env
```

**Add your credentials:**
```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOi...
ANTHROPIC_API_KEY=sk-ant-api03-...  # Optional
ALPHAVANTAGE_API_KEY=...  # Optional
SERPER_API_KEY=...  # Optional
```

Save and close.

### 8. Test Installation

```bash
# Test news scraper (simplest one)
python news_scraper.py
```

**Should see:**
```
Fetching news for: Natilus aircraft
Found 5 articles
...
Saved 48/48 articles to database
```

### 9. Run Full Collection

```bash
python run_intelligence.py
```

**This will:**
- Collect all intelligence
- Save to Supabase
- Export to `intelligence_reports/` folder

### 10. View Your Data

Open `intelligence_reports/` folder:
- `news_YYYYMMDD_HHMMSS.csv` - Open in Excel
- `news_YYYYMMDD_HHMMSS.json` - Open in text editor
- `news_YYYYMMDD_HHMMSS.xlsx` - Open in Excel

---

## ✅ Success Checklist

- [ ] Python 3.11+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed
- [ ] Supabase project created
- [ ] Database schema deployed
- [ ] .env file configured
- [ ] News scraper runs successfully
- [ ] Data exports to reports folder

---

## 🆘 Troubleshooting

### "python: command not found"
- Python not installed or not in PATH
- Try `py` instead of `python` on Windows

### "No module named 'sgmllib'"
```bash
pip install sgmllib3k
```

### "supabase_url is required"
- Check `.env` file exists
- Verify SUPABASE_URL and SUPABASE_KEY are set
- Make sure no quotes around values

### "column does not exist"
- Re-run `natilus_schema.sql` in Supabase
- Check all tables created successfully

### Patent scraper returns 0 results
- Normal - Google Patents may block scraping
- Try different search terms
- Add delays between requests

### Job scraper finds 0 jobs
- Career pages may block automated access
- Try running at different times
- Some companies use different job platforms

---

## 🎯 Next Steps

1. **Schedule automated runs:**
   - Use Windows Task Scheduler
   - Or cron on Mac/Linux
   - Run every 6 hours

2. **Customize scrapers:**
   - Edit company lists
   - Adjust search queries
   - Add new data sources

3. **Set up alerts:**
   - Monitor critical suppliers
   - Track high-priority patents
   - Alert on competitor moves

4. **Share with team:**
   - Push to GitHub
   - Share reports folder
   - Set up team access to Supabase

---

**Questions?** Open an issue on GitHub!
