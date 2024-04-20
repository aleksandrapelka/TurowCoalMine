import ee
import geemap.foliumap as geemap
import streamlit as st
import pandas as pd

# STATISTICS DATA
daily = pd.read_csv('data/daily_statistics_raw.csv')
weekly = pd.read_csv('data/weekly_statistics_raw.csv')
monthly = pd.read_csv('data/monthly_statistics_raw.csv')

daily_multihist = pd.read_csv('data/daily_multihist.csv')
weekly_multihist  = pd.read_csv('data/weekly_multihist.csv')
monthly_multihist  = pd.read_csv('data/monthly_multihist.csv')


def get_statistics_data(index_name):
    statistics = {
        'daily': daily[['Date', f'{index_name}_mean', f'{index_name}_median', f'{index_name}_mode']],
        'weekly': weekly[['Date', f'{index_name}_mean', f'{index_name}_median', f'{index_name}_mode']],
        'monthly': monthly[['Date', f'{index_name}_mean', f'{index_name}_median', f'{index_name}_mode']]
    }

    return statistics


# SPATIAL DATA
@st.cache_data
def ee_authenticate(token_name="EARTHENGINE_TOKEN"):
    geemap.ee_initialize(token_name=token_name)


ee_authenticate(token_name="EARTHENGINE_TOKEN")

selected_units = ee.FeatureCollection('users/aleksandra_pelka/selected_units')

def get_imagery_collections(index_name):
    collections = {
        'daily_collection': ee.ImageCollection('users/aleksandra_pelka/daily_indexes').select(index_name),
        'weekly_collection': ee.ImageCollection('users/aleksandra_pelka/weekly_indexes').select(index_name),
        'monthly_collection': ee.ImageCollection('projects/drought-monitoring-417414/assets/monthly_indexes').select(index_name)
    }

    return collections


