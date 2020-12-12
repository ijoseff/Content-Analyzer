# Import
import streamlit as st
import pandas as pd
import spacy
import base64

st.title("NLP Content Analyzer")
st.header('This application extracts entity and its frequency in the contents 🕵🏻‍♂️')

type = st.selectbox('Select Named Entity Type',['PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL'])
st.write('Description: ', spacy.explain(type))

# Collects user input features into dataframe
uploaded_file = st.file_uploader("Upload your input CSV file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    contents = df['Content']

    label = 'PERSON'

    nlp = spacy.load('en_core_web_sm')

    list = ['']

    for i in range(len(contents)):
        content = nlp(contents[i])
        list.append( [ent for ent in content.ents if ent.label_ == type ] )

    entities = []

    for i in range(len(list)):
        for j in list[i]:
            entities.append(j)
    
    entity = []
    count = []


    freq = {}

    for j in entities: 
        if (str(j) in freq): 
            freq[str(j)] += 1
        else: 
            freq[str(j)] = 1

    for key, value in freq.items():
        entity.append(key), count.append(value)

    
    output = pd.DataFrame(columns = ['Name', 'Frequency'])
    output['Name'] = entity


    frequency = []

    for i in output['Name']:
        j = len(contents[contents.str.contains(i)])
        frequency.append(j)


    output['Frequency'] = frequency
    output = output.sort_values(by='Frequency', ascending=False, ignore_index = True)

    st.sidebar.header('Result:')
    st.sidebar.write(output)


    def download_link(object_to_download, download_filename, download_link_text):
        
        if isinstance(object_to_download,pd.DataFrame):
            object_to_download = object_to_download.to_csv(index=False)

        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()

        return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'


    if st.sidebar.button('Generate CSV File Download Link'):
        tmp_download_link = download_link(output, 'Entity - Frequency.csv', 'Click here to download your data!')
        st.sidebar.markdown(tmp_download_link, unsafe_allow_html=True)


else:
    st.text('Data Science Hub ❤')