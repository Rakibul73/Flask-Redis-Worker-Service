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
    - Exposes a RESTful API with an endpoint to receive tasks.
    - Sends tasks to the worker service via Redis.
    - Returns appropriate HTTP status codes and messages for successful and unsuccessful requests.

2. Worker Service (`worker_service.py`):
    - Listens for tasks from the web service through Redis.
    - Processes tasks (ex - summing the values provided) and stores the results back in Redis.
    - Handles multiple tasks concurrently using worker threads.

Both services use Redis as a message broker for communication, utilizing appropriate Redis data structures and operations for sending tasks, receiving results, and managing queues.

<hr>

## Project Structure


├── web_service.py  `Python Flask web service`
├── worker_service.py `Python Flask worker service`
└── testing.py `Script for concurrent testing`

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