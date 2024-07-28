from Google import Create_Service
import base64
from email import message_from_bytes
from datetime import datetime, timedelta
import time
from message import Message
from twilio.rest import Client

account_sid = 'AC9d6692f5602687cdb3234d3e6572c3e0'
auth_token = '4bc0009693d0569733a9d9e2cd11dc54'
client = Client(account_sid, auth_token)

CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

def initialize_service():
    return Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

def send_message(sender, body, date):
    msg = f'*RECORDATORIO*\n\n*De:* {sender}\n*Hora:* {date}\n\n{body}'
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=msg,
        to='whatsapp:+5215564779982'
    )

def get_unix_time_range(hours):
    now = datetime.now()
    past_time = now - timedelta(hours=hours)
    now_unix = int(time.mktime(now.timetuple()))
    past_time_unix = int(time.mktime(past_time.timetuple()))
    return past_time_unix, now_unix

def construct_query(user_email, past_time_unix, now_unix):
    return f'from:{user_email} after:{past_time_unix} before:{now_unix}'

def fetch_messages(service, user_id, query):
    results = service.users().messages().list(userId=user_id, labelIds=['INBOX'], q=query).execute()
    return results.get('messages', [])

def process_and_send_messages(service, messages):
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        message_timestamp = int(msg['internalDate']) / 1000
        msg_date = datetime.fromtimestamp(message_timestamp)
        message_data = base64.urlsafe_b64decode(msg['payload']['parts'][0]['body']['data']).decode('utf-8')
        email_message = message_from_bytes(message_data.encode('utf-8'))
        msg_body = email_message.get_payload().strip()
        msg_sender = msg['payload']['headers'][16]['value'].split('<')[0].strip().replace('"', '')
        send_message(msg_sender, msg_body, msg_date)

def main():
    service = initialize_service()
    user_email = 'sangom2902@gmail.com'
    
    while True:
        past_time_unix, now_unix = get_unix_time_range(1)
        query = construct_query(user_email, past_time_unix, now_unix)
        messages = fetch_messages(service, 'me', query)
        
        if messages:
            process_and_send_messages(service, messages)
        
        time.sleep(3600)

if __name__ == "__main__":
    main()
