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
    sn = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    designator = db.Column(db.String(144), unique=False)
    subdesignator = db.Column(db.String(20), unique=False)
    image = db.Column(db.LargeBinary, unique=False)
    oil = db.Column(db.String(15), unique=False)
    coolant = db.Column(db.String(15), unique=False)
    department =db.Column(db.String(20), unique=False)
    motor = db.Column(db.LargeBinary, unique=False)
    


    def __init__(sn, name, designator, subdesignator,image,oil,coolant,department,motor):
        self.sn = sn
        self.name = name
        self.designator = designator
        self.subdesignator = subdesignator
        self.image = image
        self.oil = oil
        self.coolant = coolant
        self.department = department
        self.motor = motor



class SpecsSchema(ma.Schema):
    class Meta:
        fields = ('SN', 'Name', 'Designator', 'Subdesignator','Image','Oil','Coolant','Department','Motor')


Specs_schema = SpecsSchema()
Specss_schema = SpecsSchema(many=True)

@app.route("/Specs", methods=["GET"])
def get_specs():
    all_specs = Specs.query.all()
    result = Specs_schema.dump(all_specs)
    return jsonify(result)

@app.route("/Specs/<id>", methods=["GET"])
def get_specs(id):
    specs = Specs.query.get(id)
    return specs_schema.jsonify(specs)

@app.route('/Specs', methods=["POST"])
def add_specs():
    sn = request.json['sn']
    name = request.json['name']
    designator = request.json['designator']
    subdesignator = request.json['subdesignator']
    image = request.json['image']
    oil = request.json['oil']
    coolant = request.json['coolant']
    department = request.json['department']
    motor = request.json['motor']

    new_specs = Specs(sn, name, designator, subdesignator,image,oil,coolant,department,motor)

    db.session.add(new_specs)
    db.session.commit()

    specs = Specs.query.get(new_specs.id)

    return Specs_schema.jsonify(specs)

@app.route("/Specs/<id>", methods=["PUT"])
def specs_update(id):
    specs = Specs.query.get(id)
    sn = request.json['sn']
    name = request.json['name']
    designator = request.json['designator']
    subdesignator = request.json['subdesignator']
    image = request.json['image']
    oil = request.json['oil']
    coolant = request.json['coolant']
    department = request.json['department']
    motor = request.json['motor']

    Specs.sn = sn
    Specs.name = name
    Specs.designator = designator
    Specs.subdesignator = subdesignator
    Specs.image = image
    Specs.oil = oil
    Specs.coolant = coolant
    Specs.department = department
    Specs.motor = motor

    db.session.commit()
    return Specs_schema.jsonify(specs)

@app.route("/specs/<id>", methods=["DELETE"])
def specs_delete(id):
    specs = Specs.query.get(id)
    db.session.delete(specs)
    db.session.commit()

    return "Specs were successfully deleted"


if __name__ == '__main__':
    app.run(debug=True)


class Task(db.Model):
    task = db.Column(db.Integer, primary_key=True)
    lastcompleted = db.Column(db.String(100), unique=False)
    nextdue = db.Column(db.String(144), unique=False)
    
    
    


    def __init__(task, lastcompleted, nextdue):
        self.task = task
        self.lastcompleted = lastcompleted
        self.nextdue = nextdue
        
        



class TaskSchema(ma.Schema):
    class Meta:
        fields = ('task', 'lastcompleted', 'nextdue')


Task_schema = TaskSchema()
Tasks_schema = TaskSchema(many=True)

@app.route("/Task", methods=["GET"])
def get_task():
    all_task = Specs.query.all()
    result = Task_schema.dump(all_task)
    return jsonify(result)

@app.route("/Task/<id>", methods=["GET"])
def get_task(id):
    task = Task.query.get(id)
    return Task_schema.jsonify(task)

@app.route('/Task', methods=["POST"])
def add_task():
    task = request.json['task']
    lastcompleted = request.json['lastcompleted']
    nextdue = request.json['nextdue']
    

    new_task = Task(task, lastcompleted, nextdue)

    db.session.add(new_task)
    db.session.commit()

    task = Task.query.get(new_task.id)

    return Task_schema.jsonify(task)

@app.route("/Task/<id>", methods=["PUT"])
def task_update(id):
    task = Task.query.get(id)
    task = request.json['task']
    lastcompleted = request.json['lastcompleted']
    nextdue = request.json['nextdue']

    Task.task = task
    Task.lastcompleted = lastcompleted
    Task.nextdue = nextdue
    

    db.session.commit()
    return Task_schema.jsonify(task)

@app.route("/Specs/<id>", methods=["DELETE"])
def task_delete(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()

    return "Task was successfully deleted"


if __name__ == '__main__':
    app.run(debug=True)