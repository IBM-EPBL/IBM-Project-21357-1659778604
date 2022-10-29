from turtle import st
from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import escape

import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=wjy24066;PWD=3w6H3sui635KMvWX",'','')
print(conn)
print("Connecting Successful............")


app=Flask(__name__)
@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
  if request.method == 'POST':

    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    repass = request.form['re-enter password']

    sql = "SELECT * FROM Retailer WHERE name =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,name)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)

    if account:
      return render_template('signup.html', msg="You are already a member, please login using your details")
    else:
      insert_sql = "INSERT INTO Retailer VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, username)
      ibm_db.bind_param(prep_stmt, 3, password)
      ibm_db.bind_param(prep_stmt, 4, repass)
      ibm_db.execute(prep_stmt)
    
    return render_template('home.html', msg="Retailer Login successfuly..")


@app.route("/")
def index():
    return render_template("home.html")

@app.route("/home")
def hello():
    return render_template("home.html")

@app.route("/about")
def profile():
    return render_template("about.html")


@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'),404


# @app.route("/chat")
# def chat():
#     return render_template("chat.html", messages=messages)

# messages =[{"title":"message one", "content":"message one content"},{"title":"message one", "content":"message one content"},{"title":"message two","content":"message two content"}]

# @app.route("/create/", methods=('GET','POST'))
# def create():
#     if request.method == 'POST':
#         title = request.form['title']
#         content = request.form['content']
        
        
#         if not title:
#             flash('Title is required!')
#         elif not content:
#             flash('Content is required!')
#         else:
#             messages.append({'title':title, 'content':content})
#             name= 'ganesh'
#             return redirect(url_for('index', messages=messages ))
#     return render_template('create.html')
















# @app.route("/creat/" , methods=('GET','POST'))
# def create():
#     if request.method=='POST':
#         title = request.form['title']


# @app.route('/')
# def index():
#     return render_template('index.html', messages=messages)

# @app.route('/admin')
# def hello_admin():
#     return 'hello admin'

# @app.route('/guest/<guest>')
# def hello_guest(guest):
#     return 'hello %s as Guest' % guest

# @app.route('/user/<name>')
# def hello_user(name):
#     if name== 'admin':
#         return redirect(url_for('hello_adimin'))
