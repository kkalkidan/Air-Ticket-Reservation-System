from flask_sqlalchemy import SQLAlchemy
# from werkzeug import generate_password_hash, check_password_hash
import hashlib

db = SQLAlchemy()

class Flight(db.Model):
    __tablename__ = 'flight'
    airline_name = db.Column(db.String(50), primary_key = True)
    flight_num = db.Column(db.Integer, primary_key = True)
    departure_airport = db.Column(db.String(50))
    departure_time = db.Column(db.DateTime)
    arrival_airport = db.Column(db.String(50))
    arrival_time = db.Column(db.DateTime)
    price = db.Column(db.Float)
    status = db.Column(db.String(50))
    airplane_id = db.Column(db.Integer)

    def __init__(self, airline_name, flight_num, departure_airport,
     departure_time, arrival_airport, arrival_time, price, status, airplane_id):
        self.airline_name = airline_name
        self.flight_num = flight_num
        self.departure_airport = departure_airport
        self.departure_time = departure_time
        self.arrival_airport = arrival_airport
        self.arrival_time = arrival_time
        self.price = price
        self.status = status
        self.airplane_id = airplane_id

class Customer(db.Model):
    __tablename__ = 'customer'
    email = db.Column(db.String(50), primary_key = True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    building_number = db.Column(db.String(30))
    street = db.Column(db.String(30))
    city = db.Column(db.String(30))
    state = db.Column(db.String(30))
    phone_number = db.Column(db.Integer)
    passport_number = db.Column(db.String(30))
    passport_expiration = db.Column(db.Date)
    passport_country = db.Column(db.String(50))
    date_of_birth = db.Column(db.Date)

    def __init__(self, email, name, password, building_number, street, city, state,
phone_number, passport_number, passport_expiration, passport_country, date_of_birth):
        self.email = email
        self.name = name
        self.building_number = building_number
        self.street = street
        self.city = city
        self.state = state
        self.phone_number = phone_number
        self.passport_number = passport_number
        self.passport_expiration = passport_expiration
        self.passport_country = passport_country
        self.date_of_birth = date_of_birth
        self.password = self.hash_password(password)

    def hash_password(self, password):
        return hashlib.md5(password.encode()).hexdigest()

    def check_password(self, password):
        return self.hash_password(password) == self.password

class Airline_Staff(db.Model):
    __tablename__ = 'airline_staff'
    username = db.Column(db.String(50), primary_key = True)
    password = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    date_of_birth = db.Column(db.Date)
    airline_name = db.Column(db.String(50))


    def __init__(self, username, password, first_name, last_name, date_of_birth, airline_name):

        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.airline_name = airline_name
        self.password = self.hash_password(password)

    def hash_password(self, password):
        return hashlib.md5(password.encode()).hexdigest()

    def check_password(self, password):
        return self.hash_password(password) == self.password

class Airplane(db.Model):
    __tablename__ = 'airplane'
    airline_name = db.Column(db.String(50), primary_key = True)
    airplane_id = db.Column(db.Integer, primary_key = True)
    seats = db.Column(db.Integer)

    def __init__(self, airline_name,airplane_id, seats):
        self.airline_name = airline_name
        self.airplane_id = airplane_id
        self.seats = seats

class Booking_Agent(db.Model):
    __tablename__ = 'booking_agent'
    email = db.Column(db.String(50), primary_key = True)
    password = db.Column(db.String(50))
    booking_agent_id = db.Column(db.String(50))

    def __init__(self, email, password, booking_agent_id):

        self.email = email
        self.password = password
        self.booking_agent_id = booking_agent_id

    def hash_password(self, password):

        return hashlib.md5(password.encode()).hexdigest()

    def check_password(self, password):
        return self.hash_password(password) == self.password

class Ticket(db.Model):
    __tablename__ = 'ticket'
    ticket_id = db.Column(db.Integer, primary_key=True)
    airline_name = db.Column(db.String(50))
    flight_num = db.Column(db.String(50))

    def __init__(self, ticket_id, airline_name, flight_num):

        self.ticket_id = ticket_id
        self.airline_name = airline_name
        self.flight_num = flight_num

class Purchases(db.Model):
    __tablename__ = 'purchases'
    ticket_id = db.Column(db.Integer, primary_key=True)
    customer_email = db.Column(db.String(50), primary_key=True)
    booking_agent_id = db.Column(db.Integer)
    purchase_date = db.Column(db.Date)

    def __init__(self, ticket_id, customer_email, booking_agent_id, purchase_date):

        self.ticket_id = ticket_id
        self.customer_email = customer_email
        self.booking_agent_id = booking_agent_id
        self.purchase_date = purchase_date
