import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyDwNd5mMa6xFcUAwsQReoZ33BAPazXmLj4",
    "authDomain": "week7-dfecc.firebaseapp.com",
    "databaseURL": "https://week7-dfecc-default-rtdb.firebaseio.com/",
    "projectId": "week7-dfecc",
    "storageBucket": "week7-dfecc.firebasestorage.app",
    "messagingSenderId": "980347652379",
    "appId": "1:980347652379:web:65be7efcda011a92aaebbe",
    "measurementId": "G-9DD9F1DTH2"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()