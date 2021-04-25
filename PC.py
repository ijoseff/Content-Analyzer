# Import
import streamlit as st
from PIL import Image
import pandas as pd
import spacy
import base64
import re
import plotly.express as px

def app():

    image = Image.open('photo1.png')
    st.image(image, caption = ' ', use_column_width = True)

    st.title("POS Frequency Counter")
    st.header('Extract the most frequent POS tags from the content.')

    st.markdown('[Download Sample Data](https://drive.google.com/uc?export=download&id=1Wq53CzQ4THFUPQpGYF4rHo6_HhxbH42I) 📥')
    
    st.write('')

    type = st.selectbox('Select Part-of-Speech Tag',['ADP', 'ADJ', 'NOUN', 'NUM', 'SYM', 'PROPN', 'VERB'])
    st.write('Description: ', spacy.explain(type))

    st.write('')
    st.write('')

    # Collects user input features into dataframe
    uploaded_file = st.file_uploader("Upload your input CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        st.write('')

        st.markdown('### Data Table')

        st.write('')

        st.dataframe(df)

        st.write('')

        st.markdown('### Data Description')

        st.write('')

        st.write(df.describe(include = 'all'))

        st.write('')

        st.markdown('### Please select a column name in the table ❗')

        column = st.selectbox('Data in the column must be in proper text format',df.columns)
        
        contents = df[column].dropna()

        # Remove punctuation
        contents = contents.map(lambda x: re.sub('[,@#©\.!"#%\'()*+,./:;<=>?@[\\]^_`{|}~!?]','', x))

        ######

        nlp = spacy.load('en_core_web_sm-2.3.1')

        list = []

        for i in range(len(contents)):
            list.append(contents[i])

        all_text = ' '.join(list)
        all_text

        docx = nlp(all_text)

        pos = [ token.text for token in docx if token.is_stop != True and token.is_punct !=True and token.pos_ == type]

        ######

        posz = []
        freqz = []

        def CountFrequency(my_list): 

            freq = {} 
            for j in my_list: 
                if (str(j) in freq): 
                    freq[str(j)] += 1
                else: 
                    freq[str(j)] = 1

            for key, value in freq.items():
                posz.append(key), freqz.append(value)
                print(key, value)

        CountFrequency(pos)

        ######

        pos_df = pd.DataFrame(columns = ['POS', 'Frequency'])
        pos_df.POS = posz
        pos_df.Frequency = freqz

        ######

        pos_df = pos_df.sort_values(by='Frequency', ascending=False, ignore_index = True)

        st.title('Result:')

        st.markdown("### Top 10 POS Mentions")
        fig = px.bar(pos_df.head(10), x='POS', y='Frequency', color='Frequency', height=500, width = 1000)
        st.plotly_chart(fig)

        st.write('')

        st.markdown("### POS Frequency Table")

        st.write('')

        st.write(pos_df)


        ######

        def download_link(object_to_download, download_filename, download_link_text):
            
            if isinstance(object_to_download,pd.DataFrame):
                object_to_download = object_to_download.to_csv(index=False)

            # some strings <-> bytes conversions necessary here
            b64 = base64.b64encode(object_to_download.encode()).decode()

            return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

        st.write('')

        if st.button('Generate CSV File Download Link'):
            tmp_download_link = download_link(pos_df, 'POS - Frequency.csv', 'Click here to download your data!')
            st.markdown(tmp_download_link, unsafe_allow_html=True)

    else:
        st.text('')
