
import grpc
import appointment_pb2
import appointment_pb2_grpc

#For testing get 

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = appointment_pb2_grpc.AppointmentServiceStub(channel)
        response = stub.GetAppointment(appointment_pb2.GetAppointmentRequest(appointment_id=1))
        print("Appointment:", response)


if __name__ == '__main__':
        run()