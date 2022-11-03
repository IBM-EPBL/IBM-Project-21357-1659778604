from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'udhfufjndcnd76712382173dhikjndkcn'

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)