import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import json
import plotly.io as pio
st.set_page_config(layout="wide")
pio.renderers.default = 'browser'
db_host = 'sql12.freesqldatabase.com'
db_port = '3306'
db_name = 'sql12708926'
db_user = 'sql12708926'
db_password = '3p2AnmtVla'
connection_string = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = create_engine(connection_string)
query = "SELECT * FROM admissiondata"
df = pd.read_sql(query, engine)
st.title('Student Registration Data')
st.dataframe(df)
st.write('### Summary Statistics')
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="graph-container">', unsafe_allow_html=True)
    st.write('#### Distribution of Intermediate Marks')
    fig_hist = px.histogram(df, x='IntermediateMarks', nbins=20, title='Distribution of Intermediate Marks')
    fig_hist.update_layout(xaxis_title='Intermediate Marks', yaxis_title='Count')
    st.plotly_chart(fig_hist)
    status_counts = df['Status'].value_counts()
    campus_counts = df['RegisteredCampus'].value_counts()
    course_counts = df['Course'].value_counts()
    labels = list(df['Status'].unique()) + list(df['RegisteredCampus'].unique()) + list(df['Course'].unique())
    label_to_index = {label: idx for idx, label in enumerate(labels)}
    source = []
    target = []
    value = []
    status_to_campus_counts = df.groupby(['Status', 'RegisteredCampus']).size().reset_index(name='Count')
    for _, row in status_to_campus_counts.iterrows():
        source.append(label_to_index[row['Status']])
        target.append(label_to_index[row['RegisteredCampus']])
        value.append(row['Count'])
    campus_to_course_counts = df.groupby(['RegisteredCampus', 'Course']).size().reset_index(name='Count')
    for _, row in campus_to_course_counts.iterrows():
        source.append(label_to_index[row['RegisteredCampus']])
        target.append(label_to_index[row['Course']])
        value.append(row['Count'])
    fig_snakey = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels
        ),
        link=dict(
            source=source,
            target=target,
            value=value
        )
    )])
    fig_snakey.update_layout(width=700, height=600)
    st.write('### Sankey Diagram of Student Registrations')
    st.plotly_chart(fig_snakey)
    fig_violin = px.violin(df, x='Course', y='IntermediateMarks', points="all")
    fig_violin.update_layout(title='Violin Chart of Intermediate Marks by Course',
                    xaxis_title='Course',
                    yaxis_title='Intermediate Marks (Percentage)',
                    width=700, height=600)
    st.plotly_chart(fig_violin)
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="graph-container">', unsafe_allow_html=True)
    st.write('#### Sunburst Chart')
    fig_sunburst = px.sunburst(df, path=['Status', 'Gender', 'Course'], values='IntermediateMarks')
    st.plotly_chart(fig_sunburst)
    st.write('### Box Plot of Intermediate Marks by Course')
    fig_box = px.box(df, x='Course', y='IntermediateMarks', points="all",
                title='Box Plot of Intermediate Marks by Course',
                labels={'Course': 'Course', 'IntermediateMarks': 'Intermediate Marks (Percentage)'})
    fig_box.update_layout(width=800, height=600)
    st.plotly_chart(fig_box)
    fig_parallel = px.parallel_categories(df, dimensions=['Status', 'Course', 'Gender', 'AdmissionCategory'],
                             color='IntermediateMarks', color_continuous_scale=px.colors.sequential.Inferno)
    fig_parallel.update_layout(width=800, height=550)
    st.write('### Parallel Categories Plot')
    st.plotly_chart(fig_parallel)
    st.markdown('</div>', unsafe_allow_html=True)
st.write('### Scatter Plot Matrix')
fig_scatter = px.scatter_matrix(df,
                        dimensions=['IntermediateMarks', 'State', 'Gender'],
                        color='Course')
st.plotly_chart(fig_scatter)
