import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import os
from wordcloud import WordCloud


st.title("Suicide Data Analysis and Prediction")

st.markdown(
    """
    <style>
    .suicide-title {
        font-size: 108px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.write("")
st.write("")
st.write("")
st.write("")

data = pd.read_csv('123.csv')

# Create a container
container1 = st.container()
container2 = st.container()

# Add content to the container
with container1:
    st.header("Report")
    st.write("Getting the numbers")

    states = st.multiselect("Select States", data['State'].unique())
    st.write("")
    age = st.multiselect("Select Age group", data['Age_group'].unique())
    gender = st.radio("Select Gender", data["Gender"].unique())

    a = st.selectbox("More Info about victim", data['Type_code'].unique())
    filtered_data = data[data['Type_code'] == a]
    b = st.selectbox(a + " of Victim", filtered_data['Type'].unique())

    button_clicked = st.button("Get Data")

    if button_clicked:
        conditions = (data['Type_code'] == a) & \
                     (data['Gender'] == gender) & \
                     (data["Type"] == b) & \
                     (data['State'].isin(states))

        filtered_data_causes = data[conditions]
        total_suicides_causes = filtered_data_causes['Total'].sum()
        st.markdown(f"<h1 class='suicide-title'>{total_suicides_causes}</h1>", unsafe_allow_html=True)

st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")

with container2:
    st.header("Analysis")
    st.write("Anaysis of data")

    # Filter unique states
    states = data['State'].unique()

    # Sidebar - State selection
    selected_state = st.selectbox('Select State', states)

    # Filter data for the selected state
    state_data = data[data['State'] == selected_state]

    # Group data by year and calculate total suicides
    yearly_suicides = state_data.groupby('Year')['Total'].sum().reset_index()

    # Plot total suicides per year
    st.subheader(f'Total Suicides per Year in {selected_state}')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=yearly_suicides['Year'], y=yearly_suicides['Total'], mode='lines+markers', name='Total Suicides'))
    fig.update_layout(
        title=f'Total Suicides per Year in {selected_state}',
        xaxis_title='Year',
        yaxis_title='Total Suicides',
        hovermode='x',
        template='plotly_white'
    )
    st.plotly_chart(fig)

    # Filter unique Type_codes
    type_codes = data['Type_code'].unique()

    # Dropdown - Type_code selection
    selected_type_code = st.selectbox('Select Type_code', type_codes)

    # Filter unique types based on selected Type_code
    types = data[data['Type_code'] == selected_type_code]['Type'].unique()

    # Dropdown - Type selection
    selected_type = st.selectbox('Select Type', types)

    # Filter data for the selected Type_code and Type
    type_data = data[(data['Type_code'] == selected_type_code) & (data['Type'] == selected_type)]

    # Group data by year and calculate total suicides
    yearly_suicides_type = type_data.groupby('Year')['Total'].sum().reset_index()

    # Create a pie chart to visualize the distribution of suicides across different age groups
    suicides_by_age_group = type_data.groupby('Age_group')['Total'].sum()
    fig_pie = go.Figure(data=[go.Pie(labels=suicides_by_age_group.index, values=suicides_by_age_group.values)])
    fig_pie.update_layout(title=f'Distribution of Suicides by Age Group for {selected_type} ({selected_type_code})')
    st.plotly_chart(fig_pie)
