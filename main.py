import json
import os 
from datetime import datetime
import random
from prettytable import PrettyTable

from send_msg import send_whatsapp_msg , send_sms , send_email
from isauthentic import is_valid_email , is_valid_phone_no

#global variables 
CHARGE=1000
PATH = "db.json"

def load_data():
   with open(PATH, "r") as f:
      return json.load(f)

def save_data(data):
   with open(PATH, "w") as f:
      json.dump(data, f, indent=4)

def month_gap(given_date:str) -> int:
   given_date_obj = datetime.strptime(given_date, "%Y-%m-%d")
   # Get the current date and time
   current_date = datetime.now().date()
   # Calculate the difference in months
   months_passed = (current_date.year - given_date_obj.year) * 12 + (current_date.month - given_date_obj.month)
   return  months_passed

def distribute_amount(total_amount:int) -> list:
   today=datetime.now().date()
   log_list = [f"{today} {CHARGE}"]
   no_of_months=total_amount // CHARGE
   # if he paid for more then one month
   if no_of_months > 1:
      for i in range(no_of_months):
         if today.month == 12:
            today = today.replace(year=today.year + 1, month=1)
         else:
            today = today.replace(month=today.month + 1)
            
         log_list.append(f"{today} {CHARGE}")
   return log_list


def check_account(id_no:str):
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
      print("[+] No deposits have been made in this account.")



def deposit_account(id_no:str , amount:int):
   data = load_data()

   if id_no not in data:
      print("[+] This account doesn't exist")
      return

   account = data[id_no]
   account["total_money"] += amount
   
   log_list = distribute_amount(amount)
   for transaction_detail in log_list:
      account["transaction_date"].append(transaction_detail)

   save_data(data)
   
   print(f"[+] {account['username']} deposited {amount} to the account")


def delete_account(id_no:str):
   data = load_data()

   if id_no not in data:
      print("[+] This account doesn't exist")
      return

   username = data[id_no]["username"]
   del data[id_no]

   save_data(data)
   print(f"[+] {username} with id {id_no} has been deleted from the Register")


def create_account(name:str , phone_no:str , gmail_adress:str , amount:int)->bool:
   data = load_data()

   id_no = random.randint(100, 999)
   
   log_list=distribute_amount(amount)
   
   while str(id_no) in data:
      id_no = random.randint(100, 999)
   
   account = {
      "username": name,
      "account_created": f"{datetime.now():%Y-%m-%d %I:%M:%S%p}",
      "phone_no":f"+91{phone_no}",
      "gmail":gmail_adress,
      "total_money": amount,
      "transaction_date": log_list
   }

   data[str(id_no)] = account

   save_data(data)

   print(f"[+] Your username is: {name}")
   print(f"[+] Your Account ID is: {id_no}")
   return True

def send_message():
   data = load_data()
   if data:
      for id_no in data:
         account = data[id_no]
         transaction_dates = account["transaction_date"]
         
         if len(transaction_dates) != 0:
            last_transaction = transaction_dates[-1].split()
            
            last_transaction_date= last_transaction[0]
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
      name = input("Enter your name: ")
      
      while not is_valid_phone_no(phone_no:=input("Phone no: ")):
         print("[-] Invalid phone no: ")
         phone_no = input("Phone No: ")
   
      while not is_valid_email(gmail_adress:= input("Gmail: ")):
         print("[-] Invalid emali adress..")
         gmail_adress=input("Gmail: ")

      amount = int(input("[=] Enter initial amount: "))
      if amount >= CHARGE:
         create_account(name , phone_no , gmail_adress , amount)
      else:
         print(f"{amount} is less than {CHARGE}")

   elif user == 2:
      id_no= input("ID NO: ")
      check_account(id_no)
      
   elif user == 3:
      id_no = input("Id NO: ")
      amount = int(input("Amount: "))
      if amount >= CHARGE:
         deposit_account(id_no,amount)
      else:
         print(f"{amount} is less than {CHARGE}")
      
   elif user == 4:
      id_no = input("Id NO: ")
      delete_account(id_no)
      
   elif user == 5:
      send_message()
   else:
      print("[-] Invalid option.")


if __name__ == "__main__":
   main()


