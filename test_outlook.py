import requests

# Replace these variables with your values
client_id = 'YOUR_APPID'
client_secret = 'YOUR_APPSECRET'
scope = "https://graph.microsoft.com/User.Read https://graph.microsoft.com/Mail.Send"

def get_access_token():
    """Get an access token from Microsoft Identity Platform"""
    token_url = f'https://login.microsoftonline.com/common/oauth2/v2.0/token'
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': scope
    }
    token_r = requests.post(token_url, data=token_data)
    if token_r.status_code == 200:
        return token_r.json().get('access_token')
    else:
        raise Exception(f"Error getting access token: {token_r.status_code}, {token_r.text}")

def send_email(access_token):
    """Send an email using Microsoft Graph API"""
    email_endpoint = 'https://graph.microsoft.com/v1.0/me/sendMail'
    email_headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    email_data = {
        'message': {
            'subject': 'Hello from Python',
            'body': {
                'contentType': 'Text',
                'content': 'This is a test email sent using Microsoft Graph API.'
            },
            'toRecipients': [
                {
                    'emailAddress': {
                        'address': 'recipient@example.com'
                    }
                }
            ]
        }
    }
    email_r = requests.post(email_endpoint, headers=email_headers, json=email_data)
    if email_r.status_code == 202:
        print('Email sent successfully')
    else:
        print(f'Error sending email: {email_r.status_code}, {email_r.text}')

def main():
    """Main function to authenticate and send email"""
    try:
        access_token = get_access_token()
        # send_email(access_token)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
