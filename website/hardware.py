import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import imutils
import time
import cv2

from time import time
from time import sleep
from time import *
from keras.models import model_from_json # import library for cnn
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import I2C_LCD_driver
from .models import Predict
from datetime import date
from . import db

my_lcd = I2C_LCD_driver.lcd()
my_lcd.lcd_display_string("Tekan Tombol A Untuk Manalagi, B untuk Romebeauty", 1)

def button_callback():
    print("Tombol A ditekan! Memprediksi Apel Manalagi")
    camera= picamera.PiCamera()
    camera.start_preview()
    sleep(3)
    print("Camera is ON!\n")
    image_path1 = '/home/pi/ARD/website/static/manalagi/manalagi_%s.jpg' % int(round(time.time() * 1000))
    camera.capture(image_path1)
    camera.close()

def button_callback2():
    print("Tombol B ditekan! Memprediksi Apel Romebeauty")
    camera= picamera.PiCamera()
    camera.start_preview()
    sleep(3)
    print("Camera is ON!\n")
    image_path2 = '/home/pi/ARD/website/static/romebeauty/romebeauty_%s.jpg' % int(round(time.time() * 1000))
    camera.capture(image_path2)
    camera.close()

if button_callback==True:
    def manalagi(image_path1):
        tipeapel2="Manalagi"
        mod_path='C:/Users/Asus/manalagi_AUG.h5'
        json_file = open('C:/Users/Asus/manalagi_AUG.json')
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
        classes2= np.argmax(loaded_model.predict(images,batch_size=10))
        padding= " "*16
        string="Manalagi"
        pad_string=string+padding

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

        print('Tingkat Kematangan Apel: %s',classes2)
        my_lcd.lcd_display_string("Kematangan Apel: %s",classes2, 1)
        for i in range(0,len(string)):
            lcd_text= pad_string[((len(string)-1)-i):-i]
            mylcd.lcd_display_string(lcd_text,1)
            sleep(0.5)
            mylcd.lcd_display_string(padding[(15+i):i],1)

        time2=date.today()
        namaimg = image_path1.replace('/home/pi/ARD/website/static/manalagi/','')  
        result_data2= Predict(Tipe_Apel=tipeapel2,Tingkat_Kematangan=classes2,Nama_Gambar=namaimg,Jumlah_Apel=jumlah,Tanggal_Waktu_Prediksi=time2)
        db.session.add(result_data2)
        db.session.commit()
        print("Manalagi Result Added to Database")

elif button_callback2==True:
    def romebeauty(image_path2):
        tipeapel="Rome Beauty"
        mod_path='C:/Users/Asus/romebeauty_AUG.h5'
        json_file = open('C:/Users/Asus/romebeauty_AUG.json')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)

            # load weights into new model
        loaded_model.load_weights(mod_path)
        print("Model Successfully Loaded")

        new_img= image.load_img(image_path2, target_size=(224,224))
        x= image.img_to_array(new_img)
        x= np.expand_dims(x, axis=0)
        print(x.shape)
        images= np.vstack([x])
        classes= np.argmax(loaded_model.predict(images,batch_size=10))
        padding= " "*16
        string="Romebeauty"
        pad_string=string+padding
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

        print('Tingkat Kematangan Apel: %s',classes)
        my_lcd.lcd_display_string("Kematangan Apel: %s",classes, 1)
        for i in range(0,len(string)):
            lcd_text= pad_string[((len(string)-1)-i):-i]
            mylcd.lcd_display_string(lcd_text,1)
            sleep(0.5)
            mylcd.lcd_display_string(padding[(15+i):i],1)
        
        time=date.today()
        namaimg2 = image_path2.replace('/home/pi/ARD/website/static/romebeauty/','') 
        result_data= Predict(Tipe_Apel=tipeapel,Tingkat_Kematangan=classes,Nama_Gambar=namaimg2,Jumlah_Apel=jumlah2,Tanggal_Waktu_Prediksi=time)
        db.session.add(result_data)
        db.session.commit()
        print("Romebeauty Result Added to Database")


GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 11 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(11,GPIO.RISING,callback=button_callback) # Setup event on pin 11 rising edge
GPIO.add_event_detect(13,GPIO.RISING,callback2=button_callback2)

message = input("Press enter to quit\n\n") # Run until someone presses enter

GPIO.cleanup() # Clean up