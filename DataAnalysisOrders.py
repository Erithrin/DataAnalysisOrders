#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install kaggle


# In[9]:

#downloading files from kaggle
import kaggle
get_ipython().system('kaggle datasets download ankitbansal06/retail-orders -f orders.csv')


# In[27]:

#extracting dataset from zipped file
import zipfile
zipref = zipfile.ZipFile('orders.csv.zip')
zipref.extractall()
zipref.close()


# In[29]:


import pandas as pd


# In[43]:

#reading the csv file and treating some values as null
df = pd.read_csv('orders.csv', na_values = ['Not Available', 'unknown'])


# In[45]:


df['Ship Mode'].unique()


# In[47]:

#data modification and cleaning
df.columns = df.columns.str.lower()


# In[57]:


df.columns = df.columns.str.replace(' ','_')


# In[61]:


#derive new columns discount , sale price and profit
df['discount'] = df['list_price']*df['discount_percent']/100


# In[65]:

#creating a new column called sales price
df['sales_price'] = df['list_price']-df['discount']


# In[69]:

#determining the profit
df['profit'] = df['sales_price'] - df['cost_price']


# In[79]:

#removing unnecessary columns
df.drop(columns = ['list_price','cost_price','discount_percent'], inplace= True)


# In[83]:

#changing object to date
df['order_date'] = pd.to_datetime(df['order_date'],format='%Y-%m-%d')


# In[85]:


df.head()


# In[95]:


pip install pymysql


# In[108]:

#connect to database so that cleaned data can be stored in the database
import sqlalchemy as sal
engine = sal.create_engine('mysql+pymysql://root:Root88_password@localhost:3306/data_analysis')


# In[112]:


conn=engine.connect()


# In[116]:


with engine.connect() as connection:
    print("Connected to the database successfully!")


# In[118]:


df.columns


# In[120]:

#loading data to df_orders table. Table has been created using sql query
df.to_sql('df_orders',con = conn,index = False,if_exists='append')


# In[ ]:




