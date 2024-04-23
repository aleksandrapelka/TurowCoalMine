import streamlit as st
from data.data import get_statistics_data, get_imagery_collections
from maps.indexes import get_image, classify_image, add_image_to_map, detect_chages
from maps.charts import create_pie_chart
from io import StringIO

st.set_page_config(page_title="Change detection", page_icon="💧", layout="wide")


indexes = ['NDWI_I','NDWI_II','NDVI','MSAVI2','EVI', 'NMDI','MSI']
index_name = st.selectbox('Choose index:', (indexes))

stats = get_statistics_data(index_name)
collections = get_imagery_collections(index_name)
date = stats['daily']['Date']

date1 = st.selectbox('Choose first date:', (date))
date2 = st.selectbox('Choose second date:', (date))

button_clicked = st.button('Generate')

if button_clicked:
    collection = collections['daily_collection']
    image1 = get_image(index_name, str(date1), collection)
    image2 = get_image(index_name, str(date2), collection)
   
    changes = detect_chages(image1, image2)
    
    image1 = classify_image(index_name, image1)
    image2 = classify_image(index_name, image2)

    col1, col2, col3 = st.columns((1, 1, 1))
    with st.container():
        with col1:
            st.write('First image:', date1)
            add_image_to_map(image1, index_name, f'{index_name} {date1}')
        with col2:
            st.write('Second image:', date2)
            add_image_to_map(image2, index_name, f'{index_name} {date2}')
        with col3:
            st.write('Changes detection:')
            add_image_to_map(changes, 'changes', f'{index_name} changes {date1}-{date2}') 

    create_pie_chart(changes)
     

