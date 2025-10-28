import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class EmailNotifier:
    def __init__(self):
        self.test_mode = os.getenv('EMAIL_TEST_MODE', 'True').lower() == 'true'
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.sender_email = os.getenv('SENDER_EMAIL', '')
        self.sender_password = os.getenv('SENDER_PASSWORD', '')
        
    def send_alert(self, recipient, subject, message):
        """Send email alert with real SMTP or console fallback"""
        if self.test_mode or not all([self.sender_email, self.sender_password]):
            # Test mode - print to console
            print(f" EMAIL ALERT (Test Mode)")
            print(f"   To: {recipient}")
            print(f"   Subject: {subject}")
            print(f"   Message: {message}")
            print("-" * 50)
            return True
        
        try:
            # Real email sending
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient
            msg['Subject'] = subject
            
            # Create HTML email
            html_content = f"""
            <html>
                <body style="font-family: Arial, sans-serif; background: linear-gradient(135deg, #0c0c2e 0%, #1a1a3e 100%); color: white; padding: 20px;">
                    <div style="max-width: 600px; margin: 0 auto; background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; backdrop-filter: blur(10px);">
                        <h1 style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center;">
                            🔭 StellarWatch Alert
                        </h1>
                        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px 0;">
                            {message.replace('\n', '<br>')}
                        </div>
                        <p style="text-align: center; color: #a0a0c0; font-size: 12px;">
                            Sent from StellarWatch Astronomical Monitoring System
                        </p>
                    </div>
                </body>
            </html>
            """
            
            msg.attach(MIMEText(html_content, 'html'))
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            
            print(f" Email sent successfully to {recipient}")
            return True
            
        except Exception as e:
            print(f" Failed to send email: {e}")
            # Fallback to console
            print(f" FALLBACK ALERT for {recipient}: {subject}")
            return False

# Global instance
email_notifier = EmailNotifier()