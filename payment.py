from requests import post 
import json 
# Set your PayPal API credentials and the base URL (use the sandbox URL for testing)
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
base_url = "https://api-m.sandbox.paypal.com"

# Function to obtain an access token
def get_access_token():
   auth_url = f"{base_url}/v1/oauth2/token"
   headers = {
      "Content-Type": "application/x-www-form-urlencoded",
   }
   data = {
      "grant_type": "client_credentials",
   }
   response = post(auth_url, headers=headers, data=data, auth=(client_id, client_secret))
   response_data = response.json()
   return response_data.get("access_token")

# Function to create a payment request
def create_payment_request(access_token):
   payment_url = f"{base_url}/v2/checkout/orders"
   headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {access_token}",
   }
   data = {
      "intent": "CAPTURE",
      "purchase_units": [
            {
               "amount": {
                  "currency_code": "USD",
                  "value": "10.99",
               }
            }
      ]
   }
   response = post(payment_url, headers=headers, json=data)
   response_data = response.json()
   return response_data

# Function to approve the payment
def approve_payment(access_token, order_id):
   approval_url = f"{base_url}/v2/checkout/orders/{order_id}/capture"
   headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {access_token}",
   }
   response = post(approval_url, headers=headers)
   return response.status_code == 201


def paypal_authorize_payment(request_id:str):
   access_token = get_access_token()
   payment_data = create_payment_request(access_token)
   order_id = payment_data.get("id")

   print("Payment URL:", payment_data.get("links")[1].get("href"))

   # In a real application, you would direct the user to the payment URL for approval.

   # For testing purposes, you can manually approve the payment using the order_id:
   success = approve_payment(access_token, order_id)

   if success:
      print("Payment successful.")
      return True
   print("Paymet failed....")
   return False 
