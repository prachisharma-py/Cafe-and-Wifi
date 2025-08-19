import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField, URLField, BooleanField
from wtforms.validators import DataRequired
from sqlalchemy import and_
from flask_migrate import Migrate

#Load environment variables from .env file
load_dotenv()

# CREATE THE APP
app = Flask(__name__)
Bootstrap(app)

# CREATE THE SECRET KEY
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# CONNECT TO DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///instance/cafes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CREATE THE EXTENSION
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# INITIALIZE THE APP WITH THE EXTENSION
# db.init_app(app)

# CONFIGURE TABLE
class Cafes(db.Model):
    __tablename__ = 'cafe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(1000), nullable=False)
    location = db.Column(db.Text, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.Integer)
    coffee_price = db.Column(db.String(250))

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


# WTForm
class CafeForm(FlaskForm):
    name = StringField("Cafe Name", validators=[DataRequired()], render_kw={"style": "font-size: 12px"})
    map_url = URLField("Map Url", validators=[DataRequired()], render_kw={"style": "font-size: 12px"})
    img_url = URLField("Image Url", validators=[DataRequired()], render_kw={"style": "font-size: 12px"})
    location = StringField("Cafe Location", validators=[DataRequired()], render_kw={"style": "font-size: 12px"})
    has_wifi = BooleanField("Wifi Available?")
    has_sockets = BooleanField("Sockets Available?")
    has_toilet = BooleanField("Toilet Available?")
    can_take_calls = BooleanField("Can Take Calls?")
    seats = StringField("Number of Seats Available?")
    coffee_price = StringField("Cafe Coffee Price", validators=[DataRequired()], render_kw={"style": "font-size: 12px"})
    submit = SubmitField("Add Cafe", render_kw={"style": "font-size: 18px"})


def get_seats_range(selected_option):
    if selected_option == '0-10':
        return (0, 10)
    elif selected_option == '10-20':
        return (10, 20)
    elif selected_option == '20-30':
        return (20, 30)
    elif selected_option == '30-40':
        return (30, 40)
    elif selected_option == '40-50':
        return (40, 50)
    elif selected_option == '50+':
        return (50, float('inf'))
    else:
        return (0, float('inf'))


@app.route('/', methods=["GET"])
def home():
    selected_filters = {
        k: True if v.lower() == 'true' else False for k, v in request.args.items()
    }
    print("Selected Filters:", selected_filters)

    filter_conditions = []

    # Set a default value for selected_seats_option
    selected_seats_option = None

    if 'seats_dropdown' in request.args:
        selected_seats_option = request.args.get('seats_dropdown')
        print("Request Args:", request.args)
        print("Selected Seats Option:", selected_seats_option)

        if selected_filters and selected_seats_option:
            seats_range = get_seats_range(selected_seats_option)
            print("Seats Range:", seats_range)
            filter_conditions.append(and_(Cafes.seats >= seats_range[0], Cafes.seats < seats_range[1]))

    filter_conditions.extend([getattr(Cafes, k) == v for k, v in selected_filters.items() if hasattr(Cafes, k) and k != 'seats' and v])

    # Check if 'seats' filter is selected but 'seats_dropdown' is not chosen
    if 'seats' in selected_filters and selected_filters['seats'] and not selected_seats_option:
        flash('Please select the number of seats from the dropdown.', 'warning')
 
    if filter_conditions:
        filtered_cafes = Cafes.query.filter(and_(*filter_conditions)).all()
    else:
        filtered_cafes = Cafes.query.all()
    
    cafes_count = len(filtered_cafes)
    # print("Filtered Cafes:", filtered_cafes)
    

    # Check if filter conditions are provided and no cafes satisfy the conditions
    if filter_conditions and not filtered_cafes:
        return render_template("no_results.html", selected_filters=selected_filters)
    
    # Render index.html with filtered or all cafes
    return render_template("index.html", all_cafes=filtered_cafes, selected_filters=selected_filters, cafes_count=cafes_count)


@app.route('/add-cafe', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafes(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_wifi=form.has_wifi.data,
            has_sockets=form.has_sockets.data,
            has_toilet=form.has_toilet.data, 
            can_take_calls=form.can_take_calls.data,
            seats=form.seats.data,
            coffee_price=form.coffee_price.data,
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html", form=form)


@app.route('/delete-cafe', methods=["GET", "POST"])
def delete_cafe():
    if request.method == 'POST':
        cafe_id_to_delete = request.form.get('cafe_id')
        if cafe_id_to_delete:
            cafe_to_delete = Cafes.query.get_or_404(cafe_id_to_delete)
            db.session.delete(cafe_to_delete)
            db.session.commit()
            return redirect(url_for('home'))

    cafes = Cafes.query.all()
    return render_template('delete.html', all_cafes=cafes)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
