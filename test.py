from twilio.rest import Client

account_sid = 'AC9d6692f5602687cdb3234d3e6572c3e0'
auth_token = 'f281a5d3275a2f62013b5f3f1e97d025'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='whatsapp:+14155238886',
  body='Your appointment is coming up on July 21 at 3PM',
  to='whatsapp:+5215564779982'
)

print(message.sid)