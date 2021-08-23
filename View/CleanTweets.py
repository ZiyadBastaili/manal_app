import streamlit as st
import re
import View.ScrapTweets
from pandas import option_context
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import nltk
from nltk.stem.porter import *

DF = None
def clean():
    global DF
    #t.image('BOX.jpg')
    st.title('Tweets Preprocessing and Cleaning')
    DF = View.ScrapTweets.df
    st.info('Now! we will focus on cleaning and preparing data for visualization.Y'
            'ou are free to choose the steps to follow to clean the data. Your choice depends on the result you want.')
    options = st.multiselect(
        "Choose the steps to follow to clean the data : ",
        ['Remove (@user)','Remove numbers','Remove (#hashtag)','Remove ($tickers)'],
        help="Choose the steps to follow to clean the tweets.")


    st.subheader('Removing Url from tweets')
    ex1 = st.expander('Click display result of removing Twitter url !')
    with ex1:
        msg1 = '''
        Now let’s create a new column clean_tweet, it will contain the cleaned and processed tweets. \n
            **Note:**  that the pattern to remove r"http\S+|www\.\S+" , so will pick any word starting with ‘http’ or 'www.'
        '''
        st.info(msg1)
        colone1, colone2 = st.columns((1, 1))
        with colone1:
            st.subheader('**Before**')
            st.table(DF['tweet'].head(3))
        with colone2:
            st.subheader('**After**')
            # remove twitter url
            p = r"http\S+|www\.\S+"
            with st.spinner("Wait! Removing **URL** In progress"):
                DF['clean_tweet'] = np.vectorize(remove_pattern)(DF['tweet'],p)
                st.table(DF['clean_tweet'].head(3))
    st.success("Removing Url from tweets, done successfully!")
    st.write('------------------------------------------------------------------------------------------------------')

    if 'Remove (@user)' in options:
        st.subheader('Removing Twitter Handles (@user)')
        ex12 = st.expander('Click display result of removing Twitter Handles (@user)')
        with ex12:
            msg2 = '''
            Now let’s remove user mention (@user) in clean_tweet \n 
                **Note:**  To do that we use the pattern "@[\w]*" 
                '''
            st.info(msg2)
            coln1,coln2 = st.columns((1,1))
            with coln1:
                st.subheader('**Before**')
                st.table(DF['clean_tweet'].head(3))

            with coln2:
                st.subheader('**After**')
                with st.spinner("Wait Removing (@user) In progress"):
                    # remove twitter handles (@user)
                    DF['clean_tweet'] = np.vectorize(remove_pattern)(DF['clean_tweet'],"@\w+")
                    st.table(DF['clean_tweet'].head(3))
        st.success("Removing Twitter Handles (@user) done successfully")
        st.write('------------------------------------------------------------------------------------------------------')

    if 'Remove (#hashtag)' in options:
        st.subheader('Removing Twitter Handles (#hashtag)')
        ex12 = st.expander('Click display result of removing Twitter Handles (#hashtag)')
        with ex12:
            msg4 = '''
            Now let’s remove the hashtags (#hashtag) in clean_tweet \n 
                **Note:**  To do that we use the pattern "#[\w]*" 
                '''
            st.info(msg4)
            col1, col2 = st.columns((1, 1))
            with col1:
                st.subheader('**Before**')
                st.table(DF['clean_tweet'].head(3))
            with col2:
                st.subheader('**After**')
                with st.spinner("Wait Removing (#hashtag) In progress"):
                    # remove twitter handles (#hashtag)
                    DF['clean_tweet'] = np.vectorize(remove_pattern)(DF['clean_tweet'], "#\w+")

                    st.table(DF['clean_tweet'].head(3))
        st.success("Removing Twitter Handles (#hashtag) done successfully")
        st.write('------------------------------------------------------------------------------------------------------')

    if 'Remove ($tickers)' in options:
        st.subheader('Removing Twitter Handles ($tickers)')
        ex12 = st.expander('Click display result of removing Twitter Handles ($tickers)')
        with ex12:
            msg4 = '''
              Now let’s remove the tickers ($tickers) in clean_tweet \n 
                  **Note:**  To do that we use the pattern "$[\w]*" 
                  '''
            st.info(msg4)
            col1, col2 = st.columns((1, 1))
            with col1:
                st.subheader('**Before**')
                st.table(DF['clean_tweet'].head(3))
            with col2:
                st.subheader('**After**')
                with st.spinner("Wait Removing (@user) In progress"):
                    # remove twitter handles (#hashtag)
                    #DF['clean_tweet'] = np.vectorize(remove_pattern)(DF['clean_tweet'], "$\w+")
                    DF['clean_tweet'] = DF['clean_tweet'].str.replace("$[\w+ ]", " ")

                    st.table(DF['clean_tweet'].head(3))
        st.success("Removing Twitter Handles ($tickers) done successfully")
        st.write(
            '------------------------------------------------------------------------------------------------------')

    st.subheader('Removing Punctuations and Special Characters')
    msg2 = ''' 
    Punctuations, numbers and special characters do not help much. It is better to remove them from the text just as we removed the twitter handles.\n
        Here we will replace everything except characters and hashtags with spaces.
    '''
    ex3 = st.expander('Know more about removing Punctuations and Special Characters')
    with ex3:
        st.info(msg2)
        colln1,colln2 = st.columns((1,1))
        with colln1:
            st.subheader('**Before**')
            st.table(DF['clean_tweet'] .head(3))

        with colln2 :
            st.subheader('**After**')
            with st.spinner("Wait Removing Punctuations,and Special Characters"):
                # remove special characters and punctuations
                DF['clean_tweet'] = DF['clean_tweet'].str.replace("[^a-zA-Z@#$0-9 ]", " ")
                st.table(DF['clean_tweet'].head(3))
    st.success("Removing Punctuations and Special Characters done successfully")
    st.write('------------------------------------------------------------------------------------------------------')

    if 'Remove numbers' in options:
        st.subheader('Removing only isolated numbers in tweets')
        msg2 = ''' 
        In this section we will remove only isolated number from tweets \n
            Note: Conserve words that are preceded or followed directly by numbers, because it can present a valuable information.\n
            For example : 'SPAC2021'
                '''
        ex3 = st.expander('Know more about removing Numbers from tweets')
        with ex3:
            st.info(msg2)
            colln1, colln2 = st.columns((1, 1))
            with colln1:
                st.subheader('**Before**')
                st.table(DF['clean_tweet'].head(3))

            with colln2:
                st.subheader('**After**')
                with st.spinner("Wait Removing numbers from tweets"):
                    DF['clean_tweet'] =  np.vectorize(remove_pattern)(DF['clean_tweet'],"\s\d+\s")
                    st.table(DF['clean_tweet'].head(3))
        st.success("Removing numbers from tweets done successfully")
        st.write('------------------------------------------------------------------------------------------------------')

    st.header('Removing Short Words')
    msg3 = ''' Now, we remove all the words having length 3 or less.  It is better to get rid of them.\n
        For example, terms like “hmm”, “oh” are of very little use.
            '''
    ex3 = st.expander(' Know more about removing Short Words')
    with ex3:
        st.info(msg3)
        collnn1, collnn2 = st.columns((1, 1))
        with collnn1:
            st.subheader('**Before**')
            st.table(DF['clean_tweet'].head(3))

        with collnn2:
            st.subheader('**After**')
            with st.spinner("Wait Removing Short Words"):
                DF['clean_tweet'] = DF['clean_tweet'].apply(lambda x: ' '.join([w for w in x.split() if len(w) > 3]))
                st.table(DF['clean_tweet'].head(3))
    st.success("Removing Short Words done successfully")
    st.write('------------------------------------------------------------------------------------------------------')



    st.header(' Tokenization')
    msg5 = ''' 
    Now we will tokenize all the cleaned tweets in our dataset.\n
        Tokens are individual terms or words, and tokenization is the process of splitting a string of text into tokens.
    '''
    ex5 = st.expander(' Know more about Tokenization')
    with ex5:
        st.info(msg5)
        colne11,colne22, col22 = st.columns((1,0.2, 1))
        with colne11:
            st.subheader('**Before**')
            DF['clean_tweet'] = DF['clean_tweet'].apply(lambda x: ' '.join([w for w in x.split() if len(w) >= 3]))
            st.table(DF['clean_tweet'].head(3))

        with colne22:
            st.subheader('**After**')
            with st.spinner("Wait Tokenization"):
                tokenized_tweet = DF['clean_tweet'].apply(lambda x: x.split())
                st.text(tokenized_tweet.head(12))
    st.success("Tokenization done successfully")
    st.write('------------------------------------------------------------------------------------------------------')

    st.header(' Stemming')
    msg6 = ''' Stemming is a rule-based process of stripping the suffixes (“ing”, “ly”, “es”, “s” etc) from a word.\n
         For example – “play”, “player”, “played”, “plays” and “playing” are the different variations of the word – “play”.
        '''
    ex6 = st.expander(' Know more about Stemming')
    with ex6:
        st.info(msg6)
        coo11,coo22 = st.columns((1,1))
        with coo11:
            st.subheader('**Before**')
            tokenized_tweet = DF['clean_tweet'].apply(lambda x: x.split())
            st.table(DF['clean_tweet'].head(3))

        with coo22:
            st.subheader('**After**')
            with st.spinner("Wait Stemming"):
                stemmer = PorterStemmer()
                tokenized_tweet = tokenized_tweet.apply(lambda x: [stemmer.stem(i) for i in x])  # stemming
                st.text(tokenized_tweet.head(12))
    st.success("Stemming done successfully")
    st.write('------------------------------------------------------------------------------------------------------')


    st.text('Now let’s stitch these tokens back together.')
    for i in range(len(tokenized_tweet)):
        tokenized_tweet[i] = ' '.join(tokenized_tweet[i])
        DF['clean_tweet'] = tokenized_tweet
    st.success("Tokens back together done successfully")
    st.write('------------------------------------------------------------------------------------------------------')


    st.header('Comparaison betweet tweets befor and after cleaning')
    coo1, coo2 = st.columns((1, 1))
    with coo1:
        st.subheader('**Before**')
        st.table(DF['tweet'].head(3))

    with coo2:
        st.subheader('**After**')
        st.table(DF['clean_tweet'].head(3))





def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, ' ', input_txt)

    return input_txt