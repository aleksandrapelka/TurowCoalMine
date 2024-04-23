import ee
import streamlit as st
import pandas as pd
import ast
import plotly.express as px
import data.data as data
from maps.indexes import get_image, projection
from maps.visualization import get_breaks, get_palette, get_labels
from io import StringIO

def create_line_chart(index_name, data, series_name):
   fig = px.line(data, x='Date', y=[f'{index_name}_mean', f'{index_name}_median', f'{index_name}_mode'], markers=True, color_discrete_sequence=get_palette()['line_chart'])
   fig.update_layout(title=f'{series_name} {index_name} Time Series', xaxis_title='Date', yaxis_title=None,
                   legend_title=None, legend=dict(orientation="h", yanchor="top", y=1.05))
   
   st.plotly_chart(fig, use_container_width=True)  

def create_multi_year_chart(index_name, statistic_name, data):
   df = pd.DataFrame(data)
   df['Date'] = pd.to_datetime(df['Date'])
   df['Day_of_Year'] = df['Date'].dt.dayofyear
   df['Year'] = df['Date'].dt.year

   fig = px.line(df, x='Day_of_Year', y=f'{index_name}_{statistic_name}', color='Year', markers=True, color_discrete_sequence=get_palette()['multi_year_chart'])
   fig.update_layout(title=f'Multi-Year {index_name} Time Series (mean)', xaxis_title='Day of Year', yaxis_title=None,
                  legend_title=None, legend=dict(orientation="h", yanchor="top", y=1.05))
   
   st.plotly_chart(fig, use_container_width=True)

def create_multi_year_histogram(index_name, statistic_name, data):
   data['Date'] = pd.to_datetime(data['Date'])
   data['Year'] = data['Date'].dt.year
   obs_per_year = data.groupby('Year').size().reset_index(name='obs_count')
   fig = px.bar(x=data['Date'], y=data[f'{index_name}_{statistic_name}'])
   fig.update_layout(title=f'Histogram of {index_name} (mean)', xaxis_title='Date', yaxis_title=None)
   fig.update_traces(marker_color=get_palette()['multi_year_histogram'])

   for i, row in obs_per_year.iterrows():
      fig.add_annotation(x=pd.to_datetime(str(row['Year'])), y=0,
                        text=f"Count: {row['obs_count']}", showarrow=False, xshift=10, yshift=300)
      
   st.plotly_chart(fig, use_container_width=True) 

def create_histogram(index_name, date, collection):
   image = get_image(index_name, date, collection)
   index_data = image.reduceRegion(reducer=ee.Reducer.toList(), geometry=data.selected_units.geometry(),scale=1000,maxPixels=1e12).get(index_name).getInfo()

   # Mapowanie wartości wskaznika na klasy
   df = pd.DataFrame({index_name: index_data})
   df['Class'] = pd.cut(df[index_name], bins=get_breaks()[index_name], labels=get_labels()[index_name], ordered=True)

   # Grupowanie danych według klas i zliczanie pikseli w każdej klasie
   class_counts = df['Class'].value_counts().reset_index()
   class_counts.columns = ['Class', 'Count']

   fig = px.bar(class_counts, x='Class', y='Count', color='Class', 
                color_discrete_sequence=get_palette()[index_name], 
                category_orders={'Class': get_labels()[index_name]}, height=350)
   fig.update_layout(title=f'Histogram of {index_name} (scale: 1000 m) - {date}', 
                     xaxis_title=None, yaxis_title=None, showlegend=False)

   st.plotly_chart(fig, use_container_width=True)


def get_image_classes(image, index_name):
   breaks = get_breaks()[index_name]
   image = image.reproject(crs=projection['crs'], crsTransform=projection['transform'])
   classes = []
   
   for i in range(len(breaks) - 1):
      image_class = image.gt(breaks[i]).And(image.lte(breaks[i+1])).rename(f'Class_{i+1}')
      image_class = image_class.reduceRegion(reducer=ee.Reducer.sum(), geometry=data.selected_units.geometry(), scale=1000)
      classes.append(image_class)

   return classes
   
def multi_histogram(index_name, collection):
   # collection = collection.select(index_name)
   # dates = collection.toList(collection.size()).map(lambda img: ee.Image(img).get('date')).getInfo()
   # result = []

   # for i, img_date in enumerate(dates):
   #    image = ee.Image(collection.toList(collection.size()).get(i))
   #    image_classes = get_image_classes(image, index_name)
   #    record = {'Date': img_date}
   #    for j, img_class in enumerate(image_classes):
   #       record[f'Class_{j+1}'] = img_class.getInfo().get(f'Class_{j+1}')
   #    result.append(record)

   # df = pd.DataFrame(result)

   list_of_dicts = []

   for _, dict in collection[index_name].items():
      list_of_dicts.append(ast.literal_eval(dict))

   df = pd.DataFrame(list_of_dicts)

   fig = px.bar(df, x='Date', y=df.columns[1:], barmode='stack', color_discrete_sequence=get_palette()[index_name])
   fig.update_layout(title=f'Multi-Year Histogram of {index_name} (scale: 1000 m)', 
                     xaxis_title=None, yaxis_title=None, showlegend=False)

   st.plotly_chart(fig, use_container_width=True)


def create_pie_chart(changes):
    positive = changes.updateMask(changes.eq(3)).rename('positive')
    negative = changes.updateMask(changes.eq(2)).rename('negative')
    strong_positive = changes.updateMask(changes.eq(4)).rename('strong_positive')
    strong_negative = changes.updateMask(changes.eq(1)).rename('strong_negative')
    total_changes = changes.updateMask(changes).rename('total_changes')
    
    negative = negative.reduceRegion(reducer=ee.Reducer.count(), geometry=data.selected_units.geometry(), scale=100).get('negative').getInfo()
    positive = positive.reduceRegion(reducer=ee.Reducer.count(), geometry=data.selected_units.geometry(), scale=100).get('positive').getInfo()
    strong_negative = strong_negative.reduceRegion(reducer=ee.Reducer.count(), geometry=data.selected_units.geometry(), scale=100).get('strong_negative').getInfo()
    strong_positive = strong_positive.reduceRegion(reducer=ee.Reducer.count(), geometry=data.selected_units.geometry(), scale=100).get('strong_positive').getInfo()
    total_changes = total_changes.reduceRegion(reducer=ee.Reducer.count(), geometry=data.selected_units.geometry(), scale=100).get('total_changes').getInfo()

    if total_changes > 0:
        percent_positive = (positive / total_changes) * 100
        percent_negative = (negative / total_changes) * 100
        percent_strong_positive = (strong_positive / total_changes) * 100
        percent_strong_negative = (strong_negative / total_changes) * 100
    else:
        percent_positive = 0
        percent_negative = 0
        percent_strong_positive = 0
        percent_strong_negative = 0
    
    df = pd.DataFrame({'tip': ['Strong negative changes', 'Negative changes', 'Positive changes', 'Strong positive changes'], 'percent': [percent_strong_negative, percent_negative, percent_positive, percent_strong_positive],'color': get_palette()['changes']})

    fig = px.pie(df, values='percent', names='tip', color='color', title='Changes', color_discrete_sequence=get_palette()['changes'])
    st.plotly_chart(fig, use_container_width=True)   

   #  st.write('percent_positive:', percent_positive)
   #  st.write('percent_negative:', percent_negative)
   #  st.write('percent_positive:', percent_strong_positive)
   #  st.write('percent_negative:', percent_strong_negative)
   #  st.write('total_changes:', total_changes)

    
def export():
   indexes_names = ['NDWI_I','NDWI_II','NDVI','MSAVI2','EVI','NMDI','MSI']
   res = {}
   collection = ee.ImageCollection('users/aleksandra_pelka/daily_indexes')
   st.write(collection.first().bandNames().getInfo())
   for index_name in indexes_names:
      collection = collection.select(index_name)
      dates = collection.toList(collection.size()).map(lambda img: ee.Image(img).get('date')).getInfo()
      result = []

      for i, img_date in enumerate(dates):
         image = ee.Image(collection.toList(collection.size()).get(i))
         image_classes = get_image_classes(image, index_name)
         record = {'Date': img_date}
         for j, img_class in enumerate(image_classes):
            record[f'Class_{j+1}'] = img_class.getInfo().get(f'Class_{j+1}')
         res[index_name] = result.append(record)

   df = pd.DataFrame(res)

   st.download_button(
    label="Pobierz plik CSV",
    data=df.to_csv().encode('utf-8'),
    file_name='daily_multihist.csv',
    mime='text/csv'
   )
   #file_name = f'multihist{collection}.csv'
   #df.to_csv(file_name, index=False)
 
