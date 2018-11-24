from flask import Flask, render_template, request, json, session, redirect, url_for

from forms import  UpcomingForm, Login, Signup, FlightForm, StaffForm, StaffSignInForm

from models import Flight, db, Customer, Airline_Staff

from datetime import datetime

from sqlalchemy import text

# with open('queries.json') as f:
#     data = json.load(f)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:password@localhost/aviation" #configure the flask app to SQLALCHEMY
db.init_app(app)
app.secret_key = 'development-key' #cross sight request forgery
#connect = db.engine


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/upcoming", methods = ['GET', 'POST'])
def upcoming():
    form = UpcomingForm();
    if (request.method == 'GET'):
        return render_template('upcoming.html', form=form)
    elif (request.method == 'POST'):
        arrival_airport = form.arrival_airport.data
        departure_airport = form.departure_airport.data
        sql = text(
              "SELECT * "
              "FROM flight "
              "WHERE flight.arrival_airport like :x and \
              flight.departure_airport like :y")
        # flight = db.engine.execute(sql, x = arrival_airport, y=departure_airport)
        flight = Flight.query.filter_by(arrival_airport=arrival_airport, departure_airport=departure_airport)
        return render_template('upcoming.html', list=flight)
        # return redirect(url_For('search'))

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for(''))
    form = Login()
    if(request.method == 'GET'):
        return render_template('login.html', form = form)
    elif (request.method == 'POST'):
        email= form.email.data
        password = form.password.data
        customer = Customer.query.filter_by(email=email).first()
        if customer is not None and customer.check_password(password):
            session['email'] = form.email.data
            return redirect(url_for('upcoming'))
        else:
            return render_template('login.html', form=form)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = Signup()

    if(request.method == 'POST'):
        print(form.validate_on_submit())
        if not form.validate_on_submit():
            return render_template('signup.html', form=form)
        else :
            newcustomer = Customer(form.email.data, form.name.data, form.password.data, form.building_number.data, form.street.data, form.city.data, form.state.data,
            form.phone_number.data, form.passport_number.data, form.passport_expiration.data, form.passport_country.data, form.date_of_birth.data)
            db.session.add(newcustomer);
            db.session.commit()
            session['email'] = newcustomer.email
            return redirect(url_for('upcoming'))
    elif (request.method == 'GET'):
        return render_template('signup.html', form=form)


@app.route("/addflight", methods=['GET', 'POST'])
def addflight():

    if 'username' not in session:
        return redirect(url_for('upcoming'))
    form = FlightForm()
    if(request.method == 'POST'):
        if not form.validate_on_submit():

             return render_template('addflight.html', form=form)
        else :
            arrival_date_time = str(form.arrival_date.data)+ " " + str(form.arrival_time.data)
            departure_date_time = str(form.departure_date.data) + " " + str(form.departure_time.data)
            newflight = Flight(form.airline_name.data, form.flight_num.data, form.departure_airport.data,
            departure_date_time, form.arrival_airport.data, arrival_date_time, form.price.data, form.status.data, form.airplane_id.data)
            return redirect(url_for('upcoming'))
    elif (request.method == 'GET'):
        return render_template('addflight.html', form=form)


@app.route("/logout")
def logout():
    print(request)
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('index'))


@app.route("/staff", methods=['GET', 'POST'])
def airline_staff():
    form = StaffForm()
    if(request.method == 'POST'):
        print(form.validate_on_submit())
        if not form.validate_on_submit():
            return render_template('staff.html', form=form)
        else :
            newstaff = Airline_Staff(form.username.data, form.password.data, form.first_name.data,
            form.last_name.data, form.date_of_birth.data, form.airline_name.data)
            db.session.add(newstaff);
            db.session.commit()
            session['username'] = newstaff.username
            return redirect(url_for('upcoming'))
    elif (request.method == 'GET'):
        return render_template('staff.html', form=form)

@app.route("/staff_login", methods = ['GET', 'POST'])
def staff_login():
    if 'user' in session:
        return redirect(url_for(''))
    form = StaffSignInForm()
    if(request.method == 'GET'):
        return render_template('staff_login.html', form = form)
    elif (request.method == 'POST'):
        username= form.username.data
        password = form.password.data
        staff = Airline_Staff.query.filter_by(username=username).first()
        if staff is not None and staff.check_password(password):
            session['username'] = form.username.data
            return redirect(url_for('staff_view'))
        else:
            return render_template('staff_login.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)
