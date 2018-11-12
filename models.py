from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

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
    
