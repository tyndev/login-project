import sqlite3, os, time
from dotenv import load_dotenv

db_path = 'db/users.db'

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

    # sqlite3.Row: 
    # Allows accessing columns of a query by name (and position). Rows returned from the database will behave like dictionaries rather than tuples.

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    email TEXT NOT NULL,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

def insert_data(email, username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)", (email, username, password))
    conn.commit()
    cursor.close()
    conn.close()
    return

def query_db(query, args=(), one=False):
    conn = get_db_connection()
    cursor = conn.execute(query, args)
    rv = cursor.fetchall()
    cursor.close()
    conn.close()
    return (rv[0] if rv else None) if one else rv

    # query: 
        # SQL query string to execute. It can contain placeholders for parameters.
    # args: 
        # Tuple containing values to substitute into placeholders in query.
    # one:
        # Default value one=False:
            # But if one=True argument is passed into the fuction, it will override     the default.
        # If one is False: 
            # Returns all the rows fetched by the query
        # If one is True: 
            # Checks if rv is not empty (if rv) and returns the first element of the list (rv[0]) which represents the first row of the query result. If rv is empty, it returns `None`. 


# Ops -------------------------
    
if __name__ == "__main__":
    init_db()
    # Print all users.
    print("All Users ----")
    users = query_db("SELECT * FROM users")
    for user in users:
        print(f"ID: {user['id']}, Email: {user['email']}, Username: {user['username']}, Password: {user['password']}")
    # Print one user.
    print("One User ----")
    user = query_db("SELECT * FROM users WHERE username = ?", ("test", ), one=True)
    print(f"ID: {user['id']}, Email: {user['email']}, Username: {user['username']}, Password: {user['password']}")
    
    # Testing python-dotenv
    load_dotenv()
    key = os.getenv("session_key")
    