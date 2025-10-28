import schedule
import time
import threading
from datetime import datetime
from notification_engine import NotificationEngine
from config import CHECK_INTERVAL
import streamlit as st

class MonitoringScheduler:
    def __init__(self):
        self.notifier = NotificationEngine()
        self.is_running = False
        self.scheduler_thread = None
        
    def start_monitoring(self, locations=None):
        """Start the background monitoring scheduler"""
        if locations is None:
            locations = ['bangalore', 'new_york', 'london']
        
        self.is_running = True
        
        # Schedule regular checks
        schedule.every(CHECK_INTERVAL).seconds.do(self.check_all_locations, locations)
        
        # Start scheduler in background thread
        self.scheduler_thread = threading.Thread(target=self.run_scheduler)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        
        print(f" Monitoring scheduler started for {locations}")
    
    def stop_monitoring(self):
        """Stop the monitoring scheduler"""
        self.is_running = False
        schedule.clear()
        print(" Monitoring scheduler stopped")
    
    def run_scheduler(self):
        """Run the scheduler in a separate thread"""
        while self.is_running:
            schedule.run_pending()
            time.sleep(1)
    
    def check_all_locations(self, locations):
        """Check all specified locations for events"""
        print(f" Scheduled check at {datetime.now()}")
        
        for location in locations:
            try:
                alerts_sent = self.notifier.check_and_alert(location)
                if alerts_sent > 0:
                    print(f" Sent {alerts_sent} alerts for {location}")
            except Exception as e:
                print(f" Error checking {location}: {e}")
    
    def get_scheduler_status(self):
        """Get current scheduler status"""
        return {
            'is_running': self.is_running,
            'next_run': schedule.next_run() if schedule.jobs else None,
            'job_count': len(schedule.jobs)
        }

# Global scheduler instance
monitoring_scheduler = MonitoringScheduler()