import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import imutils
import time
import cv2

from keras.models import model_from_json # import library for cnn
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import I2C_LCD_driver

import mysql.connector

img_width, img_height = 64,64

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
my_lcd = I2C_LCD_driver.lcd()
my_lcd.lcd_display_string("Tekan Tombol", 1)



def button_callback(channel):
    print("Button was pushed!")
    #global hasil_prediksi
    #global image_path

    (grabbed, frame) = cap.read()
    showing = frame
    image_path = '/home/pi/project/static/luka/image_%s.jpg' % int(round(time.time() * 1000))
    
    cv2.imwrite(image_path, frame)
    cv2.waitKey(30)
    
    
    def result(image_path):
        # dimensions of our images
        img_width, img_height = 64,64

        # load the model we saved
        # load json and create new model
        json_file = open('model_v2.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)

        # load weights into new model
        loaded_model.load_weights("model_v2.h5")
        print("Loaded model from disk")

        # predicting images
        
        img = image.load_img(image_path, target_size=(img_width, img_height))
        img = image.img_to_array(img)
        img = img/255
        x = np.array(img)
        x = x.reshape(1,x.shape[0],x.shape[1],x.shape[2])
        classes = loaded_model.predict_classes(x)
        classes = loaded_model.predict_classes(x)
        
        if classes == 0:
            output = str('Sedang')
            
        elif classes == 1:
            output = str('Agak Parah')
            
        elif classes == 2:
            output = str('Sangat parah')
            
        print('Hasil Deteksi Level Luka adalah: %s' % output) # in terminal
        my_lcd.lcd_display_string("Level luka: %s" % output, 1) # in lcd

        return output    

      
    hasil_prediksi = result(image_path)
    image_name = image_path.replace('/home/pi/project/static/luka/','')  
        
    connection = mysql.connector.connect(host='localhost',
										database='login_db',
										user='pi',
										password='raspberry')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO hasil (result, prediction) VALUES (%s, %s)", (image_name, hasil_prediksi, ))
    connection.commit()
    connection.close()

    #return image_path, hasil_prediksi


GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 11 to be an input pin and set initial value to be pulled low (off)

GPIO.add_event_detect(11,GPIO.RISING,callback=button_callback) # Setup event on pin 11 rising edge

message = input("Press enter to quit\n\n") # Run until someone presses enter

GPIO.cleanup() # Clean up

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os


app = Flask(__name__)
#PEOPLE_FOLDER = os.path.join('static', 'wound')
#app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'abc'



# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'pi'
app.config['MYSQL_PASSWORD'] = 'raspberry'
app.config['MYSQL_DB'] = 'login_db'

# Intialize MySQL
mysql = MySQL(app)


# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

# http://localhost:5000/python/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
        #return redirect(url_for('carousel slide'))
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']


# Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

@app.route('/result')
def result():
    if 'loggedin' in session:
        #full_filename = os.path.join(app.config['UPLOAD_FOLDER'], '144.jpg')
        #return render_template('result.html', variable = output, user_image = full_filename)
        #imageList = os.listdir('static/wound')
        #imagelist = ['wound/' + image for image in imageList]
        
        #query = 'INSERT INTO hasil (result) VALUES (%s)'
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #cursor.executemany(query,  [(r,) for r in imagelist])
        #mysql.connection.commit()
        
        
        
        #cursor.execute('UPDATE hasil SET prediction = %s WHERE result = %s', (hasil_prediksi,image_path))
        #mysql.connection.commit()
        
        cursor.execute('SELECT * FROM hasil')
        tes = cursor.fetchall()
        return render_template("result_mult.html", value = tes)
       
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

if __name__ == '__main__':
   app.run(host = "0.0.0.0")


