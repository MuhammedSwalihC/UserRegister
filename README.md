# UserRegister

This is a sample README file for a Python Flask application that allows adding users with different roles using a Postgres database and Marshmallow schema. The application provides an API for adding users to the database with different roles such as Super Admin, Admin, Staff, Editor, and Student.

## Technologies Used

The following technologies have been used to develop this application:

1. Python 3
2. Flask Framework
3. Marshmallow Schema
4. Postgres SQL Database

## Installation

### 1. Clone the repository:

git clone https://github.com/MuhammedSwalihC/UserRegister.git

### 2. Install the required packages using the following command:

    python3 -m venv env

    source env/bin/activate

    pip install -r requirements.txt

### 3. Create a Postgres database with the name "register_db" and configure the database credentials in the application's config file (.env).

    FLASK_APP=wsgi.py
    FLASK_RUN_PORT=2020
    FLASK_DEBUG=True

### 4. Run the following command to create the database tables:

    flask db migrate
    flask db upgrade

### 5. Start the Flask server using the following command:

    flask run

## API Collection

Link = <https://api.postman.com/collections/15161399-b7ae2e26-f079-4cfd-9098-a45f2f481c56?access_key=PMAT-01GTRB8VYA8FE14WSCP06RA47Y>
