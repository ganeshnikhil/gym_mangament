import json
from datetime import datetime
import random
from prettytable import PrettyTable
import os
import re 
import smtplib, ssl
from twilio.rest import Client
from requests import post 



PATH = "gym_info.json"
CHARGE=1000
PHONE="+91"

def is_valid_email(string):
   binary_pattern=re.compile(r"^[a-zA-Z0-9_.+-]+@gmail.com$")
   return bool(binary_pattern.match(string))

def is_valid_phone_number(phone_number):
   pattern = r'^[1-9]\d{9}$'
   return bool(re.match(pattern, phone_number))
# Download the helper library from https://www.twilio.com/docs/python/install


def send_whatsapp_msg(name:str , amount:int , to_phone_no:str):
   # Find your Account SID and Auth Token at twilio.com/console
   # and set the environment variables. See http://twil.io/secure
   try:
      ## Your Twilio Account SID and Auth Token
      account_sid = ""
      ## Your token
      auth_token = ""
      
      client = Client(account_sid, auth_token)
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
   ## Your Twilio Account SID and Auth Token
   account_sid = "your_account_sid"
   ## Your token
   auth_token = "your_auth_token"
   ## Your Twilio phone number
   from_phone_number = PHONE

   # Initialize the Twilio client
   client = Client(account_sid, auth_token)

   try:
      # Compose the SMS message
      message_body = f"Dear {name}, gym member, your payment is overdue {amount}. Please make a payment as soon as possible."

      # Send the SMS
      message = client.messages.create(
            body=message_body,
            from_=from_phone_number,
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
   sender_email = ""
   
   # check is email adress valid 
   if is_valid_email(receiver_email) and is_valid_email(sender_email):
      #receiver_email = "parimalsamrat1234@gmail.com"
      try:
         ## password
         password=""
         #password = input("Type your password and press enter:")
         context = ssl.create_default_context()
         with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls()
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, email_content)
            print(f"Email send succesfully to {name}...")
            return True
      except Exception as e:
         print(f"Error sending email: {str(e)}")
   else:
      print("Invalid email adress...")
   return False 


def month_gap(given_date:str) -> int:
   given_date_obj = datetime.strptime(given_date, "%Y-%m-%d")
   # Get the current date and time
   current_date = datetime.now().date()
   # Calculate the difference in months
   months_passed = (current_date.year - given_date_obj.year) * 12 + (current_date.month - given_date_obj.month)
   return  months_passed


def load_data():
   with open(PATH, "r") as f:
      return json.load(f)

def save_data(data):
   with open(PATH, "w") as f:
      json.dump(data, f, indent=4)



def check_account():
   id_no = input("Enter your ID: ")
   data = load_data()

   if id_no not in data:
      print("[+] This account doesn't exist")
      return
   
   account = data[id_no]
   print("\n")
   print(f"ID: {id_no}")
   print(f"NAME: {account['username']}")
   print(f"PHONE NO: {account['phone_no']}")
   print(f"GMAIL: {account['gmail']}")
   print(f"DATE AND TIME OF CREATION: {account['account_created']}")
   print(f"AMOUNT: {account['total_money']}")

   table = PrettyTable()
   table.field_names = [ "Date", "Amount"]
   table.align = "r"
   table.align["Type"] = "l"
   table.align["ID"] = "l"
   
   transaction_dates = account["transaction_date"]
   
   print("\n")
   if len(transaction_dates) != 0:
      for dtime in transaction_dates:
         data = dtime.split()
         table.add_row(data)
      print(table)
   else:
      print("[+] No withdrawals, transactions, or deposits have been made for this account.")



def deposit_account():
   id_no = input("Enter your ID: ")
   data = load_data()

   if id_no not in data:
      print("[+] This account doesn't exist")
      return

   amount = int(input("[=] Enter the amount: "))
   
   account = data[id_no]
   account["total_money"] += amount
   account["transaction_date"].append(f"{datetime.now():%Y-%m-%d} {amount}")

   save_data(data)
   
   print(f"[+] {account['username']} deposited {amount} to the account")


def delete_account():
   id_no = input("Enter your ID: ")
   data = load_data()

   if id_no not in data:
      print("[+] This account doesn't exist")
      return

   username = data[id_no]["username"]
   del data[id_no]

   save_data(data)
   print(f"[+] {username} has been deleted from the gym_info")


def create_account():
   data = load_data()

   id_no = random.randint(100, 999)
   name = input("Enter your name: ")
   
   while not is_valid_phone_number(phone_no:=input("Phone no: ")):
      print("[-] Invalid phone no: ")
      phone_no = input("Phone No: ")
   
   while not is_valid_email(gmail_adress:= input("Gmail: ")):
      print("[-] Invalid emali adress..")
      gmail_adress=input("Gmail: ")
      
   amount = int(input("[=] Enter initial amount: "))
   
   while str(id_no) in data:
      id_no = random.randint(100, 999)
   
   account = {
      "username": name,
      "account_created": f"{datetime.now():%Y-%m-%d %I:%M:%S%p}",
      "phone_no":f"+91{phone_no}",
      "gmail":gmail_adress,
      "total_money": amount,
      "transaction_date": [f"{datetime.now():%Y-%m-%d} {amount}"]
   }

   data[str(id_no)] = account

   save_data(data)

   print(f"[+] Your username is: {name}")
   print(f"[+] Your Account ID is: {id_no}")


def send_message():
   data = load_data()
   if data:
      for id_no in data:
         account = data[id_no]
         transaction_dates = account["transaction_date"]
         
         if len(transaction_dates) != 0:
            last_transaction_date = transaction_dates[-1].split()[0]
            gap = month_gap(last_transaction_date)
            
            if gap > 0:
               name = account['username']
               id = id_no
               email = account['gmail']
               phone_no=account['phone_no']
               amount = gap * CHARGE
               
               if send_email(name , id , amount , email):
                  print(f"{name} , {id} is emailed about his due..")
               else:
                  print(f"{name} , {id}  email notification falied..")
               
               if send_sms(name , amount , phone_no):
                  print(f"{name} , {id} is sms about his due..")
               else:
                  print(f"{name} , {id} sms  notification falied..")
               
               if send_whatsapp_msg(name , amount , phone_no):
                  print(f"{name} , {id} is whatsapped  msg  about his due..")
               else:
                  print(f"{name} , {id} whahtsapp msg notification falied..")
   else:
      print("[+] No members registerd currently..")
   return None
            
     
def main():
   
   if not os.path.exists(PATH):
      with open(PATH, "w") as file:
            file.write("{}")
            
   print('''
   [1.] Create account: create a new account
   [2.] Check account: check the balance of an account
   [3.] Deposit account: deposit money into an account
   [4.] Delete account: delete an account
   [5.] Send Message: send notification tol all due accounts
   ''')

   user = int(input('[*] Enter your option: '))
   
   if user == 1:
      create_account()
      
   elif user == 2:
      check_account()
   elif user == 3:
      deposit_account()
   elif user == 4:
      delete_account()
   elif user == 5:
      send_message()
   else:
      print("[-] Invalid option.")


if __name__ == "__main__":
   main()


