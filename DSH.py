#app.py
import NER
import TP
import WC
import TS
import SA
import streamlit as st
from PIL import Image

PAGES = {'Named-Entity Recognition': NER, 'Topic Modeling (Fixing)': TP, 'Word Cloud Generation': WC, 'Text Summarization (Soon!)': TS, 'Sentiment Analysis (Soon!)': SA}

image = Image.open('photo1.png')
st.sidebar.image(image, caption = ' ', use_column_width = True)

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]

page.app()
