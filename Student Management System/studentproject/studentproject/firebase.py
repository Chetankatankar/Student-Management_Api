# studentproject/firebase.py
import os
import firebase_admin
from firebase_admin import credentials, firestore
from threading import Lock

_firestore_client = None
_init_lock = Lock()

def get_firestore():
    """
    Lazy-initialize and return Firestore client.
    Returns None if initialization fails.
    """
    global _firestore_client
    if _firestore_client is not None:
        return _firestore_client

    with _init_lock:
        if _firestore_client is not None:
            return _firestore_client

        try:
            cred_path = os.environ.get("FIREBASE_CRED")
            if not cred_path:
                # fallback to project relative path (dev only)
                base = os.path.dirname(os.path.abspath(__file__))
                cred_path = os.path.join(base, "..", "firebase-service-account.json")
                cred_path = os.path.abspath(cred_path)

            cred = credentials.Certificate(cred_path)
            # initialize_app must be called once; guard with try/except
            try:
                firebase_admin.get_app()
            except ValueError:
                firebase_admin.initialize_app(cred)

            _firestore_client = firestore.client()
            return _firestore_client

        except Exception as e:
            # don't raise here — returning None keeps app usable without Firebase
            print("Firebase init error:", e)
            _firestore_client = None
            return None
