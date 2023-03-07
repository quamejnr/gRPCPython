import random
import traceback

from google.protobuf import any_pb2
from google.rpc import error_details_pb2, status_pb2, code_pb2
from grpc_status import rpc_status

from movies_pb2 import Movie, MovieRecommendationResponse
from movies_pb2_grpc import MovieServiceServicer


def errorResponse(status_code: code_pb2, message: str):
    detail = any_pb2.Any()
    detail.Pack(
        error_details_pb2.DebugInfo(
            stack_entries=traceback.format_stack(),
            detail="Can't recognize this argument",
        )
    )
    return status_pb2.Status(
        code=status_code,
        message=message,
        details=[detail]
    )
    

class MovieService(MovieServiceServicer):

    def recommendMovie(self, request, context):
    
        movies = MOVIES
        if not movies:
            rich_status = errorResponse(code_pb2.NOT_FOUND, "Movie not found")
            context.abort_with_status(rpc_status.to_status(rich_status))
            
        limit = request.limit if request.limit else 3

        if request.category:
            movies = [movie for movie in MOVIES if movie.category == request.category]
            if not movies:
                rich_status = errorResponse(code_pb2.NOT_FOUND, "Movie not found")
                context.abort_with_status(rpc_status.to_status(rich_status))

        recommended_movies = random.sample(movies, limit)
        return MovieRecommendationResponse(movies=recommended_movies)
    
    
# Mock Data
MOVIES = [
    Movie(id=1, title="Sinbad", category="Adventure"),
    Movie(id=2, title="Hercules", category="Adventure"),
    Movie(id=3, title="Prince of Persia", category="Adventure"),
    Movie(id=4, title="Titanic", category="Romance"),
    Movie(id=5, title="Entergalatic", category="Romance"),
    Movie(id=6, title="Bay", category="Romance"),
    Movie(id=7, title="Star Wars", category="Sci-Fi"),
    Movie(id=8, title="Star Trek", category="Sci-Fi"),
    Movie(id=9, title="Avengers", category="Sci-Fi"),
]
