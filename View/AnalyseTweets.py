import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

import View.CleanTweets
import textblob
from textblob import TextBlob
import numpy as np
import plotly.express as px
import pandas as pd



def sentiment():
    st.title('Story Generation and Visualization from Tweets')
    st.info('In this section, we will explore the cleaned tweets text. Exploring and visualizing data.')

    st.subheader('Define  Polarity and Subjectivity for tweets  ')
    st.spinner('Adding Polarity and Subjectivity in progress ! Please wait!')
    SentimentAnaly(View.CleanTweets.DF)
    st.success("Adding Polarity and Subjectivity done successfully")

    st.subheader('Associate Sentiment to each tweet')
    st.spinner('Associate Sentiment in progress ! Please wait! ')
    View.CleanTweets.DF['Analysis'] = View.CleanTweets.DF['Polarity'].apply(getAnalysis)
    c1,c2=st.columns((16,1))
    with c1:
        st.subheader('Add column Analysis to our tweets')
        st.write( View.CleanTweets.DF[['id','tweet','clean_tweet','Subjectivity','Polarity','Analysis']])

    st.success("associating Sentiment Analysis done successfully")

    st.subheader('Pourcentage of Positive, Negative and Neutral tweets')
    cc1,cc2,cc3 = st.columns((1,2,1))
    with cc2:
        PieChart(View.CleanTweets.DF)

    st.subheader('Display most used words in our data')
    WordCloudN(View.CleanTweets.DF)
    c11,c22,c33= st.columns((1,2,1))
    with cc2:
        st.subheader('WordCloud of Tweets')
        WordCloudW(View.CleanTweets.DF)



def WordCloudW(DF):
    all_words = " ".join([sentence for sentence in View.CleanTweets.DF['clean_tweet']])
    wordcloud = WordCloud(width=800, height=500, random_state=42, max_font_size=100).generate(all_words)
    # plot the graph
    plt.figure(figsize=(15, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity


def getPolarity(text):
    return TextBlob(text).sentiment.polarity

def SentimentAnaly(DF):
# Create two new columns
    DF['Subjectivity'] = np.nan
    DF['Polarity'] = np.nan
    DF['Subjectivity'] = DF['clean_tweet'].apply(getSubjectivity)
    DF['Polarity'] = DF['clean_tweet'].apply(getPolarity)
    # Show the new dataframe with the new columns
    st.write(DF[['id','username','tweet','clean_tweet','Subjectivity','Polarity']])


#Create a function to compute the negative, neutral and positive analysis
def getAnalysis(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'

def PieChart(DF):
    sentiment_count = DF['Analysis'].value_counts()
    # st.write(sentiment_count)
    sentiment_count_df = pd.DataFrame({'Sentiment': sentiment_count.index, 'Tweets': sentiment_count.values})
    fig = px.pie(sentiment_count_df, values='Tweets', names='Sentiment')
    st.plotly_chart(fig)


def WordCloudN(DF):

    negative_words = ' '.join([text for text in DF['clean_tweet'][DF['Analysis'] == 'Negative']])
    neutral_words = ' '.join([text for text in DF['clean_tweet'][DF['Analysis'] == 'Neutral']])
    Positiv_words = ' '.join([text for text in DF['clean_tweet'][DF['Analysis'] == 'Positive']])

    col1,col2,col3 = st.columns((1,1,1))
    with col3:
        try:
            st.text('WordCloud of negative words')
            wordcloud = WordCloud(width=800, height=500,random_state=21, max_font_size=110).generate(negative_words)
            plt.figure(figsize=(10, 7))
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis('off')
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot()
        except :
            st.warning('No negative words')

    with col2:
        try:
            st.text('WordCloud of neutral words')
            wordcloud = WordCloud(width=800, height=500,
                                  random_state=21, max_font_size=110).generate(neutral_words)
            plt.figure(figsize=(10, 7))
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis('off')
            st.pyplot()
        except :
            st.warning('No Neutral Words ')


    with col1:
        try :
            st.text('WordCloud of positive words')
            wordcloud = WordCloud(width=800, height=500,
                                  random_state=21, max_font_size=110).generate(Positiv_words)
            plt.figure(figsize=(10, 7))
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis('off')
            st.pyplot()
        except:
            st.warning('No Positive Words ')


