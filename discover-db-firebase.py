import pandas as pd
import numpy as np
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
pd.options.display.max_columns = 999

cred = credentials.Certificate('D:\Code\discover-db-firebase.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://discover-db.firebaseio.com/'})

snapshot_custom = db.reference('results').order_by_key().start_at('-KtdoxwhQLhxA19-YAEJ').get()


# .start_at('b').end_at(u'b\uf8ff')
key_series = []
for key in snapshot_custom:
    key_series.append(key)

# print(key_series)
# This loops through the key_series list generated earlier and
# for each key, make a query and format the data
snapshot_drop_list = ['Barcode',
             'first_description',
             'image_url',
             'ingredients',
             'key_benefits',
             'key_ingredients',
             'research',
             'shopifyID',
             'url',
             'usa_url' ]

discover_df_all = pd.DataFrame()
for entry in key_series:
    each_snapshot = dict(db.reference('results').order_by_key().start_at(entry).limit_to_first(1).get())[entry]
    if 'email' not in each_snapshot['request']:
        continue
    left_df = pd.io.json.json_normalize(each_snapshot)
    right_df = pd.io.json.json_normalize(each_snapshot, record_path='results').drop(snapshot_drop_list, axis=1)
    right_df['email'] = each_snapshot['request']['email']
    new_df = pd.merge(left_df, right_df, left_on='request.email', right_on='email').drop(['request.email', 'results'], axis=1)
    discover_df_all = discover_df_all.append(new_df)

discover_df_all.to_csv('discover_print_to_csv.csv')
print('Printed to CSV')
