import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

def init_fb():
    # Fetch the service account key JSON file contents
    cred = credentials.Certificate('sawitcare-8a542-firebase-adminsdk-7yo8d-d6afc3987c.json')
    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://sawitcare-8a542-default-rtdb.firebaseio.com/"
    })
    
    return db
