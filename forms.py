from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.html5 import DateField, TimeField, IntegerField
from wtforms.validators import DataRequired, Email, Length
import datetime

class UpcomingForm(Form):

    arrival_airport= StringField("Arrival airport or City", validators=[DataRequired()])
    departure_airport = StringField("Departure airport or City", validators=[DataRequired()])
    submit = SubmitField("Search")

class Login(Form):

    email = StringField('Email', validators = [ DataRequired('Please enter your email'),
                    Email('Please enter a valid email address')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Sign in')

class Signup(Form):

    email = StringField('Email', validators = [ DataRequired('Please enter your email'),
                    Email('Please enter a valid email address')])
    name = StringField('Name', validators = [ DataRequired('Please enter your name')])
    password = PasswordField('Password', validators = [DataRequired(), Length(min=3)])
    building_number = StringField('Building Number', validators = [DataRequired()])
    street = StringField('Street', validators = [DataRequired()])
    city = StringField('City', validators = [DataRequired()])
    state = StringField('State', validators = [DataRequired()])
    phone_number = IntegerField("Phone number", validators = [DataRequired()])
    passport_number = StringField('Passport number', validators = [DataRequired()])
    passport_expiration = DateField('Passport Expiration', validators = [DataRequired()])
    passport_country = StringField('Passport Country', validators = [DataRequired()])
    date_of_birth = DateField('Date of birth', validators = [DataRequired()])
    submit = SubmitField('Sign up')

class FlightForm(Form):
    airline_name = StringField('Airline name', validators = [ DataRequired('Please enter the name of the airline')])
    flight_num = IntegerField("Flight number", validators = [DataRequired()])
    departure_airport = StringField('Departure airport', validators = [ DataRequired('Please enter the anme of departure airport')])
    departure_time = TimeField('Departure time',validators = [DataRequired()])
    departure_date = DateField('Departure date',validators = [DataRequired()])
    arrival_airport = StringField('Arrival airport', validators = [ DataRequired()])
    arrival_date = DateField('Arrival date',validators = [DataRequired()] )
    arrival_time = TimeField('Arrival time',validators = [DataRequired()] )
    price = IntegerField("Price", validators = [DataRequired()])
    status = StringField('Status', validators = [ DataRequired()])
    airplane_id =IntegerField("Airplane ID", validators = [DataRequired()])
    submit = SubmitField('Add Flight')

class StaffForm(Form):

    username = StringField('User name', validators = [ DataRequired()])
    password = PasswordField('Password', validators = [ DataRequired()])
    first_name = StringField('First name', validators = [ DataRequired()])
    last_name = StringField('Last name', validators = [ DataRequired()])
    date_of_birth = DateField('Date of birth',validators = [DataRequired()] )
    airline_name = StringField('Airline name', validators = [ DataRequired()])
    submit = SubmitField('Add Staff')

class StaffSignInForm(Form):

    username = StringField('User name', validators = [ DataRequired()])
    password = PasswordField('Password', validators = [ DataRequired()])
    submit = SubmitField('Sign in')

class FlightSearchByDateRange(Form):
    start_date = DateField('From', validators=[DataRequired()], default=datetime.datetime.now().date())
    end_date = DateField('To',  validators=[DataRequired()], default=datetime.datetime.now().date() + datetime.timedelta(days=30))
    submit = SubmitField('Search')

class StaffDetails(Form):
    flight_num = IntegerField('Flight Number', validators=[DataRequired()])
    edit_status = StringField('Current Status', validators=[DataRequired()])
    submit = SubmitField('Edit Status')

class AddAirPlane(Form):
    airline_name = StringField('Airline name', validators=[DataRequired()])
    airplane_id = IntegerField('Airplane Id', validators=[DataRequired()])
    seats = IntegerField('Number of seats', validators=[DataRequired()])
    submit = SubmitField('Add Airplane')

class Booking_Agent_SignInForm(Form):
    email = StringField('Email', validators = [ DataRequired()])
    password = PasswordField('Password', validators = [ DataRequired()])
    submit = SubmitField('Sign in')

class AgentPurchaseForm(Form):
    customer_email = StringField('customer_email', validators=[DataRequired()])
    booking_agent_id = IntegerField('booking_agent_id', validators=[DataRequired()])
    purchase_date = DateField('purchase date', validators=[DataRequired()])
    # submit = SubmitField('Purchase')
class ClientPurchaseForm(Form):
    customer_email = StringField('customer_email', validators=[DataRequired()])
    purchase_date = DateField('purchase date', validators=[DataRequired()])
    # submit = SubmitField('Purchase')
class AddAirport(Form):
    airport_name = StringField('Airport name', validators=[DataRequired()])
    airport_city = StringField('Airport city', validators=[DataRequired()])
    submit = SubmitField('Add Airport', validators=[DataRequired()])
