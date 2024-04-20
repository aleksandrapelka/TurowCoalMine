import streamlit as st
from maps.indexes import add_image_to_map, get_classified_image
from maps.charts import create_line_chart, create_multi_year_chart, create_histogram, create_multi_year_histogram, multi_histogram
from data.data import get_statistics_data, get_imagery_collections, daily_multihist, weekly_multihist, monthly_multihist
from io import StringIO

st.set_page_config(page_title="NDVI", page_icon="💧", layout="wide")
index = 'NDVI'

tab1, tab2, tab3, tab4 = st.tabs(["📆 Daily", "📆 Weekly", "📆 Monthly", "📉 Statistics"]) #, "📊 Multi histogram"])
stats = get_statistics_data(index)
collections = get_imagery_collections(index)

with tab1:
   st.subheader(f"Daily {index} Time Series")
   selected_date = st.select_slider('Select date:', options=stats['daily']['Date'], value=stats['daily']['Date'][int(len(stats['daily']['Date'])/4)])

   col1, col2 = st.columns((1, 3))
   with st.container():
      with col1:
         st.dataframe(stats['daily'], hide_index=True, use_container_width=True, height=250)
         create_histogram(index, selected_date, collections['daily_collection'])
      with col2:
         image = get_classified_image(index, selected_date, collections['daily_collection'])
         add_image_to_map(image, index, f'{index} {selected_date}')
   
with tab2:
   st.subheader(f"Weekly {index} Time Series")
   selected_date = st.select_slider('Select date:', options=stats['weekly']['Date'], value=stats['weekly']['Date'][int(len(stats['weekly']['Date'])/4)])

   col1, col2 = st.columns((1, 3))
   with st.container():
      with col1:
         st.dataframe(stats['weekly'], hide_index=True, use_container_width=True, height=250)
         create_histogram(index, selected_date, collections['weekly_collection'])
      with col2:
         image = get_classified_image(index, selected_date, collections['weekly_collection'])
         add_image_to_map(image, index, f'{index} {selected_date}')

with tab3:
   st.subheader(f"Monthly {index} Time Series")
   selected_date = st.select_slider('Select date:', options=stats['monthly']['Date'], value=stats['monthly']['Date'][int(len(stats['monthly']['Date'])/4)])

   col1, col2 = st.columns((1, 3))
   with st.container():
      with col1:
         st.dataframe(stats['monthly'], hide_index=True, use_container_width=True, height=250)
         create_histogram(index, selected_date, collections['monthly_collection'])
      with col2:
         image = get_classified_image(index, selected_date, collections['monthly_collection'])
         add_image_to_map(image, index, f'{index} {selected_date}')

with tab4:
   with st.expander(f"💧 See {index} daily series statistics:"):
      create_line_chart(index, stats['daily'], 'Daily') 
      create_multi_year_histogram(index, 'mean', stats['daily'])
      create_multi_year_chart(index, 'mean', stats['daily']) 
      multi_histogram(index, daily_multihist)

   with st.expander(f"💧 See {index} weekly series statistics:"):
      create_line_chart(index, stats['weekly'], 'Weekly') 
      create_multi_year_histogram(index, 'mean', stats['weekly'])
      create_multi_year_chart(index, 'mean', stats['weekly'])
      multi_histogram(index, weekly_multihist)

   with st.expander(f"💧 See {index} monthly series statistics:"):
      create_line_chart(index, stats['monthly'], 'Monthly') 
      create_multi_year_histogram(index, 'mean', stats['monthly'])
      create_multi_year_chart(index, 'mean', stats['monthly'])   
      multi_histogram(index, monthly_multihist)    
 
# with tab5:
   # with st.spinner("Loading... This histogram needs a little more time (up to 10 minutes 🙄)"):
   #    multi_histogram(index, collections['daily_collection'])
   # with st.spinner("Loading... This histogram needs a little more time (up to 10 minutes 🙄)"):
   #    multi_histogram(index, collections['weekly_collection'])
   # with st.spinner("Loading... This histogram needs a little more time (up to 10 minutes 🙄)"):
   #    multi_histogram(index, collections['monthly_collection'])  
