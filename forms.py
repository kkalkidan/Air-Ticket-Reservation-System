from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class UpcomingForm(Form):
    arrival_airport= StringField("Arrival airport or City", validators=[DataRequired()])
    departure_airport = StringField("Departure airport or City", validators=[DataRequired()])
    submit = SubmitField("Search")
