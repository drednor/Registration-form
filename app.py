from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route('/')
def home():
    return render_template('registration_form.html')

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

    return f"""
        <h1>Registration Successful!</h1>
    """

@app.route('/random')
def random():
    return render_template("random.html")
if __name__ == "__main__":
    app.run(debug=True)
