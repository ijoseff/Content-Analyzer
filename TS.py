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
    st.header('This searches group of words (i.e topic) from a collection of documents that best represents the information in the collection.')