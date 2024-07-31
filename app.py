from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import os
import logging
from logging.handlers import RotatingFileHandler



app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)


class Specs(db.Model):
    id = db.Column(db.Integer(), unique=True)
    qrcode = db.Column(db.String(), unique=False)
    sn = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(100), unique=False)
    designator = db.Column(db.String(144), unique=False)
    subdesignator = db.Column(db.String(20), unique=False)
    oil = db.Column(db.String(15), unique=False)
    coolant = db.Column(db.String(15), unique=False)
    department =db.Column(db.String(20), unique=False)
    motor = db.Column(db.String(), unique=False)
    hours = db.Column(db.String(),unique=False)


    def __init__(self,id,qrcode,sn, name, designator, subdesignator,oil,coolant,department,motor,hours):
        self.id = id
        self.qrcode = qrcode
        self.sn = sn
        self.name = name
        self.designator = designator
        self.subdesignator = subdesignator
        self.oil = oil
        self.coolant = coolant
        self.department = department
        self.motor = motor
        self.hours = hours



class SpecsSchema(ma.Schema):
    class Meta:
        fields = ('id','qrcode','sn', 'name', 'designator', 'subdesignator','oil','coolant','department','motor','hours')


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



@app.route("/Specs", methods=["POST"])
def add_specs():
    id = request.json['id']
    sn = request.json['sn']
    qrcode = request.json['qrcode']
    name = request.json['name']
    designator = request.json['designator']
    subdesignator = request.json['subdesignator']
    hours = request.json['hours']
    oil = request.json['oil']
    coolant = request.json['coolant']
    department = request.json['department']
    motor = request.json['motor']
    hours = request.json['hours']

    new_specs = Specs(id,qrcode,sn, name, designator, subdesignator,oil,coolant,department,motor,hours)

    db.session.add(new_specs)
    db.session.commit()

    specs = Specs.query.get(new_specs.sn)

    return specs_schema.jsonify(specs)

@app.route("/Specs/<sn>", methods=["PUT"])
def specs_update(sn):
    specs = Specs.query.get(sn)
    data = request.get_json()
    print(f"Received PUT request for SN: {sn} with data: {data}")

    specs.qrcode = data.get('qrcode', specs.qrcode)
    specs.sn = data.get('sn', specs.sn)
    specs.name = data.get('name', specs.name)
    specs.designator = data.get('designator', specs.designator)
    specs.subdesignator = data.get('subdesignator', specs.subdesignator)
    specs.oil = data.get('oil', specs.oil)
    specs.coolant = data.get('coolant', specs.coolant)
    specs.department = data.get('department', specs.department)
    specs.motor = data.get('motor', specs.motor)
    specs.hours = data.get('hours', specs.hours)

    db.session.commit()
    return specs_schema.jsonify(specs)

@app.route("/Specs/<sn>", methods=["DELETE"])
def specs_delete(sn):
    specs = Specs.query.get(sn)
    db.session.delete(specs)
    db.session.commit()

    return "Specs were successfully deleted"







class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String, unique=False)
    instructions = db.Column(db.String, unique=False)

    def __init__(self,id,job,instructions):
        self.id = id
        self.job = job
        self.instructions = instructions
        
       
        



class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id','job', 'instructions' )


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@app.route("/Task", methods=["GET"])
def get_tasks():
    all_task = Task.query.all()
    result = tasks_schema.dump(all_task)
    return jsonify(result)

@app.route("/Task/<id>", methods=["GET"])
def get_task(id):
    task = Task.query.get(id)
    return task_schema.jsonify(task)

@app.route("/Task", methods=["POST"])
def add_task():
    id = request.json['id']
    job = request.json['job']
    instructions = request.json['instructions']
    
    new_task = Task(id, job, instructions)

    db.session.add(new_task)
    db.session.commit()

    task = Task.query.get(new_task.id)

    return task_schema.jsonify(task)


@app.route("/Task/<id>", methods=["PUT"])
def task_update(id):
    task = Task.query.get(id)
    data = request.get_json()

    task.job = data.get('job', task.job)
    task.instructions = data.get('instructions', task.instructions)

    db.session.commit()
    return task_schema.jsonify(task)



class IBST(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    specs_sn = db.Column(db.String(), unique= False)
    task_id = db.Column(db.Integer(), db.ForeignKey('task.id'), unique=False)
    lastcompleted = db.Column(db.String(), unique=False)
    nextdue = db.Column(db.String(), unique=False)
    notes = db.Column(db.String(), unique=False)
    duration = db.Column(db.Integer(), unique=False)
    hdselector = db.Column(db.String(), unique=False)

    def __init__(self, specs_sn, task_id, lastcompleted, nextdue, notes, duration,hdselector):
        
        self.specs_sn = specs_sn
        self.task_id = task_id
        self.lastcompleted = lastcompleted
        self.nextdue = nextdue
        self.notes = notes
        self.duration = duration
        self.hdselector = hdselector
class IBSTSchema(ma.Schema):
    class Meta:
        fields = ('specs_sn', 'task_id', 'lastcompleted', 'nextdue','notes','duration', "hdselector")





ibst_schema = IBSTSchema()
ibsts_schema = IBSTSchema(many=True)
    
@app.route("/IBST", methods=["GET"])
def get_ibsts():
    all_ibst = IBST.query.all()
    result = ibsts_schema.dump(all_ibst)
    return jsonify(result)


@app.route("/IBST/<id>", methods=["GET"])
def get_ibst(id):
    ibst = IBST.query.get(id)
    return ibst_schema.jsonify(ibst)

@app.route("/IBST", methods=["POST"])
def add_ibst():

    
    try:
        specs_sn = request.json['specs_sn']
        task_id = request.json['task_id']
        lastcompleted = request.json['lastcompleted']
        nextdue = request.json['nextdue']
        notes = request.json['notes']
        duration = request.json['duration']
        hdselector = request.json['hdselector']

        logging.debug(f"Received data: {request.json}")

        new_ibst = IBST(specs_sn=specs_sn, task_id=task_id, lastcompleted=lastcompleted, nextdue=nextdue, notes=notes, duration=duration, hdselector=hdselector)

        app.logger.debug(f"New IBST added: {new_ibst}")

        db.session.add(new_ibst)
        db.session.commit()

        ibst = IBST.query.get(new_ibst.id)

        return ibst_schema.jsonify(ibst)
    except KeyError as e:
        logging.error(f"Missing key in request: {e.args[0]}")
        return jsonify({"error": f"Missing key in request: {e.args[0]}"}), 400
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
       

@app.route("/IBST/<id>", methods=["PUT"])
def ibst_update(id):
    try:
        ibst = IBST.query.get(id)
        if ibst is None:
            return jsonify({"message": "IBST not found"}), 404  # 404 Not Found
        
        data = request.json
        if 'id' in data:
            ibst.id = data['id']
        if 'specs_sn' in data:
            ibst.specs_sn = data['specs_sn']
        if 'task_id' in data:
            ibst.task_id = data['task_id']
        if 'lastcompleted' in data:
            ibst.lastcompleted = data['lastcompleted']
        if 'nextdue' in data:
            ibst.nextdue = data['nextdue']
        if 'notes' in data:
            ibst.notes = data['notes']
        if 'duration' in data:
            ibst.duration = data['duration']
        if 'hdselector' in data:
            ibst.hdselector = data['hdselector']

        db.session.commit()

        return ibst_schema.jsonify(ibst)
    except Exception as e:
        return jsonify({"message": str(e)}), 500  # 500 Internal Server Error

@app.route("/IBST/<id>", methods=["DELETE"])
def ibst_delete(id):
    ibst = IBST.query.get(id)
    db.session.delete(ibst)
    db.session.commit()
    return "IBST was successfully deleted"
    







class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20), unique=True)
    loggedin = db.Column(db.Boolean, default=False)
    
    def __init__(self, id, username, password, loggedin):
        self.id = id
        self.username = username
        self.password = password
        self.loggedin = loggedin
       

class AdminSchema(ma.Schema):
    class Meta:
        fields = ('id','username', 'password', 'loggedin')


admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)

@app.route("/Admin", methods=["GET"])
def get_admins():
    all_admins = Admin.query.all()
    result = admins_schema.dump(all_admins)
    return jsonify(result)

@app.route("/Admin/<id>", methods=["GET"])
def get_admin(id):
    admin = Admin.query.get(id)
    return admin_schema.jsonify(admin)

@app.route('/Admin', methods=["POST"])
def add_admin():
    id = request.json['id']
    username = request.json['username']
    password = request.json['password']
    loggedin = request.json['loggedin']
   
    new_admin = Admin(id, username, password, loggedin)

    db.session.add(new_admin)
    db.session.commit()

    admin = Admin.query.get(new_admin.id)

    return admin_schema.jsonify(admin)

@app.route("/Admin/<id>", methods=["PUT"])
def admin_update(id):
    admin = Admin.query.get(id)
    data = request.get_json()

    admin.id = data.get('id', admin.id)
    admin.username = data.get('username', admin.username)
    admin.password = data.get('password', admin.password)
    admin.loggedin = data.get('loggedin', admin.loggedin)

    db.session.commit()
    return admin_schema.jsonify(admin)

@app.route("/Admin/<id>/status", methods=["PUT"])
def update_admin_status(id):
    admin = Admin.query.get(id)
    if not admin:
        return jsonify({"error": "Admin not found"}), 404

    data = request.get_json()
    admin.loggedin = data.get('loggedin', admin.loggedin)

    db.session.commit()
    return admin_schema.jsonify(admin)

@app.route("/Admin/<id>", methods=["DELETE"])
def admin_delete(id):
    admin = Admin.query.get(id)
    db.session.delete(admin)
    db.session.commit()

    return "Admin was successfully deleted"


if __name__ == '__main__':
    app.run(debug=True)