import json
import logging
import sqlite3
from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

app = Flask(__name__)
global user_id
logging.basicConfig(filename='log', level=logging.DEBUG, format='%(asctime)s::%(levelname)s:%(message)s')

#connection to the data base
def dbconn():
    conn = sqlite3.connect(r'C:\Users\Yehudit\Desktop\finalproject\db.db')
    return conn

#home page
@app.route('/', methods=['GET'])
def home_page():
    logging.debug("home page request")
    return render_template('home.html')

class RegistrationForm():
    full_name = StringField('Full name', validators=[DataRequired(), Length(min=2, max=20)])
    password = StringField('Password', validators=[DataRequired()])
    real_id = StringField('ID', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_real_id(self, real_id):
        user = User.query.filter_by(real_id=real_id.data).first()
        if user:
            raise ValidationError('This ID already exists.')


class LoginForm():
    full_name = StringField('Full name', validators=[DataRequired(), Length(min=2, max=20)])
    password = StringField('Password', validators=[DataRequired()])
    real_id = StringField('ID', validators=[DataRequired()])
    submit = SubmitField('Login')


#register page
@app.route("/register", methods=['GET','POST'])
def register():
    conn = dbconn()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    logging.debug("user verified")
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(password=hashed_password, real_id=form.real_id.data)
        user = conn.execute(f'SELECT * FROM users WHERE real_id = {real_id} AND password = {password}')
        conn.commit()
        conn.close()
        flash('Your account has been created! You are now able to log in', 'success')
        logging.debug("user register successfully")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

#login page
@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    logging.debug("user verified")
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(ID=form.ID.data).first()
        flash('You have been logged in!', 'success')
        logging.debug("user successful logged in")
        return redirect(url_for('home'))
    else:
        flash('Login Unsuccessful. Please check Full name and Password', 'danger')
    return render_template('login.html', title='Login', form=form)

class User():
    def __init__(self, id_AI, full_name, password, real_id):
        self.id_AI = id_AI
        self.full_name = full_name
        self.password = password
        self.real_id = real_id

    def __repr__(self):
        return f"User('{self.id_AI}','{self.full_name }','{self.password}','{self.real_id}')"
    
#users home page
@app.route('/users_home', methods=['GET'])
def users():
    logging.debug("users home page request")
    return render_template('users.html')

@app.route('/users', methods=['GET', 'POST'])
def users_gp():
    try:
        #get request for all users
        if request.method == 'GET':
            conn = dbconn()
            allusers = ""
            users2 = conn.execute('SELECT * FROM users')
            for row in users2:
                user = {"id_ai":row[0],"full_name":row[1],"password":row[2],"real_id":row[3]}
                all_users.append(user)
            conn.close()
            return all_users
    except:
        logging.debug("something went wrong")
        return render_template('error.html')
    try:
        #creating a new user
        if request.method == 'POST':
            conn = dbconn()
            full_name = request.form['full name']
            password = request.form['password']
            real_id = request.form['id']
            conn.execute(
                f'INSERT INTO users (full_name, password, real_id) VALUES ("{full_name}","{password}","{real_id}")')
            conn.commit()
            conn.close()
            logging.debug("new user created")
            return render_template('theTicketSite.html')
    except:
        logging.debug("something went wrong")
        return render_template('error.html')

@app.route('/users/<int:id>', methods=['GET', 'DELETE'])
def user_id(id):
    try:
        #request for a specific user
        if request.method == 'GET':
            logging.debug(f"returning user {id}")
            conn = dbconn()
            user = conn.execute(f'SELECT * FROM users WHERE id_AI = {id}')
            print(user)
            users1 = ""
            for row in user:
                a={"id_ai":row[0],"full_name":row[1],"password":row[2],"real_id":row[3]}
                users1 = users1 + a
            conn.close()
            return users1
    except:
        logging.debug("something went wrong")
        return render_template('error.html')
    try:
        #request to delete a specific user
        if request.method == 'DELETE':
            logging.debug(f"deleting {id} user")
            conn = dbconn()
            conn.execute(f'DELETE FROM users WHERE  id_AI = {id}')
            conn.commit()
            conn.close()
            return 'The ticket has been deleted'
    except:
        logging.debug("something went wrong")
        return render_template('error.html')

@app.route('/users/put', methods=['PUT'])
def users_p():
    try:
        #request to update a user
        full_name = request.form['full name']
        password = request.form['psw']
        real_id = request.form['id']
        logging.debug(f"updating the user {real_id}")
        conn = dbconn()
        id_AI = f'SELECT id_AI FROM users WHERE real_id = "{real_id}"'
        conn.execute(
            f'UPDATE users SET full_name = "{full_name}", password = "{password}", real_id = "{real_id}" WHERE id_AI = {id_AI}')
        conn.commit()
        user = conn.execute(f'SELECT * FROM users WHERE id_AI= {id_AI}')
        conn.close()
        return user
    except:
        logging.debug("something went wrong")
        return render_template('error.html')

#tickets home page
@app.route('/home_tickets', methods=['GET'])
def tickets():
    logging.debug("tickets page request")
    return render_template('theTicketSite.html')

@app.route('/tickets/get', methods=['GET'])
def tickets_g():
    try:
        #request for all the tickets
        logging.debug("all the tickets request")
        tickets = dbconn().execute(f'SELECT * FROM tickets')
        alltickets = ""
        for row in tickets:
            a = str(row)
            alltickets = alltickets + a
        return alltickets
    except:
        logging.debug("something went wrong")
        return render_template('error.html')

@app.route('/tickets/<int:t_id>', methods=['GET'])
def ticket_g(t_id):
    try:
        #request of a specific ticket
        if request.method == 'GET':
            logging.debug(f"returning the ticket where the id={t_id}")
            ticket = getconn().execute(f'SELECT * FROM tickets WHERE ticket_id = {t_id}')
            dbconn().close()
            ticket2 = ""
            for row in ticket:
                a = str(row)
                ticket2 = ticket2 + a
            return ticket2
    except:
        logging.debug("something went wrong")
        return render_template('error.html')

@app.route('/tickets/post', methods=['POST'])
def tickets_p():
    try:
        #request to create a new ticket
        if request.method == 'POST':
            user_id = request.form['user id']
            flight_id = request.form['flight id']
            logging.debug(f"new ticket created")
            dbconn().execute(f'INSERT INTO tickets (user_id, flight_id) VALUES ({user_id},{flight_id})')
            dbconn().commit()
            dbconn().execute(
                f'UPDATE flights set remaining_seats = (SELECT remaining_seats FROM flights WHERE flight_id = {flight_id}) -1')
            dbconn().commit()
            dbconn().close()
            return 'the action completed'
    except:
        logging.debug("something went wrong")
        return render_template('error.html')

@app.route('/tickets/delete', methods=['DELETE'])
def ticket_d():
    try:
        #request to delete a specific ticket
        if request.method == 'DELETE':
            id = request.form['id']
            flight_id = dbconn().execute(f'SELECT flight_id FROM tickets WHERE ticket_id = {id}')
            dbconn().execute(f'DELETE FROM tickets WHERE ticket_id  = {id}')
            dbconn().commit()
            dbconn().execute(
                f'UPDATE flights set remaining_seats = (SELECT remaining_seats FROM flights WHERE flight_id = {flight_id}) +1')
            dbconn().commit()
            dbconn().close()
            logging.debug("a ticket deleted")
            return 'Ticket deleted'
    except:
        logging.debug("something went wrong")
        return render_template('error.html')

#flights home page request
@app.route('/home_flights', methods=['GET'])
def flights():
    try:
        logging.debug("flights home request")
        return render_template('theFlightSite.html')
    except:
        logging.debug("something went wrong")
        return render_template('error.html')

@app.route('/flights/get_post', methods=['GET', 'POST'])
def flights_gp():
    try:
        #request for all the flights
        if request.method == 'GET':
            flights = dbconn().execute(f'SELECT * FROM flights WHERE remaining_seats > 0')
            allflights = ""
            for row in flights:
                a = str(row)
                allflights = allflights + a
            dbconn().close()
            logging.debug("returning all the flights")
            return allflights
    except:
        logging.debug("something went wrong")
        return render_template('error.html')
    try:
        #create a new flight
        if request.method == 'POST':
            timestamp = request.form['time']
            remaining_seats = request.form['remaining seats']
            origin_country_id = request.form['original country id']
            dest_country_id = request.form['destination country id']
            dbconn().execute(
                f'INSERT INTO flights(timestamp, origin_country_id, dest_country_id, remaining_seats) VALUES({timestamp},{origin_country_id},{dest_country_id}, {remaining_seats})')
            dbconn().commit()
            dbconn().close()
            logging.debug("a new flight created")
            return 'a new flight created'
    except:
        logging.debug("something went wrong")
        return render_template('error.html')

@app.route('/flights/<int:flight_id>', methods=['GET', 'DELETE'])
def flights_gd(flight_id):
    try:
        #request of a specific flight
        if request.method == 'GET':
            logging.debug(f"getting the flights with the id {flight_id}")
            flight = dbconn().execute(f'SELECT * FROM flights WHERE flight_id = {flight_id}')
            flight1 = ""
            for row in flight:
                a = str(row)
                flight1 = flight1 + a
            dbconn().close()
            return flight1
    except:
        logging.debug("something went wrong")
        return render_template('error.html')
    try:
        #request to delete a flight
        if request.method == 'DELETE':
            dbconn().execute(f'DELETE FROM flights WHERE flight_id = {flight_id}')
            dbconn().commit()
            dbconn().close()
            logging.debug(f"deleting the flights with the id {flight_id}")
            return 'flight deletet'
    except:
        logging.debug("something went wrong")
        return render_template('error.html')

@app.route('/flights/put', methods=['PUT'])
def flights_p():
    try:
        #request to update a flight
        if request.method == 'PUT':
            flight_id = request.form['id']
            timestamp = request.form['time']
            remaining_seats = request.form['remaining seats']
            origin_country_id = request.form['original country id']
            dest_country_id = request.form['destination country id']
            dbconn().execute(
                f'UPDATE flights SET timestamp = {timestamp}, origin_country_id = {origin_country_id}, dest_country_id = {dest_country_id}, remaining_seats = {remaining_seats} WHERE flight_id = {flight_id}')
            dbconn().commit()
            dbconn().close()
            logging.debug(f"updating the flight where id = {flight_id}")
            return 'update succeeded'
    except:
        logging.debug("something went wrong")
        return render_template('error.html')

app.run()
