from flask import Flask, render_template, request, jsonify
import requests
import mysql.connector
import os


app = Flask(__name__)

# MySQL Database Configuration
# app.config['MYSQL_HOST'] = 'mysql' # Make sure this matches the service name in Docker Compose
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'DataL123'
# app.config['MYSQL_DB'] = 'mydb'
app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST") # Make sure this matches the service name in Docker Compose
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")

# Connect to MySQL
def get_db_connection():
    connection = mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )
    return connection

# Function to get picture URL from database
def getPic():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM imges;")  # Make sure the table `imges` exists in your DB
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    if data:
        # Return the first image URL from the data
        pic = data[0]["url"]
    else:
        pic = None  # Handle case where no data is found
    return pic

# Genderize.io API URL
API_URL = "https://api.genderize.io"

@app.route('/')
def index():
    pic = getPic()
    return render_template('index.html', src=pic)

@app.route('/detect_gender', methods=['POST'])
def detect_gender():
    pic = getPic()
    # Get the name from the form
    name = request.form.get('name')
    if not name:
        return jsonify({"error": "Name is required"}), 400
    if name == "amity":
        gender = "male with pussy"
        is_gay = "Yes"
        probability = "100"
        return render_template('index.html', name=name, is_gay=is_gay, probability=probability, gender=gender, src=pic)

    try:
        # Call Genderize.io API
        response = requests.get(API_URL, params={"name": name})
        data = response.json()

        # Get gender and probability from API response
        gender = data.get('gender')
        probability = data.get('probability', 0) * 100  # Convert probability to percentage

        # Assuming you're using gender to determine the "is_gay" logic (you may want to reconsider this)
        is_gay = "No"
        if gender == "female":
            is_gay = "Yes"  # Placeholder logic for demonstration

        # Render the result on the HTML page
        return render_template('index.html', name=name, is_gay=is_gay, probability=probability, gender=gender, src=pic)

    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
