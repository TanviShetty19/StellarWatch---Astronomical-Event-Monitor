import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import hashlib
import json

# =============================================================================
# CORE CLASSES (All in one file for Hugging Face compatibility)
# =============================================================================

class AstronomicalEventDetector:
    def get_all_events(self, location_name='bangalore'):
        """Get sample astronomical events for any location"""
        location = GLOBAL_LOCATIONS.get(location_name, GLOBAL_LOCATIONS['bangalore'])
        
        events = [
            {
                'event': 'International Space Station Transit',
                'time': datetime.now() + timedelta(hours=2),
                'duration': '6 minutes',
                'max_altitude': 67,
                'brightness': 'Magnitude -3.9 (Very Bright)',
                'direction': 'West to East',
                'source': 'Live Satellite Data'
            },
            {
                'event': 'Perseid Meteor Shower',
                'peak': datetime.now() + timedelta(days=3),
                'zhr': 100,
                'moon_phase': 'Waning Crescent',
                'visibility': 'Excellent',
                'constellation': 'Perseus',
                'source': 'IMO Database'
            },
            {
                'event': 'Aurora Borealis Forecast',
                'probability': '25%',
                'kp_index': 4.5,
                'best_time': '22:00-02:00 Local',
                'visibility': 'Fair',
                'source': 'NOAA Space Weather'
            },
            {
                'event': 'SpaceX Falcon 9 Launch',
                'time': datetime.now() + timedelta(hours=6),
                'mission': 'Starlink Group 8-1',
                'location': 'Cape Canaveral, Florida',
                'visibility': 'Live Stream Available',
                'source': 'Space Launch Schedule'
            }
        ]
        
        # Filter to show only upcoming events
        current_time = datetime.now()
        filtered_events = []
        for event in events:
            event_time = event.get('time') or event.get('peak')
            if not isinstance(event_time, datetime) or event_time > current_time:
                filtered_events.append(event)
        
        return filtered_events

class NotificationEngine:
    def send_alerts(self, event):
        """Send alerts (simulated for demo)"""
        st.toast(f"🔔 Alert sent: {event['event']}", icon="🚀")

class AuthSystem:
    def __init__(self):
        self.users = {
            "demo": {
                'password': self._hash_password("demo123"),
                'email': 'demo@example.com',
                'preferences': {
                    'default_location': 'bangalore',
                    'alert_types': ['ISS', 'Meteor', 'Aurora', 'Launch'],
                    'notification_method': 'email'
                }
            }
        }
    
    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login_user(self, username, password):
        if username in self.users and self.users[username]['password'] == self._hash_password(password):
            return True, "Login successful"
        return False, "Invalid username or password"
    
    def register_user(self, username, password, email):
        if username in self.users:
            return False, "Username already exists"
        self.users[username] = {
            'password': self._hash_password(password),
            'email': email,
            'preferences': {
                'default_location': 'bangalore',
                'alert_types': ['ISS', 'Meteor', 'Aurora', 'Launch'],
                'notification_method': 'email'
            }
        }
        return True, "Registration successful"
    
    def get_user_preferences(self, username):
        return self.users.get(username, {}).get('preferences', {})
    
    def update_user_preferences(self, username, preferences):
        if username in self.users:
            self.users[username]['preferences'] = preferences
            return True
        return False

class MonitoringScheduler:
    def __init__(self):
        self.is_running = False
    
    def start_monitoring(self, locations):
        self.is_running = True
        st.toast(f"🟢 Monitoring started for {len(locations)} locations", icon="📡")
    
    def stop_monitoring(self):
        self.is_running = False
        st.toast("🔴 Monitoring stopped", icon="⏹️")
    
    def get_scheduler_status(self):
        return {
            'is_running': self.is_running,
            'next_run': datetime.now() + timedelta(minutes=5) if self.is_running else None,
            'job_count': 4 if self.is_running else 0
        }

# =============================================================================
# GLOBAL DATA
# =============================================================================

GLOBAL_LOCATIONS = {
    'bangalore': {'name': 'Bangalore, India', 'lat': 12.9716, 'lon': 77.5946, 'country': 'India', 'continent': 'Asia'},
    'delhi': {'name': 'Delhi, India', 'lat': 28.7041, 'lon': 77.1025, 'country': 'India', 'continent': 'Asia'},
    'mumbai': {'name': 'Mumbai, India', 'lat': 19.0760, 'lon': 72.8777, 'country': 'India', 'continent': 'Asia'},
    'new_york': {'name': 'New York, USA', 'lat': 40.7128, 'lon': -74.0060, 'country': 'USA', 'continent': 'North America'},
    'london': {'name': 'London, UK', 'lat': 51.5074, 'lon': -0.1278, 'country': 'UK', 'continent': 'Europe'},
    'tokyo': {'name': 'Tokyo, Japan', 'lat': 35.6762, 'lon': 139.6503, 'country': 'Japan', 'continent': 'Asia'},
    'sydney': {'name': 'Sydney, Australia', 'lat': -33.8688, 'lon': 151.2093, 'country': 'Australia', 'continent': 'Oceania'},
    'dubai': {'name': 'Dubai, UAE', 'lat': 25.2048, 'lon': 55.2708, 'country': 'UAE', 'continent': 'Asia'},
    'paris': {'name': 'Paris, France', 'lat': 48.8566, 'lon': 2.3522, 'country': 'France', 'continent': 'Europe'},
    'berlin': {'name': 'Berlin, Germany', 'lat': 52.5200, 'lon': 13.4050, 'country': 'Germany', 'continent': 'Europe'}
}

def get_locations_by_continent():
    continents = {}
    for loc_id, loc_data in GLOBAL_LOCATIONS.items():
        continent = loc_data['continent']
        if continent not in continents:
            continents[continent] = {}
        continents[continent][loc_id] = loc_data
    return continents

# =============================================================================
# STREAMLIT APP
# =============================================================================

# Initialize global instances
auth_system = AuthSystem()
monitoring_scheduler = MonitoringScheduler()
detector = AstronomicalEventDetector()
notifier = NotificationEngine()

# Page configuration
st.set_page_config(
    page_title="StellarWatch - Astronomical Event Tracker",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Space-Themed CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0c0c2e 0%, #1a1a3e 50%, #2d2d5a 100%);
        color: #ffffff;
    }
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 800;
    }
    .section-header {
        font-size: 2rem;
        color: #ffffff;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
        font-weight: 600;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .event-card {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        border-left: 4px solid #667eea;
        padding: 1.2rem;
        margin: 0.8rem 0;
    }
    .login-container {
        max-width: 450px;
        margin: 3rem auto;
        padding: 2.5rem;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .icon {
        font-size: 1.2rem;
        margin-right: 0.5rem;
    }
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
""", unsafe_allow_html=True)

class StellarWatchApp:
    def __init__(self):
        self.detector = detector
        self.notifier = notifier
        
    def initialize_session_state(self):
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'username' not in st.session_state:
            st.session_state.username = None
        if 'selected_location' not in st.session_state:
            st.session_state.selected_location = 'bangalore'
        if 'user_preferences' not in st.session_state:
            st.session_state.user_preferences = {}
    
    def show_login_page(self):
        st.markdown('<h1 class="main-header">StellarWatch</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #a0a0c0; font-size: 1.2rem; margin-bottom: 3rem;">Global Astronomical Event Monitoring System</p>', unsafe_allow_html=True)
        
        with st.expander("🔧 Demo Credentials"):
            st.write("**Username:** demo")
            st.write("**Password:** demo123")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            tab1, tab2 = st.tabs(["🔐 Sign In", "📝 Create Account"])
            
            with tab1:
                st.subheader("Access Your Dashboard")
                login_username = st.text_input("Username", value="demo", key="login_user")
                login_password = st.text_input("Password", type="password", value="demo123", key="login_pass")
                
                if st.button("Authenticate", use_container_width=True, type="primary"):
                    success, message = auth_system.login_user(login_username, login_password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.username = login_username
                        st.session_state.user_preferences = auth_system.get_user_preferences(login_username)
                        st.rerun()
                    else:
                        st.error(f"Authentication failed: {message}")
            
            with tab2:
                st.subheader("Join StellarWatch")
                reg_username = st.text_input("Username", key="reg_user")
                reg_email = st.text_input("Email Address", key="reg_email")
                reg_password = st.text_input("Password", type="password", key="reg_pass")
                reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
                
                if st.button("Register Account", use_container_width=True, type="primary"):
                    if reg_password != reg_confirm:
                        st.error("Password confirmation does not match")
                    elif reg_username and reg_email and reg_password:
                        success, message = auth_system.register_user(reg_username, reg_password, reg_email)
                        if success:
                            st.success(f"{message} You can now sign in.")
                        else:
                            st.error(f"Registration failed: {message}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    def show_location_selector(self):
        st.sidebar.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.sidebar.markdown('<h3><i class="fas fa-globe-americas icon"></i>Observation Location</h3>', unsafe_allow_html=True)
        
        continents = get_locations_by_continent()
        selected_continent = st.sidebar.selectbox("Continent", list(continents.keys()))
        
        countries = list(set([loc['country'] for loc in continents[selected_continent].values()]))
        selected_country = st.sidebar.selectbox("Country", countries)
        
        country_cities = {k: v for k, v in continents[selected_continent].items() if v['country'] == selected_country}
        selected_city = st.sidebar.selectbox("City", list(country_cities.keys()), format_func=lambda x: country_cities[x]['name'])
        
        if st.sidebar.button("Set Observation Point", use_container_width=True, type="primary"):
            st.session_state.selected_location = selected_city
            st.sidebar.success(f"Tracking events for {country_cities[selected_city]['name']}")
        
        st.sidebar.markdown('</div>', unsafe_allow_html=True)
        
        # Quick locations
        st.sidebar.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.sidebar.markdown('<h4><i class="fas fa-bolt icon"></i>Quick Access</h4>', unsafe_allow_html=True)
        quick_locations = ['new_york', 'london', 'tokyo', 'sydney']
        for loc in quick_locations:
            if st.sidebar.button(f"📍 {GLOBAL_LOCATIONS[loc]['name']}", key=f"quick_{loc}", use_container_width=True):
                st.session_state.selected_location = loc
                st.rerun()
        st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    def show_user_dashboard(self):
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        with col1:
            st.markdown(f'<h1 class="main-header">StellarWatch</h1>', unsafe_allow_html=True)
            st.markdown(f'<p style="color: #a0a0c0;">Welcome back, <strong>{st.session_state.username}</strong></p>', unsafe_allow_html=True)
        with col2:
            current_loc = GLOBAL_LOCATIONS[st.session_state.selected_location]
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Observation Point", current_loc['name'])
            st.markdown('</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Local Time", datetime.now().strftime("%H:%M"))
            st.markdown('</div>', unsafe_allow_html=True)
        with col4:
            if st.button("Sign Out", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.username = None
                st.rerun()
        
        tab1, tab2, tab3, tab4 = st.tabs(["🌍 Local Events", "🗺️ Global View", "⚡ Live Monitor", "⚙️ Settings"])
        
        with tab1:
            self.show_current_location_view()
        with tab2:
            self.show_global_view()
        with tab3:
            self.show_live_monitor()
        with tab4:
            self.show_observatory_settings()
    
    def show_current_location_view(self):
        location_id = st.session_state.selected_location
        location_data = GLOBAL_LOCATIONS[location_id]
        
        st.markdown(f'<div class="section-header"><i class="fas fa-satellite icon"></i>Celestial Events - {location_data["name"]}</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Latitude", f"{location_data['lat']}°")
        with col2: st.metric("Longitude", f"{location_data['lon']}°")
        with col3: st.metric("Country", location_data['country'])
        with col4: st.metric("Continent", location_data['continent'])
        
        events = self.detector.get_all_events(location_id)
        
        if events:
            st.markdown(f'<h3><i class="fas fa-calendar-alt icon"></i>Upcoming Events ({len(events)})</h3>', unsafe_allow_html=True)
            for event in events:
                self.display_event_card(event, location_data)
        else:
            st.info("No events detected for this location.")
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        with col1: st.write("Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        with col2: 
            if st.button("Refresh Data", use_container_width=True):
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    def show_global_view(self):
        st.markdown('<div class="section-header"><i class="fas fa-globe icon"></i>Global Celestial Overview</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Global Event Distribution")
        
        map_data = []
        for loc_id, loc_data in GLOBAL_LOCATIONS.items():
            events = self.detector.get_all_events(loc_id)
            map_data.append({
                'lat': loc_data['lat'], 'lon': loc_data['lon'],
                'city': loc_data['name'], 'country': loc_data['country'],
                'events': len(events), 'size': min(len(events) * 5, 30)
            })
        
        df = pd.DataFrame(map_data)
        if not df.empty:
            fig = px.scatter_geo(df, lat='lat', lon='lon', hover_name='city',
                               hover_data={'country': True, 'events': True}, size='size',
                               projection='natural earth', title='Global Astronomical Event Distribution',
                               color='events', color_continuous_scale='viridis')
            fig.update_geos(showcountries=True, showcoastlines=True, showland=True)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    def show_live_monitor(self):
        st.markdown('<div class="section-header"><i class="fas fa-tachometer-alt icon"></i>Live Observatory Monitor</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Active Sensors", "12/12")
        with col2: st.metric("Alerts Today", "3")
        with col3: st.metric("Data Freshness", "< 2 min")
        with col4: st.metric("System Status", "Nominal")
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Manual Controls")
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            check_location = st.selectbox("Target Location", list(GLOBAL_LOCATIONS.keys()),
                                         format_func=lambda x: GLOBAL_LOCATIONS[x]['name'])
        with col2:
            if st.button("Initiate Scan", use_container_width=True):
                with st.spinner("Scanning..."):
                    events = self.detector.get_all_events(check_location)
                    st.success(f"Found {len(events)} events")
        with col3:
            if st.button("Test Alert", use_container_width=True):
                test_event = {'event': 'System Test - ISS Transit'}
                self.notifier.send_alerts(test_event)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Background Monitoring")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Start Monitoring", use_container_width=True):
                monitoring_scheduler.start_monitoring(['bangalore', 'new_york', 'london'])
        with col2:
            if st.button("Stop Monitoring", use_container_width=True):
                monitoring_scheduler.stop_monitoring()
        
        status = monitoring_scheduler.get_scheduler_status()
        st.write(f"**Status:** {'🟢 Running' if status['is_running'] else '🔴 Stopped'}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    def show_observatory_settings(self):
        st.markdown('<div class="section-header"><i class="fas fa-cogs icon"></i>Observatory Configuration</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Notification Preferences")
        col1, col2 = st.columns(2)
        with col1:
            email_notify = st.checkbox("Email Notifications", value=True)
            push_notify = st.checkbox("Push Notifications", value=True)
        with col2:
            alert_window = st.slider("Alert Time (minutes)", 15, 180, 60)
            refresh_rate = st.selectbox("Refresh Rate", ['5 minutes', '15 minutes', '30 minutes'])
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Event Filters")
        event_types = st.multiselect("Monitor events:", ['Satellite Transits', 'Meteor Showers', 'Aurora', 'Rocket Launches'],
                                   default=['Satellite Transits', 'Meteor Showers'])
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Default Location")
        default_loc = st.selectbox("Primary location", list(GLOBAL_LOCATIONS.keys()),
                                 format_func=lambda x: GLOBAL_LOCATIONS[x]['name'])
        if st.button("Save Configuration", use_container_width=True):
            st.success("Settings saved successfully!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    def display_event_card(self, event, location):
        st.markdown('<div class="event-card">', unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        with col1:
            event_type = event['event']
            if 'ISS' in event_type: icon, color = "fa-satellite", "#667eea"
            elif 'Meteor' in event_type: icon, color = "fa-meteor", "#f5576c"
            elif 'Aurora' in event_type: icon, color = "fa-cloud-moon", "#4facfe"
            elif 'Launch' in event_type: icon, color = "fa-rocket", "#764ba2"
            else: icon, color = "fa-star", "#f093fb"
            
            st.markdown(f'<h4><i class="fas {icon}" style="color: {color};"></i> {event_type}</h4>', unsafe_allow_html=True)
            
            event_time = event.get('time') or event.get('peak', 'Unknown')
            if isinstance(event_time, datetime):
                st.write(f"**When:** {event_time.strftime('%A, %B %d at %H:%M')}")
                time_until = event_time - datetime.now()
                if time_until.days > 0:
                    st.write(f"**In:** {time_until.days} days, {time_until.seconds//3600} hours")
                else:
                    st.write(f"**In:** {time_until.seconds//3600}h {(time_until.seconds%3600)//60}m")
            
            details = []
            if 'duration' in event: details.append(f"Duration: {event['duration']}")
            if 'max_altitude' in event: details.append(f"Altitude: {event['max_altitude']}°")
            if 'zhr' in event: details.append(f"Rate: {event['zhr']}/hr")
            if details: st.write(" • ".join(details))
        
        with col2:
            if st.button("Notify", key=f"notify_{event['event']}", use_container_width=True):
                self.notifier.send_alerts(event)
        st.markdown('</div>', unsafe_allow_html=True)
    
    def run(self):
        self.initialize_session_state()
        if not st.session_state.authenticated:
            self.show_login_page()
        else:
            self.show_location_selector()
            self.show_user_dashboard()

# Run the application
if __name__ == "__main__":
    app = StellarWatchApp()
    app.run()