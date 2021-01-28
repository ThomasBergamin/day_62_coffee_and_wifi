from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe location on Google Maps (URL)', validators=[DataRequired(), URL()])
    opening = StringField('Opening time (e.g. 8AM)', validators=[DataRequired()])
    closing = StringField('Closing time (e.g. 5:30PM)', validators=[DataRequired()])
    coffee = SelectField('Coffee rating', choices=['✘', '☕', '☕☕', '☕☕☕', '☕☕☕☕'], validators=[DataRequired()])
    wifi = SelectField('WiFi strength rating', choices=['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪'], validators=[DataRequired()])
    outlets = SelectField('Power socket availability', choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌'], validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', encoding="utf8", newline='', mode="a") as csv_file:
            csv_file.write(f"\n{form.cafe.data}, "
                           f"{form.location.data}, "
                           f"{form.opening.data}, "
                           f"{form.closing.data}, "
                           f"{form.coffee.data}, "
                           f"{form.wifi.data}, "
                           f"{form.outlets.data}")
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', encoding="utf8", newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
