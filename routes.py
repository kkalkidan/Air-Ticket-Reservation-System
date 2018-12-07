from flask import Flask, render_template, request, json, session, redirect, url_for

from forms import  UpcomingForm, Login, Signup, FlightForm, StaffForm, StaffSignInForm, FlightSearchByDateRange,\
                StaffDetails, AddAirPlane, Booking_Agent_SignInForm, AgentPurchaseForm, ClientPurchaseForm,\
                AddAirport



from models import Flight, db, Customer, Airline_Staff, Airplane, Booking_Agent, Ticket, Purchases

import datetime

from sqlalchemy import text, update

global fofo
global purchased_flight
global fl_inf
global purchased_ticket


# with open('queries.json') as f:
#     data = json.load(f)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:password@localhost/aviation" #configure the flask app to SQLALCHEMY
db.init_app(app)
app.secret_key = 'development-key' #cross sight request forgery
#connect = db.engine


@app.route("/", methods = ['GET', 'POST'])
def index():
    form = UpcomingForm();
    if (request.method == 'GET'):
        return render_template('index.html', form=form)
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
        return render_template('index.html', form = form, list=flight)

@app.route("/upcoming", methods = ['GET', 'POST'])
def upcoming():
    if 'agent_username' not in session:
        session.clear() #until we implement the logout button
        return redirect(url_for('booking_agent_login'))
    form = UpcomingForm()
    agent_purhcase_form = AgentPurchaseForm()
    client_purhcase_form = ClientPurchaseForm()
    # check = request.args['check'] // what ??
    check = session['check'] #checks who's searching
    count = 0;
    check3 = 0
    if check == 1:
        purchase_form = agent_purhcase_form
    else:
        purchase_form = client_purhcase_form

    if (request.method == 'GET'):
        return render_template('upcoming.html', form=form, purchase_form=purchase_form, check2 = 0, check = check, list = [])
    elif (request.method == 'POST'):
        arrival_airport = form.arrival_airport.data
        departure_airport = form.departure_airport.data
        check2 = 1
        flight = Flight.query.filter_by(arrival_airport=arrival_airport, departure_airport=departure_airport).all()
        if (len(flight) != 0):
            global fofo
            fofo = flight
        flight_info = {}
        for x in range(len(flight)):
            flight_info[x] = []
            flight_info[x].append(flight[x].airline_name)
            flight_info[x].append(flight[x].departure_time)
            flight_info[x].append(flight[x].arrival_time)
            flight_info[x].append(flight[x].price)
            flight_info[x].append(flight[x].status)
            flight_info[x].append(flight[x].flight_num)
        if (len(flight_info) != 0):
            global fl_inf
            fl_inf = flight_info
        if len(flight_info) == 0 and len(fl_inf) != 0:
            values = request.values
            for item in values.items():
                if item[1].isdigit() and len(fofo) != 0 and item[0]!="check" and item[0]!="booking_agent_id":
                    selected_flight = int(item[1])
                    if len(fl_inf) != 0:
                        # global purchased_flight
                        #flight_info[selected_flight].append(flight[selected_flight].flight_num)
                        purchased_flight = fl_inf[selected_flight]
                        #print(fl_inf[selected_flight])
                        airline_name = fl_inf[selected_flight][0]
                        flight_num = fl_inf[selected_flight][5]
                        print(airline_name)
                        print(flight_num)
                        check2 = 3
                        ticket = Ticket.query.filter_by(airline_name=airline_name, flight_num=flight_num).first()
                        print(ticket)
                        global purchased_ticket
                        purchased_ticket = ticket
                elif len(fofo) != 0 and item[0]!="check":
                    customer_email = purchase_form.customer_email.data
                    booking_agent_id = purchase_form.booking_agent_id.data
                    purchase_date = purchase_form.purchase_date.data

                    """print(customer_email)
                    print(booking_agent_id)
                    print(purchase_date)"""
                    if (booking_agent_id != None):
                        # global purchased_ticket
                        print (purchased_ticket)
                        purchase = Purchases(purchased_ticket.ticket_id, customer_email, booking_agent_id, purchase_date)
                        db.session.add(purchase);
                        db.session.commit()
                        return redirect(url_for("booking_agent_view"))

        return render_template('upcoming.html', list=flight_info, purchase_form=purchase_form, check2 = check2, check = check, form=form)
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
            return redirect(url_for('index'))
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
        return redirect(url_for('index'))
    form = FlightForm()
    airplane = AddAirPlane()
    airport = AddAirport()
    if(request.method == 'POST'):

        if(form.flight_num.data != None):
            arrival_date_time = str(form.arrival_date.data)+ " " + str(form.arrival_time.data)
            departure_date_time = str(form.departure_date.data) + " " + str(form.departure_time.data)
            newflight = Flight(form.airline_name.data, form.flight_num.data, form.departure_airport.data,
            departure_date_time, form.arrival_airport.data, arrival_date_time, form.price.data, form.status.data, form.airplane_id.data)
            db.session.add(newflight)
            db.session.commit()
            return render_template('addflight.html', form=form, airplane=airplane, airport=airport)

        if(airplane.airline_name.data != None):
            newairplane = Airplane(airplane.airline_name.data, airplane.airplane_id.data, airplane.seats.data)
            db.session.add(newairplane);
            all_airplanes = Airplane.query.filter_by(airline_name = session['airline_name'])
            db.session.commit();
            return render_template('addflight.html', form=form, airplane=airplane, all_airplanes=all_airplanes,\
            airport=airport)

        if(airport.airport_name.data != None):
            newairport= Airport(airport.airport_name, airport_airport_city)
            db.session.add(newairport)
            db.commit(airport)
            return render_template('addflight.html', form=form, airplane=airplane,\
            airport=airport)



    elif (request.method == 'GET'):
        return render_template('addflight.html', form=form, airplane=airplane, airport=airport)


@app.route("/logout")
def logout():
    print(request)
    session.pop('username', None)
    session.pop('email', None)
    session.pop('agent_username', None)
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
            session['airline_name'] = newstaff.airline_name
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
            session['airline_name'] = staff.airline_name
            return redirect(url_for('staff_view'))
        else:
            return render_template('staff_login.html', form=form)


@app.route("/staff_view", methods = ['GET', 'POST'])
def staff_view():
    if 'username' not in session:
        return redirect(url_for('staff_login'))

    form=UpcomingForm()
    lcform = StaffDetails()
    update = ''
    if(lcform.flight_num.data != None):
        updated_flight = Flight.query.filter_by(flight_num=lcform.flight_num.data).first()
        updated_flight.status = lcform.edit_status.data
        db.session.commit()
        update = 'Flight -' + str(lcform.flight_num.data) +' is Updated !'

    dform = FlightSearchByDateRange()
    arrival_airport = form.arrival_airport.data
    departure_airport = form.departure_airport.data

    start_date = str(dform.start_date.data) + ' 00:00:00'
    end_date = str(dform.end_date.data) + ' 00:00:00'
    airline_name = session['airline_name']
    sql = text(
          "SELECT * "
          "FROM flight "
          "WHERE flight.departure_time between :x and \
           :y and flight.airline_name like :z")
    flight = db.engine.execute(sql, x = start_date, y= end_date, z= airline_name)
    list = Flight.query.filter_by(arrival_airport=arrival_airport, departure_airport=departure_airport)

    return render_template('staff_view.html',dform=dform, flight=flight, form=form, list=list, lcform=lcform, \
                            update=update)


@app.route("/staff_view2", methods=['GET', 'POST'])
def staff_view2():

    if 'username' not in session:
        return redirect(url_for('staff_login'))

    agent = Booking_Agent.query.filter_by().all()

    x = datetime.datetime.today().date()
    y = x - datetime.timedelta(days=365)
    print(x, y)
    sql_top_agents = text(
          "SELECT booking_agent.email\
          FROM booking_agent, purchases\
          WHERE booking_agent.booking_agent_id = purchases.booking_agent_id \
          GROUP BY booking_agent.booking_agent_id, booking_agent.email\
          ORDER BY COUNT(*)\
          LIMIT 5 ")

    sql_freq_flyers = text(
          "SELECT purchases.customer_email, ticket.flight_num\
          FROM purchases, ticket \
          WHERE purchases.purchase_date between :x and :y \
                and ticket.airline_name like :z\
                and ticket.ticket_id = purchases.ticket_id\
          GROUP BY purchases.customer_email\
          Having COUNT(*) > 3")

    top_agents=db.engine.execute(sql_top_agents)
    top_flyers=db.engine.execute(sql_freq_flyers, x = str(x) + '00:00', y = str(y) +'00:00', \
                z = session['airline_name'])
    print(top_agents)
    return render_template('staff_view2.html', booking_agent=agent, top_agents=top_agents, \
    top_flyers=top_flyers)




@app.route("/list_customers", methods=['GET', 'POST'])
def list_customers():
    if 'username' not in session:
        return redirect(url_for('index'))
    flight_num = request.args.get('flight_num')
    print(flight_num)
    flight = Flight.query.filter_by(flight_num = flight_num)
    return render_template('list_customers.html', flight = flight)

@app.route("/booking_agent_login", methods = ['GET', 'POST'])
def booking_agent_login():
    form1 = UpcomingForm()
    if 'agent_username' in session:
        session.clear() #until we implement the logout button
        return redirect(url_for('booking_agent_view'))
    form = Booking_Agent_SignInForm()
    if(request.method == 'GET'):
        return render_template('booking_agent_login.html', form = form)
    elif (request.method == 'POST'):
        email = form.email.data
        password = form.password.data
        booking_agent = Booking_Agent.query.filter_by(email=email).first()
        if booking_agent is not None and booking_agent.check_password(password):
            print ("sdsdssdss")
            session['agent_username'] = form.email.data
            session['agent_id'] = booking_agent.booking_agent_id
            print (session["agent_username"])
            print (session["agent_id"])
            return redirect(url_for('booking_agent_view'))
        else:
            return render_template('booking_agent_login.html', form=form)

@app.route("/booking_agent_view", methods = ['GET', 'POST'])
def booking_agent_view():
    if 'agent_username' not in session:
        session.clear() #until we implement the logout button
        return redirect(url_for('booking_agent_login'))
    if request.method == 'POST':
        values = request.values
        action = []
        for item in values.items():
            action.append(item[1])
        #session['recipes'] = all_recps
        to_do = action[0]
        print (to_do)
        if (to_do == "View My Flights"):
            return redirect(url_for("my_flights"))
        if (to_do == "Search for Flights"):
            check = 1
            session["check"] = check
            return redirect(url_for("upcoming", check = check))
        if (to_do == "View My Commission"):
            return redirect(url_for("commission"))
        if (to_do == "Top Customers"):
            return redirect(url_for("top_customers"))
    return render_template('booking_agent_view.html')  # we are just loading the page

@app.route("/my_flights", methods = ["GET"])
def my_flights():
    if 'agent_username' not in session:
        session.clear() #until we implement the logout button
        return redirect(url_for('booking_agent_login'))
    booking_agent_id = session["agent_id"]

    my_flights = Purchases.query.filter_by(booking_agent_id = booking_agent_id).all()
    all_flights = {}
    for x in range (len(my_flights)):
        all_flights[x] = []
        all_flights[x].append(my_flights[x].ticket_id)
        all_flights[x].append(my_flights[x].customer_email)
        all_flights[x].append(my_flights[x].purchase_date)

    print(all_flights)
    return render_template('booking_agent_my_flight.html', all_flights=all_flights)
@app.route("/commission", methods = ["GET", "POST"])
def commission():
    if 'agent_username' not in session:
        session.clear() #until we implement the logout button
        return redirect(url_for('booking_agent_login'))

    booking_agent_id = session["agent_id"]

    my_flights = Purchases.query.filter_by(booking_agent_id=booking_agent_id).all()
    my_ticket_price = []
    for x in range (len(my_flights)):
        ticket_id = my_flights[x].ticket_id
        This_ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
        airline_name = This_ticket.airline_name
        flight_num = This_ticket.flight_num

        flight = Flight.query.filter_by(airline_name=airline_name, flight_num=flight_num).first()
        ticket_price = flight.price
        my_ticket_price.append(ticket_price)
    total_commission = 0
    for x in my_ticket_price:
        total_commission = total_commission + (x * 0.1)
    total_number_of_tickets = len(my_ticket_price)
    average_commission = total_commission/total_number_of_tickets
    return render_template('booking_agent_commision.html', total_commission=total_commission, total_number_of_tickets=total_number_of_tickets, average_commission=average_commission)

@app.route("/top_customers", methods = ["GET"])
def top_customers():
    #all the graphing goes here
    if 'agent_username' not in session:
        session.clear() #until we implement the logout button
        return redirect(url_for('booking_agent_login'))
    booking_agent_id = session["agent_id"]
    print (booking_agent_id)
    my_flights = Purchases.query.filter_by(booking_agent_id = booking_agent_id).all()
    user_commission = {}
    for x in range (len(my_flights)):
        ticket_id = my_flights[x].ticket_id
        This_ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
        airline_name = This_ticket.airline_name
        flight_num = This_ticket.flight_num

        flight = Flight.query.filter_by(airline_name=airline_name, flight_num=flight_num).first()
        ticket_price = flight.price

        user = my_flights[x].customer_email
        if user in user_commission:
            user_commission[user] = user_commission[user] + (0.1 * ticket_price)
        else:
            user_commission[user] = 0.1 * ticket_price
    max_user = ("user", 0)
    for user in user_commission:
        if user_commission[user] > max_user[1]:
            max_user = (user, user_commission[user])
        else:
            continue
    top_customer = max_user[0]
    top_customer_commission = max_user[1]
    print(max_user)
    return render_template('top_customers.html', top_customer = top_customer, top_customer_commission = top_customer_commission)




if __name__ == '__main__':
    app.run(debug=True)
