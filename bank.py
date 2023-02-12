from flask import Flask, request, render_template, session
import os

app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    # SQL injection vulnerability
    username = request.form['username']
    password = request.form['password']
    query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'"
    result = os.system(query)
    if result:
        # Insecure session management vulnerability
        session['username'] = username
        return render_template('account.html', username=username)
    else:
        return 'Invalid login credentials.'

@app.route('/transfer', methods=['POST'])
def transfer():
    # CSRF vulnerability, file inclusion vulnerability and SQL injection vulnerability
    if 'username' in session:
        recipient = request.form['recipient']
        amount = request.form['amount']
        account_number = request.form['account_number']
        query = "UPDATE accounts SET balance = balance -" + amount + " WHERE account_number='" + account_number + "'"
        os.system(query)
        query = "UPDATE accounts SET balance = balance +" + amount + " WHERE account_number='" + recipient + "'"
        os.system(query)
        return 'Funds transferred to ' + recipient
    else:
        return 'Not logged in'

@app.route('/statement', methods=['GET'])
def statement():
    # File inclusion vulnerability
    account_number = request.args.get('account_number')
    statement = open(account_number+'_statement.txt', 'r').read()
    return statement

if __name__ == '__main__':
    app.run()