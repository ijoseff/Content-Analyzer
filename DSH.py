#app.py
import NER
import TP
import WC
import TS
import streamlit as st
from PIL import Image

PAGES = {'Named Enity Recognition': NER, 'Topic Modeling': TP, 'Word Cloud Generation': WC, 'Text Summarization': TS}

image = Image.open('photo1.png')
st.sidebar.image(image, caption = ' ', use_column_width = True)

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]

page.app()


