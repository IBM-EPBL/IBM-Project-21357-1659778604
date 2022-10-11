from flask import Flask,render_template,request,url_for,redirect,flash 
from markupsafe import escape
import sqlite3 as sql
try:
    conn = sql.connect('database.db')
    conn.execute(' CREATE TABLE student(name TEXT, addr TEXT, city TEXT, pin TEXT)')
except:
    print("it already exists")

    


app=Flask(__name__)
@app.route('/signup1')
def new_student():
    return  render_template('student.html')



@app.route('/addrec', methods=['POST','GET'])
def addrec():
    if request.method =='POST':
        try:
            nm=request.form['nm']
            addr=request.form['add']
            city=request.form['city']
            pin=request.form['pin']

            with sql.connect('database.db') as con:
                cur =con.cursor()
                
                cur.execute('INSERT INTO student(name, addr, city, pin) VALUES(?,?,?,?)',(nm,addr,city,pin))
                con.commit()
                msg='record successfully added'
        except:
            con.rollback()
            msg="error"
        
        finally:
            return render_template("result.html", msg=msg)
            con.close()
@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute('select * from student')
    rows=cur.fetchall()
    return render_template('list.html',rows=rows)


@app.route("/")
def index():
    return render_template("home.html")

@app.route("/home")
def hello():
    return render_template("home.html")

@app.route("/about")
def profile():
    return render_template("about.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")


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
