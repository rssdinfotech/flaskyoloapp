# wsgi.py
from flask import Flask
# from routes import app
# from flask_mysqldb import MySQL
# import pymysql
import pymysql.cursors


mysql= pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='users',
                               charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'mp4', 'avi', 'mov', 'wmv', 'flv'}
# # MySQL configurations
# app.config['MYSQL_HOST'] = 'localhost'  # Change this to your MySQL host
# app.config['MYSQL_USER'] = 'root'   # Change this to your MySQL username
# app.config['MYSQL_PASSWORD'] = 'root'  # Change this to your MySQL password
# app.config['MYSQL_DB'] = 'users'  # Change this to your MySQL database name
app.secret_key = 'mykey'


# mysql = MySQL()
# mysql.init_app(app)


from routes import *

if __name__ == '__main__':
    app.run(debug=True)
