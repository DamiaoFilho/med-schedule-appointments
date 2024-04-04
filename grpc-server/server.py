from concurrent import futures
import grpc
import appointment_pb2_grpc
import appointment_pb2
import requests

class AppointmentServicer(appointment_pb2_grpc.AppointmentServiceServicer):
    def GetAppointment(self, request, context):
        appointment = requests.get(f'http://127.0.0.1:5000/appointments/{request.appointment_id}')
        appointment = appointment.json()
        response = appointment_pb2.AppointmentResponse(
            id=appointment.get("id"),
            id_doctor=appointment.get("id_doctor"),
            id_patient=appointment.get("id_patient"),
            date=appointment.get("date"),
            symptoms=appointment.get("symptoms"),
            diagnosis=appointment.get("diagnosis")
        )
        return response
    
    def DeleteAppointment(self, request, context):
        requests.get(f'/appointments/{request.appointment_id}')

    def ListAppointment(self, request, context):
        appointments = requests.get(f'/appointments/list')
        appointments = appointment.json()
        print(appointments)
        response = []
        for appointment in appointments:
            response.append(appointment_pb2.AppointmentResponse(
                id=appointment.get("id"),
                id_doctor=appointment.get("id_doctor"),
                id_patient=appointment.get("id_patient"),
                date=appointment.get("date"),
                symptoms=appointment.get("symptoms"),
                diagnosis=appointment.get("diagnosis")
            ))
        return response
    
        




def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    appointment_pb2_grpc.add_AppointmentServiceServicer_to_server(
        AppointmentServicer(), server)
    print("gRPC listening to port 50051")
    server.add_insecure_port("localhost:50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    server()