
from flask import Flask, redirect, render_template, session, request
import database as db
import dotenv, os

# Create a Flask app instance ------------
app = Flask(__name__,
static_url_path="/static")
app.secret_key = os.getenv("session_key")

# FIRST PAGE -----------------------------------------------
@app.route('/')
def index():
    if session.get("idLoggedIn"):
        login_id = session["idLoggedIn"]
        return redirect(f"/user/{login_id}")
    page = """
    <p> <a href="/signup" class="link">Sign Up</a> </p>
    <p> <a href="/login" class="link">Login</a> </p>
    """
    return page

# SIGN UP ------------------------------------------------
@app.route('/signup', methods=["GET", "POST"])
def signup():
    # TODO - Find a way to require all fields here. 
    if session.get("idLoggedIn"):
        login_id = session["idLoggedIn"]
        return redirect(f"/user/{login_id}")
    f = open("templates\signup.html", "r")
    page = f.read()
    f.close()
    return page

# SIGN UP - PROCESS NEW USER ------------------------------------------
# TODO add pasword salt and hash
@app.route('/process', methods=["GET", "POST"])
def process():
    if session.get("idLoggedIn"):
        login_id = session["idLoggedIn"]
        return redirect(f"/user/{login_id}")    
    form = request.form
    if request.method == "POST":
        user = db.query_db("SELECT * FROM users WHERE username = ?", (form["username"], ), one=True)
        if user is None: # username DNE check
            db.init_db()
            db.insert_data(form["email"], form["username"], form["password"])
            return redirect("/login")
        else: 
            return "Username already exists. Go back and try again."

# LOGIN -----------------------------------------------
@app.route('/login', methods=["GET", "POST"])
def login():
    if session.get("idLoggedIn"):
        login_id = session["idLoggedIn"]
        return redirect(f"/user/{login_id}")
    f = open("templates\login.html", "r")
    page = f.read()
    f.close()
    return page

# LOGIN - PROCSS LOGIN ATTEMPT ------------------------------------------
@app.route('/loginAttempt', methods=["GET", "POST"])
def loginAttempt():
    if session.get("idLoggedIn"):
        login_id = session["idLoggedIn"]
        return redirect(f"/user/{login_id}")
    if request.method == "POST":
        form = request.form
        user = db.query_db("SELECT * FROM users WHERE username = ?", (form["username"], ), one=True)
        if user is not None:
            if form["password"] == user["password"]:
                user_url = f"/user/{user['id']}"
                session["idLoggedIn"] = user["id"]
                return redirect(user_url)
            else:
                return "Wrong Password! Go back to retry or sign up."
        else:
            return "User not found", 404
    else:
        return redirect("/login")

# USER "LOGGED-IN" PAGE ------------------------------------------
@app.route('/user/<int:user_id>', methods=["GET", "POST"])
def get_user(user_id):
    if session.get("idLoggedIn"):
        login_id = session["idLoggedIn"]
        if login_id != user_id:
            return redirect(f"/user/{login_id}")
    elif not session.get("idLoggedIn"):
        return redirect("/")
    user = db.query_db('SELECT * FROM users WHERE id = ?', [user_id], one=True)
    if user is not None:
        return render_template('user.html', user=user)
    else:
        return 'User not found', 404

# LOG OUT ------------------------------------------
@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/")


# Run the app
if __name__ == '__main__':
    app.run(debug=True, host= '10.0.0.29')
