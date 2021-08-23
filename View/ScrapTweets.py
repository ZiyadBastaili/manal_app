import streamlit as st
# python -m pip install --upgrade pip
import twint
import base64
from io import BytesIO
import pandas as pd
from View.CleanTweets import clean
df = None

def scraps():
    global df
    user_name=None
    language=None
    translate=None
    since = ""
    until = ""


    st.title(' Getting twitter data - Easy and without API')
    msg='''
    In this simple web app we are going to use Twint - https://pypi.org/project/twint/ to get Twitter data.
    This is a relatively new package that manages to get around Twitter's API. \n
    **Note**: To get code source used in each section of the app, please click on *Expand me* 
        '''
    st.info(msg)
    choice = st.radio(
                      "Choice a option of scraping",
                      ('Scrap directly from Twitter', 'Scrap from a existed file'),
                      help="Choose a way of scraping, either Scrap directly from twitter or from a existed file .")

    if choice == 'Scrap directly from Twitter':
        options = st.multiselect(
            "Select criteria's of search : ",
            ['Keyword', 'Limit', 'Username', 'Language', 'Since', 'Until'],
            ['Keyword', 'Limit'],
            help="In this section, you can select multiple criteria to customize your search")
        st.subheader('Scrap directly from Twitter')
        with st.form("my_form"):
            st.write("Fill the criteria of  search :")
            keyword = st.text_input('Input Keyword for Screep', value='SPACs', max_chars=15)
            limit = st.number_input('Input Limit for Screep', 10, step=10)
            if "Username" in options:
                user_name = st.text_input('Input Username for Screep', value='TheStreet', max_chars=15)

            if "Language" in options: #it return tweets in all languages!
                language = st.text_input('Input Language of tweets', value='en', max_chars=4)

            # if "Translate" in options:
            #     translate = st.text_input('Input Specific Language to translate tweets into', value='fr', max_chars=4)
            if "Since" in options:
                since = st.date_input('Input Start date of scraping')
            if "Until" in options:
                until = st.date_input('Input End date of scraping')


            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
        if submitted:
            if keyword == "" or limit == "":
                st.error("Attention, it seems that the field Keyword or limit is empty! Try to fill it ...")
            if keyword != "" and limit != "":
                st.subheader("Loading data : ")
                with st.spinner('Loading data in progress...wait for it!'):

                    df = TwintC(keyword,limit,user_name,language,since,until)


                    st.write("This section contain top 3 recent tweets according to search criteria")
                    st.table(df[['tweet','username']].head(3))
                    st.write("In this section, you get a dataframe that contain tweets according to search criteria")
                    st.write(df)
                    st.success("Scrap Tweets Successfully done!")
                    col1,col8 = st.columns((8,1))
                    with col1:
                        st.markdown(get_Csv_download_link(df), unsafe_allow_html=True)
                    with col8:
                        st.markdown(get_table_download_link(df), unsafe_allow_html=True)






    else:
        st.write('Scrap from a existed file')
        label = 'upload a excel file'
        type = ['xlsx']
        accept_multiple_files = False

        upload_file = st.file_uploader(label=label, type=type, accept_multiple_files=accept_multiple_files)

        if upload_file is not None:
            with st.spinner('Reading Data..'):
                df = pd.read_excel(upload_file)

            st.markdown("File Preview")
            st.write(df)


def get_Csv_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href1 = f'<a href="data:file/csv;base64,{b64}" download="extractCSV.csv">Download csv file</a>'
    return href1

def to_excel(df):

    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1') # <--- here
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" Download="ExtractExcel.xlsx">Download Excel file</a>' # decode b'abc' => abc

def TwintC(keyword,limit,user_name,language,since,until):
    # config
    c = twint.Config()
    c.Search = keyword
    c.Limit = limit
    c.Popular_tweets = True
    c.Since = since
    c.Pandas = True
    c.Hide_output = True
    if user_name != "":
        c.Username = user_name

    # if language != "":       #Doesnt work it return all language
    #     c.Lang = language
    #     print(c.Lang)

    # if translate != "":      #it stop working 29 days ago
    #     c.Translate = True
    #     c.TranslateSrc = "en"
    #     c.TranslateDest = "it"
    if since != "" and until != "":
        if since > until:
            st.error('Attention , It seems like start date bigger than end date')
        else:
            c.Since = str(since)
            c.Until = str(until)
    # run
    twint.run.Search(c)
    df = twint.storage.panda.Tweets_df
    return df


def dataFrame():
    global df
    return df
