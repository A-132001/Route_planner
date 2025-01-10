#  [Loop presentation](https://drive.google.com/drive/folders/1gyQDoc5Z8bbB2oNCvlPx-1Na5aWuiKKt?usp=drive_link)

## Installation and Setup

### Clone the repository:

```bash
git clone <repository-url>
cd <repository-folder>
```

### Create and activate a virtual environment:

#### On Windows:

```bash
python -m venv venv
.\venv\Scripts\activate
```

#### On Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies:

```bash
pip install -r requirements.txt
```

### Run the Django development server:

```bash
python manage.py runserver
```

## Using the Endpoint

Make sure the server is running.

### To use the `get_route` endpoint, send a GET request to the following URL:

```bash
http://127.0.0.1:8000/api/get_route/?start=<start-coordinates>&finish=<finish-coordinates>
```

Replace `<start-coordinates>` and `<finish-coordinates>` with latitude and longitude in the format `latitude,longitude`.

#### Example:

```bash
http://127.0.0.1:8000/api/get_route/?start=37.7749,-122.4194&finish=34.0522,-118.2437
```

You will receive a JSON response with the route details, fuel stops, distance, and total cost.
