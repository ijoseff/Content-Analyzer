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

    st.title("N-Grams Frequency Counter")
    st.header('Extract the most frequent words from your content.')
