# What is this?
This is a gRPC server with a FastAPI client.

# Why this?
This was built in my attempt to better understand gRPC

# How to run this
- Clone the repo
- Install the dependencies in the requirements.txt file
- Navigate to the movies directory and run server.py with the command `python3 server.py`
- Open another terminal and start the FastAPI server with the command `uvicorn client:app --reload`
- Once your server is up and running, you can make a request to `127.0.0.1:8000/recommendMovies` to get your some movies recommended
- You can also add certain query params like category and limit. Category refers to the category of movies you want recommended while limit shows the number of movies you want recommended.
- You can choose between these 3 categories: Romance, Adventure and Sci-Fi.
- To want a recommendation for 3 movies under the category of Romance, the request will be `127.0.0.1:8000/recommendMovies?category=Romance&limit=3`

# What would you like to do next?
- Dockerize to simplify the running process.