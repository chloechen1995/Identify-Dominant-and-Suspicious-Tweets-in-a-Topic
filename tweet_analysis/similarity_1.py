#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 00:48:27 2017

@author: Chloechen
"""

"""
calculate tweet similarity
"""

#%%
import pandas as pd
from nltk.corpus import stopwords
import itertools as it
from math import factorial
import numpy as np
import os 


#%%
def create_df(user_id):
    """
    remove unnecessary words from the user_tweets.csv
    
    Argument: user_id
    
    Return: user_tweets dataframe
    """
    user_id = str(user_id)
    os.chdir('/Users/Chloechen/Desktop/Sample_Tweets')
    user_tweets = pd.read_csv(user_id + "_tweets_.csv")
    #user_tweets.columns = ['Tweet_Id', 'Created_At', 'Source', 'Favorite_Count', 'Retweet_Count', 'Tweet_Text', 'User_Id']
    special_remove = [str(tweets).decode('unicode_escape').encode('ascii','ignore') for tweets in user_tweets['Tweet_Text']] 
    user_tweets['tweet_split'] = [tweets.lower().split() for tweets in special_remove]
    user_tweets['tweet_split'] = [filter(lambda x: not (x.startswith("@") or x.startswith("#") or x.startswith("https:") or x in stopwords.words("english") or x.startswith("rt")), tweet) for tweet in user_tweets['tweet_split']]
    user_tweets['tweet_split_string'] = [' '.join(str(x) for x in tweets) for tweets in user_tweets['tweet_split']]
    return user_tweets
    

#%%
def cal_char(user_tweets):
    """
    calculate the length of tweets
    
    Argument: user_tweets dataframe created by create_df function
    
    Return: the length of every tweet
    """
    user_tweets['tweet_split'] = [str(tweets).lower().split() for tweets in user_tweets['Tweet_Text']]
    user_tweets['tweet_string'] = [filter(lambda x: not (x.startswith("@") or x.startswith("#") or x.startswith("https:") or x.startswith("rt")), tweet) for tweet in user_tweets['tweet_split']]
    char_count = [len(user_tweets['tweet_string'][i]) for i in range(len(user_tweets['tweet_string']))]
    return char_count

#%%
def comb_2(tweet_df):
    """
    calculate the number of tweet combinations
    
    Argument: num_tweets
    
    Return: total number of tweet combinations
    """
    num_tweets = len(tweet_df['Tweet_Text'])
    return int(factorial(num_tweets) / (factorial(2) * factorial(num_tweets - 2)))

#%%
def tweet_set(tweet_df):
    """
    create a set of possible tweet-to-tweet combinations among any two tweets
    
    Argument: tweet_df
    
    Return: set of tweet combinations
    """
    tweet_list = list(tweet_df["tweet_split"])
    tweet_tuples = list(it.combinations(tweet_list, 2))
    tweet_df = pd.DataFrame(tweet_tuples, columns = ["tweet_1", "tweet_2"])
    tweet_df["tweet_combination"] = tweet_df["tweet_1"] + tweet_df["tweet_2"]
    tweet_df['common_words'] = [set([x for x in tweet if tweet.count(x) > 1]) for tweet in tweet_df['tweet_combination']]
    tweet_df['common_count'] = [len(tweet_df['common_words'][i]) for i in range(len(tweet_df['common_words']))]  
    return tweet_df

#%%
def tweet_sim(user_id):
    user_tweets = create_df(user_id)
    char_count = cal_char(user_tweets)
    tweet_comb = tweet_set(user_tweets)
    sim_value = tweet_comb['common_count'].sum() / (np.mean(char_count) * comb_2(user_tweets))
    return sim_value