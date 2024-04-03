from flask import render_template, request, redirect, url_for, jsonify
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from flask_migrate import Migrate

#GRPC
from concurrent import futures
import grpc
import appointment_pb2_grpc
import appointment_pb2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:3214@localhost/med_schedule_appointments'
db = SQLAlchemy(app)
CORS(app)
migrate = Migrate(app, db)



class AppointmentService(appointment_pb2_grpc.AppointmentServiceServicer):
    def getAppointment(self, request, context):
        appointment = get_appointment(request.appointment_id)
        return appointment_pb2.AppointmentResponse(
            id=appointment.id,
            id_doctor=appointment.id_doctor,
            id_patient=appointment.id_patient,
            date=appointment.date.strftime('%Y-%m-%d %H:%M:%S'),
            symptoms=appointment.symptoms,
            diagnosis=appointment.diagnosis
        )



class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_doctor = db.Column(db.Integer, nullable=False)
    id_patiant = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    

@app.route('/appointments/create', methods=['POST'])
def create_appointment():
    data = request.get_json()
    new_appointment = Appointment(
        id_doctor=data['id_doctor'],
        id_patiant=data['id_patiant'],
        date=datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S'),
        symptoms=data['symptoms'],
        diagnosis=data['diagnosis']
    )
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment created successfully'}), 201

@app.route('/appointments/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    return jsonify({
        'id': appointment.id,
        'id_doctor': appointment.id_doctor,
        'id_patiant': appointment.id_patiant,
        'date': appointment.date.strftime('%Y-%m-%d %H:%M:%S'),
        'symptoms': appointment.symptoms,
        'diagnosis': appointment.diagnosis
    })

@app.route('/appointments/list', methods=['GET'])
def list_appointment():
    appointments = Appointment.query.all()
    appointment_list = []
    for appointment in appointments:
        appointment_data = {
            'id': appointment.id,
            'id_doctor': appointment.id_doctor,
            'id_patiant': appointment.id_patiant,
            'date': appointment.date.strftime('%Y-%m-%d %H:%M:%S'),
            'symptoms': appointment.symptoms,
            'diagnosis': appointment.diagnosis
        }
        appointment_list.append(appointment_data)
    return jsonify(appointment_list)

@app.route('/appointments/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    data = request.get_json()
    appointment.id_doctor = data['id_doctor']
    appointment.id_patiant = data['id_patiant']
    appointment.date = datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S')
    appointment.symptoms = data['symptoms']
    appointment.diagnosis = data['diagnosis']
    db.session.commit()
    return jsonify({'message': 'Appointment updated successfully'})

@app.route('/appointments/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    db.session.delete(appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment deleted successfully'})


def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    appointment_pb2_grpc.add_AppointmentServiceServicer_to_server(
        AppointmentService(), server)
    server.add_insecure_port('localhost:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    server()