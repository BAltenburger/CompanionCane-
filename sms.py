from twilio.rest import Client

def sms(message):
    account_sid = 'ACc311cdf474fb9bad277dfb2bf1872ed0'
    auth_token = '436c27e335f9febebe8860848e53a366'
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body=message,
                        from_='+15204127054',
                        to=str(open("emergency_contacts1.txt", "r").read())
                        )
    message2 = client.messages \
                    .create(
                        body = message,
                        from_='+15204127054',
                        to=str(open("physician_contact.txt", "r").read())
                        )
    message
    message2
