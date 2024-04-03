# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import appointment_pb2 as appointment__pb2


class AppointmentServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetAppointment = channel.unary_unary(
                '/appointment.AppointmentService/GetAppointment',
                request_serializer=appointment__pb2.GetAppointmentRequest.SerializeToString,
                response_deserializer=appointment__pb2.AppointmentResponse.FromString,
                )


class AppointmentServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetAppointment(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AppointmentServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetAppointment': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAppointment,
                    request_deserializer=appointment__pb2.GetAppointmentRequest.FromString,
                    response_serializer=appointment__pb2.AppointmentResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'appointment.AppointmentService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AppointmentService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetAppointment(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/appointment.AppointmentService/GetAppointment',
            appointment__pb2.GetAppointmentRequest.SerializeToString,
            appointment__pb2.AppointmentResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)