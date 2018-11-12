from flask import Flask, render_template, request, json

from forms import  UpcomingForm

from models import Flight, db

from sqlalchemy import text

with open('queries.json') as f:
    data = json.load(f)

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

# @app.route("/search",  methods = ['GET', 'POST'])
# def search():
#     if(request.method == 'POST'):
#         return render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True)
