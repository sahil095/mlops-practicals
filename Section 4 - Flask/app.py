from flask import Flask, request, render_template

'''
    It creates an instance of the Flask class,
    which will be your WSGI (Web Server Gateway Interface) application.
'''

app = Flask(__name__)

@app.route("/")
def welcome():
    return "Welcome to Flask tutorial."

@app.route("/profile", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/form", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        name = request.form["name"]
        return f'Hello {name}!'
    return render_template("form.html")

# Variable rule
@app.route('/success/<int:score>')
def success(score):
    res = ""
    if score >= 50:
        res = "PASS"
    else:
        res = "FAIL"
    return render_template("result.html",results=res)

if __name__ == "__main__":
    app.run(debug=True)
