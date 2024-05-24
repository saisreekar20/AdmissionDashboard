import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go

# Configure the page
st.set_page_config(layout="wide")
pio.renderers.default = 'browser'

# Database connection settings
db_host = 'sql12.freesqldatabase.com'
db_port = '3306'
db_name = 'sql12708926'
db_user = 'sql12708926'
db_password = '3p2AnmtVla'
connection_string = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = create_engine(connection_string)

# Function to load data based on selected table
def load_data(table_name):
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, engine)
    return df

# Dropdown menu to select dataset
table_options = ['btech', 'bba', 'bsc']
selected_table = st.selectbox('Select dataset to display:', table_options, index=0)
df = load_data(selected_table)

# Display the dataframe
st.title(f'Student Registration Data: {selected_table.upper()}')
st.dataframe(df)

# Plot: Application Status Distribution
status_counts = df["Status"].value_counts()
fig1 = px.bar(status_counts, x=status_counts.index, y=status_counts.values, 
              labels={'x': 'Status', 'y': 'Number of Applications'}, 
              title='Application Status Distribution')

# Plot: Sankey Diagram for Gender, Department, Registered Campus
sankey_data = df.groupby(['Gender', 'Department', 'RegisteredCampus']).size().reset_index(name='count')
labels = list(sankey_data['Gender'].unique()) + list(sankey_data['Department'].unique()) + list(sankey_data['RegisteredCampus'].unique())
gender_to_id = {gender: i for i, gender in enumerate(sankey_data['Gender'].unique())}
dept_to_id = {dept: i + len(gender_to_id) for i, dept in enumerate(sankey_data['Department'].unique())}
campus_to_id = {campus: i + len(gender_to_id) + len(dept_to_id) for i, campus in enumerate(sankey_data['RegisteredCampus'].unique())}

sources = [gender_to_id[gender] for gender in sankey_data['Gender']] + [dept_to_id[dept] for dept in sankey_data['Department']]
targets = [dept_to_id[dept] for dept in sankey_data['Department']] + [campus_to_id[campus] for campus in sankey_data['RegisteredCampus']]
values = list(sankey_data['count']) + list(sankey_data['count'])

fig2 = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values
    )
)])
fig2.update_layout(title_text="Sankey Diagram: Flow of Students from Gender to Department to Campus", font_size=10)

# Display two graphs in a row
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1)
with col2:
    st.plotly_chart(fig2)

# Additional Plots
fig3 = px.box(df, x='Status', y='IntermediateMarks', 
              title='Distribution of Intermediate Marks by Status', 
              color='Status')
fig4 = px.scatter(df, x='RegisteredCampus', y='IntermediateMarks', 
                  color='RegisteredCampus', size='IntermediateMarks', 
                  hover_data=['RegisteredName'], 
                  title='Intermediate Marks vs. Registered Campus')

fig5 = px.sunburst(df, path=['Gender', 'Department', 'RegisteredCampus'], 
                   title='Sunburst Chart of Gender, Department, and Registered Campus',
                   hover_data=['RegisteredName'],
                   color_continuous_scale='RdBu')
fig6 = px.treemap(df, path=['RegisteredCampus', 'Department', 'Gender'], values='IntermediateMarks',
                  title='Treemap of Campus, Department, and Gender',
                  color='IntermediateMarks', hover_data=['RegisteredName'],
                  color_continuous_scale='Viridis')

col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(fig3)
with col4:
    st.plotly_chart(fig4)

col5, col6 = st.columns(2)
with col5:
    st.plotly_chart(fig5)
with col6:
    st.plotly_chart(fig6)

fig7 = px.parallel_categories(df, dimensions=['Status', 'Gender', 'Department', 'RegisteredCampus'],
                              color='IntermediateMarks', color_continuous_scale=px.colors.sequential.Inferno,
                              title='Parallel Categories Diagram')
fig8 = px.violin(df, y='IntermediateMarks', x='Department', box=True, points='all',
                 title='Violin Plot of Intermediate Marks by Department',
                 color='Department')

col7, col8 = st.columns(2)
with col7:
    st.plotly_chart(fig7)
with col8:
    st.plotly_chart(fig8)

avg_marks_dept = df.groupby('Department')['IntermediateMarks'].mean().reset_index()
fig9 = px.bar(avg_marks_dept, x='Department', y='IntermediateMarks', 
              title='Average Intermediate Marks by Department',
              labels={'IntermediateMarks': 'Average Intermediate Marks', 'Department': 'Department'})

fig10 = px.strip(df, x='Department', y='IntermediateMarks', color='Gender', 
                 title='Strip Plot of Intermediate Marks by Department and Gender',
                 labels={'IntermediateMarks': 'Intermediate Marks', 'Department': 'Department'})

col9, col10 = st.columns(2)
with col9:
    st.plotly_chart(fig9)
with col10:
    st.plotly_chart(fig10)

fig11 = px.line_polar(avg_marks_dept, r='IntermediateMarks', theta='Department', line_close=True,
                      title='Average Marks across Different Departments')

sankey_data = df.groupby(['Gender', 'Department', 'RegisteredCampus']).size().reset_index(name='count')
labels = list(sankey_data['Gender'].unique()) + list(sankey_data['Department'].unique()) + list(sankey_data['RegisteredCampus'].unique())
gender_to_id = {gender: i for i, gender in enumerate(sankey_data['Gender'].unique())}
dept_to_id = {dept: i + len(gender_to_id) for i, dept in enumerate(sankey_data['Department'].unique())}
campus_to_id = {campus: i + len(gender_to_id) + len(dept_to_id) for i, campus in enumerate(sankey_data['RegisteredCampus'].unique())}

sources = [gender_to_id[gender] for gender in sankey_data['Gender']] + [dept_to_id[dept] for dept in sankey_data['Department']]
targets = [dept_to_id[dept] for dept in sankey_data['Department']] + [campus_to_id[campus] for campus in sankey_data['RegisteredCampus']]
values = list(sankey_data['count']) + list(sankey_data['count'])

fig12 = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values
    )
)])
fig12.update_layout(title_text="Sankey Diagram: Flow of Students from Gender to Department to Campus", font_size=10)

col11, col12 = st.columns(2)
with col11:
    st.plotly_chart(fig11)
with col12:
    st.plotly_chart(fig12)
