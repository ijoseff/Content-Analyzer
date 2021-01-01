#app.py
import NER
import TP
import WC
import TS
import SA
import streamlit as st
from PIL import Image

PAGES = {'Named-Entity Recognition': NER, 'Topic Modeling': TP, 'Word Cloud Generation': WC, 'Text Summarization (Soon)': TS, 'Sentiment Analysis (Soon)': SA}

image = Image.open('photo2.png')
st.sidebar.image(image, caption = ' ', use_column_width = True)

st.sidebar.title('Navigation')

selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]

st.sidebar.write('')
st.sidebar.write('')

st.sidebar.title("Contribution")
st.sidebar.info('This web application is designed to help team of insight analyst in their explanatory data analysis.')

st.sidebar.title("About")
st.sidebar.warning('This app is maintained by Joseff Tan. You can learn about him or send bug report/suggestion at ijoseff.github.io')

page.app()
