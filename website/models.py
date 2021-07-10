from . import db
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from datetime import date
import pytz
newdate= date.today()
lastdate=newdate.strftime("%d/%m/%Y")

class Predict(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    Tipe_Apel=db.Column(db.String(50),nullable=False)
    Tingkat_Kematangan= db.Column(db.String(50), nullable=False)
    Nama_Gambar= db.Column(db.String(100),nullable=False)
    Jumlah_Apel= db.Column(db.Integer)
    Tanggal_Waktu_Prediksi=db.Column(db.String(50),default=lastdate)

    def __init__(self,Tipe_Apel,Tingkat_Kematangan,Nama_Gambar,Jumlah_Apel,Tanggal_Waktu_Prediksi):
        self.Tipe_Apel=Tipe_Apel
        self.Tingkat_Kematangan=Tingkat_Kematangan
        self.Nama_Gambar=Nama_Gambar
        self.Jumlah_Apel= Jumlah_Apel
        self.Tanggal_Waktu_Prediksi=Tanggal_Waktu_Prediksi
        
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    image_file= db.Column(db.String(20), nullable=True, default='default')

    def __init__(self,username,password,first_name,image_file):
        self.username=username
        self.password= password
        self.first_name= first_name
        self.image_file= image_file

