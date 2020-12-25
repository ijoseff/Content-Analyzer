# Import
import streamlit as st
from PIL import Image
import pandas as pd
import spacy
import base64
import re

def app():
    image = Image.open('photo1.png')
    st.image(image, caption = ' ', use_column_width = True)

    st.title("Topic Modeling")
    st.header('Searches group of words (i.e topic) from the contents.')

    # Collects user input features into dataframe
    uploaded_file = st.file_uploader("Upload your input CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        contents = df['Content']
