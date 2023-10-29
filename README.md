# URL Shortener

This service provides functionality to create shortened versions of requested URLs and offers analysis on the activity of their use. Additionally, the service includes middleware that blocks access from prohibited subnets. The server is hosted at http://localhost:8000, and the PgAdmin for the database can be accessed at http://localhost:80.


## Endpoints

### 1. Ping Database

- **Endpoint:** `GET /ping`
- **Description:** Pings the database to check the connection status.
- **Raises:**
  - `HTTPException`: If the connection to the database cannot be established.
- **Response:**
  - `200 OK`:
    ```json
    {
      "ping_time": 0.123
    }
    ```
    - `ping_time`: Ping time in seconds.

### 2. Create Shortened URL

- **Endpoint:** `POST /`
- **Description:** Creates a short URL for the given original URL.
- **Parameters:**
  - `entity_in` (required): Original URL to be shortened.
- **Raises:**
  - `HTTPException (410)`: If the requested URL is already in the database but marked as deleted.
- **Response:**
  - `201 Created`:
    ```json
    {
      "id": 123,
      "original_url": "http://example.com/original",
      "shortened_url": "http://tinyurl.com/abc123"
    }
    ```

### 3. Get Original URL

- **Endpoint:** `GET /{url_id}`
- **Description:** Returns the original URL corresponding to the given `url_id`.
- **Parameters:**
  - `url_id` (required): Unique identifier of the requested URL.
- **Raises:**
  - `HTTPException (404)`: If a URL with the requested `url_id` does not exist.
  - `HTTPException (410)`: If a URL has been marked as deleted.
- **Response:**
  - `307 Temporary Redirect`:
    ```json
    {
      "original_url": "http://example.com/original"
    }
    ```

### 4. Get Usage Status

- **Endpoint:** `GET /{url_id}/status`
- **Description:** Returns the usage status of the requested URL.
- **Parameters:**
  - `url_id` (required): Unique identifier of the requested URL.
  - `full_info` (optional): False for obtaining the total number of requests, True for additional detailed information about each request (Default: False).
  - `pagination_parameters` (optional): Dictionary with pagination parameters (`max_result` for the number of rows returned, `offset` for skipping rows) (Default: `{ "max_result": 10, "offset": 0 }`).
- **Raises:**
  - `HTTPException (404)`: If a URL with the requested `url_id` does not exist.
- **Response:**
  - `200 OK`:
    - Total number of requests (if `full_info` is False):
     ```json
    {
      3
    }
    ```
    - List of request details (if `full_info` is True):
    ```json
        [
    {
        "url_id": 10,
        "usage_datetime": "2023-10-28T14:14:39.967234",
        "client_host": "172.19.0.1",
        "client_port": 58410
    },
    {
        "url_id": 10,
        "usage_datetime": "2023-10-28T15:01:29.835141",
        "client_host": "172.19.0.1",
        "client_port": 58628
    },
    {
        "url_id": 10,
        "usage_datetime": "2023-10-28T15:22:12.491003",
        "client_host": "172.19.0.1",
        "client_port": 58726
    }
    ]
    ```


### 5. Delete Short URL

- **Endpoint:** `DELETE /{url_id}`
- **Description:** Removes a short URL by its ID. The entry in the database remains but is marked as 'deleted'.
- **Parameters:**
  - `url_id` (required): Unique identifier of the requested URL.
- **Raises:**
  - `HTTPException (404)`: If a URL with the requested `url_id` does not exist.
  - `HTTPException (410)`: If a URL has been already marked as deleted.
- **Response:**
  - `200 OK`: Short URL successfully marked as deleted.


## Installation

    docker-compose build
    docker-compose up -d


## Migrations

    docker-compose exec webserver bash
    alembic current
    alembic revision --autogenerate -m 01_initial-db
    exit
