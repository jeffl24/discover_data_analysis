
# coding: utf-8

# ### Methodology
# 1. Import and format Discover and Shopify sales data
# 2. Combine the details of each Discover taker's **earliest** attempt into Shopify data
# 3. Identify NEW customers and match their earliest purchase with their earliest Discover attempt
# 4. Perform calculations, such as:
#     1. Percentage of transactions that actually contain at least one of the recommended SKUs
#     2. Average/median/min/max time taken to purchase after attempting Discover
#     3. etc

# In[4]:

import numpy as np
import pandas as pd
pd.set_option("display.max_columns", 100)


# In[5]:

# import discover data
discover_data = pd.read_csv("discover_user_input_results.csv")

# Populate a table of emails, keeping the EARLIEST discover attempt of each customer.
discover_first = discover_data.drop_duplicates(subset = ['email'], keep='first')
discover_first['timestamp'] = pd.to_datetime(discover_first['timestamp'].map(lambda x: x.replace('th', "")))
discover_first.drop('timestamp', axis=1,inplace=True)
# discover_first.to_csv('discover_first.csv')


# In[55]:

# Import shopify sales data
sales_data = pd.read_csv("shopify_orders_export_20180207.csv",
                         low_memory=False,
                         parse_dates=['Paid at', 'Fulfilled at', 'Created at'])

sales_data_clean = sales_data.drop(sales_data.columns.to_series()[-11:-1], axis=1)
# remove in-store purchases by dropping NA rows in Email column
sales_data_clean.dropna(subset=['Email'], axis=0, inplace=True)

# add columns referencing each customer's FIRST use of discover
sales_data_clean['discover_first_date'] = sales_data_clean['Email'].map(discover_first.set_index('email')['timestamp2'])
sales_data_clean['used_discover_already'] = (sales_data_clean['Created at']> sales_data_clean['discover_first_date']).map({True: "Used Discover", False: "Not yet"})
sales_data_clean['discover_sales_lead_time'] = sales_data_clean['Created at'] - sales_data_clean['discover_first_date']

# create sales dataset filtering customers who had used discover
# regardless of whether they are existing or completely new customers
post_discover_sales = sales_data_clean[sales_data_clean['used_discover_already'] == "Used Discover"]

# create sales dataset filtering customers who have never used discover and
# and also those customers' purchase histories right before they use discover
pre_discover_sales = sales_data_clean[~(sales_data_clean['used_discover_already'] == "Used Discover")]


# In[ ]:

same_day_purchase = sales_data_clean[(sales_data_clean['discover_sales_lead_time'] <= "1 days") &                                      (sales_data_clean['discover_sales_lead_time'] > "0 days")]
same_day_purchases_count = len(same_day_purchase['Email'].unique())

post_discover_launch_customer_count = len(discover_first['email'].unique())
percentage_same_day_purchase = same_day_purchases_count/post_discover_launch_customer_count

print("same_day_purchases_count:", same_day_purchases_count)
print("post_discover_launch_customer_count:", post_discover_launch_customer_count)
print("Count of customers who made a purchase on the same day after using Discover:",len(same_day_purchase['Email'].unique()))
print("Number of unique customers after the launch of Discover:", len(discover_first['email'].unique()))
print("percentage_same_day_purchase: {0:.2f}%".format(percentage_same_day_purchase))


# In[53]:

# create sales dataset filtering NEW customers who HAD NOT purchased prior to trying out discover
## obtain the transactions of new customers acquired after Discover launch who have used discover
post_discover_new_customers = post_discover_sales[~(post_discover_sales['Email'].isin(pre_discover_sales['Email']))
                                                  #&
                                                  #(pd.isnull(post_discover_sales['discover_first_date']) == False)
                                                 ]
post_discover_new_customers_unique = post_discover_new_customers[['Email', 'Created at']].drop_duplicates()
post_discover_new_customers_unique.sort_values('Created at', inplace=True)
post_discover_new_customers_unique['Previous Transaction'] = post_discover_new_customers_unique.groupby(['Email'])['Created at'].shift()
post_discover_new_customers_unique['Days Between'] = post_discover_new_customers_unique['Created at'] - post_discover_new_customers_unique['Previous Transaction']
post_discover_new_customers_unique['Days Between Int'] = (post_discover_new_customers_unique['Days Between'].dropna()/ np.timedelta64(1, "D")).astype(int)
post_discover_new_customers_unique['Buy Count'] = post_discover_new_customers_unique.groupby(['Email'])['Created at'].cumcount()+1
post_discover_new_customers_unique['Days Between'].mean()
# post_discover_new_customers_unique.to_excel("post_discover_new_customers_unique.xlsx")


# In[96]:

pre_discover_new_customers = sales_data_clean[~(sales_data_clean['Email'].isin(post_discover_new_customers['Email']))]
pre_discover_new_customers_unique = pre_discover_new_customers[['Email', 'Created at']].drop_duplicates()
pre_discover_new_customers_unique.sort_values('Created at', inplace=True)
pre_discover_new_customers_unique['Previous Transaction'] = pre_discover_new_customers_unique.groupby(['Email'])['Created at'].shift()
pre_discover_new_customers_unique['Days Between'] = pre_discover_new_customers_unique['Created at'] - pre_discover_new_customers_unique['Previous Transaction']
pre_discover_new_customers_unique['Days Between Int'] = (pre_discover_new_customers_unique['Days Between'].dropna()/ np.timedelta64(1, "D")).astype(int)
pre_discover_new_customers_unique['Buy Count'] = pre_discover_new_customers_unique.groupby(['Email'])['Created at'].cumcount()+1
pre_discover_new_customers_unique['Days Between'].mean()
#pre_discover_new_customers_unique.to_excel("pre_discover_new_customers_unique.xlsx")

# In[102]:

discover_taker_sales = sales_data_clean[sales_data_clean['discover_first_date'].isnull() == False]
discover_taker_dates = discover_taker_sales[['Email', 'Created at']].drop_duplicates()
discover_taker_dates.sort_values('Created at', inplace=True)
discover_taker_dates['Previous Transaction'] = discover_taker_dates.groupby(['Email'])['Created at'].shift()
discover_taker_dates['Days Between'] = discover_taker_dates['Created at'] - discover_taker_dates['Previous Transaction']
discover_taker_dates['Days Between Int'] = (discover_taker_dates['Days Between'].dropna()/ np.timedelta64(1, "D")).astype(int)
discover_taker_dates['Buy Count'] = discover_taker_dates.groupby(['Email'])['Created at'].cumcount()+1
discover_taker_dates.to_excel("discover_taker_dates.xlsx")
discover_taker_dates['Days Between'].mean()


# In[103]:

non_discover_taker_sales = sales_data_clean[sales_data_clean['discover_first_date'].isnull() == True]
non_discover_taker_dates = non_discover_taker_sales[['Email', 'Created at']].drop_duplicates()
non_discover_taker_dates.sort_values('Created at', inplace=True)
non_discover_taker_dates['Previous Transaction'] = non_discover_taker_dates.groupby(['Email'])['Created at'].shift()
non_discover_taker_dates['Days Between'] = non_discover_taker_dates['Created at'] - non_discover_taker_dates['Previous Transaction']
non_discover_taker_dates['Days Between Int'] = (non_discover_taker_dates['Days Between'].dropna()/ np.timedelta64(1, "D")).astype(int)
non_discover_taker_dates['Buy Count'] = non_discover_taker_dates.groupby(['Email'])['Created at'].cumcount()+1
non_discover_taker_dates.to_excel("non_discover_taker_dates.xlsx")
non_discover_taker_dates['Days Between'].mean()


# # Section 2
# ## How long does it take for brand new customers to buy something after using Discover?
# ### First, identify customers who had not purchased before Discover launch
#
# 1. Create a new column that indicates whether this customer has made any purchase before the launch of Discover
#     1. Note: this assumes that the
# 2. Create a table containing Emails, First Tried Discover Date and whether they existed before 2017-09-09 (Discover Launch)
#     1. Note: this EXCLUDES those customers who *have not tried Discover*, regardless of whether they have made a purchase before/after the launch of Discover

# In[98]:

# Lead time to purchase for new customers after taking Discover

new_customers_test = pd.DataFrame(post_discover_sales['Email'].unique(), columns=["Post Launch Emails"])
new_customers_test['Exist before launch?'] = new_customers_test.isin(pre_discover_sales['Email'].unique())

new_customers_test = new_customers_test.merge(right=discover_first[['email', 'timestamp2']], left_on='Post Launch Emails', right_on='email')
new_customers_test = new_customers_test.drop('email', axis=1)
new_customers_test = new_customers_test.rename(columns={"timestamp2": "First Tried Discover"})

# get first transaction date of each of the "new" customers
post_discover_first_purchase = post_discover_sales[['Email', 'Created at']].drop_duplicates(subset='Email', keep='last')
# print("Number of rows:", len(post_discover_first_purchase))

new_customers_test = new_customers_test.merge(post_discover_first_purchase, left_on="Post Launch Emails", right_on="Email")
new_customers_test = new_customers_test.drop('Email', axis=1).rename(index=str, columns={"Created at": "First Purchase Date"})
new_customers_test['Time To Buy'] = new_customers_test['First Purchase Date']- new_customers_test['First Tried Discover']
print(new_customers_test['Time To Buy'].describe())
print(new_customers_test['Time To Buy'].quantile(0.85))


# In[ ]:

# To obtain the list of unique emails of NEW customers who did not take Discover

post_discover_sales_unique = pd.DataFrame(post_discover_sales['Email'].unique(), columns=["Post Launch Emails"])
new_customers_no_discover = post_discover_sales_unique[~post_discover_sales_unique.isin(pre_discover_sales['Email'].unique())]
new_customers_no_discover = new_customers_no_discover.dropna()
new_customers_no_discover.rename(columns={"Post Launch Emails": "Post Launch non-Discover Takers"})
