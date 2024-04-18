# worker_service.py
import json
import os
import time
from flask import Flask, jsonify
import redis
import threading

app = Flask(__name__)
redis_client = redis.from_url(os.environ['REDIS_URL'])

@app.route('/' , methods=['GET'])
def index():
    return jsonify({"Flask Worker Service Running"})

# Function to process tasks retrieved from the Redis queue indefinitely
def process_task():
    while True:
        try:
            # Retrieve task data from Redis
            task_data = redis_client.rpop('task_queue')
            if task_data:
                # convert the task_data to a python dictionary
                task_data = json.loads(task_data)
                print("Previous data: ",task_data)
                # Process the task (sum of the values save into a task_data["sum"])
                task_data["sum"] = sum(task_data["value"])
                # convert task data to JSON format string
                processed_data = json.dumps(task_data)
                # Store the processed data back to Redis
                redis_client.lpush('processed_data', processed_data)
                print("Modified data: ", processed_data , "\n")
            else:
                # No task available, wait for a short period before checking again to avoid excessive CPU usage
                time.sleep(1)
        except Exception as e:
            print("Error processing task:", str(e))

# Start multiple worker threads
for _ in range(5):
    worker_thread = threading.Thread(target=process_task)
    # Threads will terminate when the main thread terminates
    worker_thread.daemon = True
    worker_thread.start()

if __name__ == '__main__':
    app.run(debug=True , port = 5001)
