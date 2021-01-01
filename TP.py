# Import
import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import base64

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import matplotlib.pyplot as plt
import plotly.express as px


def app():
    image = Image.open('photo1.png')
    st.image(image, caption = ' ', use_column_width = True)

    st.title("Topic Modeling")
    st.header('Searches group of words (i.e topic) in the content.')

    st.write('')

    no = st.slider('Select Number of Topics', 0, 50, 5)

    st.write('')

    no1 = st.slider('Select Number of Top Words per Topic', 0, 100, 20)

    st.write('')

    # Collects user input features into dataframe
    uploaded_file = st.file_uploader("Upload your input csv file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        contents = df

        tfidf = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')

        dtm = tfidf.fit_transform(df['Content'])

        nmf_model = NMF(n_components= no,random_state=42)

        nmf_model.fit(dtm)

        topic_results = nmf_model.transform(dtm)

        Topic = ['']
        Words = ['']

        for index,topic in enumerate(nmf_model.components_):
            Topic.append(f'Topic {index}')
            Words.append([tfidf.get_feature_names()[i] for i in topic.argsort()[- no1:]])

        output = pd.DataFrame(columns = ['Topic #', 'Top Words'])

        output['Topic #'] = Topic

        output['Top Words'] = Words

        st.title('Topic\'s Top Words:')

        st.write(output)

        def download_link(object_to_download, download_filename, download_link_text):
            
            if isinstance(object_to_download,pd.DataFrame):
                object_to_download = object_to_download.to_csv(index=False)

            # some strings <-> bytes conversions necessary here
            b64 = base64.b64encode(object_to_download.encode()).decode()

            return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

        st.write('')

        if st.button('Generate Topic\'s Top Words CSV File Download Link'):
            tmp_download_link = download_link(output, 'Topic\'s Top Words.csv', 'Click here to download your data!')
            st.markdown(tmp_download_link, unsafe_allow_html=True)

        st.write('')

        st.write('')

        df['Topic'] = topic_results.argmax(axis=1)

        df = df[['Content', 'Topic']]

        st.title('Content Topic Classification:')

        st.write(df)

        st.write('')

        if st.button('Generate Content Topic Classification CSV File Download Link'):
            tmp_download_link = download_link(df, 'Content Topic Classification.csv', 'Click here to download your data!')
            st.markdown(tmp_download_link, unsafe_allow_html=True)

        st.write('')

        st.write('')

        st.title('Content Topics Distribution:')

        select = st.selectbox('Visualization type', ['Bar plot', 'Pie chart'], key='1')
        sentiment_count = df['Topic'].value_counts()
        sentiment_count = pd.DataFrame({'Topic':sentiment_count.index, 'Frequency':sentiment_count.values})
        if st.checkbox("Show", False):
            st.markdown("### Frequency of Topics:")
            if select == 'Bar plot':
                fig = px.bar(sentiment_count, x='Topic', y='Frequency', color='Frequency', height=500)
                st.plotly_chart(fig)
            else:
                fig = px.pie(sentiment_count, values='Frequency', names='Topic')
                st.plotly_chart(fig)

    else:
        st.text('')
