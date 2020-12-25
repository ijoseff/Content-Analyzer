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

    st.title("Word Cloud Generation")
    st.header('Create a collection, or cluster, of words depicted in different sizes from the content.')

    # Collects user input features into dataframe
    uploaded_file = st.file_uploader("Upload your input CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        contents = df['Content']

        # Remove punctuation
        df['Content'] = df['Content'].map(lambda x: re.sub('[,@#\.!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~!?]','', x))

        # Convert the contents to lowercase
        df['Content'] = df['Content'].map(lambda x: x.lower())

        # Print out the first rows of papers
        df['Content'].head()

        # Join the different titles together.
        long_string = ','.join(list(df['Content'].values))

        # Generate the word cloud
        wordcloud = WordCloud(background_color = 'white',
                            max_words = 200,
                            contour_width = 3,
                            contour_color = 'steelblue',
                            collocations = False, width=1000, height=500).generate(long_string)

        # Visualize the word cloud
        st.title('Result:')
        st.title('')
        st.image(wordcloud.to_image())

    else:
        st.text('')
