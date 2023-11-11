from setting import change_enviro
import smtplib
import ssl
from twilio.rest import Client
import os 
from dotenv import load_dotenv

# Download the helper library from https://www.twilio.com/docs/python/install

if not os.path.exists('.env'):
   change_enviro()

load_dotenv()

SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

SMS_ACCOUNT_SID = os.getenv("SMS_ACCOUNT_SID")
SMS_AUTH_TOKEN = os.getenv("SMS_AUTH_TOKEN")

WHATSAPP_ACCOUNT_SID = os.getenv("WHATSAPP_ACCOUNT_SID")
WHATSAPP_AUTH_TOKEN = os.getenv("WHATSAPP_AUTH_TOKEN")

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")

PHONE=os.getenv("PHONE")



def send_whatsapp_msg(name:str , amount:int , to_phone_no:str):
   # Find your Account SID and Auth Token at twilio.com/console
   # and set the environment variables. See http://twil.io/secure
   try:
      client = Client(WHATSAPP_ACCOUNT_SID, WHATSAPP_AUTH_TOKEN)
      message = client.messages.create(
            body=f"Dear {name}, gym member, your payment is overdue {amount}. Please make a payment as soon as possible.",
            from_=f'whatsapp:+91{PHONE}',
            to=f'whatsapp:+91{to_phone_no}',
      )
      print(f"Message sent with SID: {message.sid}")
      return True 
   except Exception as e:
      print(f"An error occurred: {str(e)}")
   return False 

def send_sms(name:str , amount:int , to_phone_number:str) -> bool:
   # ## Your Twilio Account SID and Auth Token
   # account_sid = "your_account_sid"
   # ## Your token
   # auth_token = "your_auth_token"

   # Initialize the Twilio client
   client = Client(SMS_ACCOUNT_SID, SMS_AUTH_TOKEN)

   try:
      # Compose the SMS message
      message_body = f"Dear {name}, gym member, your payment is overdue {amount}. Please make a payment as soon as possible."

      # Send the SMS
      message = client.messages.create(
            body=message_body,
            from_=PHONE,
            to=to_phone_number
      )

      print(f"Message sent to {to_phone_number}: {message.sid}")
      return True
   except Exception as e:
      print(f"Error sending message: {str(e)}")
   return False


def send_email(name:str,email:str ,id:str,amount:int,receiver_email:str):
   email_content = '''
   Subject: Payment Request

   Dear {name},

   We kindly request you to make a payment of ${amount} for your bill.
   Your ID: {id}

   Please remit the payment at your earliest convenience.

   Thank you for your prompt attention to this matter.

   Sincerely,
   fit me
   '''
 
   email_content.format(name=name, amount=amount, id=id)
   port = 587  # For starttls
   smtp_server = "smtp.gmail.com"
   
   ## Your email
   #sender_email = ""
   
   # check is email adress valid 
   
      #receiver_email = "parimalsamrat1234@gmail.com"
   try:
      ## password
      #password=""
      #password = input("Type your password and press enter:")
      context = ssl.create_default_context()
      with smtplib.SMTP(smtp_server, port) as server:
         server.ehlo()  # Can be omitted
         server.starttls()
         server.ehlo()  # Can be omitted
         server.login(EMAIL_ADDRESS, SMTP_PASSWORD)
         server.sendmail(EMAIL_ADDRESS, receiver_email, email_content)
         print(f"Email send succesfully to {name}...")
         return True
   except Exception as e:
      print(f"Error sending email: {str(e)}")
   return False 
