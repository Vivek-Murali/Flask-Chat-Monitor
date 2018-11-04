from flask import Flask, render_template, make_response, session
import flask_admin as admin
from flask_sqlalchemy import SQLAlchemy
from models.admin import AnotherAdminView,MyAdminView, MyView


__author__ = 'Jetfire'


app = Flask(__name__)
app.secret_key = "Shrinking-Spell"


@app.route('/admin')
def index_admin():
    return MyView().render('index.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login_template():
    return render_template('login.html')


@app.route('/register')
def register_template():
    return render_template('register.html')


admin = admin.Admin(name="Example: Simple Views", template_mode='bootstrap3')
admin.add_view(MyAdminView(name="view1", category='Test'))
admin.add_view(AnotherAdminView(name="view2", category='Test'))
admin.init_app(app)
if __name__== "__main__":
    app.run(port=5000, debug=True)

