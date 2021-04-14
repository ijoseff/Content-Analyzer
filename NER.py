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

    st.title("Named-Entity Recognition")
    st.header('Extracts named-entity and its frequency in the content.')

    type = st.selectbox('Select Named Entity Type',['PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL'])
    st.write('Description: ', spacy.explain(type))

    st.write('')
    st.write('')

    # Collects user input features into dataframe
    uploaded_file = st.file_uploader("Upload your input CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file).dropna()
        
        contents = df['Content'].dropna()

        # Remove punctuation
        contents = contents.map(lambda x: re.sub('[,@#©\.!"#%\'()*+,./:;<=>?@[\\]^_`{|}~!?]','', x))

        nlp = spacy.load('en_core_web_sm-2.3.1')

        list = ['']

        for i in range(len(contents)):
            content = nlp(contents[i])
            list.append( [ent for ent in content.ents if ent.label_ == type ] )

        entities = []

        for i in range(len(list)):
            for j in list[i]:
                entities.append(j)
        
        freq = {}

        for j in entities: 
            if (str(j) in freq): 
                freq[str(j)] += 1
            else: 
                freq[str(j)] = 1
                
        def getList(dict):  
            return [*dict] 

        entity = getList(freq)

        output = pd.DataFrame(columns = ['Name', 'Frequency'])
        output['Name'] = entity

        frequency = []

        for i in output['Name']:
            j = len(contents[contents.str.contains(i)])
            frequency.append(j)

        output['Frequency'] = frequency
        output = output.sort_values(by='Frequency', ascending=False, ignore_index = True)

        st.title('Result:')

        st.markdown("### Top 10 Entity Mentions")
        fig = px.bar(output.head(10), x='Name', y='Frequency', color='Frequency', height=500, width = 1000)
        st.plotly_chart(fig)

        st.write('')

        st.markdown("### Entity Frequency Table")

        st.write('')

        st.write(output)

        def download_link(object_to_download, download_filename, download_link_text):
            
            if isinstance(object_to_download,pd.DataFrame):
                object_to_download = object_to_download.to_csv(index=False)

            # some strings <-> bytes conversions necessary here
            b64 = base64.b64encode(object_to_download.encode()).decode()

            return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

        st.write('')

        if st.button('Generate CSV File Download Link'):
            tmp_download_link = download_link(output, 'Entity - Frequency.csv', 'Click here to download your data!')
            st.markdown(tmp_download_link, unsafe_allow_html=True)

    else:
        st.text('')
