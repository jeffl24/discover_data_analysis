import pandas as pd
import numpy as np
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
pd.options.display.max_columns = 999

cred = credentials.Certificate('D:\Code\discover_data_analysis\discover-db-firebase.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://discover-db.firebaseio.com/'})

snapshot_custom = db.reference('results').order_by_child('timestamp').limit_to_last(10).get()


# .start_at('b').end_at(u'b\uf8ff')
for key in snapshot_custom:
    print(key)
