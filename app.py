from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os




app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Specs(db.Model):
    qrcode = db.Column(db.String, unique=False)
    sn = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    designator = db.Column(db.String(144), unique=False)
    subdesignator = db.Column(db.String(20), unique=False)
    
    oil = db.Column(db.String(15), unique=False)
    coolant = db.Column(db.String(15), unique=False)
    department =db.Column(db.String(20), unique=False)
    motor = db.Column(db.String, unique=False)
    


    def __init__(self,qrcode,sn, name, designator, subdesignator,oil,coolant,department,motor):
        self.qrcode = qrcode
        self.sn = sn
        self.name = name
        self.designator = designator
        self.subdesignator = subdesignator
        
        self.oil = oil
        self.coolant = coolant
        self.department = department
        self.motor = motor



class SpecsSchema(ma.Schema):
    class Meta:
        fields = ('qrcode','sn', 'name', 'designator', 'subdesignator','oil','coolant','department','motor')


specs_schema = SpecsSchema()
specss_schema = SpecsSchema(many=True)

@app.route("/Specs", methods=["GET"])
def get_specss():
    all_specs = Specs.query.all()
    result = specss_schema.dump(all_specs)
    return jsonify(result)

@app.route("/Specs/<sn>", methods=["GET"])
def get_specs(sn):
    specs = Specs.query.get(sn)
    return specs_schema.jsonify(specs)

@app.route('/Specs', methods=["POST"])
def add_specs():
    qrcode = request.json['qrcode']
    sn = request.json['sn']
    name = request.json['name']
    designator = request.json['designator']
    subdesignator = request.json['subdesignator']
    
    oil = request.json['oil']
    coolant = request.json['coolant']
    department = request.json['department']
    motor = request.json['motor']

    new_specs = Specs(qrcode,sn, name, designator, subdesignator,oil,coolant,department,motor)

    db.session.add(new_specs)
    db.session.commit()

    specs = Specs.query.get(new_specs.id)

    return specs_schema.jsonify(specs)

@app.route("/Specs/<sn>", methods=["PUT"])
def specs_update(sn):
    specs = Specs.query.get(sn)
    qrcode = request.json['qrcode']
    sn = request.json['sn']
    name = request.json['name']
    designator = request.json['designator']
    subdesignator = request.json['subdesignator']
    oil = request.json['oil']
    coolant = request.json['coolant']
    department = request.json['department']
    motor = request.json['motor']

    Specs.qrcode = qrcode
    Specs.sn = sn
    Specs.name = name
    Specs.designator = designator
    Specs.subdesignator = subdesignator
    
    Specs.oil = oil
    Specs.coolant = coolant
    Specs.department = department
    Specs.motor = motor

    db.session.commit()
    return specs_schema.jsonify(specs)

@app.route("/Specs/<sn>", methods=["DELETE"])
def specs_delete(sn):
    specs = Specs.query.get(sn)
    db.session.delete(specs)
    db.session.commit()

    return "Specs were successfully deleted"


if __name__ == '__main__':
    app.run(debug=True)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String, unique=False)
    lastcompleted = db.Column(db.String(20), unique=False)
    nextdue = db.Column(db.String(20), unique=False)
    
    
    


    def __init__(self, id, task, lastcompleted, nextdue):
        self.id = id
        self.task = task
        self.lastcompleted = lastcompleted
        self.nextdue = nextdue
        
        



class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id','task', 'lastcompleted', 'nextdue')


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@app.route("/Task", methods=["GET"])
def get_tasks():
    all_task = Specs.query.all()
    result = tasks_schema.dump(all_task)
    return jsonify(result)

@app.route("/Task/<id>", methods=["GET"])
def get_task(id):
    task = Task.query.get(id)
    return task_schema.jsonify(task)

@app.route('/Task', methods=["POST"])
def add_task():
    id = request.json['id']
    task = request.json['task']
    lastcompleted = request.json['lastcompleted']
    nextdue = request.json['nextdue']
    

    new_task = Task(id, task, lastcompleted, nextdue)

    db.session.add(new_task)
    db.session.commit()

    task = Task.query.get(new_task.id)

    return task_schema.jsonify(task)

@app.route("/Task/<id>", methods=["PUT"])
def task_update(id):
    task = Task.query.get(id)
    id = request.json['id']
    task = request.json['task']
    lastcompleted = request.json['lastcompleted']
    nextdue = request.json['nextdue']

    Task.id = id
    Task.task = task
    Task.lastcompleted = lastcompleted
    Task.nextdue = nextdue
    

    db.session.commit()
    return task_schema.jsonify(task)

@app.route("/Task/<id>", methods=["DELETE"])
def task_delete(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()

    return "Task was successfully deleted"


if __name__ == '__main__':
    app.run(debug=True)