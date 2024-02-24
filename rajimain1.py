import pickle
import streamlit as st
import sqlite3
from passlib.hash import pbkdf2_sha256
import os

global_array=[]

def create_table():
    connection = sqlite3.connect('team.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movie_history (
            id INTEGER PRIMARY KEY,
            movie_name VARCHAR(255) NOT NULL
        )
    ''')

    connection.commit()
    connection.close()

# Function to insert search operation in a table
def insert_search(query):
    connection = sqlite3.connect('team.db')
    cursor = connection.cursor()

    cursor.execute("INSERT INTO movie_history (movie_name) VALUES (?)", (query,))

    connection.commit()
    connection.close()

# Function to retrieve search history
def get_search_history():
    connection = sqlite3.connect('team.db')
    cursor = connection.cursor()

    cursor.execute("SELECT movie_name FROM movie_history ORDER BY id DESC")
    history = [row[0] for row in cursor.fetchall()]

    connection.close()
    return history

def his_print():
    create_table()
    history = get_search_history()
    #sidebar
    with st.sidebar:
        st.header("HISTORY")
        if history:
            for query in history:
                st.write("🕒  ",query)
        else:
            st.write("No search history.")


#--------------------------------------------------------------------------------------------

# Function to create the login_info table
def create_users_table():
    conn = sqlite3.connect('team.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login_info (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            age INTEGER,
            email TEXT,
            mobile_number VARCHAR(225)
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert user into the login_info table
def insert_user(username, password, age, email, mobile_number):
    conn = sqlite3.connect('team.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO login_info (username, password, age, email, mobile_number)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, pbkdf2_sha256.hash(password), age, email, mobile_number))
    conn.commit()
    conn.close()

# Function to check credentials and set session state
def authenticate(username, password):
    conn = sqlite3.connect('team.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM login_info WHERE username=?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user and pbkdf2_sha256.verify(password, user[2]):
        return True
    else:
        return False


def log_in():

    # Create the login_info table
    create_users_table()

    # Sidebar navigation
    selected_page = st.sidebar.radio("Select a page", ["Login", "Signup", "log in history"])
    # Add a button to trigger the deletion
    with st.sidebar:
        if st.button('Delete log in info'):
            delete_database()

    if selected_page == "Login":
        st.header("Login")
        username_input_login = st.text_input("*Username:")
        password_input_login = st.text_input("*Password:", type="password")
        login_button = st.button("Login")

        if login_button:
            if not username_input_login or not password_input_login:
                st.error("Both username and password are required for login.")
            elif authenticate(username_input_login, password_input_login):
                st.success("Login successful!")
                global_array.insert(0,username_input_login)
                # st.success(f"Username '{username_input_login}' added to global array.")
            else:
                st.error("Invalid details please sign up before log in")

    elif selected_page == "Signup":
        st.header("Signup")
        username_input_signup = st.text_input("*Username:")
        password_input_signup = st.text_input("*Password:", type="password")
        age_input_signup = st.number_input("age", min_value=0)
        email_input_signup = st.text_input("Email")
        mobile_input_signup = st.text_input("Mobile Number")
        signup_button = st.button("Signup")

        if signup_button:
            if not username_input_signup or not password_input_signup:
                st.error("Both username and password are required for signup.")
            elif not authenticate(username_input_signup, password_input_signup):
                insert_user(username_input_signup, password_input_signup, age_input_signup, email_input_signup,
                            mobile_input_signup)
                st.success("Signup successful! You can now login.")
            else:
                st.warning("User already exists. Please choose a different username.")

    elif selected_page == "log in history":
        st.header("DETAILS")
        conn = sqlite3.connect('team.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM login_info')
        data = cursor.fetchall()
        conn.close()

        if data:
            st.table(data)
        else:
            st.warning("No users")


def display_users_list():
    condition=''
    for element in global_array:
        condition=element
        break
    conn = sqlite3.connect('team.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username,age,email,mobile_number FROM login_info WHERE username = ? ORDER BY id DESC LIMIT 1',(condition,))
    first_row = cursor.fetchone()
    conn.close()
    if first_row:
        hint=first_row[0]
        st.header(f"HI..{hint}")
        st.write(f"Name: {first_row[0]}")
        st.write(f"age: {first_row[1]}")
        st.write(f"email: {first_row[2]}")
        st.write(f"mobile number: {first_row[3]}")
    else:
        st.warning("No data")

# Function to delete the database
def delete_database():
    # Replace 'your_database.db' with your actual database file
    database_path = 'team.db'

    # Attempt to delete the database file
    try:
        os.remove(database_path)
        st.success("info deleted successfully.")
    except FileNotFoundError:
        st.error("not found")
    except Exception as e:
        st.error(f"Error: {e}")