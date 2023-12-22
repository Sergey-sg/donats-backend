# ZCY Donation

## Prerequisites
- [Python 3.11](https://www.python.org/downloads/) installed
- [MySQL](https://www.mysql.com/downloads/) installed

## Installation Instructions

### 1. Python and Virtual Environment Setup
1. Install Python 3.11 if you haven't already. You can download it from the [official Python website](https://www.python.org/downloads/).
2. Create a virtual environment for this project (optional but recommended):

```bash
python3.11 -m venv myenv
source myenv/bin/activate  # For Unix/Mac 
myenv\Scripts\activate  # For Windows 
```

### 2. Packages Installation
```bash
cd zcy_donation
pip install -r requirements.txt
```

### 3. Creating a `.env` File and Adding `DATABASE_URL` in the `zcy_donation` Folder

To manage sensitive data and configurations separately, follow these steps:

1. **Navigate to the `zcy_donation` Folder:**
   ```bash
   cd /path/to/zcy_donation
   ```

2. **Create the `.env` File:**
   ```bash
   touch .env
   ```

3. **Add `DATABASE_URL` to `.env`:**
   - Open the `.env` file with a text editor and add your `DATABASE_URL` information:
     ```dotenv
     DATABASE_URL=your_database_url_here
     ```
     Replace `your_database_url_here` with the actual database URL or connection string.

4. **Save the `.env` File:**
   - Save the changes made to the `.env` file.
   - Ensure this file remains secure and is not committed to version control systems.

### 3. MySQL Configuration
Make sure the MySQL server is running.

### 4. Running the Application
1. Navigate to the project directory containing the Django project.
2. Run the Django development server:
   ```bash
   python manage.py runserver
   ```

### 5. Accessing the Application
Open a web browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to access the application.