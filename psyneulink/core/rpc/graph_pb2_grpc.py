# Princeton University licenses this file to You under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  You may obtain a copy of the License at:
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

# ********************************** PNL ProtoBuf Python Classes *************************************************


# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import graph_pb2 as graph__pb2


class ServeGraphStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.LoadCustomPnl = channel.unary_unary(
                '/graph.ServeGraph/LoadCustomPnl',
                request_serializer=graph__pb2.PNLPath.SerializeToString,
                response_deserializer=graph__pb2.NullArgument.FromString,
                )
        self.LoadScript = channel.unary_unary(
                '/graph.ServeGraph/LoadScript',
                request_serializer=graph__pb2.ScriptPath.SerializeToString,
                response_deserializer=graph__pb2.ScriptCompositions.FromString,
                )
        self.LoadGraphics = channel.unary_unary(
                '/graph.ServeGraph/LoadGraphics',
                request_serializer=graph__pb2.ScriptPath.SerializeToString,
                response_deserializer=graph__pb2.StyleJSON.FromString,
                )
        self.GetCompositions = channel.unary_unary(
                '/graph.ServeGraph/GetCompositions',
                request_serializer=graph__pb2.NullArgument.SerializeToString,
                response_deserializer=graph__pb2.ScriptCompositions.FromString,
                )
        self.GetJSON = channel.unary_unary(
                '/graph.ServeGraph/GetJSON',
                request_serializer=graph__pb2.GraphName.SerializeToString,
                response_deserializer=graph__pb2.GraphJSON.FromString,
                )
        self.HealthCheck = channel.unary_unary(
                '/graph.ServeGraph/HealthCheck',
                request_serializer=graph__pb2.NullArgument.SerializeToString,
                response_deserializer=graph__pb2.HealthStatus.FromString,
                )
        self.UpdateStylesheet = channel.stream_unary(
                '/graph.ServeGraph/UpdateStylesheet',
                request_serializer=graph__pb2.StyleJSON.SerializeToString,
                response_deserializer=graph__pb2.NullArgument.FromString,
                )
        self.RunComposition = channel.unary_stream(
                '/graph.ServeGraph/RunComposition',
                request_serializer=graph__pb2.RunTimeParams.SerializeToString,
                response_deserializer=graph__pb2.Entry.FromString,
                )


class ServeGraphServicer(object):
    """Missing associated documentation comment in .proto file."""

    def LoadCustomPnl(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LoadScript(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LoadGraphics(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetCompositions(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetJSON(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def HealthCheck(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateStylesheet(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RunComposition(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ServeGraphServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'LoadCustomPnl': grpc.unary_unary_rpc_method_handler(
                    servicer.LoadCustomPnl,
                    request_deserializer=graph__pb2.PNLPath.FromString,
                    response_serializer=graph__pb2.NullArgument.SerializeToString,
            ),
            'LoadScript': grpc.unary_unary_rpc_method_handler(
                    servicer.LoadScript,
                    request_deserializer=graph__pb2.ScriptPath.FromString,
                    response_serializer=graph__pb2.ScriptCompositions.SerializeToString,
            ),
            'LoadGraphics': grpc.unary_unary_rpc_method_handler(
                    servicer.LoadGraphics,
                    request_deserializer=graph__pb2.ScriptPath.FromString,
                    response_serializer=graph__pb2.StyleJSON.SerializeToString,
            ),
            'GetCompositions': grpc.unary_unary_rpc_method_handler(
                    servicer.GetCompositions,
                    request_deserializer=graph__pb2.NullArgument.FromString,
                    response_serializer=graph__pb2.ScriptCompositions.SerializeToString,
            ),
            'GetJSON': grpc.unary_unary_rpc_method_handler(
                    servicer.GetJSON,
                    request_deserializer=graph__pb2.GraphName.FromString,
                    response_serializer=graph__pb2.GraphJSON.SerializeToString,
            ),
            'HealthCheck': grpc.unary_unary_rpc_method_handler(
                    servicer.HealthCheck,
                    request_deserializer=graph__pb2.NullArgument.FromString,
                    response_serializer=graph__pb2.HealthStatus.SerializeToString,
            ),
            'UpdateStylesheet': grpc.stream_unary_rpc_method_handler(
                    servicer.UpdateStylesheet,
                    request_deserializer=graph__pb2.StyleJSON.FromString,
                    response_serializer=graph__pb2.NullArgument.SerializeToString,
            ),
            'RunComposition': grpc.unary_stream_rpc_method_handler(
                    servicer.RunComposition,
                    request_deserializer=graph__pb2.RunTimeParams.FromString,
                    response_serializer=graph__pb2.Entry.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'graph.ServeGraph', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ServeGraph(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def LoadCustomPnl(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/graph.ServeGraph/LoadCustomPnl',
            graph__pb2.PNLPath.SerializeToString,
            graph__pb2.NullArgument.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def LoadScript(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/graph.ServeGraph/LoadScript',
            graph__pb2.ScriptPath.SerializeToString,
            graph__pb2.ScriptCompositions.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def LoadGraphics(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/graph.ServeGraph/LoadGraphics',
            graph__pb2.ScriptPath.SerializeToString,
            graph__pb2.StyleJSON.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetCompositions(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/graph.ServeGraph/GetCompositions',
            graph__pb2.NullArgument.SerializeToString,
            graph__pb2.ScriptCompositions.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetJSON(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/graph.ServeGraph/GetJSON',
            graph__pb2.GraphName.SerializeToString,
            graph__pb2.GraphJSON.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def HealthCheck(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/graph.ServeGraph/HealthCheck',
            graph__pb2.NullArgument.SerializeToString,
            graph__pb2.HealthStatus.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateStylesheet(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/graph.ServeGraph/UpdateStylesheet',
            graph__pb2.StyleJSON.SerializeToString,
            graph__pb2.NullArgument.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RunComposition(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/graph.ServeGraph/RunComposition',
            graph__pb2.RunTimeParams.SerializeToString,
            graph__pb2.Entry.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
