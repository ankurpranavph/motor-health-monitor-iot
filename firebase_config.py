import firebase_admin
from firebase_admin import credentials, db

if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL":  "https://motor-monitor-c7836-default-rtdb.asia-southeast1.firebasedatabase.app"
    })