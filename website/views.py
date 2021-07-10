from flask import Blueprint, render_template, request, flash, jsonify,redirect,url_for,session
from flask import session
from flask.helpers import send_from_directory
from flask_login import login_required, current_user
from . import db
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential, load_model
from keras.models import load_model
from keras.models import model_from_json
from keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array
from flask import request
from flask import jsonify
from flask import Flask
from .forms import UpdateAccountForm
from .models import Predict
from datetime import date
import pytz
import json
from sqlalchemy.sql import func
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import imutils
import time
from time import time
from time import sleep
from time import *
from . import I2C_LCD_driver
from picamera import PiCamera
import uuid
from sqlalchemy.ext.declarative import DeclarativeMeta
from werkzeug.utils import secure_filename
import urllib.request
import os

views = Blueprint('views', __name__,static_folder= ('static'),template_folder=('template'))
UPLOAD_FOLDER= '/home/pi/ARD/website/static/romebeauty'
UPLOAD_FOLDER2='/home/pi/ARD/website/static/manalagi'
ALLOWED_EXTENSIONS= set(['png','jpg','jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def button_callback2(channel):
    print("Tombol B ditekan! Memprediksi Apel Romebeauty")
    my_lcd = I2C_LCD_driver.lcd()
    my_lcd.lcd_display_string("B: Romebeauty",2)
    camera=PiCamera()
    print("Camera is ON!\n")
    camera.start_preview()
    sleep(2)
    uuid_str=str(uuid.uuid4())
    image_path2 = '/home/pi/ARD/website/static/romebeauty/%s.jpg' %uuid_str
    camera.capture(image_path2)
    camera.stop_preview()
    camera.close()
    def result(image_path2):
        mod_path='/home/pi/ARD/romebeauty_AUG.h5'
        json_file = open('/home/pi/ARD/romebeauty_AUG.json')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights(mod_path)
        print("Model Successfully Loaded")

        new_img= image.load_img(image_path2, target_size=(224,224))
        x= image.img_to_array(new_img)
        x= np.expand_dims(x, axis=0)
        print(x.shape)
        images= np.vstack([x])
        global classes
        classes= np.argmax(loaded_model.predict(images,batch_size=10))

        mylcd= I2C_LCD_driver.lcd()
        padding= " "*16
        string="Romebeauty"
        pad_string=string+padding

        if classes==0:
            classes="Mentah"
            print(mylcd.lcd_display_string("Tingkat: Mentah",2,0))
        elif classes==1:
            classes="Mengkal(Setengah Matang)"
            print(mylcd.lcd_display_string("Tingkat: Mengkal",2,0))
        elif classes==2:
            classes="Matang"
            print(mylcd.lcd_display_string("Tingkat: Matang",2,0))
        else:
            print(mylcd.lcd_display_string("Tidak Terdeteksi",2,0))

        print('Tingkat Kematangan Apel: %s',classes)
        for i in range(0,len(string)):
            lcd_text= pad_string[((len(string)-1)-i):-i]
            mylcd.lcd_display_string(lcd_text,1)
            sleep(0.5)
            mylcd.lcd_display_string(padding[(15+i):i],1)
            
    global tipeapel
    tipeapel="Romebeauty"
    global jumlahapel
    jumlahapel=1
    global hasil
    hasil=result(image_path2)
    print("Tingkat Kematangan: ",hasil)
    global image_name1
    image_name1 = image_path2.replace('/home/pi/ARD/static/romebeauty/','')
    global time
    time=date.today()
    global result_data4
    result_data4= Predict(Tipe_Apel=tipeapel,Tingkat_Kematangan=classes,Nama_Gambar=image_name1,Jumlah_Apel=jumlahapel,Tanggal_Waktu_Prediksi=time)
    print("Rome Beauty Predicted, Result Added to Database")
    print(result_data4)
    
def button_callback(channel):
    print("Tombol A ditekan! Memprediksi Apel Manalagi")
    my_lcd = I2C_LCD_driver.lcd()
    my_lcd.lcd_display_string("A: Manalagi",1)
    camera=PiCamera()
    print("Camera is ON!\n")
    camera.start_preview()
    sleep(2)
    uuid_str=str(uuid.uuid4())
    image_path1 = '/home/pi/ARD/website/static/manalagi/%s.jpg'% uuid_str
    camera.capture(image_path1)
    camera.stop_preview()
    camera.close()
    def result(image_path1):
        mod_path='/home/pi/ARD/manalagi_AUGrev1.h5'
        json_file = open('/home/pi/ARD/manalagi_AUGrev1.json')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights(mod_path)
        print("Model Successfully Loaded")
                
        new_img1= image.load_img(image_path1, target_size=(224,224))
        xm= image.img_to_array(new_img1)
        xm= np.expand_dims(xm, axis=0)
        print(xm.shape)
        images= np.vstack([xm])
        global classes2
        classes2= np.argmax(loaded_model.predict(images,batch_size=10))

        mylcd= I2C_LCD_driver.lcd()
        padding= " "*16
        string="Manalagi"
        pad_string=string+padding

        if classes2==0:
            classes2="Mentah"
            print(mylcd.lcd_display_string("Tingkat: Mentah",2,0))
        elif classes2==1:
            classes2="Mengkal(Setengah Matang)"
            print(mylcd.lcd_display_string("Tingkat: Mengkal",2,0))
        elif classes2==2:
            classes2="Matang"
            print(mylcd.lcd_display_string("Tingkat: Matang",2,0))
        else:
            print(mylcd.lcd_display_string("Tidak Terdeteksi",2,0))

        print('Tingkat Kematangan Apel: %s',classes2)
        for i in range(0,len(string)):
            lcd_text= pad_string[((len(string)-1)-i):-i]
            mylcd.lcd_display_string(lcd_text,1)
            sleep(0.5)
            mylcd.lcd_display_string(padding[(15+i):i],1)
            
    global tipeapel
    tipeapel="Manalagi"
    global hasil2
    hasil2=result(image_path1)
    print("Tingkat Kematangan: ",hasil2)
    global image_name2
    image_name2 = image_path1.replace('/home/pi/ARD/static/manalagi/','')
    global jumlah
    jumlah=1
    global time
    time=date.today()
    global result_data3
    result_data3= Predict(Tipe_Apel=tipeapel,Tingkat_Kematangan=classes2,Nama_Gambar=image_name2,Jumlah_Apel=jumlah,Tanggal_Waktu_Prediksi=time)
    print("Manalagi Predicted, Result Added to Database")
    print(result_data3)

@views.route('/', methods=['GET', 'POST'])
@login_required
def wow():
    return render_template("index.html", user=current_user)

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("index.html", user=current_user)

@views.route('/about')
def about():
    return render_template("about.html")

@views.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.password = form.password.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.password.data = current_user.password
    image_file = url_for('static', filename='images/binusaso.png')
    return render_template('profile.html', title='Account',
                           image_file=image_file, form=form)

@views.route("/romebeauty", methods=['GET','POST'])
def romebeauty():
    return render_template("romebeauty.html")

@views.route("/manalagi")
def manalagi():
    return render_template("manalagi.html")

@views.route("/predict", methods=['GET','POST'])
def predict():
    if request.method=="POST":
        tipeapel=request.form.get('romebeauty')
        mod_path='/home/pi/ARD/romebeauty_AUG.h5'
        json_file = open('/home/pi/ARD/romebeauty_AUG.json')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)

        # load weights into new model
        loaded_model.load_weights(mod_path)
        print("Model Successfully Loaded")

        imagefile= request.files['imagefile']
        if imagefile.filename=='':
            flash('No Image Selected',category='error')
            return redirect(request.url)
        if imagefile and allowed_file(imagefile.filename):
            filename= secure_filename(imagefile.filename)
            image_path= "/home/pi/ARD/website/static/romebeauty/" +imagefile.filename
            imagefile.save(image_path)
            new_img= image.load_img(image_path, target_size=(224,224))
            x= image.img_to_array(new_img)
            x= np.expand_dims(x, axis=0)
            print(x.shape)
            images= np.vstack([x])
            classes= np.argmax(loaded_model.predict(images,batch_size=10))
            jumlahapel=0
            if classes==0:
                classes="Mentah"
                jumlahapel+=1
                jumlah2=jumlahapel
            elif classes==1:
                classes="Mengkal(Setengah Matang)"
                jumlahapel+=1
                jumlah2=jumlahapel
            elif classes==2:
                classes="Matang"
                jumlahapel+=1
                jumlah2=jumlahapel
            else:
                jumlahapel==jumlahapel
            time=date.today()
            namaimg2=image_path
            result_data= Predict(Tipe_Apel=tipeapel,Tingkat_Kematangan=classes,Nama_Gambar=namaimg2,Jumlah_Apel=jumlah2,Tanggal_Waktu_Prediksi=time)
            db.session.add(result_data)
            db.session.commit()
            flash('Result Prediction Added to Database', category='success')
            return render_template("predict.html", user=current_user, imagefile=imagefile, classes=classes)
        else:
            flash('Allowed Image Types Are: PNG, JPG and JPEG Only',category='error')
            return redirect(request.url)
        #image_path= "/home/pi/ARD/website/static/romebeauty/" +imagefile.filename
        #imagefile.save(image_path)

@views.route("/display")
def display(filename):
    return redirect(url_for('static',filename='romebeauty/'+filename),code=301)

@views.route("/display2")
def display2(filename):
    return redirect(url_for('static',filename='manalagi/'+filename),code=301)
    
@views.route("/predict2", methods=['GET','POST'])
def predict2():
     if request.method=="POST":
        tipeapel2=request.form.get('manalagi')
        mod_path='/home/pi/ARD/manalagi_AUGrev1.h5'
        json_file = open('/home/pi/ARD/manalagi_AUGrev1.json')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)

        # load weights into new model
        loaded_model.load_weights(mod_path)
        print("Model Successfully Loaded")

        imgfile= request.files['imgfile']
        if imgfile.filename=='':
            flash('No Image Selected',category='error')
            return redirect(request.url)
        if imgfile and allowed_file(imgfile.filename):
            img_path= "/home/pi/ARD/website/static/manalagi/" +imgfile.filename
            imgfile.save(img_path)
            new_img1= image.load_img(img_path, target_size=(224,224))
            xm= image.img_to_array(new_img1)
            xm= np.expand_dims(xm, axis=0)
            print(xm.shape)
            images= np.vstack([xm])
            classes2= np.argmax(loaded_model.predict(images,batch_size=10))
            jumlahapel=0
            if classes2==0:
                classes2="Mentah"
                jumlahapel+=1
                jumlah=jumlahapel
            elif classes2==1:
                classes2="Mengkal(Setengah Matang)"
                jumlahapel+=1
                jumlah=jumlahapel
            elif classes2==2:
                classes2="Matang"
                jumlahapel+=1
                jumlah=jumlahapel
            else:
                jumlahapel==jumlahapel

            time2=date.today()
            namaimg=img_path
            result_data2= Predict(Tipe_Apel=tipeapel2,Tingkat_Kematangan=classes2,Nama_Gambar=namaimg,Jumlah_Apel=jumlah,Tanggal_Waktu_Prediksi=time2)
            db.session.add(result_data2)
            db.session.commit()
            flash('Result Prediction Added to Database', category='success')
            return render_template("predict2.html", user=current_user, imgfile=imgfile, classes2=classes2)
        else:
            flash('Allowed Image Types Are: PNG, JPG and JPEG Only',category='error')
            return redirect(request.url)

@views.route("/result", methods=['GET','POST'], defaults={"page":1})
@views.route("/<int:page>",methods=['GET','POST'])
def result(page):
    page=page
    pages= 10
    prediksi= Predict.query.order_by(Predict.id.asc()).paginate(page,pages,error_out=False)
    print("PREDIKSI:",prediksi)

    if request.method=='POST' and 'tag' in request.form:
        tag= request.form["tag"]
        search= "%{}%".format(tag)
        prediksi= Predict.query.filter(Predict.Tipe_Apel.like(search)).paginate(per_page=pages, error_out=True)
        return render_template('result.html',prediksi=prediksi,tag=tag)
    return render_template("result.html",prediksi=prediksi,user=current_user)

@views.route("/chart")
def chart():
    mana_vs_rome = db.session.query(db.func.sum(Predict.Jumlah_Apel), Predict.Tipe_Apel).group_by(Predict.Tipe_Apel).order_by(Predict.Tipe_Apel).all()
    
    matang_mengkal_mentah=db.session.query(db.func.sum(Predict.Jumlah_Apel), Predict.Tingkat_Kematangan).group_by(Predict.Tingkat_Kematangan)
    
    dates = db.session.query(db.func.sum(Predict.Jumlah_Apel), Predict.Tanggal_Waktu_Prediksi).group_by(Predict.Tanggal_Waktu_Prediksi).order_by(Predict.Tanggal_Waktu_Prediksi).all()

    totalprediksi = []
    for total_amount, _ in mana_vs_rome:
        totalprediksi.append(total_amount)

    totalapel=[]
    for amounts, _ in matang_mengkal_mentah:
        totalapel.append(amounts)

    apelperhari = []
    dates_label = []
    for Jumlah_Apel, Tanggal_Waktu_Prediksi in dates:
        dates_label.append(Tanggal_Waktu_Prediksi)
        apelperhari.append(Jumlah_Apel)

    return render_template('chart.html',
                            mana_vs_rome=json.dumps(totalprediksi),
                            matang_mengkal_mentah=json.dumps(totalapel),
                            apelperhari=json.dumps(apelperhari),
                            dates_label=json.dumps(dates_label)
                        )

@views.route("/live")
def live():
    my_lcd = I2C_LCD_driver.lcd()
    my_lcd.lcd_display_string("Tekan A:Manalagi", 1)

    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 11 to be an input pin and set initial value to be pulled low (off)
    
    GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback) # Setup event on pin 11 rising edge
    
    message = input("Press enter to quit\n\n") # Run until someone presses enter
    print(message)
    GPIO.cleanup() # Clean up
    db.session.add(result_data3)
    db.session.commit()
    return render_template("live.html",user=current_user,classes2=classes2)

@views.route("/live2")
def live2():
    my_lcd = I2C_LCD_driver.lcd()
    my_lcd.lcd_display_string("Tekan B:Romebeauty", 2)

    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.add_event_detect(23,GPIO.RISING,callback=button_callback2)

    message = input("Press enter to quit\n\n") # Run until someone presses enter
    print(message)
    GPIO.cleanup() # Clean up
    db.session.add(result_data4)
    db.session.commit()
    return render_template("live2.html",user=current_user,classes=classes)