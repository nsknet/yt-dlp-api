# yt_dlp API Application

This is a simple Python application that provides several API endpoints to interact with YouTube videos using `yt_dlp`.

## Prerequisites

- Python 3.7 or higher
- `pip` (Python package installer)

## Installation

1. Clone the repository to your local machine:

    ```sh
    git clone https://github.com/your-username/yt_dlp_api_app.git
    cd yt_dlp_api_app
    ```

2. Create a virtual environment (recommended):

    ```sh
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:

        ```sh
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```sh
        source venv/bin/activate
        ```

4. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Running the Application

1. Start the Flask application:

    ```sh
    python main.py
    ```

2. The application will start running on `http://127.0.0.1:5000/`.

## API Endpoints

### 1. Get Download Info

- **Endpoint:** `/api/get-download-info?url={url}`
- **Method:** `GET`
- **Description:** Retrieves information about the YouTube video without downloading it.
- **Response:** JSON containing video details such as `id`, `title`, `thumbnail`, `duration`, `formats`, etc.

### 2. Start Download

- **Endpoint:** `/api/start-download?url={url}&format={format}`
- **Method:** `GET`
- **Description:** Starts downloading the video in the specified format. Returns a `sessionId`.
- **Response:** JSON containing the `sessionId`.

### 3. Session Status

- **Endpoint:** `/api/session-status/{sessionId}`
- **Method:** `GET`
- **Description:** Retrieves the current status of the download session.
- **Response:** JSON containing the current status of the download.

### 4. Download File

- **Endpoint:** `/api/download-file/{sessionId}`
- **Method:** `GET`
- **Description:** Returns the downloaded file for the given session.
- **Response:** The downloaded file.

## Sample requests

    http://127.0.0.1:5000/api/get-download-json?url=https://www.youtube.com/watch?v=nfWlot6h_JM
    http://127.0.0.1:5000/api/get-download-info?url=https://www.youtube.com/watch?v=nfWlot6h_JM
    
    http://127.0.0.1:5000/api/start-download?url=https://www.youtube.com/watch?v=nfWlot6h_JM
    http://127.0.0.1:5000/api/session-status/WSOmYOYQlQ

    http://127.0.0.1:5000/api/download-file/WSOmYOYQlQ
