# System Installation Guide

## Prerequisites

Ensure you have Python 3.10 or newer installed on your system.

## Steps

1. **Clone the Repository**
   - Execute `git clone https://github.com/danlopatenco/product_price_monitor.git` to clone the project to your local machine.

2. **Set up a Virtual Environment** (Recommended)
   - Navigate to the project directory.
   - Create a virtual environment with `python3 -m venv venv`.
   - Activate it:
     - Windows: `.\venv\Scripts\activate`
     - Unix/MacOS: `source venv/bin/activate`

3. **Install Dependencies**
   - Install required Python packages with `pip install -r requirements/requirements.txt`.

4. **Database Migrations**
   - Prepare your database with `python manage.py migrate`.

5. **Run the Application**
   - Start the server using `python manage.py runserver`.
   - Access the app at `http://127.0.0.1:8000`.

## **Execute Tests**
Execute `python manage.py test` from the project directory to start the automated tests.
