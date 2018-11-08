from flask import Flask, render_template, make_response, session, request, redirect, url_for, flash
from flask_login import login_user, current_user
from flask_socketio import SocketIO, send
from common.config import *
import sys
import bcrypt
import functools

__author__ = 'Jetfire'

sys.path.insert(1, "PATH TO LOCAL PYTHON PACKAGES")
sys.path.insert(2, "PATH TO FLASK DIRECTORY")
app = Flask(__name__)
app.secret_key = "Shrinking-Spell"
socketio = SocketIO(app)


@app.route('/')
def index():
    session.clear()
    return render_template('index.html')


@app.route('/login_template')
def login_template():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    results = sql_query3(''' SELECT * FROM data_table where username = ?''',(username, ))
    pass1 = results[6]
    if results is not None:
        password1 = bcrypt.checkpw(password.encode('utf-8'),pass1)
        if password1 == True and username == "Admin":
            session['username'] = username
            session['logged_in'] = True
            return render_template('Adminhome.html', username=username)
        elif password1 == True:
            session['username'] = username
            session['logged_in'] = True
            return render_template('home.html', username=username)
        else:
            return render_template('login.html')
    return render_template('index.html')


@app.route('/register_template')
def register_template():
    return render_template('register.html')


@app.route('/Adminuser')
def Adminuser_template():
    return render_template('Adminuser.html')


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        last_name = request.form['last_name']
        first_name = request.form['first_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        phone = request.form['phone']
        password1 = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        sql_edit_insert(''' INSERT INTO data_table (first_name,last_name,email,username,password,phone) VALUES (?,?,?,?,?,?) ''', (first_name,last_name,email,username,password1,phone) )
    flash("Registered Successfully", category='success')
    return render_template('index.html')


@app.route('/logout/')
def logout():
    session.clear()
    return render_template('index.html')


@app.route('/Admin')
def sql_database():
    results = sql_query(''' SELECT * FROM data_table''')
    msg = 'SELECT * FROM data_table'
    return render_template('Adminuser.html', results=results)

@app.route('/useradd')
def sql_add():
    return render_template('useradd.html')


@app.route('/insert',methods = ['POST', 'GET']) #this is when user submits an insert
def sql_datainsert():
    if request.method == 'POST':
        last_name = request.form['last_name']
        first_name = request.form['first_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        phone = request.form['phone']
        password1 = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        sql_edit_insert(''' INSERT INTO data_table (first_name,last_name,email,username,password,phone) VALUES (?,?,?,?,?,?) ''', (first_name,last_name,email,username,password1,phone) )
    results = sql_query(''' SELECT * FROM data_table''')
    return render_template('sqldatabase.html', results=results)


@app.route('/delete',methods = ['POST', 'GET']) #this is when user clicks delete link
def sql_datadelete():
    if request.method == 'GET':
        username = request.args.get('username')
        sql_delete(''' DELETE FROM data_table where username = ? ''', (username,))
    results = sql_query(''' SELECT * FROM data_table''')
    return render_template('Adminhome.html', results=results)


@app.route('/query_edit',methods = ['POST', 'GET'])#this is when user clicks edit link
def sql_editlink():
    if request.method == 'GET':
        eusername = request.args.get('eusername')
        eresults = sql_query2(''' SELECT * FROM data_table where username = ? ''', (eusername,))
    results = sql_query(''' SELECT * FROM data_table''')
    return render_template('sqldatabase.html', eresults=eresults, results=results)


@app.route('/edit',methods = ['POST', 'GET']) #this is when user submits an edit
def sql_dataedit():
    if request.method == 'POST':
        old_last_name = request.form['old_last_name']
        old_first_name = request.form['old_first_name']
        last_name = request.form['last_name']
        first_name = request.form['first_name']
        address = request.form['email']
        city = request.form['username']
        state = request.form['password']
        zip = request.form['phone']
        state1 = bcrypt.hashpw(state.encode('utf-8'),bcrypt.gensalt())
        sql_edit_insert(''' UPDATE data_table set first_name=?,last_name=?,email=?,username=?,password=?,phone=? WHERE first_name=? and last_name=? ''', (first_name,last_name,address,city,state1,zip,old_first_name,old_last_name) )
    results = sql_query(''' SELECT * FROM data_table''')
    return render_template('sqldatabase.html', results=results)


@socketio.on('message')
def handleMessage(msg):
    username = session['username']
    print('Message from {0}: {1}'.format(username, msg))
    send(msg, broadcast=True)


if __name__== "__main__":
    app.run(port=5000, debug=True)
    socketio.run(app)

