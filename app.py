from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Specs(db.Model):
    SN = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), unique=False)
    Designator = db.Column(db.String(144), unique=False)
    Subdesignator = db.Column(db.String(20), unique=False)
    Image = db.Column(db.LargeBinary, unique=False)
    Oil = db.Column(db.String(15), unique=False)
    Coolant = db.Column(db.String(15), unique=False)
    Department =db.Column(db.String(20), unique=False)
    Motor = db.Column(db.LargeBinary, unique=False)
    


    def __init__(SN, Name, Designator, Subdesignator,Image,Oil,Coolant,Department,Motor):
        self.SN = SN
        self.Name = Name
        self.Designator = Designator
        self.Subdesignator = Subdesignator
        self.Image = Image
        self.Oil = Oil
        self.Coolant = Coolant
        self.Department = Department
        self.Motor = Motor



class SpecsSchema(ma.Schema):
    class Meta:
        fields = ('SN', 'Name', 'Designator', 'Subdesignator','Image','Oil','Coolant','Department','Motor')


Specs_schema = SpecsSchema()
Specss_schema = SpecsSchema(many=True)


if __name__ == '__main__':
    app.run(debug=True)