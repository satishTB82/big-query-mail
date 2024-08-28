import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Replace these with your actual details
smtp_server = "smtp.office365.com"
smtp_port = 587
username = "your_email@example.com"
password = "your_password"

def send_email():
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = "recipient@example.com"  # Replace with the recipient's email address
    msg['Subject'] = "HTML Email Test"

    # Define the HTML content
    html_content = """
    <html>
    <body>
        <h1 style="color:blue;">Hello from Python</h1>
        <p>This is a test email sent using SMTP with password authentication.</p>
        <p><b>Enjoy coding!</b></p>
    </body>
    </html>
    """
    msg.attach(MIMEText(html_content, 'html'))

    # Connect to the SMTP server
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
        server.login(username, password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    send_email()
