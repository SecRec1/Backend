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
    Fluids = db.Column(db.String(50), unique=False)
    Department =db.Column(db.String(20), unique=False)
    Motor = db.Column(db.String(100), unique=False)


    def __init__(self, title, content):
        self.title = title
        self.content = content


class SpecsSchema(ma.Schema):
    class Meta:
        fields = ('title', 'content')


Specs_schema = SpecsSchema()
Specss_schema = SpecsSchema(many=True)


if __name__ == '__main__':
    app.run(debug=True)