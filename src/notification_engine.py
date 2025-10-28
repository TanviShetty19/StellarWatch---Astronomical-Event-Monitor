import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
import json

# Import config first
try:
    from config import *
except ImportError:
    # Fallback config
    ALERT_WINDOW = 60

# Import other modules with error handling
try:
    from src.event_detector import AstronomicalEventDetector
    from src.email_notifier import email_notifier
except ImportError:
    # Fallback for direct execution
    try:
        from event_detector import AstronomicalEventDetector
        from email_notifier import email_notifier
    except ImportError:
        # Create fallback classes
        class AstronomicalEventDetector:
            def get_all_events(self, location):
                return []
        
        class EmailNotifier:
            def send_alert(self, recipient, subject, message):
                print(f"Email alert: {subject}")
        
        email_notifier = EmailNotifier()

class NotificationEngine:
    def __init__(self):
        self.detector = AstronomicalEventDetector()
        self.sent_alerts = set()  # Track alerts we've already sent
        
    def should_send_alert(self, event):
        """Check if we should send an alert for this event"""
        # Create a unique identifier for this event
        event_time = event.get('time') or event.get('peak')
        event_id = f"{event['event']}_{event_time}"
        
        # Don't send duplicate alerts
        if event_id in self.sent_alerts:
            return False
            
        # Check if event is within alert window (for time-based events)
        if isinstance(event_time, datetime):
            time_until_event = event_time - datetime.now()
            return time_until_event <= timedelta(minutes=ALERT_WINDOW)
        
        # For events without specific times, always alert
        return True
    
    def format_alert_message(self, event):
        """Create a user-friendly alert message"""
        event_type = event['event']
        
        if 'ISS' in event_type:
            event_time = event.get('time', datetime.now())
            if isinstance(event_time, datetime):
                time_str = event_time.strftime('%H:%M')
            else:
                time_str = str(event_time)
                
            return f"""
🚀 INTERNATIONAL SPACE STATION PASSING OVERHEAD!

Look {event.get('direction', 'up')} at {time_str} for {event.get('duration', '5-6 minutes')}. 
Maximum altitude: {event.get('max_altitude', 0)}°. 
Brightness: {event.get('brightness', 'Very bright')}

Perfect viewing conditions tonight! The ISS will be clearly visible moving across the sky.
"""
        
        elif 'Meteor' in event_type:
            peak_time = event.get('peak', datetime.now())
            if isinstance(peak_time, datetime):
                peak_str = peak_time.strftime('%B %d at %H:%M')
            else:
                peak_str = str(peak_time)
                
            return f"""
🌠 METEOR SHOWER ALERT!

{event['event']} peaks on {peak_str}.
Expected rate: {event.get('zhr', 0)} meteors per hour under ideal conditions.
Moon Phase: {event.get('moon_phase', 'Favorable')}
Visibility: {event.get('visibility', 'Good')}

Find a dark location away from city lights for best viewing!
"""
        
        elif 'Aurora' in event_type:
            return f"""
🌌 NORTHERN LIGHTS POSSIBILITY!

There's a chance to see aurora tonight!
KP Index: {event.get('kp_index', 0)}
Best viewing time: {event.get('best_time', 'midnight to 3 AM')}
Visibility: {event.get('visibility', 'Possible with dark skies')}

Look toward the northern horizon from dark locations.
"""
        
        elif 'Launch' in event_type:
            launch_time = event.get('time', datetime.now())
            if isinstance(launch_time, datetime):
                time_str = launch_time.strftime('%B %d at %H:%M UTC')
            else:
                time_str = str(launch_time)
                
            return f"""
🚀 ROCKET LAUNCH ALERT!

{event['event']} scheduled for {time_str}
Mission: {event.get('mission', 'Unknown')}
Launch Site: {event.get('location', 'Unknown')}

Watch live streams online for this exciting launch!
"""
        
        else:
            return f"""
🔭 ASTRONOMICAL EVENT ALERT!

{event['event']} is happening soon!

Check your astronomy apps for detailed viewing information.
"""
    
    def send_alerts(self, event):
        """Send both console and email alerts"""
        message = self.format_alert_message(event)
        
        # Console alert
        print("\n" + "="*60)
        print("🔔 ASTRONOMICAL ALERT!")
        print("="*60)
        print(message)
        print("="*60 + "\n")
        
        # Email alert (to test email - you can change this)
        test_email = "user@example.com"
        subject = f"🔭 Alert: {event['event']}"
        email_notifier.send_alert(test_email, subject, message)
        
        # Mark as sent
        event_time = event.get('time') or event.get('peak')
        event_id = f"{event['event']}_{event_time}"
        self.sent_alerts.add(event_id)
    
    def check_and_alert(self, location_name='bangalore'):
        """Check for events and send alerts"""
        print(f"🔍 Checking for events in {location_name}...")
        events = self.detector.get_all_events(location_name)
        
        alerts_sent = 0
        for event in events:
            if self.should_send_alert(event):
                self.send_alerts(event)
                alerts_sent += 1
        
        if alerts_sent == 0:
            print("✅ No new alerts at this time.")
        else:
            print(f"✅ Sent {alerts_sent} alert(s)!")
        
        return alerts_sent

def main():
    """Run the notification engine"""
    engine = NotificationEngine()
    
    print("🛰️ Starting Astronomical Event Notifier...")
    print("📍 Monitoring: Bangalore, India")
    print("⏰ Check interval: Every 5 minutes")
    print("🔔 Alert window: 60 minutes before event")
    print("📧 Email notifications: ENABLED (test mode)")
    print("-" * 50)
    
    # Initial check
    engine.check_and_alert('bangalore')

if __name__ == "__main__":
    main()