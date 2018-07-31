from flask import Flask, request
from flask import render_template
from flask import url_for, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_restful import Resource, Api
from flask_restful import fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm as Form
from wtforms.fields import StringField, SubmitField

### app setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'please, tell nobody'

login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)
rest_api = Api(app)

### User management

users = {'foo@bar.tld': {'password': 'secret'}}

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    email = request.form['email']
    if request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        login_user(user)
        dest = request.args.get('next')
        try:
            dest_url = url_for(dest)
        except:
            return redirect(url_for('root'))
        return redirect(dest_url)

    return 'Bad login'

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))


### domain objects

class Lunch(db.Model):
    """A single lunch"""
    id = db.Column(db.Integer, primary_key=True)
    submitter = db.Column(db.String(63))
    food = db.Column(db.String(255))

    def __str__(self):
        return "{} ate {}".format(self.submitter, self.food)

### views

class LunchForm(Form):
    submitter = StringField(u'Hi, my name is')
    food = StringField(u'and I ate')
    submit = SubmitField(u'share my lunch!')

### endpoints

@app.route("/")
@login_required
def root():
    user = current_user.id
    lunches = Lunch.query.all()
    form = LunchForm()
    return render_template('index.html', form=form, lunches=lunches, user=user)

@app.route(u'/new', methods=[u'POST'])
@login_required
def newlunch():
    form = LunchForm()
    if form.validate_on_submit():
        lunch = Lunch()
        form.populate_obj(lunch)
        db.session.add(lunch)
        db.session.commit()
    return redirect(url_for('root'))

### REST stuff

resource_fields = {
    'submitter':   fields.String,
    'food':        fields.String,
#     'uri':         fields.Url('lunch_ep')
}

class RestLunch(Resource):
    @marshal_with(resource_fields)
    def get(self, lunch_id):
        try:
            l = Lunch.query.filter_by(id=lunch_id).first()
        except IndexError as ie:
            abort(404, message="Lunch {} doesn't exist".format(lunch_id))
            
        return l

    @marshal_with(resource_fields)
    def put(self, lunch_id):
        newlunch = Lunch() ## TODO: figure out how to get data
        try:
            db.session.add(newlunch)
            db.session.commit()
        except IndexError as ie:
            abort(404, message="Lunch {} doesn't exist".format(lunch_id))
            
        return newlunch, 201

## TODO: how to require login for REST api?
rest_api.add_resource(RestLunch, '/rest/<int:lunch_id>', endpoint='lunch_ep')

### main

if __name__ == "__main__":
    db.create_all()  # make our sqlalchemy tables
    app.run()
