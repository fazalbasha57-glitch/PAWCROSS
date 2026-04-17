import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timezone, timedelta
import time

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="PAW CROSS | Active Observatory", layout="wide", page_icon="🐾", initial_sidebar_state="expanded")

SHEET_ID = "1cwPIsNP-_c5YN5E36tLzSOEPUPPOGcQ6jXA5CThxl4c"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# --- 2. CSS INJECTION ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&family=Space+Grotesk:wght@500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #111312 !important;
    color: #e2e8f0 !important;
}

.stApp {
    background-color: #111312 !important;
}

[data-testid="stSidebar"] {
    background-color: #0a0c0b !important;
    border-right: 1px solid #1f2421;
}

/* Hide header */
header {visibility: hidden;}

/* Custom typography */
h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #ffffff !important;
}

/* Tactical Green Accent */
.text-tactical {
    color: #86efac !important;
}

/* Metric overriding */
[data-testid="stMetricValue"] {
    font-size: 3.5rem !important;
    font-weight: 800 !important;
    font-family: 'Space Grotesk', sans-serif;
    color: #ffffff !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.85rem !important;
    color: #94a3b8 !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 600;
}

/* Custom Cards */
div.stHtml {
    width: 100%;
}

.tactical-card {
    background-color: #171a18;
    border: 1px solid #242926;
    border-radius: 12px;
    padding: 24px;
    height: 100%;
}

/* Sidebar additions */
.deploy-btn {
    background-color: #86efac;
    color: #064e3b;
    font-weight: 700;
    text-align: center;
    padding: 12px;
    border-radius: 8px;
    display: block;
    text-decoration: none;
    margin-top: 30px;
    margin-bottom: 20px;
    transition: all 0.2s ease;
}
.deploy-btn:hover {
    background-color: #4ade80;
}

.sidebar-profile {
    display: flex;
    align-items: center;
    gap: 12px;
    padding-top: 20px;
    border-top: 1px solid #1f2421;
}
.sidebar-profile img {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 2px solid #242926;
}

/* Image Containers */
.feed-container {
    position: relative;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #242926;
}
.feed-overlay-top {
    position: absolute;
    top: 20px;
    left: 20px;
    background: rgba(0,0,0,0.7);
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1px;
    backdrop-filter: blur(4px);
    border: 1px solid rgba(255,255,255,0.1);
    display: flex;
    align-items: center;
    gap: 8px;
}
.live-dot {
    height: 8px;
    width: 8px;
    background-color: #ef4444;
    border-radius: 50%;
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(239, 68, 68, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}

.feed-overlay-bottom {
    position: absolute;
    bottom: 20px;
    left: 20px;
    font-family: 'Space Grotesk', monospace;
    font-size: 0.7rem;
    color: #86efac;
    line-height: 1.5;
}

hr {
    border-color: #1f2421;
}

</style>
""", unsafe_allow_html=True)


# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='margin-bottom:0; color:#86efac !important;'>PAW CROSS</h2><p style='color:#64748b; font-size:0.8rem; letter-spacing:1px; margin-top:0;'>ACTIVE OBSERVATORY</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Custom Navigation
    page = st.radio("NAVIGATION", ["Observatory", "Project Details"], label_visibility="collapsed")
    
    st.markdown("""
        <a href="#" class="deploy-btn">Deploy Ranger</a>
        <div class="sidebar-profile">
            <img src="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=100&q=80" alt="Chief Warden">
            <div>
                <div style="font-weight:600; font-size:0.9rem; color:#fff;">Chief Warden</div>
                <div style="font-size:0.75rem; color:#64748b;">Sentinel Sector 7</div>
            </div>
        </div>
    """, unsafe_allow_html=True)


# --- 4. DATA LOADING & TIMEZONE LOGIC ---
@st.cache_data(ttl=5) # Cache for 5s to avoid hitting sheets API too hard
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], dayfirst=True, errors='coerce')
        return df
    except Exception as e:
        return pd.DataFrame()


# --- 5. PAGE: OBSERVATORY (LIVE DASHBOARD) ---
if page == "Observatory":
    
    st.markdown("""
        <div style="display:flex; align-items:baseline; gap:15px; margin-bottom: 20px;">
            <h1 style="margin:0; font-size:3rem;">Observatory</h1>
            <div style="color:#86efac; font-size:0.8rem; font-weight:600; letter-spacing:1px; display:flex; align-items:center; gap:6px;">
                <div style="width:6px; height:6px; background-color:#86efac; border-radius:50%;"></div> LIVE FEED ACTIVE
            </div>
        </div>
    """, unsafe_allow_html=True)

    df = load_data()
    
    is_alert = False
    last_timestamp_str = "N/A"
    
    if not df.empty:
        last_entry = df.iloc[-1]
        
        # TIMEZONE FIX (UTC -> IST) - Crucial for cloud deployment
        current_utc = datetime.now(timezone.utc)
        current_ist_naive = (current_utc + timedelta(hours=5, minutes=30)).replace(tzinfo=None)
        
        time_diff = (current_ist_naive - last_entry['Timestamp']).total_seconds()
        
        if 0 <= time_diff < 30:
            is_alert = True
            
        last_timestamp_str = last_entry['Timestamp'].strftime('%H:%M:%S')

    if is_alert:
        st.error(f"🚨 TACTICAL ALERT: MOTION SIGNATURE DETECTED ({last_timestamp_str})", icon="🚨")
        st.toast("🐾 TACTICAL ALERT: BIOMETRIC SIGNATURE DETECTED!", icon='⚠️')
        # Optional Sound
        # st.components.v1.html("""<script>new Audio('https://actions.google.com/sounds/v1/alarms/beep_short.ogg').play();</script>""", height=0)


    # Dashboard Layout
    col_main, col_side = st.columns([2.5, 1])

    with col_main:
        # Live Feed Visual
        st.markdown(f"""
            <div class="feed-container">
                <img src="https://images.unsplash.com/photo-1549479363-d144e5cb401e?auto=format&fit=crop&q=80&w=1200" style="width:100%; display:block; filter: sepia(0.6) hue-rotate(50deg) saturate(0.8) brightness(0.6) contrast(1.2);">
                <div class="feed-overlay-top">
                    <div class="live-dot"></div> LIVE &nbsp;|&nbsp; CAM 04 // SECTOR DELTA
                </div>
                <div class="feed-overlay-bottom">
                    LAT: 45.2891° N<br>
                    LON: 122.3412° W<br>
                    ALT: 1,242M<br>
                    <div style="margin-top:10px; width:200px; height:4px; background:#242926; border-radius:2px; overflow:hidden;">
                        <div style="width:75%; height:100%; background:#86efac;"></div>
                    </div>
                    <div style="margin-top:4px; font-size:0.6rem; color:#64748b;">THERMAL SIGNATURE STRENGTH</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Heatmap Visual
        st.markdown("""
            <div class="tactical-card" style="padding:0; overflow:hidden; position:relative; border: 1px solid #242926;">
                <img src="https://images.unsplash.com/photo-1524661135-423995f22d0b?auto=format&fit=crop&q=80&w=1200" style="width:100%; height:250px; object-fit:cover; filter: grayscale(1) invert(0.8) sepia(0.5) hue-rotate(70deg) contrast(1.5) opacity(0.6);">
                <div style="position:absolute; top:20px; left:20px;">
                    <h3 style="margin:0; font-size:1.2rem; color: #fff;">Movement Heatmap</h3>
                    <p style="color:#94a3b8; font-size:0.75rem; letter-spacing:1px; margin:0; text-transform:uppercase;">Density Analysis • Last 24 Hours</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col_side:
        total_detections = len(df) if not df.empty else 0
        
        # Metrics Cards
        st.markdown(f"""
            <div class="tactical-card" style="margin-bottom: 20px;">
                <div style="color:#94a3b8; font-size:0.75rem; font-weight:600; letter-spacing:1px; margin-bottom:10px;">TOTAL DETECTIONS</div>
                <div style="font-size:3rem; font-family:'Space Grotesk', sans-serif; font-weight:800; color:#fff; line-height:1;">{total_detections:,} <span style="font-size:1rem; color:#86efac; font-weight:600;">+12%</span></div>
            </div>
            
            <div class="tactical-card" style="margin-bottom: 20px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                    <div style="color:#94a3b8; font-size:0.75rem; font-weight:600; letter-spacing:1px;">LAST ACTIVITY</div>
                </div>
                <div style="font-size:1.5rem; font-family:'Space Grotesk', sans-serif; font-weight:700; color:#fff;">Panthera tigris</div>
                <div style="color:#94a3b8; font-size:0.85rem; margin-bottom:15px;">Sector Delta • {last_timestamp_str}</div>
                <div style="display:flex; align-items:center; gap:8px;">
                    <img src="https://images.unsplash.com/photo-1549479363-d144e5cb401e?auto=format&fit=crop&w=50&h=50&q=80" style="width:30px; height:30px; border-radius:50%; object-fit:cover;">
                    <div style="background:#064e3b; color:#86efac; padding:4px 8px; border-radius:12px; font-size:0.75rem; font-weight:bold;">+4</div>
                </div>
            </div>
            
            <div class="tactical-card">
                <div style="color:#94a3b8; font-size:0.75rem; font-weight:600; letter-spacing:1px; margin-bottom:15px;">SYSTEM STATUS</div>
                <div style="display:flex; justify-content:space-between; margin-bottom:10px; font-size:0.85rem;">
                    <span style="color:#cbd5e1;">Uptime</span>
                    <span style="color:#fff; font-family:monospace;">99.98%</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:10px; font-size:0.85rem;">
                    <span style="color:#cbd5e1;">Latency</span>
                    <span style="color:#86efac; font-family:monospace;">24ms</span>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:0.85rem;">
                    <span style="color:#cbd5e1;">Active Nodes</span>
                    <span style="color:#fff; font-family:monospace;">12/14</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    time.sleep(5)
    st.rerun()

# --- 6. PAGE: PROJECT DETAILS ---
elif page == "Project Details":
    
    # Hero Section
    st.markdown("""
        <div style="position:relative; border-radius:16px; overflow:hidden; border: 1px solid #242926; margin-bottom: 40px; text-align:center;">
            <img src="https://images.unsplash.com/photo-1588693813134-2e23d043dcd7?auto=format&fit=crop&q=80&w=1600&h=600" style="width:100%; height:400px; object-fit:cover; opacity:0.4;">
            <div style="position:absolute; top:50%; left:50%; transform:translate(-50%, -50%); width:100%;">
                <div style="color:#86efac; font-size:0.8rem; font-weight:700; letter-spacing:2px; margin-bottom:10px;">TACTICAL INTELLIGENCE REPORT</div>
                <h1 style="font-size:3.5rem; margin:0; line-height:1.1;">Project <span style="color:#86efac;">PAW CROSS</span>:<br>High-Tech Guardian</h1>
                <p style="color:#cbd5e1; max-width:600px; margin:20px auto; font-size:1.1rem; line-height:1.5;">
                    Protecting endangered wildlife through real-time biometric telemetry and edge-computing surveillance.
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align:center; font-size:2.5rem; margin-bottom:40px;'>Mission Objective</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("""
            <div style="margin-bottom:30px;">
                <div style="display:flex; align-items:center; gap:15px; margin-bottom:10px;">
                    <div style="background:#064e3b; color:#86efac; width:40px; height:40px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-weight:bold; font-size:1.2rem;">🛡️</div>
                    <h3 style="margin:0; font-size:1.3rem;">Anti-Poaching Shield</h3>
                </div>
                <p style="color:#94a3b8; font-size:0.95rem; line-height:1.6; margin-left:55px;">Implementing a silent, non-invasive perimeter that detects human incursions within milliseconds.</p>
            </div>
            
            <div style="margin-bottom:30px;">
                <div style="display:flex; align-items:center; gap:15px; margin-bottom:10px;">
                    <div style="background:#064e3b; color:#86efac; width:40px; height:40px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-weight:bold; font-size:1.2rem;">📊</div>
                    <h3 style="margin:0; font-size:1.3rem;">Biometric Insight</h3>
                </div>
                <p style="color:#94a3b8; font-size:0.95rem; line-height:1.6; margin-left:55px;">Monitoring population health through motion-capture analysis and thermal heat mapping.</p>
            </div>
            
            <div>
                <div style="display:flex; align-items:center; gap:15px; margin-bottom:10px;">
                    <div style="background:#064e3b; color:#86efac; width:40px; height:40px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-weight:bold; font-size:1.2rem;">🛰️</div>
                    <h3 style="margin:0; font-size:1.3rem;">Global Connectivity</h3>
                </div>
                <p style="color:#94a3b8; font-size:0.95rem; line-height:1.6; margin-left:55px;">Bridging remote forest nodes with satellite backhaul for 100% uptime in deep wilderness.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div class="tactical-card" style="position:relative; padding:0; overflow:hidden;">
                <img src="https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&q=80&w=800" style="width:100%; height:350px; object-fit:cover; opacity:0.6; filter:contrast(1.2);">
                <div style="position:absolute; bottom:20px; left:20px; right:20px; background:rgba(10,12,11,0.85); backdrop-filter:blur(10px); padding:20px; border-radius:12px; border:1px solid rgba(255,255,255,0.1);">
                    <div style="color:#86efac; font-size:0.7rem; font-weight:700; letter-spacing:1px; margin-bottom:8px;">LIVE SENTINEL LOG</div>
                    <p style="color:#fff; font-style:italic; font-size:0.9rem; margin:0;">"The Sentinel system maintains a 99.8% detection accuracy across 4,000 hectares of dense canopy."</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<hr style='margin: 60px 0;'>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style="text-align:center; margin-bottom:40px;">
            <h2 style="font-size:2.5rem; margin-bottom:10px;">Neural Architecture</h2>
            <p style="color:#94a3b8;">An end-to-edge ecosystem designed for maximum stealth and data integrity.</p>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    
    def architecture_card(num, title, desc, img_url):
        return f"""
        <div class="tactical-card" style="display:flex; flex-direction:column; height:100%;">
            <div style="font-size:4rem; font-family:'Space Grotesk', sans-serif; font-weight:800; color:rgba(134,239,172,0.15); line-height:1; margin-bottom:10px;">{num}</div>
            <h3 style="font-size:1.3rem; margin-top:0; margin-bottom:15px;">{title}</h3>
            <p style="color:#94a3b8; font-size:0.9rem; line-height:1.6; flex-grow:1;">{desc}</p>
            <div style="border-radius:8px; overflow:hidden; margin-top:20px; border:1px solid #242926; height:120px;">
                <img src="{img_url}" style="width:100%; height:100%; object-fit:cover; opacity:0.7;">
            </div>
        </div>
        """
        
    with c1:
        st.markdown(architecture_card(
            "01", "The Sensor Node", 
            "PIR and thermal arrays detect movement signatures at the edge. Low-power Arduino cores handle initial noise filtering.",
            "https://images.unsplash.com/photo-1558346490-a72e53ae2d4f?auto=format&fit=crop&q=80&w=400"
        ), unsafe_allow_html=True)
    with c2:
        st.markdown(architecture_card(
            "02", "Mesh Gateway", 
            "ESP32 clusters aggregate local node data and push encrypted streams to our cloud-based backend.",
            "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&q=80&w=400"
        ), unsafe_allow_html=True)
    with c3:
        st.markdown(architecture_card(
            "03", "Command Center", 
            "Streamlit dashboards visualize real-time trajectories and trigger automated ranger deployment.",
            "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&q=80&w=400"
        ), unsafe_allow_html=True)
