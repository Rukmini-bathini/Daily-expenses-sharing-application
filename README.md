# Daily Expenses Sharing Application

## Description
This application allows users to share daily expenses, add users, and generate balance sheets. The balance sheets include total paid and total expenses for each user.

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/Rukmini-bathini/Daily-expenses-sharing-application
2. Navigate to the project directory
   ```sh
   cd Daily-expenses-sharing-application
3. Create and activate a virtual environment:
   On Windows:
    ```sh
    python -m venv venv
    venv\Scripts\activate
    ```

   On macOS/Linux:
     ```sh
    python -m venv venv
    source venv\bin\activate
     ```
5. Install the dependencies:
   ```sh
   pip install -r requirements.txt
6. Run the Application
   ```sh
   python app.py

## Project Structure
### `app.py`
- Initializes the Flask application and SQLAlchemy.
- Defines routes for creating users, adding expenses, and generating the balance sheet.
- Implements the logic for splitting expenses and calculating total paid and total expenses for each user.

### `config.py`
- Contains configuration settings for the Flask application, including the database URI.

### `models/`
- **`__init__.py`**: Initializes the SQLAlchemy database instance.
- **`user.py`**: Defines the `User` model with fields for ID, email, name, and mobile number. This model represents users in the application.
- **`expense.py`**: Defines the `Expense` model with fields for ID, description, amount, payer ID, and split method. This model represents expenses recorded in the application.
- **`expense_split.py`**: Defines the `ExpenseSplit` model with fields for ID, expense ID, user ID, amount, and percentage. This model represents how each expense is split among users.

### `templates/`
- **`index.html`**: Provides a web interface with forms to add users and expenses, and a button to download the balance sheet CSV file. It uses Bootstrap for styling and includes JavaScript for handling form submissions.

### `requirements.txt`
- Lists the Python packages required to run the application, such as Flask and SQLAlchemy.

### `README.md`
- Provides an overview of the project, instructions for installation and running the application, and details about the project structure and usage.



