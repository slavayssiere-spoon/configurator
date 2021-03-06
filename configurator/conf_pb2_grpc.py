# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import conf_pb2 as conf__pb2


class configuratorStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Get = channel.unary_unary(
                '/configurator.configurator/Get',
                request_serializer=conf__pb2.Conf.SerializeToString,
                response_deserializer=conf__pb2.Conf.FromString,
                )
        self.SetAdminConf = channel.unary_unary(
                '/configurator.configurator/SetAdminConf',
                request_serializer=conf__pb2.AdminConf.SerializeToString,
                response_deserializer=conf__pb2.AdminConf.FromString,
                )
        self.SetAutoConf = channel.unary_unary(
                '/configurator.configurator/SetAutoConf',
                request_serializer=conf__pb2.AutoConf.SerializeToString,
                response_deserializer=conf__pb2.AutoConf.FromString,
                )


class configuratorServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Get(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetAdminConf(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetAutoConf(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_configuratorServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Get': grpc.unary_unary_rpc_method_handler(
                    servicer.Get,
                    request_deserializer=conf__pb2.Conf.FromString,
                    response_serializer=conf__pb2.Conf.SerializeToString,
            ),
            'SetAdminConf': grpc.unary_unary_rpc_method_handler(
                    servicer.SetAdminConf,
                    request_deserializer=conf__pb2.AdminConf.FromString,
                    response_serializer=conf__pb2.AdminConf.SerializeToString,
            ),
            'SetAutoConf': grpc.unary_unary_rpc_method_handler(
                    servicer.SetAutoConf,
                    request_deserializer=conf__pb2.AutoConf.FromString,
                    response_serializer=conf__pb2.AutoConf.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'configurator.configurator', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class configurator(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/configurator.configurator/Get',
            conf__pb2.Conf.SerializeToString,
            conf__pb2.Conf.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetAdminConf(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/configurator.configurator/SetAdminConf',
            conf__pb2.AdminConf.SerializeToString,
            conf__pb2.AdminConf.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetAutoConf(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/configurator.configurator/SetAutoConf',
            conf__pb2.AutoConf.SerializeToString,
            conf__pb2.AutoConf.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
