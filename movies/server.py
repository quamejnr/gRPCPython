import grpc
from concurrent import futures 
from movie_service import MovieService
from movies_pb2_grpc import add_MovieServiceServicer_to_server
from signal import signal, SIGTERM


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_MovieServiceServicer_to_server(MovieService(), server)
    server.add_insecure_port("[::]: 50051")
    print("Listening on port :50051")
    server.start()

    def handle_sigterm(*_):
        print("Received shutdown signal")
        all_rpcs_done_event = server.stop(30)
        all_rpcs_done_event.wait(30)
        print("Shut down gracefully")

    signal(SIGTERM, handle_sigterm)
    server.wait_for_termination()
    server.wait_for_termination()

    
if __name__ == "__main__":
    serve()