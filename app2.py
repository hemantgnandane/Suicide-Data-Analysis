import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
st.title("Suicide Data Analysis")

data = pd.read_csv('123.csv')

container1 = st.container()

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

container2 = st.container()




with container2:
    st.header("Analysis")
    st.write("Analysis of data")

    selected_state = st.selectbox('Select State', data['State'].unique())

    state_data = data[data['State'] == selected_state]

    yearly_suicides = state_data.groupby('Year')['Total'].sum().reset_index()



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

    selected_type_code = st.selectbox('Select Type_code', data['Type_code'].unique())

    types = data[data['Type_code'] == selected_type_code]['Type'].unique()

    selected_type = st.selectbox('Select Type', types)

    type_data = data[(data['Type_code'] == selected_type_code) & (data['Type'] == selected_type)]

    yearly_suicides_type = type_data.groupby('Year')['Total'].sum().reset_index()

    suicides_by_age_group = type_data.groupby('Age_group')['Total'].sum()
    fig_pie = go.Figure(data=[go.Pie(labels=suicides_by_age_group.index, values=suicides_by_age_group.values)])
    fig_pie.update_layout(title=f'Distribution of Suicides by Age Group for {selected_type} ({selected_type_code})')
    st.plotly_chart(fig_pie)





# Load data from CSV file
data = pd.read_csv("123.csv")

label_encoders = {}
for column in ['State', 'Type_code', 'Type', 'Gender', 'Age_group']:
    label_encoders[column] = LabelEncoder()
    data[column] = label_encoders[column].fit_transform(data[column])

X = data.drop(columns=['Total'])
y = data['Total']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

knn_model = KNeighborsClassifier(n_neighbors=3)
knn_model.fit(X_train, y_train)

y_pred = knn_model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
