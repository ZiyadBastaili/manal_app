import streamlit as st
from View.ScrapTweets import scraps
from View.AnalyseTweets import sentiment
from View.CleanTweets import clean
import View.ScrapTweets

def main():

  st.set_page_config(
    page_title="Sentiment Analysist",
    page_icon="Box.jpg",
    layout="wide",
    initial_sidebar_state="expanded"
  )

  st.sidebar.title("App Mode")

  app_mode = st.sidebar.selectbox("Choose the app mode",
    ["Scrape Twitter tweets", "Data cleaning and processing","Sentiment Analysis"],help="Choose a option to navigate into another window")

  if app_mode == "Scrape Twitter tweets":
    vid_name = 'videoDemo.webm'
    SetSideBar(vid_name)
    scraps()

  elif app_mode == "Data cleaning and processing":
    clean()

  else :
    sentiment()


def SetSideBar(vid_name):
  st.sidebar.write("--------------------------------------")
  st.sidebar.header("Video Demo")
  st.sidebar.write('Click expand for Demo video')
  my_expender1 = st.sidebar.expander("Expand me ", expanded=True)
  with my_expender1:
      st.video(vid_name)

  st.sidebar.write("--------------------------------------")



if __name__ == "__main__":
    main()

