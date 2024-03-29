# ZCY Donation Installation Guide

## Prerequisites
- Make sure Python 3.11 is installed. You can get it from the [official Python website](https://www.python.org/downloads/).
- Ensure MySQL is installed for the necessary database setup.

## Installation Steps

### 1. Python and Virtual Environment Setup
1. If Python 3.11 isn't installed, download it from the [official Python website](https://www.python.org/downloads/).
2. Install Poetry by executing:
    ```bash
    pip install poetry 
    ```

### 2. Package Installation
Install the required packages by running:
```bash
poetry install
```

### 3. Configuring Sensitive Data
1. **Navigate to the `config` Folder:**
    ```bash
    cd /path/to/config
    ```
2. **Create the `.env` File:**
    ```bash
    touch .env
    ```
3. **Edit the `.env` file:**
    Add your database connection details as separate fields:
    ```dotenv
    DB_NAME='dbname'
    DB_USER='username'
    DB_PASSWORD='password'
    DB_HOST='hostname'
    DB_PORT='your_port'
    DB_ROOT_PASSWORD='your_root_password'
    ```
    Replace `'dbname'`, `'username'`, `'password'`, `'hostname'`, `'your_port'`, and `'your_root_password'` with your actual database credentials.
    Also, update the key:
    ```dotenv
    SECRET_KEY='secret_key'
    ```
    Generate the key with:
    ```bash
    python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
    ```
    Add your Cloudinary api settings:
    ```dotenv
    CLOUD_NAME='cloud name'
    API_KEY='api key'
    API_SECRET='api secret'
    ```

4. **Save the Changes:**
    Save the `.env` file with the added database configuration fields.

### 4. MySQL Configuration
Ensure the MySQL server is active and running.

### 5. Running the Application
1. Navigate to the Django project directory.
2. Start the Django development server:
    ```bash
    poetry run python manage.py runserver
    ```
### 6. Run docker container
Make sure the docker is downloaded locally and .env file is on the same level as docker-compose.yml
1. Navigate to the Django project directory.
2. Run docker:
    ```bash
    docker-compose up --build
    ```
### 7. Accessing the Application
Open a web browser and go to [http://localhost:8080/](http://localhost:8080/) to access the application.
