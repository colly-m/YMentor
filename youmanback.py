from flask import Flask, jsonify, request, render_template, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import mysql.connector
#from models import Model
from datetime import datetime

#conn = mysql.connector.connect(host="localhost")

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_username'
app.config['MYSQL_PASSWORD'] = 'your_password'
#app.config['MYSQL_DB'] = 'mentors_app'
app.config['SECRET_KEY'] = '58c65d7f2e4ec6a6830b51db79dcb1f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///youmentor.db'

db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    #posts =  db.relationship('Post', backref='author', lazy=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Users('{self.username}','{self.email}', '{self.image_file}')"
    

#class Post(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    #title = db.Column(db.String(100), nullable=False)
    #date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #content = db.Column(db.Text, nullable=False)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    #def __repr__(self):
        #return f"Post('{self.title}','{self.date_posted}')"

"""Sample mentor data"""
mentors = [
    {"id": 1, "name": "John Doe", "field": "Engineering"},
    {"id": 2, "name": "Jane Smith", "field": "Art"},
    # Add more mentor data as needed
]

users = {
    'user1': {'email': ''},
    'user2': {'email': ''}
}

"""Default route to handle unspecified routes"""
@app.route('/', methods=['GET'])
@app.route('/home')
def home():
    #user = User(username='john', email='john@example.com')
    #db.session.add(user)
    #db.session.commit()

    #users = User.query.all()
    #return str(users)

    return render_template('index.html', mentors=mentors)

@app.route("/about")
def about():
    return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            # Successful login
            return redirect(url_for('index'))
        else:
            # Invalid credentials
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html', error='Invalid username or password')

    # GET request (initial login page or forgot password link clicked)
    if 'forgot_password' in request.args:
        # Render forgot password page
        return render_template('forgot_password.html')

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return render_template('register.html' , error="Passwords do not match")
        
        if username in users:
            # User already exists
            flash('Username already exists', 'error')
            return render_template('register.html')
            # Add new user to the database (replace with database interaction)
        users[username] = {'email': email, 'password': password}
            # Successful sign-up
        flash('Sign up successful! Please log in.', 'success')
        return redirect(url_for('home'))
    return render_template('register.html')


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        if email in users:
            # Send password reset email (not implemented)
            flash('Password reset email sent.', 'info')
            return redirect(url_for('login'))
        else:
            flash('Email address not found.', 'error')
    return render_template('passreset.html')


# Create Custom Error Pages

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_not_found(e):
    return render_template('500.html'), 500


"""API endpoint to get all mentors"""
@app.route('/mentors', methods=['GET'])
def get_mentors():
    return jsonify(mentors)

"""API endpoint to add a new mentor"""
@app.route('/mentors', methods=['GER', 'POST'])
def add_mentor():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM mentors")
        mentors = cur.fetchall()
        cur.close()
        return jsonify(mentors)
    elif request.method == 'POST':
        new_mentor = request.json
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO mentors (name, field) VALUES (%s, %s)", (new_mentor['name'], new_mentor['field']))
        mysql.connection.commit()
        cur.close()
    return jsonify({"message": "Mentor added successfully", "mentor": mentor}), 201


if __name__ == '__main__':
    app.run(debug=True)  # Enable debugging to help diagnose errors