from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, ForeignKey
from sqlalchemy.orm import relationship
import os

app = Flask(__name__)
### Suggest change to mysql for performance, for easy testing
app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('database_uri','sqlite:///./test.db');
db = SQLAlchemy(app)

class Device(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    imei = db.Column(db.Integer,unique=True)
    deviceName = db.Column(db.String(120),unique=True)
    returnName = db.Column(db.String(120))
    returnAddr1 = db.Column(db.String(120))
    returnAddr2 = db.Column(db.String(120))
    def __init__(self,imei,deviceName,returnName,returnAddr1,returnAddr2):
        self.imei=imei
        self.deviceName=deviceName
        self.returnName=returnName
        self.returnAddr1=returnAddr1
        self.returnAddr2=returnAddr2
    def __repr__(self):
        return '<Device %r>' % self.deviceName

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imei = db.Column(db.Integer,ForeignKey(Device.imei))
    device = relationship('Device', foreign_keys='Data.imei')
    momsn = db.Column(db.Integer) # not unique cause the counter rolls over
    time = db.Column(db.Integer)
    latitude = db.Column(db.String(20)) # lazy hack, probably should be a double
    longitude = db.Column(db.String(20)) # same as above its almost 3:30 am
    cep = db.Column(db.String(20)) # need research
    #ToDo: other data
    def __init__(self,imei,momsn,time,latitude,longitude,cep):
        self.imei=imei
        self.momsn=momsn
        self.time=time
        self.latitude=latitude
        self.longitude=longitude
        self.cep=cep
    def __repr__(self):
        return '<Data %r>' % self.imei

db.create_all();
imei=int(input("What is the RockBLOCK's IMEI Number: "))
deviceName=input("What do you want the device to be called publicly? ")
returnName=input("What name is to be used in case of recovery? ")
returnAddr1=input("What Address is to be used in case of recovery? Line 1: ")
returnAddr2=input("What Address is to be used in case of recovery? Line 2: ")
device=Device(imei,deviceName,returnName,returnAddr1,returnAddr2)
db.session.add(device)
db.session.commit()
