# web_service.py
import json
from flask import Flask, jsonify, request
import redis

app = Flask(__name__)
# Initialize Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/' , methods=['GET'])
def index():
    return jsonify({"Flask Web Service Running"})

# endpoint to receive tasks via POST request
@app.route('/tasks', methods=['POST'])
def receive_task():
    task_data = request.get_json()
    if not task_data:
        return jsonify({"error": "Task data not provided"}), 400
    try:
        # convert task data to JSON format string
        task_data_json = json.dumps(task_data)
        # Send task data to Redis
        redis_client.lpush('task_queue', task_data_json)
        return jsonify({"message": "Task received and sent for processing"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# endpoint to retrieve processed results
@app.route('/results', methods=['GET'])
def get_results():
    try:
        # Retrieve processed results from Redis
        results = redis_client.lrange('processed_data', 0, -1)
        # Convert bytes to strings
        results_str = [json.loads(result) for result in results]
        return jsonify({"results": results_str}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/monitor_queue', methods=['GET'])
def monitor_queue():
    # Get the length of the queue
    queue_length = redis_client.llen('task_queue')
    # Get the list of tasks in the queue
    tasks = redis_client.lrange('task_queue', 0, -1)
    # Convert bytes to strings
    tasks_str = [task.decode('utf-8') for task in tasks]
    # Return the queue length and list of tasks as JSON
    return jsonify({
        'queue_length': queue_length,
        'tasks': tasks_str
    })

if __name__ == '__main__':
    app.run(debug=True , port = 5000)
