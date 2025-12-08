"""
Financial Intelligence Scraper V2 - Alpha Vantage API
Real-time stock and financial data for supplier monitoring
"""

import requests
from datetime import datetime
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import time

load_dotenv()

# Supabase setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Key suppliers to monitor
SUPPLIERS = {
    'SPR': 'Spirit AeroSystems',
    'TDG': 'TransDigm Group',
    'HWM': 'Howmet Aerospace',
    'BA': 'Boeing',
    'LMT': 'Lockheed Martin',
    'NOC': 'Northrop Grumman',
    'GD': 'General Dynamics',
    'HEI': 'HEICO Corporation',
    'ATRO': 'Astronics Corporation'
}

def get_stock_quote(ticker):
    """Get real-time stock quote from Alpha Vantage"""
    base_url = "https://www.alphavantage.co/query"
    
    params = {
        'function': 'GLOBAL_QUOTE',
        'symbol': ticker,
        'apikey': ALPHAVANTAGE_API_KEY
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        data = response.json()
        
        if 'Global Quote' in data and data['Global Quote']:
            quote = data['Global Quote']
            
            return {
                'price': float(quote.get('05. price', 0)),
                'change_percent': float(quote.get('10. change percent', '0%').replace('%', '')),
                'volume': int(quote.get('06. volume', 0)),
                'latest_trading_day': quote.get('07. latest trading day', '')
            }
        else:
            print(f"No data for {ticker}: {data.get('Note', data.get('Information', 'Unknown error'))}")
            return None
            
    except Exception as e:
        print(f"Error fetching quote for {ticker}: {str(e)}")
        return None

def get_company_overview(ticker):
    """Get company fundamental data from Alpha Vantage"""
    base_url = "https://www.alphavantage.co/query"
    
    params = {
        'function': 'OVERVIEW',
        'symbol': ticker,
        'apikey': ALPHAVANTAGE_API_KEY
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        data = response.json()
        
        if data and 'Symbol' in data:
            return {
                'market_cap': int(float(data.get('MarketCapitalization', 0))),
                'pe_ratio': float(data.get('PERatio', 0)),
                'beta': float(data.get('Beta', 1.0)),
                'profit_margin': float(data.get('ProfitMargin', 0)),
                'description': data.get('Description', '')[:200]
            }
        else:
            return None
            
    except Exception as e:
        print(f"Error fetching overview for {ticker}: {str(e)}")
        return None

def get_recent_news(ticker, company_name):
    """Get latest news headlines for the company"""
    base_url = "https://www.alphavantage.co/query"
    
    params = {
        'function': 'NEWS_SENTIMENT',
        'tickers': ticker,
        'apikey': ALPHAVANTAGE_API_KEY,
        'limit': 3
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        data = response.json()
        
        if 'feed' in data and data['feed']:
            # Get most recent headline
            latest = data['feed'][0]
            return latest.get('title', 'No recent news')
        else:
            return "No recent news available"
            
    except Exception as e:
        print(f"Error fetching news for {ticker}: {str(e)}")
        return "Error fetching news"

def calculate_health_score(ticker_data, overview_data, ticker):
    """Calculate financial health score (1-100)"""
    score = 50  # Baseline
    
    if not ticker_data:
        return score
    
    # Price trend
    change_pct = ticker_data['change_percent']
    if change_pct > 5:
        score += 20
    elif change_pct > 0:
        score += 10
    elif change_pct < -10:
        score -= 30
    elif change_pct < -5:
        score -= 20
    
    # Market cap (bigger = more stable)
    if overview_data:
        market_cap = overview_data.get('market_cap', 0)
        if market_cap > 10_000_000_000:  # >$10B
            score += 15
        elif market_cap > 1_000_000_000:  # >$1B
            score += 5
        
        # Profitability
        profit_margin = overview_data.get('profit_margin', 0)
        if profit_margin > 0.10:  # >10% margin
            score += 10
        elif profit_margin < 0:  # Unprofitable
            score -= 15
    
    # Special case: Spirit AeroSystems (known troubled supplier)
    if ticker == 'SPR':
        score -= 25  # Known financial difficulties
    
    return max(0, min(100, score))  # Clamp between 0-100

def assess_risk_level(health_score, headline):
    """Determine risk level based on health score and news"""
    headline_lower = headline.lower()
    
    # Check for bankruptcy keywords
    if any(word in headline_lower for word in ['bankruptcy', 'chapter 11', 'insolvent', 'default']):
        return "CRITICAL"
    
    # Check health score
    if health_score < 30:
        return "HIGH"
    elif health_score < 50:
        return "MEDIUM"
    else:
        return "LOW"

def monitor_supplier(ticker, name):
    """Monitor a single supplier"""
    print(f"\n{'='*60}")
    print(f"Monitoring: {name} ({ticker})")
    print(f"{'='*60}")
    
    # Get stock quote
    quote_data = get_stock_quote(ticker)
    if not quote_data:
        print(f"⚠️  Could not fetch data for {ticker}")
        return None
    
    print(f"💰 Price: ${quote_data['price']:.2f} ({quote_data['change_percent']:+.2f}%)")
    
    # Get company overview (rate limit: do this sparingly)
    time.sleep(12)  # Alpha Vantage: 5 calls/minute on free tier
    overview_data = get_company_overview(ticker)
    
    # Get recent news
    time.sleep(12)
    latest_headline = get_recent_news(ticker, name)
    
    # Calculate health score
    health_score = calculate_health_score(quote_data, overview_data, ticker)
    risk_level = assess_risk_level(health_score, latest_headline)
    
    print(f"📊 Health Score: {health_score}/100")
    print(f"⚠️  Risk Level: {risk_level}")
    print(f"📰 Latest: {latest_headline[:70]}...")
    
    # Prepare data for database
    supplier_data = {
        'supplier_name': name,
        'ticker_symbol': ticker,
        'stock_price': quote_data['price'],
        'price_change_percent': quote_data['change_percent'],
        'market_cap': overview_data.get('market_cap', 0) if overview_data else 0,
        'last_news_headline': latest_headline,
        'financial_health_score': health_score,
        'risk_level': risk_level,
        'bankruptcy_risk': 'bankruptcy' in latest_headline.lower() or health_score < 25,
        'last_updated': datetime.now().isoformat()
    }
    
    return supplier_data

def save_supplier_data(suppliers_data):
    """Save supplier data to Supabase"""
    saved_count = 0
    
    for data in suppliers_data:
        try:
            result = supabase.table('supplier_monitoring').upsert(
                data,
                on_conflict='supplier_name'
            ).execute()
            saved_count += 1
        except Exception as e:
            print(f"Error saving supplier {data['supplier_name']}: {str(e)}")
    
    print(f"\nSaved {saved_count}/{len(suppliers_data)} suppliers to database")
    return saved_count

def run_financial_scraper():
    """Main function to monitor supplier health"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║       NATILUS FINANCIAL INTELLIGENCE V2                  ║
    ║              Alpha Vantage Real-Time Data                ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    if not ALPHAVANTAGE_API_KEY or ALPHAVANTAGE_API_KEY == "your_alpha_vantage_key":
        print("❌ ERROR: ALPHAVANTAGE_API_KEY not set in .env")
        print("Get free key at: https://www.alphavantage.co/support/#api-key")
        return
    
    all_suppliers = []
    
    for ticker, name in list(SUPPLIERS.items())[:3]:  # Limit to 3 for testing (rate limits)
        supplier_data = monitor_supplier(ticker, name)
        
        if supplier_data:
            all_suppliers.append(supplier_data)
    
    if all_suppliers:
        print(f"\n{'='*60}")
        print(f"Total suppliers monitored: {len(all_suppliers)}")
        print(f"{'='*60}")
        
        save_supplier_data(all_suppliers)
        
        # Alert on critical suppliers
        critical = [s for s in all_suppliers if s['risk_level'] in ['CRITICAL', 'HIGH']]
        if critical:
            print(f"\n🚨 CRITICAL/HIGH RISK SUPPLIERS: {len(critical)}")
            for s in critical:
                print(f"  - {s['supplier_name']}: {s['risk_level']} (Score: {s['financial_health_score']})")
                print(f"    {s['last_news_headline'][:60]}...")

if __name__ == "__main__":
    run_financial_scraper()
