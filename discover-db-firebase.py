import pandas as pd
import numpy as np
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('D:\Code\discover_data_analysis\discover-db-firebase.json')
firebase_admin.initialize_app(cred,
                              {'databaseURL': 'https://discover-db.firebaseio.com/'})
ref = db.reference('results/-L-F3vs_iWKf3O6yXN_P')

print(ref.order_by_key().limit_to_last(1).get())
