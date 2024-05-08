# utils.py
import mysql.connector
# import pyodbc
from flask import request,session,jsonify
from wsgi import mysql


def authenticate_user(username, password):
    
    print('auth')
    
    try:
        # # Connect to the database
        cursor = mysql.connection.cursor()


        # # Execute a query to fetch the user's credentials
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        # cursor.execute("SELECT * FROM users")
        
        # # Fetch one row (if exists) containing user's credentials
        row = cursor.fetchone()
        print(row)
        # # Close the cursor and connection
        # cursor.close()
        # mysql.connection.close()

        # # Check if a row with matching credentials was found
        if row:
            return True
        else:
            return False

    except Exception as e:
        print(f"Error: {e}")
        return False

    
    


def auth_login(username, password):
    print("test")
    print(username, password)

    if authenticate_user(username, password):
        # Store user session
        session['logged_in'] = True
        session['username'] = username
        return True
    else:
        print('user not found')
        return False
 


def auth_logout():
    # Clear user session
    session.clear()
    return jsonify({'message': 'Logout successful'}),200
