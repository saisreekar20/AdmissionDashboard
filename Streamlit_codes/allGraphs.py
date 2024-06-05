import pymysql
import streamlit as st
import pandas as pd
import plotly.express as px

def connect_to_database():
    try:
        connection = pymysql.connect(
            host=" sql12.freesqldatabase.com",
            user="sql12711951",
            password="XGnGcadYwE",
            database="sql12711951"
            
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except mysql.connector.Error as error:
        print("Failed to connect to MySQL database: {}".format(error))
        return None

def fetch_data(connection, table_name):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM {}".format(table_name))
        data = cursor.fetchall()
        return data
    except mysql.connector.Error as error:
        print("Failed to fetch data from MySQL table: {}".format(error))
        return None

def main():
    st.set_page_config(layout="wide", page_title="Admission Dashboard", page_icon=":bar_chart:", initial_sidebar_state="expanded")
    st.title("Admission Dashboard")
    search_name = st.text_input("Search Name", "")
    row1_filter_col, row2_filter_col, row3_filter_col, row4_filter_col, row5_filter_col = st.columns(5)
    with row1_filter_col:
        assigned_counsellor = st.selectbox("Assigned Counsellor", ["All", "Kishore", "Sreekar", "Praveen"])
    with row2_filter_col:
        gender = st.selectbox("Gender", ["All", "Male", "Female"])
    with row3_filter_col:
        course = st.selectbox("Course", ["All", "B.Tech", "BBA", "BSC"])
    with row4_filter_col:
        campus = st.selectbox("Campus", ["All", "Vizianagaram campus", "PKD campus", "Bhuvaneshwar campus"])
    with row5_filter_col:
        status = st.selectbox("Status", ["All", "Accepted", "Rejected", "Pending"])   
    connection = connect_to_database()
    if connection:
        table_name = "admissiondata"
        data = fetch_data(connection, table_name) 
        if data:
            st.write("Data from MySQL Table:")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM {}".format(table_name))
            column_names = cursor.column_names
            df = pd.DataFrame(data, columns=column_names)
            if assigned_counsellor != "All":
                df = df[df['Assign_to_Counsellor'] == assigned_counsellor]
            if gender != "All":
                df = df[df['Gender'] == gender]
            if course != "All":
                df = df[df['Course'] == course]
            if campus != "All":
                df = df[df['Registered_Campus'] == campus]
            if status != "All":
                df = df[df['Status'] == status]
            if search_name:
                df = df[df['RegisteredName'].str.contains(search_name, case=False)]          
            st.write("Filtered Dataframe:")
            st.dataframe(df) 
            if not df.empty:
                status_counts = df['Status'].value_counts()
                course_counts = df['Course'].value_counts()               
                st.subheader("Number of Applications:")
                col1, col2, col3 = st.columns(3)  # Create three columns
                with col1:
                    accepted_placeholder = st.empty()
                with col2:
                    rejected_placeholder = st.empty()
                with col3:
                    pending_placeholder = st.empty()

                accepted_placeholder.markdown('<div style="width:100px;height:100px;background-color:#f8f9fa;color:#000000;text-align:center;border-radius:5px;font-size:16px;display:flex;flex-direction:column;justify-content:center"><div>Accepted</div><div style="font-size:50px;line-height:1.2">' + str(status_counts.get('Accepted', 0)) + '</div></div>', unsafe_allow_html=True)
                rejected_placeholder.markdown('<div style="width:100px;height:100px;background-color:#f8f9fa;color:#000000;text-align:center;border-radius:5px;font-size:16px;display:flex;flex-direction:column;justify-content:center"><div>Declined</div><div style="font-size:50px;line-height:1.2">' + str(status_counts.get('Declined', 0)) + '</div></div>', unsafe_allow_html=True)
                pending_placeholder.markdown('<div style="width:100px;height:100px;background-color:#f8f9fa;color:#000000;text-align:center;border-radius:5px;font-size:16px;display:flex;flex-direction:column;justify-content:center"><div>Pending</div><div style="font-size:50px;line-height:1.2">' + str(status_counts.get('Pending', 0)) + '</div></div>', unsafe_allow_html=True)

                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.subheader("Bar Plot of Status")
                    bar_fig = px.bar(x=status_counts.index, y=status_counts.values, labels={'x':'Status', 'y':'Count'},
                                     title='Bar Plot of Status', color=status_counts.index)
                    st.plotly_chart(bar_fig, use_container_width=True)   
                    st.subheader("Count Plot of Courses")
                    count_plot_courses = px.bar(x=course_counts.index, y=course_counts.values, labels={'x':'Course', 'y':'Count'},
                                   title='Count Plot of Courses', color=course_counts.index)
                    st.plotly_chart(count_plot_courses, use_container_width=True) 
                    fig_boxplot_marks = px.box(df, x='Status', y='IntermediateMarks', title='Box Plot of Intermediate Marks Grouped by Status')
                    fig_boxplot_marks.update_yaxes(range=[0, 100])
                    st.plotly_chart(fig_boxplot_marks, use_container_width=True)           
                with col2:
                    st.subheader("Pie Chart of Gender Distribution")
                    gender_counts = df['Gender'].value_counts()
                    pie_fig = px.pie(names=gender_counts.index, values=gender_counts.values, title='Pie Chart of Gender Distribution')
                    st.plotly_chart(pie_fig, use_container_width=True)                  
                    st.subheader("Count Plot of Status")
                    count_plot_status = px.bar(x=status_counts.index, y=status_counts.values, labels={'x':'Status', 'y':'Count'},
                                   title='Count Plot of Status', color=status_counts.index)
                    st.plotly_chart(count_plot_status, use_container_width=True) 
                    st.subheader("Count Plot of Gender and Course")
                    gender_course_counts = df.groupby(['Gender', 'Course']).size().reset_index(name='Count')
                    gender_course_plot = px.bar(gender_course_counts, x='Course', y='Count', color='Gender', barmode='group',
                                                labels={'x':'Course', 'y':'Count'}, title='Count Plot of Gender and Course')
                    st.plotly_chart(gender_course_plot, use_container_width=True)    
                with col3:
                    st.subheader("Count Plot of Assigned Counsellors")
                    counsellor_counts = df['AssignToCounsellor'].value_counts()
                    counsellor_plot = px.bar(x=counsellor_counts.index, y=counsellor_counts.values, labels={'x':'Counsellor', 'y':'Count'},
                                   title='Count Plot of Assigned Counsellors', color=counsellor_counts.index)
                    st.plotly_chart(counsellor_plot, use_container_width=True)           
                    st.subheader("Count Plot of Campuses")
                    campus_counts = df['RegisteredCampus'].value_counts()
                    campus_plot = px.bar(x=campus_counts.index, y=campus_counts.values, labels={'x':'Campus', 'y':'Count'},
                                   title='Count Plot of Campuses', color=campus_counts.index)
                    st.plotly_chart(campus_plot, use_container_width=True)
                    fig_hist_fee = px.histogram(df, x='RegistrationFee', color='Status',
                            title='Histogram of Registration_Fee')
                    st.plotly_chart(fig_hist_fee, use_container_width=True) 
            else:
                st.write("No records found for the applied filters.")
        else:
            st.write("Failed to fetch data from MySQL table.")

if __name__ == "__main__":
    main()
