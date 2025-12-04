# At the top of dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from supabase import create_client
from datetime import datetime, timedelta


st.set_page_config(
    page_title="Natilus Intelligence Center",
    page_icon="✈️",
    layout="wide"
)

# This reads from your .streamlit/secrets.toml file
@st.cache_resource
def init_supabase():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

supabase = init_supabase()

# Custom CSS for professional look
st.markdown("""
<style>
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
    }
    .alert-box {
        padding: 20px;
        background-color: #ff4b4b;
        color: white;
        border-radius: 10px;
        margin: 10px 0;
    }
    .opportunity-box {
        padding: 15px;
        background-color: #00cc88;
        color: white;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Supabase
@st.cache_resource
def init_supabase():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

supabase = init_supabase()

# Header
st.title("🚀 Natilus Intelligence Center")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')} PST")

# Top-level metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Real-time talent available
    talent_count = supabase.table('aerospace_talent').select("*", count='exact').execute()
    st.metric(
        "🎯 Available Talent",
        talent_count.count,
        "+12 since yesterday",
        help="Boeing/Spirit engineers actively looking"
    )

# In the Series A metrics section, change:
with col2:
    # Days to Series A close
    series_a_target = datetime(2025, 3, 15)  # Updated for Series A
    days_left = (series_a_target - datetime.now()).days
    st.metric(
        "📅 Days to Series A Close",
        days_left,
        "Target: $15-20M",  # Series A range
        help="Currently in due diligence"
    )

with col3:
    # Competitor activity
    st.metric(
        "⚠️ Competitor Moves",
        "3 this week",
        "JetZero hiring surge",
        delta_color="inverse"
    )

with col4:
    # Supply chain risks
    st.metric(
        "🏭 Supply Chain Risks",
        "2 Critical",
        "Spirit bankruptcy risk",
        delta_color="inverse"
    )

# Alerts Section
st.markdown("---")
st.subheader("⚡ Immediate Actions Required")

alerts_col1, alerts_col2 = st.columns(2)

with alerts_col1:
    st.markdown("""
    <div class='alert-box'>
    <b>🚨 URGENT: Top Boeing Composite Engineer Available</b><br>
    - Name: [Redacted for Demo]<br>
    - 15 years on 787 program<br>
    - Blue Origin also pursuing<br>
    - ACTION: Contact TODAY
    </div>
    """, unsafe_allow_html=True)

with alerts_col2:
    st.markdown("""
    <div class='opportunity-box'>
    <b>💎 OPPORTUNITY: Wichita Talent Pool</b><br>
    - Spirit laying off 400 this week<br>
    - 47 match Natilus needs<br>
    - Lower salary expectations<br>
    - ACTION: Schedule Wichita trip
    </div>
    """, unsafe_allow_html=True)

# Main Dashboard Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Talent Pipeline", 
    "🏆 Competition Tracker", 
    "🏭 Supply Chain", 
    "📊 Series A Metrics",
    "🧠 Strategic Insights"
])

with tab1:
    st.subheader("High-Priority Talent Available Now")
    
    # Filters
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    with filter_col1:
        role_filter = st.multiselect(
            "Role",
            ["Composite Engineer", "Cert Specialist", "Manufacturing", "Flight Test"],
            default=["Composite Engineer"]
        )
    with filter_col2:
        location_filter = st.multiselect(
            "Location",
            ["Seattle", "Wichita", "Los Angeles", "Fort Worth"],
            default=["Seattle"]
        )
    with filter_col3:
        urgency = st.select_slider(
            "Urgency",
            ["Low", "Medium", "High", "Critical"],
            value="High"
        )
    
    # Talent table with scores
    talent_data = {
        'Name': ['John Smith', 'Sarah Chen', 'Mike Johnson', 'Lisa Wang', 'Tom Brown'],
        'Current Co': ['Boeing', 'Spirit', 'Boeing', 'Textron', 'Boeing'],
        'Role': ['Sr. Composite Eng', 'Cert Specialist', 'Mfg Engineer', 'Composite Lead', 'Flight Test Eng'],
        'Years Exp': [15, 12, 8, 10, 7],
        'Score': [95, 92, 88, 85, 82],
        'Status': ['🔴 Urgent', '🔴 Urgent', '🟡 High', '🟡 High', '🟢 Medium'],
        'Competition': ['Blue Origin, Joby', 'Archer', 'None yet', 'Reliable', 'Multiple'],
        'LinkedIn': ['View', 'View', 'View', 'View', 'View']
    }
    
    df = pd.DataFrame(talent_data)
    
    # Interactive table
    st.dataframe(
        df,
        use_container_width=True,
        height=300,
        column_config={
            "Score": st.column_config.ProgressColumn(
                "Priority Score",
                help="Based on skills, experience, and availability",
                format="%d",
                min_value=0,
                max_value=100,
            ),
            "LinkedIn": st.column_config.LinkColumn("Profile"),
        }
    )
    
    # Talent flow visualization
    st.subheader("Talent Movement Patterns")
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=["Boeing", "Spirit", "Textron", "Blue Origin", "Joby", "Archer", "AVAILABLE", "Natilus Target"],
            color=["red", "red", "orange", "blue", "blue", "blue", "green", "gold"]
        ),
        link=dict(
            source=[0, 1, 2, 0, 1, 6, 6, 6],
            target=[6, 6, 6, 3, 4, 7, 3, 4],
            value=[400, 300, 100, 50, 30, 20, 10, 5],
            label=["Layoffs", "Layoffs", "Attrition", "Poached", "Poached", "Target", "Competition", "Competition"],
            color=["rgba(255,0,0,0.4)", "rgba(255,0,0,0.4)", "rgba(255,165,0,0.4)", 
                   "rgba(0,0,255,0.4)", "rgba(0,0,255,0.4)", "rgba(0,255,0,0.4)",
                   "rgba(255,0,0,0.4)", "rgba(255,0,0,0.4)"]
        )
    )])
    
    fig.update_layout(title_text="Where Boeing/Spirit Talent is Going", font_size=12)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Competitive Intelligence")
    
    # Competitor comparison
    competitors = pd.DataFrame({
        'Company': ['Natilus', 'JetZero', 'Joby Aviation', 'Archer', 'Beta'],
        'Funding': [20, 235, 1800, 1100, 800],  # in millions
        'Employees': [30, 150, 1000, 700, 400],
        'Hiring/Month': [5, 25, 40, 30, 20],
        'Market Focus': ['Cargo BWB', 'Military BWB', 'eVTOL', 'eVTOL', 'eCTOL']
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.bar(
            competitors, 
            x='Company', 
            y='Hiring/Month',
            title='Monthly Hiring Velocity',
            color='Company',
            color_discrete_map={'Natilus': 'gold', 'JetZero': 'red'}
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.scatter(
            competitors,
            x='Funding',
            y='Employees',
            size='Hiring/Month',
            color='Company',
            title='Funding vs Team Size',
            text='Company'
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Recent competitor moves
    st.subheader("Recent Competitor Activity")
    
    competitor_news = pd.DataFrame({
        'Date': pd.date_range(start='2024-11-20', periods=5, freq='3D'),
        'Company': ['JetZero', 'Joby', 'JetZero', 'Archer', 'Beta'],
        'Action': [
            'Hired ex-Boeing BWB lead',
            'Announced 100 engineer hiring spree',
            'Filed 3 new BWB patents',
            'Opened Wichita facility',
            'Raised $300M Series C'
        ],
        'Impact': ['HIGH', 'MEDIUM', 'HIGH', 'LOW', 'MEDIUM']
    })
    
    for _, row in competitor_news.iterrows():
        if row['Impact'] == 'HIGH':
            st.error(f"🔴 {row['Date'].strftime('%Y-%m-%d')} - **{row['Company']}**: {row['Action']}")
        else:
            st.warning(f"🟡 {row['Date'].strftime('%Y-%m-%d')} - {row['Company']}: {row['Action']}")

with tab3:
    st.subheader("Supply Chain Risk Monitor")
    
    # Risk matrix
    suppliers = pd.DataFrame({
        'Supplier': ['Spirit AeroSystems', 'Hexcel', 'Toray', 'GE Aviation', 'Pratt & Whitney'],
        'Component': ['Fuselage sections', 'Carbon fiber', 'Prepreg materials', 'Engines', 'Engines'],
        'Risk Level': [90, 20, 30, 15, 20],
        'Financial Health': ['Critical', 'Stable', 'Good', 'Excellent', 'Good'],
        'Alternative': ['Triumph, FACC', 'Toray, SGL', 'Hexcel, Mitsubishi', 'Rolls-Royce', 'Rolls-Royce']
    })
    
    fig = px.scatter(
        suppliers,
        x='Risk Level',
        y='Component',
        color='Financial Health',
        size='Risk Level',
        hover_data=['Alternative'],
        title='Supplier Risk Assessment',
        color_discrete_map={'Critical': 'red', 'Stable': 'green', 'Good': 'blue', 'Excellent': 'darkgreen'}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Critical alerts
    st.error("""
    ⚠️ **CRITICAL: Spirit AeroSystems Update**
    - Boeing considering acquisition
    - Chapter 11 bankruptcy possible
    - ACTION: Engage Triumph as backup immediately
    """)

with tab4:
    st.subheader("Series A Fundraising Tracker")
    
    # Fundraising pipeline
    investors = pd.DataFrame({
        'Investor': ['Bessemer', 'Lux Capital', 'Prime Movers', 'Eclipse', 'Founders Fund'],
        'Stage': ['Due Diligence', 'Term Sheet', 'First Meeting', 'Deep Dive', 'First Meeting'],
        'Amount': [10, 15, 5, 8, 20],  # millions
        'Probability': [60, 80, 20, 50, 30],
        'Decision Date': ['2025-01-15', '2025-01-10', '2025-02-01', '2025-01-20', '2025-02-05']
    })
    
    # Funnel chart
    stages = ['First Meeting', 'Deep Dive', 'Due Diligence', 'Term Sheet', 'Closed']
    values = [8, 4, 2, 1, 0]
    
    fig = go.Figure(go.Funnel(
        y=stages,
        x=values,
        textinfo="value+percent initial"
    ))
    
    fig.update_layout(title="Investor Pipeline")
    st.plotly_chart(fig, use_container_width=True)
    
    # Key metrics for investors
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Monthly Burn", "$450K", "-$50K", help="Reduced through efficiency gains")
    with col2:
        st.metric("Runway", "8 months", "-1 month")
    with col3:
        st.metric("Customer LOIs", "$45M", "+$5M this week")

with tab5:
    st.subheader("Strategic Insights for Leadership")
    
    st.info("""
    ### 🎯 This Week's Strategic Priorities
    
    1. **Talent Acquisition Window**: Boeing announced 2,500 additional layoffs. We have ~2 weeks before competitors lock up the best talent.
    
    2. **Series A Narrative**: JetZero's military focus is actually HELPING us. Emphasize: "They validate BWB technology, we validate the business model."
    
    3. **Supply Chain Pivot**: Spirit's bankruptcy risk means we need to lock in Triumph NOW. They have capacity and are eager for new customers.
    
    4. **Manufacturing Site**: Fort Worth Alliance offering additional $10M in incentives if we decide by Jan 31.
    
    5. **Competition Alert**: Reliable Robotics quietly recruiting composite engineers. They may be building competing cargo aircraft.
    """)
    
    # Strategic decision matrix
    st.subheader("Decision Matrix: Next 30 Days")
    
    decisions = pd.DataFrame({
        'Decision': ['Hire 10 Boeing engineers', 'Lock Triumph as supplier', 'Choose Fort Worth site', 'Close Series A lead'],
        'Impact': [85, 70, 95, 100],
        'Urgency': [95, 80, 70, 90],
        'Risk if Delayed': ['Lose to competitors', 'No backup for Spirit', 'Lose incentives', 'Run out of runway']
    })
    
    fig = px.scatter(
        decisions,
        x='Urgency',
        y='Impact',
        text='Decision',
        size=[40, 40, 40, 40],
        title='Strategic Priority Matrix'
    )
    
    fig.add_hline(y=50, line_dash="dash", line_color="gray")
    fig.add_vline(x=50, line_dash="dash", line_color="gray")
    
    fig.add_annotation(x=75, y=75, text="DO NOW", showarrow=False, font=dict(size=20, color="red"))
    fig.add_annotation(x=25, y=75, text="IMPORTANT", showarrow=False, font=dict(size=15, color="orange"))
    fig.add_annotation(x=75, y=25, text="DELEGATE", showarrow=False, font=dict(size=15, color="blue"))
    fig.add_annotation(x=25, y=25, text="DELAY", showarrow=False, font=dict(size=15, color="gray"))
    
    st.plotly_chart(fig, use_container_width=True)

# Footer with refresh
st.markdown("---")
refresh_col1, refresh_col2, refresh_col3 = st.columns([1, 2, 1])
with refresh_col2:
    if st.button("🔄 Refresh Data", type="primary", use_container_width=True):
        st.rerun()

# Auto-refresh every 5 minutes
st.markdown("""
<script>
    setTimeout(function(){
        window.location.reload();
    }, 300000);
</script>
""", unsafe_allow_html=True)