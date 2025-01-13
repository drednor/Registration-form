from flask import Flask, render_template, request, session, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore
import random
import os
import json

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default_secret")

if os.getenv("RENDER") == "true":  # Set this env var in Render
    print("Running in Production...")
    firebase_credentials = os.getenv("FIREBASE_CREDENTIALS")
    if firebase_credentials:
        cred_dict = json.loads(firebase_credentials)  # Load from env var
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    else:
        raise ValueError("FIREBASE_CREDENTIALS environment variable not set")
else:
    print("Running Locally...")
    cred = credentials.Certificate("firebase-credentials.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['POST'])
def register():
    fullname = request.form['fullname']
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    pincode = request.form['pincode']
    phone = request.form['phone']
    email = request.form.get('email', 'N/A')  # Optional field

    print(f"Fullname: {fullname}, Address: {address}, City: {city}, State: {state}, Pincode: {pincode}, Phone: {phone}, Email: {email}")

    # Save the data to Firestore
    user_ref = db.collection('users').document()
    user_ref.set({
        'fullname': fullname,
        'address': address,
        'city': city,
        'state': state,
        'pincode': pincode,
        'phone': phone,
        'email': email
    })
    print("saved to database")

    return f"""
        <h1>Registration Successful!</h1>
    """

@app.route('/send_otp', methods=['POST'])
def send_otp():
    phone = request.form['phone']
    print(f"Sending OTP to {phone}")
    otp = random.randint(100000, 999999)
    session['otp'] = otp
    session['phone'] = phone
    print(f"OTP: {otp}")
    return render_template('verify_otp.html', error=None)

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    entered_otp = request.form['otp']

    if 'otp' in session and entered_otp == str(session['otp']):
        session['authenticated'] = True
        return redirect(url_for('registration_form'))

    # If OTP is incorrect, re-render the same page with an error message
    return render_template('verify_otp.html', error="Invalid OTP. Please try again.")

@app.route('/registration_form')
def registration_form():
    if not session.get('authenticated'):
        return "<h1>Unauthorized. Please verify OTP first.</h1>", 403
    print("Authenticated")
    return render_template('registration_form.html')

@app.route('/verify_phone', methods=['POST'])
def verify_phone():
    session['authenticated'] = True  # Store session after verification
    return redirect(url_for('registration_form'))
    
if __name__ == "__main__":
    app.run()
