# 🛩️ Natilus Intelligence Platform

Real-time competitive intelligence system for aerospace industry. Collects data from competitor job postings, patent filings, financial markets, and news sources.

## 🎯 What It Does

- **📰 News Intelligence**: Monitors aerospace industry news, tracks competitor announcements
- **💼 Job Intelligence**: Scrapes competitor career pages (JetZero, Boom, Boeing, Airbus)
- **📜 Patent Intelligence**: Searches Google Patents for BWB and cargo aircraft technologies
- **📊 Financial Intelligence**: Tracks supplier stock prices and financial health
- **👥 Talent Intelligence**: Discovers aerospace engineers on LinkedIn (optional)
- **🤖 AI Analysis**: Claude-powered strategic insights (optional)

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.11+ (3.14 works but 3.11-3.12 recommended)
- Supabase account (free tier)
- Anthropic API key (optional, for AI analysis)

### 2. Installation

```bash
# Clone repository
git clone https://github.com/yourusername/natilus-intelligence.git
cd natilus-intelligence

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
```

Required in `.env`:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key
```

Optional in `.env`:
```
ANTHROPIC_API_KEY=sk-ant-api03-...  # For AI analysis
ALPHAVANTAGE_API_KEY=...  # For financial data
SERPER_API_KEY=...  # For LinkedIn search
```

### 4. Database Setup

1. Go to [Supabase](https://supabase.com) and create a project
2. In SQL Editor, run `natilus_schema.sql`
3. Copy your project URL and anon key to `.env`

### 5. Run Intelligence Collection

```bash
python run_intelligence.py
```

This will:
- Collect data from all sources
- Save to Supabase database
- Export to `intelligence_reports/` folder as JSON, CSV, and Excel

## 📂 Data Exports

All data is exported to `intelligence_reports/` in three formats:

- **JSON**: `news_YYYYMMDD_HHMMSS.json`
- **CSV**: `news_YYYYMMDD_HHMMSS.csv`  
- **Excel**: `news_YYYYMMDD_HHMMSS.xlsx`

Open these files in Excel, Google Sheets, or any text editor.

## 🔧 Individual Scrapers

Run scrapers individually:

```bash
python news_scraper.py          # News articles
python patent_scraper_v4.py     # Patent filings
python job_scraper_v2.py        # Job postings
python financial_scraper_v2.py  # Stock data
python linkedin_intel.py        # LinkedIn talent (requires SERPER_API_KEY)
python strategic_analyst.py     # AI analysis (requires ANTHROPIC_API_KEY)
```

## 📊 Data Sources

| Source | Type | Free? | Rate Limit |
|--------|------|-------|------------|
| Google News RSS | News | ✅ Yes | None |
| Google Patents | Patents | ✅ Yes | Respectful scraping |
| Lever/Greenhouse | Jobs | ✅ Yes | Respectful scraping |
| Alpha Vantage | Stocks | ✅ Yes | 500/day |
| Serper | LinkedIn | ✅ Free tier | 2,500/month |
| Anthropic | AI Analysis | 💰 $5 credit | Pay as you go |

## 🎯 Use Cases

### Competitive Intelligence
- Track JetZero and Boom hiring patterns
- Monitor patent filings in BWB technology
- Identify strategic hiring signals (manufacturing ramp-up, certification push)

### Talent Acquisition
- Discover aerospace engineers updating GitHub profiles
- Find "open to work" candidates on LinkedIn
- Track competitor talent movements

### Supply Chain Risk
- Monitor supplier financial health
- Get early warning on bankruptcy risks
- Track stock price trends

### Strategic Planning
- AI-generated insights on competitor moves
- Patent threat assessments
- Market opportunity identification

## 🔒 Security Notes

- Never commit `.env` file to Git (already in `.gitignore`)
- Keep API keys secure
- Use Supabase Row Level Security for production
- Respect rate limits and robots.txt

## 📝 License

MIT License - See LICENSE file

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 🆘 Support

For issues or questions:
1. Check existing GitHub issues
2. Create new issue with detailed description
3. Include error messages and Python version

## 🏗️ Project Structure

```
natilus-intelligence/
├── run_intelligence.py       # Main collection script
├── news_scraper.py           # News intelligence
├── job_scraper_v2.py         # Job postings scraper
├── patent_scraper_v4.py      # Patent scraper
├── financial_scraper_v2.py   # Financial data
├── linkedin_intel.py         # LinkedIn talent
├── strategic_analyst.py      # AI analysis
├── natilus_schema.sql        # Database schema
├── requirements.txt          # Dependencies
├── .env.example              # Environment template
└── intelligence_reports/     # Exported data
```

## 🎓 Built For

Built for [Natilus](https://natilus.com) - Blended Wing Body cargo aircraft company

---

**⭐ Star this repo if you find it useful!**
