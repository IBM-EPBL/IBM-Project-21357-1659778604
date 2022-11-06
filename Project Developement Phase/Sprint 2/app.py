# Inventory Manager

from flask import jsonify, json

from flask import Flask, request, redirect, render_template, session
from cs50 import SQL
from tempfile import mkdtemp
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from functions import login_required, apology

# Configure application
app = Flask(__name__)

# Ensure tamplates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "nocache"
    return response

# Configure session to use filesystem
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///ims.db")


@app.route("/")
@login_required
def index():
    """Homepage"""
    totals = db.execute("SELECT COUNT(productName) as total_products, SUM(inventoryOut) as total_orders, SUM(inventoryIn) as total_purchases FROM products")
    ups = db.execute("SELECT COUNT(id) as total_ups FROM products WHERE inventoryOnHand < minimumReq AND minimumReq != 0")

    return render_template("index.html", totals = totals, ups = ups)

@app.route("/get_data")
def get_data():
    """ Sends data to charts"""
    totals = db.execute("SELECT COUNT(productName) as total_products, SUM(inventoryOut) as total_orders, SUM(inventoryIn) as total_purchases FROM products")
    labels = ["Total Products", "Total Orders", "Total Purchases"]
    data = [ totals[0]["total_products"],totals[0]["total_orders"],totals[0]["total_purchases"]]


    mtotal = db.execute(
        "SELECT SUM(CASE WHEN strftime('%m', oDate) = '01' THEN 1 ELSE 0 END) as jan, SUM(CASE WHEN strftime('%m', oDate) = '02' THEN 1 ELSE 0 END) as feb, SUM(CASE WHEN strftime('%m', oDate) = '03' THEN 1 ELSE 0 END) as mar, SUM(CASE WHEN strftime('%m', oDate) = '04' THEN 1 ELSE 0 END) as apr, SUM(CASE WHEN strftime('%m', oDate) = '05' THEN 1 ELSE 0 END) as may, SUM(CASE WHEN strftime('%m', oDate) = '06' THEN 1 ELSE 0 END) as jun, SUM(CASE WHEN strftime('%m', oDate) = '07' THEN 1 ELSE 0 END) as jul, SUM(CASE WHEN strftime('%m', oDate) = '08' THEN 1 ELSE 0 END) as aug, SUM(CASE WHEN strftime('%m', oDate) = '09' THEN 1 ELSE 0 END) as sep, SUM(CASE WHEN strftime('%m', oDate) = '10' THEN 1 ELSE 0 END) as oct, SUM(CASE WHEN strftime('%m', oDate) = '11' THEN 1 ELSE 0 END) as nov, SUM(CASE WHEN strftime('%m', oDate) = '12' THEN 1 ELSE 0 END) as dec FROM orders"
        )

    mtotals = [ mtotal[0]["jan"], mtotal[0]["feb"], mtotal[0]["mar"], mtotal[0]["apr"], mtotal[0]["may"], mtotal[0]["jun"], mtotal[0]["jul"], mtotal[0]["aug"], mtotal[0]["sep"], mtotal[0]["oct"], mtotal[0]["nov"], mtotal[0]["dec"]]

    return jsonify({'payload':json.dumps({'data':data, 'labels':labels, 'mtotals':mtotals})})


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached via POST
    if request.method == "POST":

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                            username = request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("pwd")):
            return "Incorrect ID or Pass" #render_template("404.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["fullname"] = rows[0]["fullname"]

        # Redirect user to Dashboard
        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Registers User"""

    # User reached via POST
    if request.method == "POST":

        hash = generate_password_hash(request.form.get("pwd"))

        new_user = db.execute("INSERT INTO users (username, hash, fullname) VALUES (:username, :hash, :fullname)",
                                username = request.form.get("username"), hash = hash, fullname = request.form.get("fullname"))

        if not new_user:
            return render_template("404.html")

        session["user_id"] = new_user

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/change", methods=["GET", "POST"])
def change():
    """Change user's password"""
    if request.method == "POST":

        if request.form.get("new-pwd") != request.form.get("new-pwd-again"):
            return "Password not matched"

        hash = generate_password_hash(request.form.get("new-pwd"))

        db.execute("UPDATE users SET hash = :hash WHERE id = :user_id", hash = hash, user_id = session["user_id"])

        return redirect("/")

    else:
        return render_template("change.html")

@app.route("/productv", methods=["GET", "POST"])
@login_required
def productv():

    if request.method == "POST":


        test = db.execute("INSERT INTO products (productName, partNumber, productLabel, startingInventory, inventoryIn, inventoryOut, inventoryOnHand, minimumReq) VALUES (:productName, :partNumber, :productLabel, :startingInventory, :inventoryIn, :inventoryOut, :inventoryOnHand, :minimumReq)", productName = request.form.get("product-name"), partNumber = request.form.get("part-number"), productLabel = request.form.get("product-label"), startingInventory = request.form.get("starting-inventory"), inventoryIn = request.form.get("inventory-in"), inventoryOut = request.form.get("inventory-out"), inventoryOnHand = request.form.get("inventory-on-hand"), minimumReq = request.form.get("minimum-req"))
        if not test:
            return "Can't Insert the data"


        return redirect("/productv")

    else:
        return render_template("productv.html")


@app.route("/orderv", methods=["GET", "POST"])
@login_required
def orderv():
    """Adds Orders"""
    if request.method == "POST":

        try:
            orders = int(request.form.get("orders"))
        except:
            return "Orders Must be positive number"

        if orders <= 0:
            return "Orders Must be greater than 0"


        db.execute("UPDATE products SET inventoryOnHand = inventoryOnHand - :orders, inventoryOut = inventoryOut + :orders WHERE productName = :productName", productName = request.form.get("product-name"), orders = request.form.get("orders"))
        db.execute("INSERT INTO orders (first, middle, last, product_name, numberOut, oDate) VALUES (:first, :middle, :last, :product_name, :numberOut, :oDate)", first = request.form.get("first-name"), middle = request.form.get("middle-name"), last = request.form.get("last-name"), product_name = request.form.get("product-name"), numberOut = request.form.get("orders"), oDate = request.form.get("order-date"))


        return redirect("/orderv")
    else:
        products = db.execute("SELECT id, productName, partNumber FROM products")

        return render_template("orderv.html", products = products)

@app.route("/purchasev", methods=["GET", "POST"])
@login_required
def purchasev():
    """Adds Purchase Record"""
    if request.method == "POST":

        try:
            purchases = int(request.form.get("purchases"))
        except:
            return "Purchases Must be positive number"

        if purchases <= 0:
            return "Purchases Must be greater than 0"


        db.execute("UPDATE products SET inventoryOnHand = inventoryOnHand + :purchases, inventoryIn = inventoryIn + :purchases WHERE productName = :productName", productName = request.form.get("product-name"), purchases = request.form.get("purchases"))
        db.execute("INSERT INTO purchases (supplier_name, product_name, numberIn, pDate) VALUES (:supplier_name, :product_name, :numberIn, :pDate)", supplier_name = request.form.get("supplier-name"), product_name = request.form.get("product-name"), numberIn = request.form.get("purchases"), pDate = request.form.get("purchase-date"))


        return redirect("/purchasev")
    else:
        products = db.execute("SELECT id, productName, partNumber FROM products")
        suppliers = db.execute("SELECT id, supplier FROM suppliers")

        return render_template("purchasev.html", products = products, suppliers = suppliers)

@app.route("/supplierv", methods=["GET", "POST"])
@login_required
def supplierv():
    """Add Suppliers"""
    if request.method == "POST":

        db.execute("INSERT INTO suppliers (supplier) VALUES (:supplier)", supplier = request.form.get("supplier"))

    return render_template("supplierv.html")


@app.route("/productl", methods=["POST", "GET"])
@login_required
def productl():
    """ Lists Products"""

    rows = db.execute("SELECT * FROM products")

    return render_template("productl.html", rows = rows)

@app.route("/orderl", methods=["GET", "POST"])
@login_required
def orderl():
    """ Lists Orders"""

    rows = db.execute("SELECT orderId, first, middle, last, product_name, numberOut, oDate, partNumber FROM orders JOIN products ON orders.product_name = products.productName")

    return render_template("orderl.html", rows = rows)


@app.route("/purchasel", methods=["GET", "POST"])
@login_required
def purchasel():
    """Lists Purchses"""

    rows = db.execute("SELECT purchaseId, supplier_name, product_name, numberIn, pDate, partNumber FROM purchases JOIN products ON purchases.product_name = products.productName")

    return render_template("purchasel.html", rows = rows)




app.run(debug=True,port=5001)