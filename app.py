from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.utils import secure_filename
import os
import pymysql.cursors
import time
from model import main

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# Configuration for file uploads
app.config['UPLOAD_FOLDER'] = 'static/photos/'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}

# Database connection
def get_db_connection():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='',
                           db='hackthon',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def login():
    error_message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE username = %s AND passwords = %s"
                cursor.execute(sql, (username, password))
                user = cursor.fetchone()

                if user:
                    session['username'] = username
                    return redirect(url_for('user_circles'))
                else:
                    error_message = "Invalid username or password. Please try again."
        finally:
            connection.close()
    
    return render_template('login.html', error_message=error_message)

@app.route('/circles')
def user_circles():
    if 'username' not in session:
        return redirect(url_for('login'))
        
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # First query: fetch all records
            sql_all = "SELECT * FROM tagging_images"
            cursor.execute(sql_all)
            results_all = cursor.fetchall()
            
            # Second query: group by tagging_numbers
            sql_grouped = "SELECT * FROM tagging_images GROUP BY tag_numbers"
                
            cursor.execute(sql_grouped)
            results_grouped = cursor.fetchall()
    finally:
        connection.close()
    
    return render_template('circle.html', results_all=results_all, results_grouped=results_grouped)


@app.route('/upload', methods=['GET', 'POST'])
def upload_media():
    if 'username' not in session:
        return redirect(url_for('login'))
   
    if request.method == 'POST':
        # Get form data
        name = session['username']
        
        file = request.files['file']

        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # Secure the filename
            filename = secure_filename(file.filename)
            user_folder = os.path.join(app.config['UPLOAD_FOLDER'], name)

            # Create user-specific folder if it doesn't exist
            if not os.path.exists(user_folder):
                os.makedirs(user_folder)

            file_path = os.path.join(user_folder, filename)
            model=main(file_path,'static\photos\reddyj699@gmail.com')
            print("hello this model tag",model)
            tag_numbers = model
            
            
            # If file exists, create a new filename with a timestamp
            if os.path.exists(file_path):
                filename, file_extension = os.path.splitext(filename)
                timestamp = int(time.time())
                filename = f"{filename}_{timestamp}{file_extension}"
                file_path = os.path.join(user_folder, filename)
            
            # Save the file
            file.save(file_path)
            file_url = 'photos/'+name+'/'+filename
            
            # Insert file details into database
            connection = get_db_connection()
            try:
                with connection.cursor() as cursor:
                    # Insert data into database
                    sql = "INSERT INTO tagging_images (name, photo, tag_numbers) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (name, file_url, tag_numbers))
                    connection.commit()
                    return redirect(url_for('user_circles'))
            finally:
                connection.close()
    
    return render_template('circle.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Registration route
@app.route('/reg-data', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['firstName']
        clgid = request.form['lastName']
        email = request.form['email']
        phoneno = request.form['phoneno']
        password = request.form['password']

        if first_name and clgid and email:
            session['first'] = first_name
            session['clgid'] = clgid
            session['email'] = email
            session['phoneno'] = phoneno
            session['password'] = password

            return render_template('otp-verfication.html')
        else:
            error_message = 'Please fill out all required fields.'
            return render_template('register.html', error_message=error_message)

    return render_template('register.html')

@app.route('/otpfile')
def otpfile():
    if 'email' not in session:
        return redirect(url_for('register'))
    return render_template('otpfile.html')
@app.route('/registration')
def registration():
    return render_template('registration.html')
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        id = request.form['id']
        
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Query to fetch records where tag_numbers equals the provided id
                sql = "SELECT * FROM tagging_images WHERE tag_numbers = %s"
                cursor.execute(sql, (id,))
                results_all = cursor.fetchall()
        finally:
            connection.close()
            
        return render_template('circle.html', results_all=results_all)




if __name__ == '__main__':
    app.run(debug=True, port=5000)
    