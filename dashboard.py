"""
Natilus Intelligence Dashboard - Streamlit UI
Real-time intelligence visualization for strategic decision-making
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from supabase import create_client, Client
import plotly.express as px
import plotly.graph_objects as go
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Natilus Intelligence Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Supabase setup
@st.cache_resource
def init_supabase():
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        st.error("❌ Supabase credentials not found. Please set SUPABASE_URL and SUPABASE_KEY in .env file")
        st.stop()
    
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# Custom CSS
st.markdown("""
<style>
    .big-metric { font-size: 2.5rem; font-weight: bold; }
    .priority-critical { color: #FF4444; font-weight: bold; }
    .priority-high { color: #FF8800; font-weight: bold; }
    .priority-medium { color: #FFB800; }
    .priority-low { color: #00AA00; }
    .action-box { 
        background-color: #FFF3CD; 
        border-left: 5px solid #FF8800; 
        padding: 15px; 
        margin: 10px 0; 
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 1.1rem;
        padding: 12px 24px;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def load_data(table_name, limit=100, order_by='created_at', ascending=False):
    """Load data from Supabase table"""
    try:
        query = supabase.table(table_name).select("*").limit(limit)
        
        if order_by:
            query = query.order(order_by, desc=not ascending)
        
        result = query.execute()
        
        if result.data:
            return pd.DataFrame(result.data)
        return pd.DataFrame()
    
    except Exception as e:
        st.error(f"Error loading {table_name}: {str(e)}")
        return pd.DataFrame()

def count_records(table_name, filter_column=None, filter_value=None):
    """Count records in a table with optional filter"""
    try:
        query = supabase.table(table_name).select("*", count="exact")
        
        if filter_column and filter_value:
            query = query.eq(filter_column, filter_value)
        
        result = query.execute()
        return result.count if hasattr(result, 'count') else len(result.data)
    except:
        return 0

# Header
st.title("✈️ Natilus Intelligence Dashboard")
st.caption(f"Real-Time Strategic Intelligence • Last Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")

# Sidebar filters
with st.sidebar:
    st.header("⚙️ Filters")
    
    st.subheader("Priority Levels")
    show_critical = st.checkbox("🔴 Critical", value=True)
    show_high = st.checkbox("🟠 High", value=True)
    show_medium = st.checkbox("🟡 Medium", value=True)
    show_low = st.checkbox("🟢 Low", value=False)
    
    st.subheader("Time Range")
    days_back = st.slider("Days of history", 1, 90, 30)
    
    st.subheader("Categories")
    show_talent = st.checkbox("👥 Talent", value=True)
    show_competitors = st.checkbox("🎯 Competitors", value=True)
    show_suppliers = st.checkbox("📦 Suppliers", value=True)
    show_investors = st.checkbox("💰 Investors", value=True)
    
    st.markdown("---")
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

# Main dashboard tabs
tabs = st.tabs(["🎯 Action Required", "👥 Talent Pipeline", "📊 Competitor Intelligence", 
                "📦 Supply Chain", "💰 Investor Signals", "📰 News Feed"])

# TAB 1: ACTION REQUIRED
with tabs[0]:
    st.header("⚡ Immediate Actions Required")
    
    # Load action-critical data
    talents_df = load_data('talent_leads', limit=50, order_by='action_deadline')
    jobs_df = load_data('competitor_jobs', limit=50, order_by='posted_date')
    suppliers_df = load_data('supplier_monitoring')
    news_df = load_data('intelligence_feed', limit=50, order_by='published_date')
    
    # Critical talent leads
    if not talents_df.empty:
        critical_talent = talents_df[
            (talents_df['priority'].isin(['CRITICAL', 'HIGH'])) &
            (pd.to_datetime(talents_df['action_deadline']) <= datetime.now() + timedelta(days=3))
        ]
        
        if not critical_talent.empty:
            st.subheader("🔴 URGENT: Talent Opportunities Closing")
            for idx, talent in critical_talent.iterrows():
                with st.container():
                    col1, col2, col3 = st.columns([3, 2, 1])
                    
                    with col1:
                        st.markdown(f"**{talent['name']}** - {talent['current_title']}")
                        st.caption(f"📍 {talent['location']} | 🏢 {talent['current_company']}")
                    
                    with col2:
                        deadline = pd.to_datetime(talent['action_deadline'])
                        days_left = (deadline - datetime.now()).days
                        st.markdown(f"⏰ **Contact by:** {deadline.strftime('%b %d')} ({days_left} days)")
                    
                    with col3:
                        priority_class = f"priority-{talent['priority'].lower()}"
                        st.markdown(f"<span class='{priority_class}'>{talent['priority']}</span>", 
                                  unsafe_allow_html=True)
                    
                    if talent.get('linkedin_url'):
                        st.markdown(f"[LinkedIn Profile]({talent['linkedin_url']})")
                    if talent.get('github_url'):
                        st.markdown(f"[GitHub Profile]({talent['github_url']})")
                    
                    st.markdown("---")
    
    # Critical supplier risks
    if not suppliers_df.empty:
        critical_suppliers = suppliers_df[suppliers_df['risk_level'].isin(['CRITICAL', 'HIGH'])]
        
        if not critical_suppliers.empty:
            st.subheader("🚨 Supply Chain Alerts")
            for idx, supplier in critical_suppliers.iterrows():
                with st.container():
                    col1, col2, col3 = st.columns([3, 2, 1])
                    
                    with col1:
                        st.markdown(f"**{supplier['supplier_name']}** ({supplier['ticker_symbol']})")
                        st.caption(supplier['last_news_headline'])
                    
                    with col2:
                        price_emoji = "📉" if supplier['price_change_percent'] < 0 else "📈"
                        st.markdown(f"{price_emoji} ${supplier['stock_price']} ({supplier['price_change_percent']:+.2f}%)")
                        st.caption(f"Health Score: {supplier['financial_health_score']}/100")
                    
                    with col3:
                        risk_color = "🔴" if supplier['risk_level'] == 'CRITICAL' else "🟠"
                        st.markdown(f"{risk_color} **{supplier['risk_level']}**")
                    
                    st.markdown("---")
    
    # Action-required news
    if not news_df.empty:
        action_news = news_df[news_df['action_required'] == True]
        
        if not action_news.empty:
            st.subheader("📰 Intelligence Requiring Response")
            for idx, article in action_news.head(5).iterrows():
                with st.container():
                    st.markdown(f"**{article['headline']}**")
                    st.caption(f"📰 {article['source']} | {article['category']} | {article['sentiment']}")
                    if article.get('entities'):
                        st.caption(f"Entities: {', '.join(article['entities'])}")
                    st.markdown(f"[Read Article]({article['url']})")
                    st.markdown("---")

# TAB 2: TALENT PIPELINE
with tabs[1]:
    st.header("👥 Talent Pipeline Intelligence")
    
    talents_df = load_data('talent_leads', limit=100)
    
    if not talents_df.empty:
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_leads = len(talents_df)
            st.metric("Total Leads", total_leads)
        
        with col2:
            critical_leads = len(talents_df[talents_df['priority'] == 'CRITICAL'])
            st.metric("Critical Priority", critical_leads)
        
        with col3:
            open_to_work = len(talents_df[talents_df['open_to_work'] == True])
            st.metric("Open to Work", open_to_work)
        
        with col4:
            contacted = len(talents_df[talents_df['contact_status'] != 'NOT_CONTACTED'])
            st.metric("Contacted", contacted)
        
        # Talent table
        st.subheader("Recent Talent Discoveries")
        
        # Prepare display dataframe
        display_df = talents_df[[
            'name', 'current_company', 'current_title', 'location', 
            'priority', 'open_to_work', 'action_deadline'
        ]].copy()
        
        display_df['action_deadline'] = pd.to_datetime(display_df['action_deadline']).dt.strftime('%b %d, %Y')
        
        st.dataframe(
            display_df.head(20),
            use_container_width=True,
            column_config={
                "name": "Name",
                "current_company": "Company",
                "current_title": "Title",
                "location": "Location",
                "priority": st.column_config.TextColumn("Priority"),
                "open_to_work": st.column_config.CheckboxColumn("Open to Work"),
                "action_deadline": "Contact By"
            }
        )
        
        # Priority distribution
        st.subheader("Priority Distribution")
        priority_counts = talents_df['priority'].value_counts()
        fig = px.pie(
            values=priority_counts.values,
            names=priority_counts.index,
            color=priority_counts.index,
            color_discrete_map={
                'CRITICAL': '#FF4444',
                'HIGH': '#FF8800',
                'MEDIUM': '#FFB800',
                'LOW': '#00AA00'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.info("No talent leads found. Run the GitHub talent discovery scraper to populate data.")

# TAB 3: COMPETITOR INTELLIGENCE
with tabs[2]:
    st.header("🎯 Competitor Intelligence")
    
    jobs_df = load_data('competitor_jobs', limit=200)
    patents_df = load_data('patents', limit=100)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Recent Job Postings by Competitor")
        
        if not jobs_df.empty:
            # Company hiring trends
            company_counts = jobs_df['company'].value_counts()
            fig = px.bar(
                x=company_counts.index,
                y=company_counts.values,
                labels={'x': 'Company', 'y': 'Job Postings'},
                color=company_counts.values,
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Strategic signals
            st.subheader("Strategic Hiring Signals")
            signals = jobs_df['strategic_signal'].value_counts()
            for signal, count in signals.head(5).items():
                st.markdown(f"**{signal}**: {count} roles")
        else:
            st.info("No competitor jobs found. Run the job scraper to populate data.")
    
    with col2:
        st.subheader("Patent Activity")
        
        if not patents_df.empty:
            # Patent trends by company
            assignee_counts = patents_df['assignee'].value_counts()
            fig = px.bar(
                x=assignee_counts.index,
                y=assignee_counts.values,
                labels={'x': 'Company', 'y': 'Patents Filed'},
                color=assignee_counts.values,
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # High-threat patents
            high_threat = patents_df[patents_df['competitive_threat'] == 'HIGH']
            if not high_threat.empty:
                st.subheader("⚠️ High-Threat Patents")
                for idx, patent in high_threat.head(5).iterrows():
                    st.markdown(f"**{patent['title'][:60]}...**")
                    st.caption(f"{patent['assignee']} | {patent['technology_area']}")
                    st.markdown(f"[View Patent]({patent['url']})")
                    st.markdown("---")
        else:
            st.info("No patents found. Run the patent scraper to populate data.")

# TAB 4: SUPPLY CHAIN
with tabs[3]:
    st.header("📦 Supply Chain Health Monitor")
    
    suppliers_df = load_data('supplier_monitoring')
    
    if not suppliers_df.empty:
        # Health score distribution
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Supplier Financial Health")
            
            fig = go.Figure()
            
            for idx, supplier in suppliers_df.iterrows():
                color = '#FF4444' if supplier['risk_level'] == 'CRITICAL' else \
                        '#FF8800' if supplier['risk_level'] == 'HIGH' else \
                        '#FFB800' if supplier['risk_level'] == 'MEDIUM' else '#00AA00'
                
                fig.add_trace(go.Bar(
                    x=[supplier['supplier_name']],
                    y=[supplier['financial_health_score']],
                    name=supplier['supplier_name'],
                    marker_color=color,
                    showlegend=False
                ))
            
            fig.update_layout(
                yaxis_title="Health Score (0-100)",
                xaxis_title="Supplier",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Risk Summary")
            
            risk_counts = suppliers_df['risk_level'].value_counts()
            
            st.metric("🔴 Critical", risk_counts.get('CRITICAL', 0))
            st.metric("🟠 High", risk_counts.get('HIGH', 0))
            st.metric("🟡 Medium", risk_counts.get('MEDIUM', 0))
            st.metric("🟢 Low", risk_counts.get('LOW', 0))
        
        # Detailed supplier table
        st.subheader("Supplier Details")
        st.dataframe(
            suppliers_df[[
                'supplier_name', 'stock_price', 'price_change_percent',
                'financial_health_score', 'risk_level', 'last_news_headline'
            ]],
            use_container_width=True,
            column_config={
                "supplier_name": "Supplier",
                "stock_price": st.column_config.NumberColumn("Price", format="$%.2f"),
                "price_change_percent": st.column_config.NumberColumn("Change %", format="%.2f%%"),
                "financial_health_score": st.column_config.ProgressColumn(
                    "Health Score",
                    min_value=0,
                    max_value=100
                ),
                "risk_level": "Risk",
                "last_news_headline": "Latest News"
            }
        )
    else:
        st.info("No supplier data found. Run the supplier monitor to populate data.")

# TAB 5: INVESTOR SIGNALS (Placeholder - would need Crunchbase/PitchBook integration)
with tabs[4]:
    st.header("💰 Investor Activity & Signals")
    st.info("VC intelligence feed - Coming soon (requires Crunchbase/PitchBook API access)")
    
    st.markdown("""
    **Planned Features:**
    - Recent aerospace/deep tech investments
    - Active VCs in the space
    - Deal flow trends
    - Investment thesis signals
    """)

# TAB 6: NEWS FEED
with tabs[5]:
    st.header("📰 Intelligence News Feed")
    
    news_df = load_data('intelligence_feed', limit=100, order_by='published_date')
    
    if not news_df.empty:
        # Category filter
        categories = st.multiselect(
            "Filter by category",
            options=news_df['category'].unique(),
            default=news_df['category'].unique()
        )
        
        filtered_news = news_df[news_df['category'].isin(categories)]
        
        # Display news
        for idx, article in filtered_news.head(20).iterrows():
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"### {article['headline']}")
                    st.caption(f"📰 {article['source']} | Published: {pd.to_datetime(article['published_date']).strftime('%b %d, %Y')}")
                    
                    if article.get('summary'):
                        st.markdown(article['summary'][:200] + "...")
                    
                    if article.get('entities'):
                        st.caption(f"**Entities:** {', '.join(article['entities'])}")
                    
                    st.markdown(f"[Read Full Article]({article['url']})")
                
                with col2:
                    # Category badge
                    category_colors = {
                        'COMPETITOR': '🎯',
                        'SUPPLIER': '📦',
                        'REGULATORY': '⚖️',
                        'INVESTOR': '💰',
                        'INDUSTRY': '🏭'
                    }
                    emoji = category_colors.get(article['category'], '📰')
                    st.markdown(f"{emoji} **{article['category']}**")
                    
                    # Sentiment
                    sentiment_emoji = "😊" if article['sentiment'] == 'POSITIVE' else \
                                    "😐" if article['sentiment'] == 'NEUTRAL' else "😟"
                    st.caption(f"{sentiment_emoji} {article['sentiment']}")
                
                st.markdown("---")
    else:
        st.info("No news articles found. Run the news scraper to populate data.")

# Footer
st.markdown("---")
st.caption("Natilus Intelligence Dashboard • Powered by real-time data from Indeed, Google Patents, Yahoo Finance, GitHub, and Google News")
