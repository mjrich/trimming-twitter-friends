
# coding: utf-8

# In[1]:

print("Hello World")


# In[7]:

import tweepy
import pandas as pd

#Then create new twitter app: https://apps.twitter.com/
#Then set up Oauth below (filling in the empty double quotes)


# In[5]:

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.
# Source: https://github.com/tweepy/tweepy/blob/master/examples/oauth.py

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key=""
consumer_secret=""

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
access_token=""
access_token_secret=""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# If the authentication was successful, you should
# see the name of the account print out
print(api.me().name)


# In[6]:

#If you set up to write as well as read, you can send this message
api.update_status(status='This tweet just came from my local Jupyter notebook. Thanks project Jupyter and Tweepy for the helpful docs!')


# In[17]:

#put your twitter handle below instead of mine to get list of who you follow
friend_ids_all = api.friends_ids("richmanmax")
len(friend_ids_all)


# In[104]:

#put your twitter handle below instead of mine to get list of who follows you
followers_ids_all = api.followers_ids("richmanmax")
len(followers_ids_all)


# In[72]:

#choose how many friends (people who follow you) you want to analyze
#note: in the next section you will hit rate limit of 180 calls
#so pick a number under 180 or be prepared to wait
friend_ids_some = friend_ids_all[0:10]
friend_ids_some


# In[78]:

#check how many user API calls we have left
api.rate_limit_status()['resources']['users']


# In[79]:

user_json = []
for i in friend_ids_some:
    user_json += [api.get_user(i).__getstate__()['_json']]
len(user_json)


# In[80]:

#check how many user API calls we have left
api.rate_limit_status()['resources']['users']


# In[81]:

user_json


# In[111]:

from pandas.io.json import json_normalize
df_user_data = json_normalize(user_json)
df_user_data


# In[112]:

df_user_data.columns


# In[113]:

#example frequency of a variable
df_user_data['time_zone'].value_counts(dropna=False)


# In[120]:

#merge in information if they follow you
followback = []
for x in range(len(followers_ids_all)):
    followback.append("TRUE")
user_data_followback = zip(followers_ids_all,followback)
df_user_data_followback = pd.DataFrame(user_data_followback)
df_user_data_followback.columns = ["id","follow_back"]
df_user_data_followback
df_user_data_merge = pd.DataFrame.merge(df_user_data,df_user_data_followback, how='left', on='id')
df_user_data_merge


# In[126]:

#simplify data frame to just the key variables of interest
#then sort by those  following with most tweets and fewest followers (likely for me to still follow)
df_user_simple = df_user_data_merge[['id','name','screen_name','follow_back','statuses_count','followers_count','friends_count']]
df_user_simple.sort_values(["follow_back","statuses_count","followers_count"],ascending=[False,False,True])


# In[127]:

#DANGER WILL ROBINSON: This is the write command that will unfollow people
#it is appropriately called "destroy friendship" so use with care.
#designed currently for using one ID from above at a time for #####

api.destroy_friendship(######)


# In[ ]:



