from flask import Flask, render_template, request, jsonify
import requests
import mysql.connector 
import os
import random
from werkzeug.utils import secure_filename
from prometheus_client import start_http_server, Summary,Gauge
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from flask import Response
# Create a Prometheus metric (this is a simple timer)
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
VISITOR_COUNTER = Gauge('flask_app_visitor_count', 'Current number of visitors')
#check
app = Flask(__name__)

# MySQL Database Configuration
# app.config['MYSQL_HOST'] = 'mysql' # Make sure this matches the service name in Docker Compose
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'DataL123'
# app.config['MYSQL_DB'] = 'mydb'
app.config['PORT'] = os.getenv("PORT")
app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST") # Make sure this matches the service name in Docker Compose
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")
app.config['COUNTER']=0

# Set the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = os.path.join('static', UPLOAD_FOLDER)

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
    pic_urls = [item["url"] for item in data]
    print(pic_urls)
   


    if data:
        # Return the first image URL from the data
        #pic = data[0]["url"]
            # Get a random item
        #random_item = random.choice(pic_urls)
        random_item=pic_urls[-1]
        pic=random_item
        if not pic.startswith("https://"):
            pic = os.path.join("uploads", pic)
            pic = os.path.join("static", pic)
            

    else:
        pic = None  # Handle case where no data is found
    return pic
def getCounter():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM count;")  
    data = cursor.fetchone()
    print("#########################################################")
    print(data)
    cursor.close()
    conn.close()
    counter = int(data["counter"])

    return counter
def updateCounter(counter):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # Use parameterized queries to avoid SQL injection risks
        query = "UPDATE count SET counter = %s WHERE idcounter = 1;"
        ret = cursor.execute(query, (counter,))
        
        # Commit the transaction to apply the update
        conn.commit()

        cursor.close()
        conn.close()
        return ret
    except Exception as e:
        print(f"Error: {e}")  # Log the error message
        return False
def insert_img(name,path):
    conn = get_db_connection()
    cursor = conn.cursor()
   # Use %s for placeholders in MySQL
    cursor.execute("INSERT INTO imges (name, url) VALUES (%s, %s)", (name, path))
    conn.commit()  # Commit the transaction
    cursor.close()
    conn.close()

# Genderize.io API URL
API_URL = "https://api.genderize.io"
@REQUEST_TIME.time()
@app.route('/')
def index():
    counter=getCounter()
    counter+=1
    if updateCounter(counter):
        print("ok")
    else:
        print("nooooo")  
    # Set Prometheus counter to match SQL counter (avoid double counting)
    VISITOR_COUNTER._value.set(counter) 
    pic = getPic()
    return render_template('index.html', src=pic,visits=counter)
@app.route('/add_img')
def add_img():
    return render_template('add_img.html')
@app.route('/postAddImg', methods=['POST'])
def post_add_img():
     # Check if the request has the file part
    if 'image' not in request.files:
        msg="error!!"
        render_template('add_img.html',msg=msg)
    file = request.files['image']
    
    # If no file is selected
    if file.filename == '':
        msg="error!!"
        render_template('add_img.html',msg=msg)
    
    # Check if the file is allowed
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Get the name from the form
        name = request.form['name']
        #formatted_src = filepath.replace('/', '\\')
        insert_img(name,filename)
        msg="success!!"
    else:
         msg="error!!"


    return render_template('add_img.html',msg=msg)

@app.route('/metrics')
def metrics():
    # Return all metrics in Prometheus format
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

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
        counter=int(app.config['COUNTER'])
        return render_template('index.html', name=name, is_gay=is_gay, probability=probability, gender=gender, src=pic,visits=counter)

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
    port=app.config['PORT']
    app.run(host='0.0.0.0',port=int(os.getenv('PORT',5000)) )
