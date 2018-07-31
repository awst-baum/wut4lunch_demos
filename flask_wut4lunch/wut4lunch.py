from flask import Flask, request
from flask_restful import Resource, Api
from flask_restful import fields, reqparse, marshal_with, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

rest_api = Api(app)

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

class Lunch(db.Model):
    """A single lunch"""
    id = db.Column(db.Integer, primary_key=True)
    submitter = db.Column(db.String(63))
    food = db.Column(db.String(255))

    def __str__(self):
        return "{} ate {}".format(self.submitter, self.food)

#from flask_wtf import Form
from flask_wtf import FlaskForm as Form
from wtforms.fields import StringField, SubmitField

app.config['SECRET_KEY'] = 'please, tell nobody'

class LunchForm(Form):
    submitter = StringField(u'Hi, my name is')
    food = StringField(u'and I ate')
    submit = SubmitField(u'share my lunch!')

from flask import render_template

@app.route("/")
def root():
    lunches = Lunch.query.all()
    form = LunchForm()
    return render_template('index.html', form=form, lunches=lunches)

from flask import url_for, redirect

@app.route(u'/new', methods=[u'POST'])
def newlunch():
    form = LunchForm()
    if form.validate_on_submit():
        lunch = Lunch()
        form.populate_obj(lunch)
        db.session.add(lunch)
        db.session.commit()
    return redirect(url_for('root'))


lunches = Lunch.query.all()

resource_fields = {
    'submitter':   fields.String,
    'food':        fields.String,
#     'uri':         fields.Url('lunch_ep')
}

parser = reqparse.RequestParser()
parser.add_argument('submitter')
parser.add_argument('food')

class RestLunch(Resource):
    @marshal_with(resource_fields)
    def get(self, lunch_id):
        try:
            l = lunches[lunch_id]
        except IndexError as ie:
            abort(404, message="Lunch {} doesn't exist".format(lunch_id))
            
        return l

    @marshal_with(resource_fields)
    def put(self, lunch_id):
        newlunch = Lunch() ## TODO: figure out how to get data passed
        try:
            lunches[lunch_id] = newlunch
            db.session.add(newlunch)
            db.session.commit()
        except IndexError as ie:
            abort(404, message="Lunch {} doesn't exist".format(lunch_id))
            
        return newlunch, 201


rest_api.add_resource(RestLunch, '/rest/<int:lunch_id>', endpoint='lunch_ep')

if __name__ == "__main__":
    db.create_all()  # make our sqlalchemy tables
    app.run()
