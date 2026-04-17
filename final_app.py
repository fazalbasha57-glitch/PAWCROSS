import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timezone, timedelta
import time

# --- 1. CONFIGURATION ---
SHEET_ID = "1cwPIsNP-_c5YN5E36tLzSOEPUPPOGcQ6jXA5CThxl4c"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.set_page_config(page_title="PAW CROSS | Wildlife Safety", layout="wide", page_icon="🐾")

# --- 2. SIDEBAR NAVIGATION ---
st.sidebar.title("🐾 PAW CROSS Menu")
page = st.sidebar.radio("Navigate to:", ["Home", "Live Dashboard", "Project Details"])

# --- 3. PAGE 1: HOME ---
if page == "Home":
    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.title("Welcome to PAW CROSS")
        st.subheader("The Digital Guardian for Wildlife Safety")
        st.write("""
            Forest roads are shared spaces. PAW CROSS uses IoT and thermal sensing 
            to detect animal presence and alert drivers instantly, reducing 
            accidents and protecting biodiversity.
        """)
        st.info("👈 Use the sidebar to monitor live detections.")

    with col2:
        st.image("https://images.unsplash.com/photo-1484406566174-9da000fda645?auto=format&fit=crop&q=80&w=1200&h=675", 
                 caption="Bridging Technology and Nature", use_container_width=True)

    st.markdown("---")
    
    st.subheader("🚀 System Quick Look")
    s1, s2, s3 = st.columns(3)
    s1.success("🛰️ Cloud: Connected")
    s2.info("🔋 Hardware: Active")
    s3.warning("📡 Sensor: Monitoring")

    st.markdown("---")
    
    st.subheader("🛠️ Technology Stack")
    t1, t2 = st.columns(2)
    with t1:
        st.markdown("""
        - **Microcontroller:** Arduino with ESP8266 Wi-Fi
        - **Sensing:** PIR Thermal Motion Sensors
        - **Database:** Google Sheets (Cloud Storage)
        """)
    with t2:
        st.markdown("""
        - **Frontend:** Streamlit Web Framework (Python)
        - **Analytics:** Plotly Real-time Graphing
        - **Bridge:** Python Serial-to-HTTPS
        """)

# --- 4. PAGE 2: DASHBOARD ---
elif page == "Live Dashboard":
    st.title("🐾 Real-Time Monitoring Dashboard")
    
    try:
        # Load Data
        df = pd.read_csv(SHEET_URL)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], dayfirst=True, errors='coerce')
        
        # --- UPDATE: ALERT LOGIC WITH TIME-WINDOW VALIDATION ---
        if not df.empty:
            # 1. Get the most recent entry
            last_entry = df.iloc[-1]
            
            # 2. Calculate how long ago it happened
            # Get current time in UTC, then convert to IST (+05:30) to match Google Sheets
            current_utc = datetime.now(timezone.utc)
            current_ist_naive = (current_utc + timedelta(hours=5, minutes=30)).replace(tzinfo=None)
            
            time_diff = (current_ist_naive - last_entry['Timestamp']).total_seconds()

            # 3. ONLY trigger alert if it happened within the last 30 seconds
            # Ensure time_diff is positive (to handle potential slight future time discrepancies)
            if 0 <= time_diff < 30: 
                st.error(f"🚨 LIVE ALERT: MOTION DETECTED ({last_entry['Timestamp'].strftime('%H:%M:%S')})")
                st.toast("🐾 PAW DETECTED!", icon='⚠️')
                
                # Play Sound
                st.components.v1.html(
                    """<script>new Audio('https://actions.google.com/sounds/v1/alarms/beep_short.ogg').play();</script>""", 
                    height=0
                )
            else:
                st.success("✅ System Clear: No recent motion detected.")
        
        # Metrics & Visuals
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Detections", len(df))
        m2.metric("Last Activity", last_entry['Timestamp'].strftime('%H:%M') if not df.empty else "N/A")
        m3.metric("System Status", "LIVE")

        chart_col, table_col = st.columns([2, 1])
        with chart_col:
            fig = px.area(df, x='Timestamp', y=df.index, title="Detection History", color_discrete_sequence=['#2E7D32'])
            st.plotly_chart(fig, use_container_width=True)
        
        with table_col:
            st.write("Recent Activity Log")
            st.dataframe(df.tail(10), use_container_width=True)

        # Auto-Refresh logic
        time.sleep(5)
        st.rerun()

    except Exception as e:
        st.warning("Connecting to Cloud Database... Wave sensor to start data flow.")

# --- 5. PAGE: PROJECT DETAILS ---
elif page == "Project Details":
    st.title("🐾 About PAW CROSS")

    st.markdown("### 🌐 Global Access")
    c1, c2 = st.columns(2)
    with c1:
        st.info("🔗 **Live Dashboard:** [paw-cross.streamlit.app](https://pawcross-wcoggwmycm8niw2lyk35hm.streamlit.app)")
    with c2:
        st.success("💻 **Source Code:** [GitHub Repository](https://github.com/fazalbasha57-glitch/PAWCROSS/tree/main)")

    st.markdown("---")

    col_info, col_img = st.columns([1.5, 1])
    
    with col_info:
        st.markdown("""
        ### 🎯 Project Objective
        The primary goal is to create an affordable, scalable IoT solution for forest-bordering roads. 
        By using **thermal detection** instead of standard cameras for motion triggering, we:
        - Protect animal privacy.
        - Reduce data costs and power consumption.
        - Maintain 24/7 surveillance in complete darkness.

        ### ⚙️ How it Works
        1. **Sensing:** PIR sensors detect infrared heat signatures from wildlife.
        2. **Processing:** Arduino/ESP32 processes the signal and bridges it to the web.
        3. **Cloud Logging:** Data is securely logged into a Google Sheet for analysis.
        4. **Real-time Alert:** This Web App and roadside LEDs notify drivers and rangers.
        """)
    
    with col_img:
        st.image("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&q=80&w=800", 
                 caption="IoT Architecture for Wildlife Safety", use_container_width=True)

    st.markdown("---")
    st.info("🎓 **Final Year BCA Project** | Focus: Smart Cities & Wildlife Conservation")
