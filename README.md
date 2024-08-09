# Transfer Appliation

This is a simple Flask web application simulating a basic banking system where users can log in, view their balance, transfer money to other users, and view their transaction history.

# NOTE!

Application on purpose has couple of vulnerabilities:
- plaintext password storage: Passwords are stored without hashing, making them easily retrievable from the database.
- lack of input validation: The application allows negative values in the transfer amount, which could lead to logic flaws such as increasing one's balance through negative transfers.
- no CSRF protection: The application is vulnerable to Cross-Site Request Forgery attacks.
- no rate limiting: The login functionality is vulnerable to brute-force attacks due to the absence of rate limiting.


# Running the application

To run the application, follow these steps:

#### Application - front-end side:

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/bank-transfer-app.git
    cd bank-transfer-app
    ```

2. Install dependencies:
    ```bash
    pip install Flask
    ```

3. Initialize the Database:
    ```bash
    python init_db.py
    ```

4. Run the applciation:
    ```bash
    python app.py
    ```

5. Access the Application:

Open your web browser and navigate to http://127.0.0.1:5000/.

# Tech stack
Application was created using:
- Python 3.6+,
- Flask,
- SQLite3.