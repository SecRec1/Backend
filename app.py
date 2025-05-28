from flask import Flask, httpx, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os
import logging
from logging.handlers import RotatingFileHandler



app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins
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
    id = httpx.json['id']
    sn = httpx.json['sn']
    qrcode = httpx.json['qrcode']
    name = httpx.json['name']
    designator = httpx.json['designator']
    subdesignator = httpx.json['subdesignator']
    hours = httpx.json['hours']
    oil = httpx.json['oil']
    coolant = httpx.json['coolant']
    department = httpx.json['department']
    motor = httpx.json['motor']
    hours = httpx.json['hours']

    new_specs = Specs(id,qrcode,sn, name, designator, subdesignator,oil,coolant,department,motor,hours)

    db.session.add(new_specs)
    db.session.commit()

    specs = Specs.query.get(new_specs.sn)

    return specs_schema.jsonify(specs)

@app.route("/Specs/<sn>", methods=["PUT"])
def specs_update(sn):
    specs = Specs.query.get(sn)
    data = httpx.get_json()
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

@app.route("/Specs/id/<int:id>", methods=["DELETE"])
def delete_by_id(id):
    specs = Specs.query.filter_by(id=id).first()
    if specs:
        db.session.delete(specs)
        db.session.commit()
        return "Specs successfully deleted", 200
    return "Specs not found", 404







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
    id = httpx.json['id']
    job = httpx.json['job']
    instructions = httpx.json['instructions']
    
    new_task = Task(id, job, instructions)

    db.session.add(new_task)
    db.session.commit()

    task = Task.query.get(new_task.id)

    return task_schema.jsonify(task)


@app.route("/Task/<id>", methods=["PUT"])
def task_update(id):
    task = Task.query.get(id)
    data = httpx.get_json()

    task.job = data.get('job', task.job)
    task.instructions = data.get('instructions', task.instructions)

    db.session.commit()
    return task_schema.jsonify(task)



class IBST(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
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
        fields = ('id','specs_sn', 'task_id', 'lastcompleted', 'nextdue','notes','duration', "hdselector")





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
        
        specs_sn = httpx.json['specs_sn']
        task_id = httpx.json['task_id']
        lastcompleted = httpx.json['lastcompleted']
        nextdue = httpx.json['nextdue']
        notes = httpx.json['notes']
        duration = httpx.json['duration']
        hdselector = httpx.json['hdselector']

        logging.debug(f"Received data: {httpx.json}")

        new_ibst = IBST(specs_sn=specs_sn, task_id=task_id, lastcompleted=lastcompleted, nextdue=nextdue, notes=notes, duration=duration, hdselector=hdselector)

        app.logger.debug(f"New IBST added: {new_ibst}")

        db.session.add(new_ibst)
        db.session.commit()

        ibst = IBST.query.get(new_ibst.id)

        return ibst_schema.jsonify(ibst)
    except KeyError as e:
        logging.error(f"Missing key in httpx: {e.args[0]}")
        return jsonify({"error": f"Missing key in httpx: {e.args[0]}"}), 400
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
       

@app.route("/IBST/<id>", methods=["PUT"])
def ibst_update(id):
    try:
        ibst = IBST.query.get(id)
        if ibst is None:
            return jsonify({"message": "IBST not found"}), 404  # 404 Not Found
        
        data = httpx.json
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
    id = httpx.json['id']
    username = httpx.json['username']
    password = httpx.json['password']
    loggedin = httpx.json['loggedin']
   
    new_admin = Admin(id, username, password, loggedin)

    db.session.add(new_admin)
    db.session.commit()

    admin = Admin.query.get(new_admin.id)

    return admin_schema.jsonify(admin)

@app.route("/Admin/<id>", methods=["PUT"])
def admin_update(id):
    admin = Admin.query.get(id)
    data = httpx.get_json()

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

    data = httpx.get_json()
    admin.loggedin = data.get('loggedin', admin.loggedin)

    db.session.commit()
    return admin_schema.jsonify(admin)

@app.route("/Admin/<id>", methods=["DELETE"])
def admin_delete(id):
    admin = Admin.query.get(id)
    db.session.delete(admin)
    db.session.commit()

    return "Admin was successfully deleted"



class Notes(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    note = db.Column(db.String(),unique=False)
    date = db.Column(db.String(),nullable=False)
    retired = db.Column(db.String(),nullable=False) 

    def __init__(self, note, date, retired):
        
        self.note = note
        self.date = date
        self.retired = retired
        
        
        
class NotesSchema(ma.Schema):
    class Meta:
        fields = ("id", "note", "date", "retired")





note_schema = NotesSchema()
notes_schema = NotesSchema(many=True)


@app.route("/Notes", methods=["GET"])
def get_notes():
    all_notes = Notes.query.all()
    result = notes_schema.dump(all_notes)
    return jsonify(result)


@app.route("/Notes/<id>", methods=["GET"])
def get_note(id):
    note = Notes.query.get(id)
    return note_schema.jsonify(note)

@app.route("/Notes", methods=["POST"])
def add_note():

    try:
        note = httpx.json['note']
        date = httpx.json['date']
        retired = httpx.json['retired']
        
        logging.debug(f"Received data: {httpx.json}")

        new_note = Notes(note=note, date=date, retired=retired)

        app.logger.debug(f"New Note added: {new_note}")
        
        db.session.add(new_note)
        db.session.commit()

        note = Notes.query.get(new_note.id)
        return note_schema.jsonify(note)
    except KeyError as e:
        logging.error(f"Missing key in httpx: {e.args[0]}")
        return jsonify({"error": f"Missing key in httpx: {e.args[0]}"}), 400
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500
    

@app.route("/Notes/<id>", methods=["PUT"])
def note_update(id):
    try:
        note = Notes.query.get(id)
        if note is None:
            return jsonify({"message": "Note not found"}), 404  # 404 Not Found
        
        data = httpx.json
        if 'id' in data:
            note.id = data['id']
        if 'note' in data:
            note.note = data['note']
        if 'date' in data:
            note.date = data['date']
        if'retired' in data:
            note.retired = data['retired']
                    
        db.session.commit()
        return note_schema.jsonify(note)
    except Exception as e:
        return jsonify({"message": str(e)}), 500  # 500 Internal Server Error


@app.route("/Notes/<id>", methods=["DELETE"])
def note_delete(id):
    note = Notes.query.get(id)
    db.session.delete(note)
    db.session.commit()
    return "Note was successfully deleted"


class Toolneeds(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    tool = db.Column(db.String(), unique=False)
    size = db.Column(db.String(), unique=False)
    count = db.Column(db.Integer(),unique=False)

    def __init__(self, tool, size, count):
        
        self.tool = tool
        self.size = size
        self.count = count


class ToolneedsSchema(ma.Schema):
    class Meta:
        fields = ("id", "tool", "size", "count")



toolneed_schema = ToolneedsSchema()
toolneeds_schema = ToolneedsSchema(many=True)

@app.route("/ToolNeeds", methods=["GET"])
def get_toolneeds():
    all_toolneeds = Toolneeds.query.all()
    result = toolneeds_schema.dump(all_toolneeds)
    return jsonify(result)

@app.route("/ToolNeeds/<id>", methods=["GET"])
def get_toolneed(id):
    toolneed = Toolneeds.query.get(id)
    return toolneed_schema.jsonify(toolneed)

@app.route("/ToolNeeds", methods=["POST"])
def add_toolneed():
    tool = httpx.json['tool']
    size = httpx.json['size']
    count = httpx.json['count']
    
    new_toolneed = Toolneeds(tool=tool, size=size, count=count)
    
    db.session.add(new_toolneed)
    db.session.commit()
    
    toolneed = Toolneeds.query.get(new_toolneed.id)
    return toolneed_schema.jsonify(toolneed)

@app.route("/ToolNeeds/<id>", methods=["PUT"])
def toolneed_update(id):
    toolneed = Toolneeds.query.get(id)
    if toolneed is None:
        return jsonify({"message": "ToolNeed not found"}), 404  # 404 Not Found
    
    data = httpx.json
    if 'id' in data:
        toolneed.id = data['id']
    if 'tool' in data:
        toolneed.tool = data['tool']
    if'size' in data:
        toolneed.size = data['size']
    if 'count' in data:
        toolneed.count = data['count']
                    
    db.session.commit()
    return toolneed_schema.jsonify(toolneed)

@app.route("/ToolNeeds/<id>", methods=["DELETE"])
def toolneed_delete(id):
    toolneed = Toolneeds.query.get(id)
    db.session.delete(toolneed)
    db.session.commit()
    return "ToolNeed was successfully deleted"


class Parts(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    part = db.Column(db.String(), unique=False)
    quantity = db.Column(db.Integer(),unique=False)
    ordered = db.Column(db.String(), nullable=False)
    eta = db.Column(db.String(), nullable=False)

    def __init__(self, part, quantity, ordered, eta):
        
        self.part = part
        self.quantity = quantity
        self.ordered = ordered
        self.eta = eta

class PartsSchema(ma.Schema):
    class Meta:
        fields = ("id", "part", "quantity", "ordered", "eta")


part_schema = PartsSchema()

parts_schema = PartsSchema(many=True)

@app.route("/Parts", methods=["GET"])
def get_parts():
    all_parts = Parts.query.all()
    result = parts_schema.dump(all_parts)
    return jsonify(result)

@app.route("/Parts/<id>", methods=["GET"])
def get_part(id):
    part = Parts.query.get(id)
    return part_schema.jsonify(part)

@app.route("/Parts", methods=["POST"])
def add_part():
    part = httpx.json['part']
    quantity = httpx.json['quantity']
    ordered = httpx.json['ordered']
    eta = httpx.json['eta']
    
    new_part = Parts(part=part, quantity=quantity, ordered=ordered, eta=eta)
    
    db.session.add(new_part)
    db.session.commit()
    
    part = Parts.query.get(new_part.id)
    return part_schema.jsonify(part)

@app.route("/Parts/<id>", methods=["PUT"])
def part_update(id):
    part = Parts.query.get(id)
    if part is None:
        return jsonify({"message": "Part not found"}), 404  # 404 Not Found
    
    data = httpx.json
    if 'id' in data:
        part.id = data['id']
    if 'part' in data:
        part.part = data['part']
    if 'quantity' in data:
        part.quantity = data['quantity']
    if 'ordered' in data:
        part.ordered = data['ordered']
    if 'eta' in data:
        part.eta = data['eta']
                    
    db.session.commit()
    return part_schema.jsonify(part)

@app.route("/Parts/<id>", methods=["DELETE"])
def part_delete(id):
    part = Parts.query.get(id)
    db.session.delete(part)
    db.session.commit()
    return "Part was successfully deleted"


class Contractors(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    company = db.Column(db.String(), unique=False)
    onsitestart = db.Column(db.String(), unique=False)
    onsiteend = db.Column(db.String(), unique=False)
    indoor = db.Column(db.String(), unique=False)

    def __init__(self, company, onsitestart, onsiteend, indoor):
        
        self.company = company
        self.onsitestart = onsitestart
        self.onsiteend = onsiteend
        self.indoor = indoor

class ContractorsSchema(ma.Schema):
    class Meta:
        fields = ("id", "company", "onsitestart", "onsiteend", "indoor")

    
contractor_schema = ContractorsSchema()

contractors_schema = ContractorsSchema(many=True)

@app.route("/Contractors", methods=["GET"])
def get_contractors():
    all_contractors = Contractors.query.all()
    result = contractors_schema.dump(all_contractors)
    return jsonify(result)

@app.route("/Contractors/<id>", methods=["GET"])
def get_contractor(id):
    contractor = Contractors.query.get(id)
    return contractor_schema.jsonify(contractor)

@app.route("/Contractors", methods=["POST"])
def add_contractor():
    company = httpx.json['company']
    onsitestart = httpx.json['onsitestart']
    onsiteend = httpx.json['onsiteend']
    indoor = httpx.json['indoor']
    
    new_contractor = Contractors(company=company, onsitestart=onsitestart, onsiteend=onsiteend, indoor=indoor)
    
    db.session.add(new_contractor)
    db.session.commit()
    
    contractor = Contractors.query.get(new_contractor.id)
    return contractor_schema.jsonify(contractor)

@app.route("/Contractors/<id>", methods=["PUT"])
def contractor_update(id):
    contractor = Contractors.query.get(id)
    if contractor is None:
        return jsonify({"message": "Contractor not found"}), 404  # 404 Not Found
    
    data = httpx.json
    if 'id' in data:
        contractor.id = data['id']
    if 'company' in data:
        contractor.company = data['company']
    if 'onsitestart' in data:
        contractor.onsitestart = data['onsitestart']
    if 'onsiteend' in data:
        contractor.onsiteend = data['onsiteend']
    if 'indoor' in data:
        contractor.indoor = data['indoor']
                    
    db.session.commit()
    return contractor_schema.jsonify(contractor)

@app.route("/Contractors/<id>", methods=["DELETE"])
def contractor_delete(id):
    contractor = Contractors.query.get(id)
    db.session.delete(contractor)
    db.session.commit()
    return "Contractor was successfully deleted"



class Jobs(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    job = db.Column(db.String(), unique=False)
    reasons = db.Column(db.String(),unique=False)

    def __init__(self, job, reasons):
        
        self.job = job
        self.reasons = reasons

class JobsSchema(ma.Schema):
    class Meta:
        fields = ("id", "job", "reasons")


job_schema = JobsSchema()

jobs_schema = JobsSchema(many=True)

@app.route("/Jobs", methods=["GET"])
def get_jobs():
    all_jobs = Jobs.query.all()
    result = jobs_schema.dump(all_jobs)
    return jsonify(result)

@app.route("/Jobs/<id>", methods=["GET"])
def get_job(id):
    job = Jobs.query.get(id)
    return job_schema.jsonify(job)

@app.route("/Jobs", methods=["POST"])
def add_job():
    job = httpx.json['job']
    reasons = httpx.json['reasons']
    
    new_job = Jobs(job=job, reasons=reasons)
    
    db.session.add(new_job)
    db.session.commit()
    
    job = Jobs.query.get(new_job.id)
    return job_schema.jsonify(job)

@app.route("/Jobs/<id>", methods=["PUT"])
def job_update(id):
    job = Jobs.query.get(id)
    if job is None:
        return jsonify({"message": "Job not found"}), 404  # 404 Not Found
    
    data = httpx.json
    if 'id' in data:
        job.id = data['id']
    if 'job' in data:
        job.job = data['job']
    if'reasons' in data:
        job.reasons = data['reasons']
                    
    db.session.commit()
    return job_schema.jsonify(job)

@app.route("/Jobs/<id>", methods=["DELETE"])
def job_delete(id):
    job = Jobs.query.get(id)
    db.session.delete(job)
    db.session.commit()
    return "Job was successfully deleted"



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)