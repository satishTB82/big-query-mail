import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader

# Email server setup
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_user = 'satish.prajapati@tecblic.com'
smtp_password = 'lxkb iwju qvpy vhmd'

def send_email(to_email, subject, html_body):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the HTML body
    msg.attach(MIMEText(html_body, 'html'))

    # Send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Upgrade to a secure connection
        server.login(smtp_user, smtp_password)
        server.send_message(msg)

# Data provided
data = {
    'askId': 'UHGWM110-000305',
    'no_of_apis': 83,
    'gateway_distribution': 'mcg0 stargate40 azure0',
    'val': 'High Performing API :43 Medium Performing API :13 Medium Performing API :27',
    'NumberOfConsumer': 2289,
    'recommendation': '1) 15 no activity APIs can be considered for decommission. 2) 27 APIs require immediate attention as their performance is Inadequate. 3) Gateway timeouts of [10] of your APIs are way higher than actual. Consider reducing the timeout. 4) 0 API are in Non-compliant Gateway. Consider moving them to MCG.',
    'service_owner': "Balamukundan",
    'monthly_transaction_volume': '1.04B (^10% MoM)',
    'no_of_consuming_apps': 25,
    'no_of_noncompliant_gateways': 1
}

# Split and prepare data for the template
data['val_lines'] = data['val'].split('Medium Performing API :')  # Adjust split logic as needed
data['recommendations'] = [rec.strip() for rec in data['recommendation'].split(')') if rec.strip()]
data['month'] = "July"

# Set up Jinja2 environment and load the template
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('email_template.html')

# Render the template with the data
html_body = template.render(data)

# Example: Sending the email
send_email('shreshangthakor.tecblic@gmail.com', f"API Performance Report - {data['askId']}", html_body)