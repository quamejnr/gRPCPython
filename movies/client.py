import grpc
from grpc_status import rpc_status
from movies_pb2_grpc import MovieServiceStub
from movies_pb2 import MovieRecommendationRequest
from google.protobuf.json_format import MessageToDict

# FastAPI
from fastapi import FastAPI


def client_request(category=None, limit=0):
    channel = grpc.insecure_channel("localhost:50051")
    client = MovieServiceStub(channel)
    request = MovieRecommendationRequest(category=category, limit=limit)
    resp = client.recommendMovie(request)
    return resp


STATUS_CODE_INT_TO_ENUM_MAP = {item.value[0]: item for item in grpc.StatusCode}


app = FastAPI()


@app.get("/recommendMovies")
async def get_recommended_movies(category: str = None, limit: int = 0):
    try:
        results = client_request(category, limit)
        results_dict = MessageToDict(results)
        movies = results_dict['movies']
        return {
            "status": 200,
            "movies": movies
        }
    except grpc.RpcError as err:
        detail = rpc_status.from_call(err)
        print(detail)
        return {
            "error": {
                "code": str(STATUS_CODE_INT_TO_ENUM_MAP.get(detail.code)),
                "detail": detail.message
            }
        }
