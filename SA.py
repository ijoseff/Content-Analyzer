# Import
import streamlit as st
from PIL import Image
import pandas as pd
import spacy
import base64
import re
from wordcloud import WordCloud

def app():
    image = Image.open('photo1.png')
    st.image(image, caption = ' ', use_column_width = True)

    st.title("Sentiment Analysis")
    st.header('Analyze positive, neutral and negative statements in the content.')
