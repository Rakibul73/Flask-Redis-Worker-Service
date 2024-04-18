# Python Flask Web Service and Worker Service with Redis Integration


This project implements a `web service` and a `worker service` using `Python Flask`, with communication between them facilitated by `Redis` as a message broker. The web service receives tasks via a `RESTful API` endpoint, sends them to the worker service through Redis, and returns appropriate responses. The worker service listens for tasks from the web service, processes them, and stores the results back in Redis.

## Table of Contents

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

<hr>

## Project Overview

The project consists of two main components:

1. Web Service (`web_service.py`):
    - The code creates a Python Flask web service that exposes a RESTful API with an endpoint (`/tasks`) to receive tasks.
    - Tasks received by the web service are sent to the worker service via Redis using appropriate Redis data structures (`redis_client.lpush` to add tasks to a Redis list).
    - The web service returns appropriate HTTP status codes and messages for successful and unsuccessful requests (`400` for missing task data, `500` for internal server error).

2. Worker Service (`worker_service.py`):
    - The code also implements a Python Flask worker service that listens for tasks from the web service through Redis.
    - Once a task is received, the worker service processes it (summing the values provided) and stores the result back in Redis (`redis_client.lpush` to add processed data to another Redis list).
    - The worker service is designed to handle multiple tasks concurrently using multiple worker threads (`threading.Thread`).

Both services use Redis as a message broker for communication, They use appropriate Redis data structures and operations for sending tasks (`redis_client.lpush`), receiving results (`redis_client.rpop`), and managing queues (`task_queue` and `processed_data` lists).

<hr>

## Project Structure


├── web_service.py  `Python Flask web service`<br>
├── worker_service.py `Python Flask worker service`<br>
└── testing.py `Script for concurrent testing`<br>

<hr>

## Setup

To run the project locally, follow these steps in the respective folder:

1. Create & Activate venv Install Dependencies:
    ```bash
    cd web_service
    python -m venv .venv/
    .\venv\Scripts\activate
    pip install -r requirements. txt
    ```
    > Same for worker service

2. Run Redis Server:
    Ensure that Redis is installed and running on your system. If not, you can [download and install Redis](https://redis.io/download) from the official website. After that run
    ```bash
    sudo service redis-server start
    redis-cli
    ```
    To clear the all database
    ```bash
    FLUSHALL
    ```
    To see the queue list
    ```bash
    lrange task_queue 0 -1
    ```
    To see the processed data list
    ```bash
     lrange processed_data 0 -1
    ```

3. Start the Web Service:
    ```bash
    python web_service.py
    ```

4. Start the Worker Service:
    ```bash
    python worker_service.py
    ```

<hr>

## Usage

Once the services are running, you can interact with the web service by sending HTTP requests to its API endpoint (`http://localhost:5000/tasks`). Use the provided payloads in `testing.py` for concurrent testing.
##### Sample:

```bash
POST /tasks HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json
Content-Length: 97
body:
{
    "task": "one",
    "value": [
        5,
        6,
        9
    ],
    "sum": 0
}
```

To monitor the task queue, you can make a GET request to the `/monitor_queue` endpoint (`http://localhost:5000/monitor_queue`).
or you can use the `redis-cli` command to view the task queue and processed data lists in Run Redis Server section [here](#setup)

<hr>

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or create a pull request.

<hr>