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

    st.title("Text Summarization")
    st.header('Generate summary from all the texts in the contents.')
