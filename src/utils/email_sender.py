import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_interview_email(to_email, candidate_name, vacancy_title, company_name="Ledgerly Invoices"):
    """Send interview invitation email."""
    
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = "587"
    SMTP_USERNAME = "testme8910@gmail.com"
    SMTP_PASSWORD = "nwrw qihs muwi xzxa"
    
    subject = f"Interview Invitation - {vacancy_title}"
    body = f"""
    Dear {candidate_name},

    Thank you for applying for the {vacancy_title} position at {company_name}.

    We are pleased to inform you that your application has been shortlisted. We would like to invite you for an interview.

    Please reply to this email to confirm your availability for the next week.

    Best regards,
    {company_name} HR Team
    """
    
    try:
        # Create email
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False
    