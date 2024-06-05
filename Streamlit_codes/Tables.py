import mysql.connector
import streamlit as st
import pandas as pd

def connect_to_database():
    try:
        connection = mysql.connector.connect(
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
        column_names = cursor.column_names
        data = []
        for row in cursor.fetchall():
            data.append(row)
        cursor.close()  # Close cursor after fetching all rows
        return data, column_names
    except mysql.connector.Error as error:
        print("Failed to fetch data from MySQL table: {}".format(error))
        return None, None

def main():
    st.set_page_config(layout="wide", page_title="Streamlit MySQL Database App", page_icon=":bar_chart:", initial_sidebar_state="expanded")
    st.title("Registered Students Coursewise")
    
    connection = connect_to_database()
    if connection:
        table_name = st.text_input("Enter table name:", "btech")  # Text input field for the table name, default value is "btech"
        data, column_names = fetch_data(connection, table_name) 
        if data and column_names:
            st.subheader(f"{table_name.capitalize()} Table:")
            df = pd.DataFrame(data, columns=column_names)
            st.dataframe(df.style.set_properties(**{'font-weight': 'bold', 'color': 'black', 
                                                     'border': '1px solid black', 'border-collapse': 'collapse',
                                                     'text-align': 'center', 'background-color': '#f0f0f0',
                                                     'height': '300px'})) 
        else:
            st.write(f"Failed to fetch {table_name} data from MySQL table.")

if __name__ == "__main__":
    main()
