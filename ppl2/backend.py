import mysql.connector
import mysql.connector
import random
import string

# Create connection to MySQL server
def create_server_connection():
    connection = mysql.connector.connect(user="root",
                                         host="127.0.0.1",
                                         passwd="#Pranav16")
    return connection

# Create a database
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS user_info")
    cursor.close()

# Create connection to the database
def create_connection():
    connection = mysql.connector.connect(user="root",
                                         host="127.0.0.1",
                                         database="user_info",
                                         passwd="#Pranav16")
    return connection

# Drop the existing users table if it exists
def drop_table_if_exists(connection):
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    connection.commit()

# Create table in the database
def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL UNIQUE,
            random_number INT NOT NULL,
            random_characters VARCHAR(255) NOT NULL
        );
    """)
    connection.commit()

# Generate non-repetitive, case-sensitive random characters
def generate_random_characters(length):
    characters = list(string.ascii_letters + string.digits)
    random.shuffle(characters)
    return ''.join(characters[:length])

# Check if username or password already exists
def user_exists(connection, username, password):
    cursor = connection.cursor()
    cursor.execute("SELECT username, password FROM users WHERE username = %s OR password = %s", (username, password))
    return cursor.fetchall()

# Insert user into database
def insert_user(connection, username, password):
    if username == password:
        print("Username and password should not be the same.")
        return
    
    existing_users = user_exists(connection, username, password)
    if existing_users:
        for user in existing_users:
            if user[0] == username:
                print("Username already taken. Please choose a different one.")
            if user[1] == password:
                print("Password already taken. Please choose a different one.")
        return
    
    random_number = random.randint(10, 99)
    random_chars = generate_random_characters(random_number)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (username, password, random_number, random_characters) VALUES (%s, %s, %s, %s)", (username, password, random_number, random_chars))
    connection.commit()
    print("Credentials, random number, and random characters added successfully!")

# Fetch all users from database
def fetch_users(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    users_list = ""
    for row in rows:
        users_list += f"ID: {row[0]}, Username: {row[1]}, Password: {row[2]}, Random Number: {row[3]}, Random Characters: {row[4]}<br>"
    return users_list

# Fetch random characters for a specific user
def fetch_random_characters(connection, username):
    cursor = connection.cursor()
    cursor.execute("SELECT random_characters FROM users WHERE username = %s", (username,))
    row = cursor.fetchone()
    return row[0] if row else None

# Main function to handle user input and database operations
def main():
    # Create server connection
    server_connection = create_server_connection()
    
    # Create database if it doesn't exist
    create_database(server_connection)
    
    # Create database connection
    connection = create_connection()
    
    # Drop existing users table if it exists
    drop_table_if_exists(connection)
    
    # Create table in the database
    create_table(connection)
    
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")
        
        # Ensure username and password are unique and different before inserting
        if username != password:
            insert_user(connection, username, password)
            break
        else:
            print("Username and password should be different. Please try again.")
            
    print("Final credentials in the database:")
    fetch_users(connection)

if __name__ == "__main__":
    main()








