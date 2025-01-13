import firebase_admin
from firebase_admin import credentials, firestore
import json
import os

if os.getenv("RENDER") == "true":  # Render environment
    print("Running in Production...")
    firebase_credentials = os.getenv("FIREBASE_CREDENTIALS")
    if firebase_credentials:
        cred_dict = json.loads(firebase_credentials)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    else:
        raise ValueError("FIREBASE_CREDENTIALS environment variable not set!")
else:  # Local environment
    print("Running Locally...")
    cred = credentials.Certificate("firebase_credentials.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()
