import os

def change_enviro() -> None:

   # Prompt the user for input
   email_address = input("Enter your Email Address: ")
   phone_no = input("Enter your phone no: ")
   smtp_password = input("Enter your SMTP Password: ")
   sms_account_sid = input("Enter your SMS Account SID: ")
   sms_auth_token = input("Enter your SMS Auth Token: ")
   whatsapp_account_sid = input("Enter your WhatsApp Account SID: ")
   whatsapp_auth_token = input("Enter your WhatsApp Auth Token: ")
   charger = input("Your service charge: ")

      # Update the environment variables
   os.environ["EMAIL_ADDRESS"] = email_address
   os.environ["PHONE_NO"] = phone_no
   os.environ["SMTP_PASSWORD"] = smtp_password
   os.environ["SMS_ACCOUNT_SID"] = sms_account_sid
   os.environ["SMS_AUTH_TOKEN"] = sms_auth_token
   os.environ["WHATSAPP_ACCOUNT_SID"] = whatsapp_account_sid
   os.environ["WHATSAPP_AUTH_TOKEN"] = whatsapp_auth_token
   os.environ["CHARGE"] = charger
   os.environ["FLAG"] = 'True'
      # Save the changes to the .env file
   with open(".env", "w") as env_file:
      for key, value in os.environ.items():
         env_file.write(f"{key}={value}\n")
      print("Environment variables updated and saved in .env file.")
   return 
