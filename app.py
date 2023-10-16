from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
import logging

app = Flask(__name__)

# MySQL database configuration
db_config = {
    'host': 'zaigam-assignment-database.cnuytreilxhx.eu-north-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'admin1234',
    'database': 'zaigam'
}

# Configure logging to write errors to a log file
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def connect_to_database():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Exception as e:
        logging.error("Error connecting to the database: %s", str(e))
        return None

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = connect_to_database()
        if conn is not None:
            try:
                cursor = conn.cursor()
                insert_query = "INSERT INTO user (username, password) VALUES (%s, %s)"
                cursor.execute(insert_query, (username, password))
                conn.commit()
                cursor.close()
                conn.close()
                logging.info("User added to the database: %s", username)
                return redirect(url_for('add_user'))
            except Exception as e:
                logging.error("Error adding user to the database: %s", str(e))
        else:
            logging.error("Failed to connect to the database.")

    return render_template('add_user.html')

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
