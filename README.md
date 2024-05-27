# Spacer-App-Backend.

## Installation Guide

### Prerequisites

Before proceeding with the installation, make sure you have the following prerequisites installed on your system:

- Python 3.8.13
- pip package manager

### Installation Steps

1. **Clone the repository:**
- Using HTTPS
   ```bash
   git clone https://github.com/allankimanzi2/Spacer-App-Backend.git
   ```
 - Using SSH
    ```bash
   git clone git@github.com:allankimanzi2/Spacer-App-Backend.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd Spacer-App-Backend
   ```

3. **Create a virtual environment :**

   ```bash
   python -m venv .venv
   ```

4. **Activate the virtual environment :**

   ```bash
   source .venv/bin/activate
   ```

5. **Install the project dependencies:**

   ```bash
   pip install -r requirements.txt
   ```



   ## Backend online installation


pip install flask-cors Flask Flask-JWT Flask Flask-JWT-Extended flask flask-sqlalchemy Flask Flask-Bcrypt flask_cors


## Backeng alembic and migration instructions
 - If you have deleted the alembic folder, then follow the following steps:

     pip install alembic

     alembic init alembic

     alembic revision --autogenerate -m "description_of_migration"

     alembic upgrade head 


 - if you haven't deleted the folder:
    alembic revision --autogenerate -m "description_of_migration"
    alembic upgrade head

## On mpesa integration  with python daraja
## Python Daraja

 Python Daraja is a Python wrapper for handling payment requests through the Daraja MPESA API. It provides a simple and convenient way to integrate MPESA payments into your Python applications.

1. Features
  - Trigger STK Push for automatic payment requests
  - Query payment request status
  - Support for both Paybill and Buy Goods account types
  - Secure communication with the Daraja API

2. Installation
You can install Python Daraja using pip:

pip install python-daraja


## Initial Setup
- Before using the library, you need to set the following constants:

 from python_daraja import payment

payment.SHORT_CODE = "YOUR_SHORTCODE"
payment.PASSKEY = "YOUR PASSKEY"
payment.CONSUMER_SECRET = "YOUR CONSUMER SECRET"
payment.CONSUMER_KEY = "YOUR CONSUMER KEY"
payment.ACCOUNT_TYPE = "PAYBILL"  # Set to TILL for Buy Goods

Replace the placeholders with your actual Daraja API credentials.
Triggering STK Push
To initiate an automatic payment request (STK Push) on your customer's phone, use the trigger_stk_push function:
python
from python_daraja import payment

details = payment.trigger_stk_push(
    phone_number=2547123456,
    amount=1,
    callback_url='https://your-domain/callback/',
    description='Payment for services rendered',
    account_ref='Python Good PHP Bad and Co.'
)
print(details)

This function returns a dictionary with the result of the payment request. Note that this only indicates whether the request was successful, not if the customer has actually paid.
Querying Payment Status
To check the status of a payment request, use the query_stk_push function:
python
from python_daraja import payment

details = payment.query_stk_push(checkout_request_id='ws_CO_DMZ_123212312_2342347678234')
print(details)

Pass the checkout_request_id obtained from the previous trigger_stk_push call. A response code of 0 generally indicates a successful transaction.

## Server set up
To receive payment notifications from the Daraja API, you need to set up a secure server (HTTPS) with an endpoint that accepts POST requests. The server should not be localhost or 127.0.0.1.

You can use tools like ngrok to tunnel your local development server to a live secure server.
If you have CSRF protection enabled, you need to whitelist the following IP addresses in your server:
192.201.214.200
196.201.214.206
196.201.213.114
196.201.214.207
196.201.214.208
196.201.213.44
196.201.212.127
196.201.212.128
196.201.212.129
196.201.212.136
196.201.212.74
196.201.212.69


