# gym_mangament


## Backend Implementation

This project involves creating a backend system to manage user accounts and send notifications for payment dues. Here's a brief explanation of how the backend works and the functions provided.

### Backend Structure

The backend is implemented in Python and uses JSON files for data storage. The following functions are provided:

1. **load_data(filename):** Loads user data from a JSON file.
2. **save_data(data, filename):** Saves user data to a JSON file.
3. **is_valid_email(email):** Validates email addresses (custom logic can be implemented).
4. **is_valid_phone(phone):** Validates phone numbers (custom logic can be implemented).
5. **send_sms(api_key, to, message):** Sends SMS messages using the Twilio API.
6. **send_email(subject, message, to, from_email, password):** Sends email using SMTP (credentials need to be set up).
7. **create_account(data, unique_id, username, gmail, phone_no, total_money):** Creates a new user account.
8. **check_account(data, unique_id):** Checks account details of a user using their unique ID.
9. **deposit_account(data, unique_id, amount):** Deposits money for a service into a user's account.
10. **delete_account(data, unique_id):** Deletes a user account.
11. **send_payment_due_notifications(data, api_key_twilio, api_key_smtp, smtp_email, smtp_password):** Sends payment due notifications to users.

### Example Usage

You can use these functions to manage user accounts, deposit money, and send payment due notifications. The provided script demonstrates how to interact with these


### Detailed explantion
implement functions to check account details  register new user with unique id , phone number , gmail  , date of registration and deposit log list which have date of payment  and  amount.  . you have to get some api . it is for sending sms you can use twilio api and use smptlib  api for sending email . get api keys of both . you can send sms and email when the last transaction  month and current month gap difference  is greater than 0 send sms and gmail about payment dues also create a function to delete user account when needed you can delete user. for storing data you can use .json file format . for large user base you can use sql database But for know 100 to 200 people json file format is good to go. Use python twilio.client  library to send msg on whatsapp msg get  api  key from twilio website  ...
json data register format for each user

# Json data format

```
/ unique id
"672": 

   {  "username": "client_name",

      "account_created": "2023-06-16 16:06:57",

      "gmail":"client_gmail", 

     "phone_no":"client_phone_no",

     "total_money": 124,

// transaction log  ["date_of_deposit amount"]

     "transaction_date": ["2023-06-16 4","2023-06-19 10","T 2023-06-19 10","2023-07-08 1000","2023-07-08  1000","2023-07-08 2000","2023-08-22 100"]}

} ```


