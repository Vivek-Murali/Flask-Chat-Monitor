from flask import Flask, render_template, make_response, session, request, redirect, url_for, flash
from flask_login import login_user, current_user
from flask_socketio import SocketIO, send
from common.config import *
import sys
import bcrypt
import functools
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import names
import pandas as pd
import datetime
import csv
import collections
import nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
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


@app.route('/home_template')
def home_template():
    return render_template('home.html', username=session['username'])


@app.route('/profile/<string:username>')
def profile_template(username):
    results = sql_query3(''' SELECT * FROM data_table where username = ?''', (username,))
    messages = sql_query3(''' SELECT * FROM chats where username = ?''', (username,))
    print(results[1])
    print(messages[3])
    return render_template('profile.html', username=session['username'], results=results,
                           messages = messages)



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
            username = session['username']
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


@app.route('/Admin_chat')
def chat_database():
    results = sql_query(''' SELECT * FROM chats''')
    return render_template('admin_chat.html', results=results, username=session['username'])

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



@app.route('/view_user_all/',methods = ['POST', 'GET'])#this is when user submits an insert
def chat_datainsert():
    messege = request.form['description']
    username = session['username']
    date_msg = datetime.datetime.utcnow()
    sql_edit_insert(''' INSERT INTO chats (messege, username, date) VALUES (?,?,?) ''', (messege,username, date_msg))
    results = sql_query(''' SELECT * FROM chats''')
    pop = results[0]
    '''positive_vocab = ['awesome', 'outstanding', 'fantastic', 'terrific', 'good', 'nice', 'great', ':)', 'cool', 'pretty']
    negative_vocab = ['bad', 'terrible', 'useless', 'hate', ':(', 'Kill', 'Bomb', 'kill', 'murder', 'bash']
    neutral_vocab = ['movie', 'the', 'sound', 'was', 'is', 'actors', 'did', 'know', 'words', 'not']
    data1 = {'positive_vocab':positive_vocab, 'negative_vocab':negative_vocab,'neutral_vocab':neutral_vocab}
    df1 = pd.DataFrame(data1)
    df1.to_csv('stopwords', index=False)'''
    df1 = pd.read_csv('stopwords.csv')
    positive_vocab = df1['positive_vocab']
    negative_vocab = df1['negative_vocab']
    neutral_vocab = df1['neutral_vocab']
    positive_features = [(word_feats(pos), 'pos') for pos in positive_vocab]
    negative_features = [(word_feats(neg), 'neg') for neg in negative_vocab]
    neutral_features = [(word_feats(neu), 'neu') for neu in neutral_vocab]
    train_set = negative_features + positive_features + neutral_features
    classifier = NaiveBayesClassifier.train(train_set)
    neg = 0
    pos = 0
    sentence = "Awesome movie, I liked it"
    sentence = sentence.lower()
    words = sentence.split(' ')
    for word in words:
        classResult = classifier.classify(word_feats(word))
        if classResult == 'neg':
            neg = neg + 1
        if classResult == 'pos':
            pos = pos + 1

    Positive = str(float(pos) / len(words)).encode('utf-8')
    Negative = str(float(neg) / len(words)).encode('utf-8')
    #sql_edit_insert(''' INSERT INTO monitor (negitive, posivtive, id) VALUES (?,?,?) ''', (Negative, Positive, pop))
    #df = pd.DataFrame()
    data = {"datetime":date_msg, "Positive":Positive, "Negative":Negative, "Username":username,"Messege_id":pop ,"Message":messege}
    #df = df.append(data, ignore_index=True)
    #df.to_csv("log.csv", index=False)
    with open('log.csv', "a") as csvfile:
        headers = ['Message','Messege_id', 'Negative', 'Positive', 'Username', 'datetime']
        writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n', fieldnames=headers)
        writer.writerow(data)

    posids = df1['positive_vocab']
    negids = df1['negative_vocab']
    stopset = set(stopwords.words('english'))
    messege1 = word_tokenize(messege)
    wordsFiltered = []
    for w in messege1:
        if w not in stopset:
            wordsFiltered.append(w)

    for word in wordsFiltered:
        classResult = classifier.classify(word_feats(word))
        if classResult == 'neg':
            neg = neg + 1
        if classResult == 'pos':
            pos = pos + 1

    Positive = str(float(pos) / len(words)).encode('utf-8')
    Negative = str(float(neg) / len(words)).encode('utf-8')
    data1 = {"datetime": date_msg, "Positive": Positive, "Negative": Negative, "Username": username, "Messege_id": pop,
            "Message": messege}
    #df2 = pd.DataFrame()
    #df2 = df2.append(data, ignore_index=True)
    #df2.to_csv("message_pre.csv", index=False)
    with open('message_pre.csv', "a") as csvfile1:
        headers1 = ['Message','Messege_id', 'Negative', 'Positive', 'Username', 'datetime']
        writer = csv.DictWriter(csvfile1, delimiter=',', lineterminator='\n', fieldnames=headers1)
        writer.writerow(data)
    return render_template('home.html', results=results, username=session['username'])


@app.route('/view_user_all',methods = ['POST', 'GET'])#this is when user submits an insert
def chat_datainsert1(room_id):
    if request.method == 'POST':
        messege = request.form['description']
        username = session['username']
        room_id = room_id
        sql_edit_insert(''' INSERT INTO chats (messeges, username, room_id) VALUES (?,?,?) ''', (messege,username,room_id))
    results = sql_query(''' SELECT * FROM chats''')
    return render_template('chat.html', results=results, username=session['username'])


@app.route('/delete',methods = ['POST', 'GET']) #this is when user clicks delete link
def sql_datadelete():
    if request.method == 'GET':
        username = request.args.get('username')
        sql_delete(''' DELETE FROM data_table where username = ? ''', (username,))
    results = sql_query(''' SELECT * FROM data_table''')
    return render_template('Adminhome.html', results=results)


@app.route('/delete_chat',methods = ['POST', 'GET']) #this is when user clicks delete link
def chat_datadelete():
    if request.method == 'GET':
        messege_id = request.args.get('messege_id')
        sql_delete(''' DELETE FROM chats where messege_id = ? ''', (messege_id,))
    results = sql_query(''' SELECT * FROM chats''')
    return render_template('Adminhome.html', results=results)


@app.route('/edit_profile',methods = ['POST', 'GET'])#this is when user clicks edit link
def sql_editlink1():
    return render_template('sqldatabase1.html',username = session['username'])


@app.route('/edit_pro',methods = ['POST', 'GET']) #this is when user submits an edit
def sql_dataedit1():
    if request.method == 'POST':
        last_name = request.form['last_name']
        first_name = request.form['first_name']
        address = request.form['email']
        city = request.form['username']
        state = request.form['password']
        zip = request.form['phone']
        username1 = session['username']
        state1 = bcrypt.hashpw(state.encode('utf-8'),bcrypt.gensalt())
        sql_edit_insert(''' UPDATE data_table set first_name=?,last_name=?,email=?,password=?,phone=? WHERE username=?  ''', (first_name,last_name,address,state1,zip, username1) )
    results = sql_query(''' SELECT * FROM data_table''')
    return render_template('profile.html', results=results)


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


def word_feats(words):
    #stopset = set(stopwords.words('english'))
    return dict([(word, True) for word in words])


def stopword_filtered_word_feats(words):
    stopset = set(stopwords.words('english'))
    return dict([(word, True) for word in words if word not in stopset])



if __name__== "__main__":
    app.run(port=5000, debug=True)
    socketio.run(app)

