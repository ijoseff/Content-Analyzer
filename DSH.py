# Import
import streamlit as st
from PIL import Image
import re
import pandas as pd
import spacy
import base64



image = Image.open('photo1.png')
st.image(image, caption = ' ', use_column_width = True)

st.title("NLP Content Analyzer")
st.header('This application extracts entity and its frequency in the contents 🕵🏻‍♂️')

type = st.selectbox('Select Named Entity Type',['PERSON - People, including fictional.', 'NORP - Nationalities or religious or political groups.', 'FAC - Buildings, airports, highways, bridges, etc.', 'ORG - Companies, agencies, institutions, etc.', 'GPE - Countries, cities, states.', 'LOC - Non-GPE locations, mountain ranges, bodies of water.', 'PRODUCT - Objects, vehicles, foods, etc. (Not services.)', 'EVENT - Named hurricanes, battles, wars, sports events, etc.', 'WORK OF ART - Titles of books, songs, etc.', 'LAW - Named documents made into laws.', 'LANGUAGE - Any named language.', 'DATE - Absolute or relative dates or periods.', 'TIME - Times smaller than a day.', 'PERCENT - Percentage, including %', 'MONEY - Monetary values, including unit.', 'QUANTITY - Measurements, as of weight or distance.', 'ORDINAL - first, second, etc.', 'CARDINAL - Numerals that do not fall under another type.'])

# Collects user input features into dataframe
uploaded_file = st.file_uploader("Upload your input CSV file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    contents = df['Content']
    
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

    st.subheader('Result:')
    st.write(output)


    def download_link(object_to_download, download_filename, download_link_text):
        
        if isinstance(object_to_download,pd.DataFrame):
            object_to_download = object_to_download.to_csv(index=False)

        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()

        return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'


    if st.button('Generate CSV File Download Link'):
        tmp_download_link = download_link(output, 'Entity - Frequency.csv', 'Click here to download your data!')
        st.markdown(tmp_download_link, unsafe_allow_html=True)


else:
    st.text('Data Science Hub ❤')
