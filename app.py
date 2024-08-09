from flask import Flask, request, redirect, render_template, session, url_for, g, jsonify
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

DATABASE = 'database.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def query_db(query, args=(), one=False):
    con = get_db()
    cur = con.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# def init_db():
#     with app.app_context():
#         db = get_db()
#         with open('schema.sql', 'r') as f:
#             db.executescript(f.read())

# @app.before_first_request
# def setup():
#     init_db()

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = query_db('SELECT * FROM users WHERE username = ? AND password = ?', [username, password], one=True)
        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/user/<id>')
def get_user(id):
    user = query_db('SELECT username FROM users WHERE id = ?', [id], one=True)
    username = user['username']
    print(username)
    return jsonify({"username": username})

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = query_db('SELECT * FROM users WHERE username = ?', [session['username']], one=True)
    return render_template('dashboard.html', user=user)

@app.route('/history')
def history():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = query_db('SELECT * FROM users WHERE username = ?', [session['username']], one=True)
    all_transactions = query_db('''
        SELECT * FROM transactions 
        WHERE sender_id = ? OR recipient_id = ?
        ORDER BY timestamp DESC
    ''', [user['id'], user['id']])
    in_transactions = query_db('''
        SELECT * FROM transactions 
        WHERE recipient_id = ?
        ORDER BY timestamp DESC
    ''', [user['id']])
    out_transactions = query_db('''
        SELECT * FROM transactions 
        WHERE sender_id = ?
        ORDER BY timestamp DESC
    ''', [user['id']])
    return render_template('history.html',
                            all_transactions=all_transactions, 
                            user=user,
                            in_transactions=in_transactions,
                            out_transactions=out_transactions
                            )

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        recipient_id = request.form['recipient']
        amount = float(request.form['amount'])
        print(recipient_id)
        # if amount <= 0:
        #     return "Amount must be positive", 400
        user = query_db('SELECT * FROM users WHERE username = ?', [session['username']], one=True)
        recipient = query_db('SELECT * FROM users WHERE id = ?', [recipient_id], one=True)
        if recipient and user['balance'] >= amount:
            with get_db() as con:
                con.execute('UPDATE users SET balance = balance - ? WHERE username = ?', [amount, session['username']])
                con.execute('UPDATE users SET balance = balance + ? WHERE id = ?', [amount, recipient_id])
                con.execute('INSERT INTO transactions (sender_id, recipient_id, amount) VALUES (?, ?, ?)',
                             [user['id'], recipient['id'], amount])
                con.commit()
            return redirect(url_for('dashboard'))
        else:
            return "Transaction failed. Check recipient and balance.", 400
    users = query_db('SELECT username FROM users WHERE username != ?', [session['username']])
    return render_template('transfer.html', users=[user['username'] for user in users])

@app.route('/all-users', methods=['GET'])
def all_users():
    if 'username' not in session:
        return redirect(url_for('login'))
    users = query_db('SELECT id, username FROM users WHERE username != ?', [session['username']])
    return jsonify([{'id': user['id'], 'username': user['username']} for user in users])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
