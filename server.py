# Roy's Notes:
# url for testing   http://a.co/d2fyJAZ   
# get easier urls from sharing off of amazon.

import psycopg2
import psycopg2.extras
import sys
import os
import uuid
import time
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit, send, join_room, leave_room

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'secret!'
app.secret_key = os.urandom(24).encode('hex')

socketio = SocketIO(app)

page = ""

#----------------------------------------------------------------------------------------------------------------------------------
@socketio.on('connect', namespace='/lister')
def makeConnection():
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    session['uuid'] = uuid.uuid1()
    
@socketio.on('getData', namespace='/lister')
def getData():
  conn = connectToDB()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  
  user = []
  try:
    cur.execute("SELECT item_name FROM most_wanted WHERE user_email = %s;", (session['UserEmail'],))
    results=cur.fetchone() 
    user.append({'title' : 'most' , 'result' : results['item_name']})
    
    cur.execute("SELECT date_joined FROM user_join_date WHERE user_email = %s;", (session['UserEmail'],))
    results=cur.fetchone() 
    user.append({'title' : 'most' , 'result' : results['date_joined']})
    
    cur.execute("SELECT birth_date FROM user_date_of_birth WHERE user_email = %s;", (session['UserEmail'],))
    results=cur.fetchone() 
    user.append({'title' : 'most' , 'result' : results['birth_date']})
    
    cur.execute("SELECT gender FROM user_gender WHERE user_email = %s;", (session['UserEmail'],))
    results=cur.fetchone() 
    user.append({'title' : 'most' , 'result' : results['gender']})
  
    cur.execute("SELECT address FROM user_address WHERE user_email = %s;", (session['UserEmail'],))
    results=cur.fetchone() 
    user.append({'title' : 'most' , 'result' : results['address']})
  
    cur.execute("SELECT phone_number FROM user_phone_number WHERE user_email = %s;", (session['UserEmail'],))
    results=cur.fetchone() 
    user.append({'title' : 'most' , 'result' : results['phone_number']})
  
    emit('setData', user)
  except:
    print ""
      
@socketio.on('register', namespace='/lister')
def register(email, pw, cpw, fn, ln):
  conn = connectToDB()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  print("getting into socket")
  if pw == cpw:
    # Hunter Renard
    cur.execute("select * from users WHERE email = %s", (email,))
    if cur.fetchone():
      print "Account already registered to that name"
      emit('registerfailure', "Email already registered!")
      
    else:
      print("aaaaaaaaaaaaaa")
      # Hunter Renard
      cur.execute("INSERT INTO users (email, password, firstname, lastname) VALUES(%s, crypt(%s, gen_salt('bf')), %s, %s);", (email, pw, fn, ln))
      conn.commit()
      
      cur.execute("INSERT INTO most_wanted (user_email, item_name) VALUES(%s, %s);", (email, "N/A",))
      conn.commit()
      
      print(time.strftime("%d/%m/%Y"))
      joinDate = time.strftime("%d/%m/%Y")
      cur.execute("INSERT INTO user_join_date (user_email, date_joined) VALUES(%s, %s);", (email, joinDate,))
      conn.commit()
      cur.execute("INSERT INTO user_date_of_birth (user_email, birth_date) VALUES(%s, %s);", (email, "N/A",))
      conn.commit()
      cur.execute("INSERT INTO user_gender (user_email, gender) VALUES(%s, %s);", (email, "N/A",))
      conn.commit()
      cur.execute("INSERT INTO user_phone_number (user_email, phone_number) VALUES(%s, %s);", (email, "N/A",))
      conn.commit()
      cur.execute("INSERT INTO user_address (user_email, address) VALUES(%s, %s);", (email, "N/A",))
      conn.commit()
      print("yes&&&&&&&")
      emit('registersuccess')
  else:
    emit('registerfailure', "Passwords don't match!")
    
@socketio.on('most', namespace='/lister')
def most(data):
  conn = connectToDB()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  cur.execute("UPDATE most_wanted SET item_name = %s WHERE user_email = %s;", (data,session['UserEmail']))
  conn.commit()
  
@socketio.on('birth', namespace='/lister')
def birth(data):
  conn = connectToDB()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  cur.execute("UPDATE user_date_of_birth SET birth_date = %s WHERE user_email = %s;", (data,session['UserEmail']))
  conn.commit()
  
@socketio.on('gender', namespace='/lister')
def gender(data):
  conn = connectToDB()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  cur.execute("UPDATE user_gender SET gender = %s WHERE user_email = %s;", (data,session['UserEmail']))
  conn.commit()
  
@socketio.on('home', namespace='/lister')
def home(data):
  conn = connectToDB()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  cur.execute("UPDATE user_address SET address = %s WHERE user_email = %s;", (data,session['UserEmail']))
  conn.commit()
  
@socketio.on('number', namespace='/lister')
def number(data):
  conn = connectToDB()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  cur.execute("UPDATE user_phone_number SET phone_number = %s WHERE user_email = %s;", (data,session['UserEmail']))
  conn.commit()
  
@socketio.on('getResults', namespace='/lister')
def getResults(data):
  conn = connectToDB()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  
  results = []

  cur.execute("SELECT firstname, lastname, email FROM users WHERE firstname LIKE %s OR lastname LIKE %s OR email LIKE %s;", (data + "%", data + "%", data + "%"))
  for res in cur.fetchall():
    result = False;
    if session['UserEmail'] != res['email']:
      cur.execute("select * from friends_with where user_email = %s AND friend_email = %s;", (session['UserEmail'],res['email']))
      print(res['email'])
      res2 = cur.fetchone()
      if (res2):
        print "!!!!"
        result = True; 
      print(result)
      results.append({'name' : res['firstname'] + " " + res['lastname'], 'email' : res['email'], 'subbed' : result})
  emit('searchResults', results)
  
@socketio.on('getFriendData', namespace='/lister')
def getFriendData(data):
  conn = connectToDB()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  
  user = []
  
  try:
    cur.execute("SELECT firstname FROM users WHERE email = %s;", (data,))
    results=cur.fetchone() 
    user.append({'title' : 'most' , 'result' : results['firstname']})  
    
    cur.execute("SELECT lastname FROM users WHERE email = %s;", (data,))
    results=cur.fetchone() 
    user.append({'title' : 'most' , 'result' : results['lastname']})
    
    user.append({'title' : 'most' , 'result' : data})
    
    cur.execute("SELECT item_name FROM most_wanted WHERE user_email = %s;", (data,))
    results=cur.fetchone() 
    user.append({'title' : 'most' , 'result' : results['item_name']})
    
    cur.execute("SELECT date_joined FROM user_join_date WHERE user_email = %s;", (data,))
    results=cur.fetchone() 
    user.append({'title' : 'most' , 'result' : results['date_joined']})
    
    cur.execute("SELECT birth_date FROM user_date_of_birth WHERE user_email = %s;", (data,))
    results=cur.fetchone() 
    user.append({'title' : 'most' , 'result' : results['birth_date']})
    
    cur.execute("SELECT gender FROM user_gender WHERE user_email = %s;", (data,))
    results=cur.fetchone() 
    user.append({'title' : 'most' , 'result' : results['gender']})
  
    cur.execute("SELECT address FROM user_address WHERE user_email = %s;", (data,))
    results=cur.fetchone() 
    user.append({'title' : 'most' , 'result' : results['address']})
  
    cur.execute("SELECT phone_number FROM user_phone_number WHERE user_email = %s;", (data,))
    results=cur.fetchone() 
    user.append({'title' : 'most' , 'result' : results['phone_number']})
    
    cur.execute("SELECT item_name FROM items WHERE user_email = %s;", (data,))
    results=cur.fetchall()
    for result in results:
      user.append({'title':'most', 'result':result['item_name']})
    
    cur.execute("select * from friends_with where user_email = %s AND friend_email = %s;", (session['UserEmail'],data))
    res2 = cur.fetchone()
    if (res2):
      print "!!!!"
      result = True;
      user.append({'title' : 'most' , 'result' : True})
    else:
      user.append({'title' : 'most' , 'result' : False})
  
    emit('setFriendData', user)
  except:
    print ""
  
@socketio.on('subscribe', namespace='/lister')
def subscribe(data):
  conn = connectToDB()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  
  cur.execute("select email, firstName, lastName from users where email like %s;", (data,))
  results = cur.fetchone()
  if (results):
    cur.execute("insert into friends_with (user_email, friend_email) VALUES (%s, %s);", (session['UserEmail'], data))
    conn.commit()

@socketio.on('checkSub', namespace='/lister')
def checkSub(data):
  conn = connectToDB()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  result = False

  cur.execute("select * from friends_with where user_email = %s AND friend_email = %s;", (session['UserEmail'],data))
  results = cur.fetchone()
  if (results):
    result = True;
    
  emit('isSub', result)

@socketio.on('unsubscribe', namespace='/lister')
def unsubscribe(data):
  conn = connectToDB()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  cur.execute("DELETE FROM friends_with WHERE user_email = %s AND friend_email = %s", (session['UserEmail'],data))
  conn.commit()
  
  
#----------------------------------------------------------------------------------------------------------------------------------

def connectToDB():
  connectionString = 'dbname=lister user=testuser password=password host=localhost'
  print connectionString
  try:
    return psycopg2.connect(connectionString)
  except:
    print("Can't connect to database")
    
@app.route('/')
def mainIndex():
  if 'UserEmail' in session:
    return redirect(url_for('showProfile'))
  else:
    return render_template('index.html')
  
@app.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('mainIndex'))

@app.route('/profile', methods=['GET', 'POST'])
def showProfile():
  
  if 'UserEmail' in session:
    return redirect(url_for('showList'))
  else:
    return redirect(url_for('mainIndex'))
  
@app.route('/wishlist', methods=['GET', 'POST'])
def showList():
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    results = [];
    resultsfinal=[]
    if 'UserEmail' in session:
      print ("true")
    else:
      return redirect(url_for('mainIndex'))
 
    user=[session['UserEmail'],session['UserFirstName'], session['UserLastName']]

    print(user[0])
 
    if request.method == 'POST':
      print(session['UserEmail'])
      try:
        cur.execute("INSERT INTO items (user_email, item_name, item_price) VALUES (%s, %s, %s);", (session['UserEmail'], request.form['item_name'], request.form['item_price']))
      except:
        print("ERROR: Could not add item.")
        conn.rollback()
      conn.commit()
      
      #added stuff for url
      cur.execute("SELECT id FROM items WHERE item_name = %s AND user_email = %s", (request.form['item_name'],session['UserEmail']))
      results=cur.fetchone()
      print(results)
      print(results[0])
      
      try:
        cur.execute("INSERT INTO links (item_id, url) VALUES (%s, %s);", (results[0], request.form['item_url']))
      except:
        print("ERROR: Could not add url.")
        conn.rollback()
      conn.commit()
      
    try:
      cur.execute("SELECT c.item_name, c.item_price, d.url FROM items c JOIN links d ON c.id = d.item_id WHERE user_email = %s;", (session['UserEmail'],))  #make sure this join works
      resultsfinal=cur.fetchall() 
    except:
      print("ERROR: Could not SELECT")
    
    return render_template('wishlist.html', user=user, item=resultsfinal, page="list")

 
@app.route('/login', methods=['GET', 'POST'])
def login():
  conn = connectToDB()
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  print("Makes it to login")
  if request.method == 'POST':
    username = request.form['email']
    password = request.form['password']
    
    # Roy O'Dell
    cur.execute("select * from users where email = %s and password = crypt(%s, password);", (username, password))
    row = cur.fetchone()
    while row is not None:
      session['UserFirstName'] = row['firstname']
      session['UserLastName'] = row['lastname']
      session['UserEmail'] = row['email']
      print(session['UserFirstName'])
      return redirect(url_for('showList'))
    else:
      return redirect(url_for('mainIndex'))
  else:
    return redirect(url_for('mainIndex'))
  
@app.route('/subscriptions', methods=['GET', 'POST'])
def subscriptions():
  friendname=""
  conn = connectToDB()
  cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  results=[]
  user=[session['UserEmail'], session['UserFirstName'], session['UserLastName']]
  print("Makes it to subscriptions")
  if request.method=='POST':
    friendname = request.form['friendname']
    try:
      cur.execute("select email, firstName, lastName from users where email like %s;", (friendname,))
      results = cur.fetchone()
      if (results):
        print(session['UserEmail'], friendname)
        cur.execute("insert into friends_with (user_email, friend_email) VALUES (%s, %s);", (session['UserEmail'], friendname))
        conn.commit()
    except:
      print("Error")
      conn.rollback()
      
  cur.execute("select c.firstName, c.lastName FROM users c JOIN friends_with d ON c.email = d.friend_email WHERE d.user_email = %s;", (session['UserEmail'],))
  results=cur.fetchall()
  print(results)
  return render_template('subscriptions.html', user=user, results=results)
  
if __name__ == '__main__':
        socketio.run(app, host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)
