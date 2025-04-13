from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    jsonify,
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from os import getenv
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = getenv("SECRET")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sentiment_app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db = SQLAlchemy(app)


# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_banned = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}>"


# Create tables
with app.app_context():
    db.create_all()
    # Create admin user if it doesn't exist
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(
            username="admin",
            email="admin@app.com",
            password=generate_password_hash("admin"),
            is_admin=True,
        )
        db.session.add(admin)
        db.session.commit()


# Authentication decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page", "warning")
            return redirect(url_for("login"))

        user = db.session.get(User, session["user_id"])
        if not user or not user.is_admin:
            flash("You do not have permission to access this page", "danger")
            return redirect(url_for("index"))
        return f(*args, **kwargs)

    return decorated_function


def ban_check(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" in session:
            user = db.session.get(User, session["user_id"])
            if user and user.is_banned:
                session.clear()
                flash("Your account has been banned", "danger")
                return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


# Apply ban_check to all routes
def before_request():
    if "user_id" in session:
        user = db.session.get(User, session["user_id"])
        if user and user.is_banned:
            session.clear()
            flash("Your account has been banned", "danger")
            return redirect(url_for("login"))


# Routes
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Validate form data
        if not username or not email or not password:
            flash("All fields are required", "danger")
            return redirect(url_for("signup"))

        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash("Username already taken", "danger")
            return redirect(url_for("signup"))

        if User.query.filter_by(email=email).first():
            flash("Email already registered", "danger")
            return redirect(url_for("signup"))

        # Create new user
        new_user = User(
            username=username, email=email, password=generate_password_hash(password)
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            flash("An error occurred. Please try again.", "danger")
            return redirect(url_for("signup"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Find user by username
        user = User.query.filter_by(username=username).first()

        # Check user existence and password
        if not user or not check_password_hash(user.password, password):
            flash("Invalid username or password", "danger")
            return redirect(url_for("login"))

        # Check if user is banned
        if user.is_banned:
            flash("Your account has been banned", "danger")
            return redirect(url_for("login"))

        # Log user in
        session["user_id"] = user.id

        flash(f"Welcome back, {user.username}!", "success")

        # Redirect based on user type
        if user.is_admin:
            return redirect(url_for("admin_dashboard"))
        else:
            # Redirect normal users to external URL
            return redirect("http://localhost:5678")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out", "info")
    return redirect(url_for("login"))


# Admin routes
@app.route("/admin")
@admin_required
def admin_dashboard():
    users = User.query.filter(User.username != "admin").all()
    return render_template("admin/dashboard.html", users=users)


@app.route("/admin/ban/<int:user_id>", methods=["POST"])
@admin_required
def ban_user(user_id):
    user = User.query.get_or_404(user_id)

    if user.username == "admin":
        flash("Cannot ban admin user", "danger")
        return redirect(url_for("admin_dashboard"))

    user.is_banned = not user.is_banned

    try:
        db.session.commit()
        status = "banned" if user.is_banned else "unbanned"
        flash(f"User {user.username} has been {status}", "success")
    except Exception as e:
        flash("An error occurred", "danger")

    return redirect(url_for("admin_dashboard"))


# API routes for validation
@app.route("/api/check-username", methods=["POST"])
def check_username():
    username = request.json.get("username", "")
    user = User.query.filter_by(username=username).first()
    return jsonify({"available": not user})


if __name__ == "__main__":
    app.run(debug=True)
