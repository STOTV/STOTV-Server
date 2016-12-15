from flask import Flask, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, ForeignKey
from sqlalchemy.orm import relationship
import json, os

app = Flask(__name__,static_url_path='/static')
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

#api endpoint for rockBlock servers to send us location information
@app.route("/api/v1/send", methods=['POST'])
def submit():
    # rockBlock unique identifier 15 digits
    imei=form['imei']
    # "message id" can be used to prevent replays
    momsn=form['momsn']
    time=form['transmit_time']
    ### latitude and longitude may be replaced with submited data
    latitude=form['iridium_latitude']
    longitude=form['iridium_longitude']
    #how accurate latitude and longitude are
    cep=form['iridium_cep']
    data=form['data']
    decodedData=data.decode("hex")
    sanityCheck=Session.query(exists().where(Device.imei==imei))
    if sanityCheck:
        loc=Data(imei,momsn,time,latitude,longitude,cep)
        db.session.add(loc)
        db.session.commit()
    return "OK"

#api endpoint for getting return information if found
@app.route("/api/v1/found/<imei>")
def found(imei):
    data={}
    device=Device.query.filter_by(imei=imei).first()
    if device:
        data['deviceName']=device.deviceName
        data['returnName']=device.returnName
        data['returnAddr1']=device.returnAddr1
        data['returnAddr2']=device.returnAddr2
    return json.dumps(data)

#api endpoint for tracking all or specific tracker
@app.route("/api/v1/location")
@app.route("/api/v1/location/<id>")
def location(id=None):
    if id is None:
        locations=Data.query.order_by(desc(Data.time)).limit(20).all()
    else:
        locations=Data.query.filter_by(id=id).order_by(desc(Data.time)).limit(20)
    data= []
    for location in locations:
        loc={}
        loc['deviceId']=location.device.id
        loc['name']=location.device.deviceName
        loc['time']=location.time
        loc['latitude']=location.latitude
        loc['longitude']=location.longitude
        loc['cep']=location.cep
    return json.dumps(data)

### for testing ONLY, use nginx for better security and performance
#sends static index.html to request (DUH!)
@app.route("/")
def index():
    return app.send_static_file('index.html')
#sends static files requested
@app.route("/<path:path>")
def send_static(path):
    return send_from_directory('static', path)

#only start server if not being run from uWSGI
if __name__ == "__main__":
    app.run()
