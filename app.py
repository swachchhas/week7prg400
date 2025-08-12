from flask import Flask, render_template, request, redirect, session, url_for
from firebase_config import auth, db
import functools

app = Flask(__name__)
app.secret_key = "supersecretkey"

# --- Decorator for login required ---
def login_required(role=None):
    def wrapper(func):
        @functools.wraps(func)
        def decorated_view(*args, **kwargs):
            if "user" not in session:
                return redirect(url_for("login"))
            if role and session.get("role") != role:
                return "Access Denied", 403
            return func(*args, **kwargs)
        return decorated_view
    return wrapper

# --- Routes ---
@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]
        try:
            user = auth.create_user_with_email_and_password(email, password)
            db.child("users").child(user["localId"]).set({"email": email, "role": role})
            return redirect(url_for("login"))
        except Exception as e:
            print("Error:", e)  # Shows error in terminal
            return f"Registration Failed: {e}"
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            user_id = user["localId"]
            role = db.child("users").child(user_id).child("role").get().val()
            session["user"] = user_id
            session["role"] = role
            if role == "admin":
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("user_dashboard"))
        except:
            return "Login Failed"
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# --- Admin Dashboard ---
@app.route("/admin", methods=["GET"])
@login_required(role="admin")
def admin_dashboard():
    movies = db.child("movies").get().val() or {}
    return render_template("admin_dashboard.html", movies=movies)

@app.route("/admin/add", methods=["GET", "POST"])
@login_required(role="admin")
def add_movie():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        db.child("movies").push({"title": title, "description": description})
        return redirect(url_for("admin_dashboard"))
    return render_template("add_movie.html")

# --- User Dashboard ---
@app.route("/user", methods=["GET"])
@login_required(role="user")
def user_dashboard():
    movies = db.child("movies").get().val() or {}
    return render_template("user_dashboard.html", movies=movies)

if __name__ == "__main__":
    app.run(debug=True)