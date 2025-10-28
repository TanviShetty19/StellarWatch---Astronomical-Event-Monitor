import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
import json
from event_detector import AstronomicalEventDetector
from config import *

class NotificationEngine:
    def __init__(self):
        self.detector = AstronomicalEventDetector()
        self.sent_alerts = set()  # Track alerts we've already sent
        
    def should_send_alert(self, event):
        """Check if we should send an alert for this event"""
        # Create a unique identifier for this event
        event_id = f"{event['event']}_{event.get('time', event.get('peak', ''))}"
        
        # Don't send duplicate alerts
        if event_id in self.sent_alerts:
            return False
            
        # Check if event is within alert window
        event_time = event.get('time') or event.get('peak')
        if isinstance(event_time, str):
            return True
            
        time_until_event = event_time - datetime.now()
        return time_until_event <= timedelta(minutes=ALERT_WINDOW)
    
    def format_alert_message(self, event):
        """Create a user-friendly alert message"""
        event_type = event['event']
        
        if 'ISS' in event_type:
            return f"🚀 ISS VISIBLE TONIGHT!\n\nLook {event.get('direction', 'up')} at {event.get('time').strftime('%H:%M')} for {event.get('duration', '5-6 minutes')}. Maximum altitude: {event.get('max_altitude', 0)}°. {event.get('brightness', 'Very bright')}!"
        
        elif 'Meteor' in event_type:
            return f"🌠 METEOR SHOWER ALERT!\n\n{event['event']} peaks {event.get('peak').strftime('%b %d')}. Expected rate: {event.get('zhr', 0)} meteors/hour. Moon phase: {event.get('moon_phase', 'Good')}. Visibility: {event.get('visibility', 'Good')}."
        
        elif 'Aurora' in event_type:
            return f"🌌 AURORA POSSIBILITY!\n\nChance to see northern lights tonight! KP Index: {event.get('kp_index', 0)}. Best viewing: {event.get('best_time', 'midnight-3am')}."
        
        elif 'Launch' in event_type:
            return f"🚀 ROCKET LAUNCH!\n\n{event['event']} scheduled for {event.get('time').strftime('%H:%M UTC')}. Mission: {event.get('mission', 'Unknown')}."
        
        else:
            return f"🔭 ASTRONOMICAL EVENT!\n\n{event['event']} happening soon!"
    
    def send_console_alert(self, event):
        """Send alert to console (for testing)"""
        message = self.format_alert_message(event)
        print("\n" + "="*50)
        print("🔔 ASTRONOMICAL ALERT!")
        print("="*50)
        print(message)
        print("="*50 + "\n")
        
        # Mark as sent
        event_id = f"{event['event']}_{event.get('time', event.get('peak', ''))}"
        self.sent_alerts.add(event_id)
    
    def check_and_alert(self, location_name='bangalore'):
        """Check for events and send alerts"""
        print(f"🔍 Checking for events in {location_name}...")
        events = self.detector.get_all_events(location_name)
        
        alerts_sent = 0
        for event in events:
            if self.should_send_alert(event):
                self.send_console_alert(event)
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
    print("-" * 50)
    
    # Initial check
    engine.check_and_alert('bangalore')
    
    # Instructions for continuous monitoring
    print("\n💡 To run continuously, we'll set up a scheduler in the next task!")
    print("📱 Next: We'll add Telegram/SMS notifications and a web dashboard!")

if __name__ == "__main__":
    main()