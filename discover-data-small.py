
# coding: utf-8

# In[1]:

import json
from pprint import pprint
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize


# In[2]:

data = json.load(open('discover-data-small.json', encoding='UTF-8'))


# In[3]:

pprint(data)


# In[4]:

df = pd.DataFrame.from_dict(json_normalize(data), orient='columns')


# In[5]:

df


# In[6]:

df_split = pd.DataFrame(df.concerns.values.tolist()).add_prefix('concern_')
df_split_concerns = pd.concat([df, df_split], axis=1)
df_split_concerns


# In[7]:

split_results = pd.DataFrame(df.results.values.tolist()).add_prefix('result_')
split_results


# In[8]:

pd.DataFrame(df.results.values.tolist()).add_prefix('result_')
# single_col_extract = split_results['result_0'].apply(pd.Series)
sku_extract = split_results.applymap(lambda x: x['sku'] if isnull(x) == False)
sku_extract


# dict_test = {'concerns_addressed_count': 2,
#                'name': 'Clear Pore Normalizing Cleanser Salicylic Acid',
#                'sku': '6002'}
# type(dict_test.get('location'))

# '''x=[]
# for entry in split_results['result_11']:
#     x.append(entry['sku'] if )
#     
# x'''
# split_results['result_11']['sku']

# In[ ]:

split_results_nine = split_results.iloc[:, :10].applymap(lambda x: x['sku'])
split_results_nine


# In[12]:

df_split_all = pd.concat([df_split_concerns, split_results_nine], axis=1)
df_proper = df_split_all.drop(['concerns', 'results'], axis=1)
df_proper.to_csv('json_to_csv.csv')

