from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from validate_email import validate_email

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(64))
    password = db.Column(db.String(128))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"User(username={self.username}, email={self.email}, password={self.password})"


"""
with app.app_context():
    db.create_all()
"""


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            return "Invalid username or password."

        else:
            return redirect(f"/home/{username}")

    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if the email is valid and properly formatted
        is_valid = validate_email(email, check_mx=True)

        if not is_valid:
            return "The provided email is not valid. Please provide a valid email."

        used_password = User.query.filter_by(password=password).first()
        used_username = User.query.filter_by(username=username).first()
        used_email = User.query.filter_by(email=email).first()

        if used_username is not None or used_email is not None:
            return "This username or email is already taken. Please choose a different one."

        if used_password is None:
            user = User(username=username, email=email)
            user.set_password(password)  # Hash password before storing
            try:
                db.session.add(user)
                db.session.commit()
                return redirect(f"/home/{username}")
            except Exception as e:
                return (
                    f"There was an error creating your account: {e} Please try again..."
                )

        else:
            return "This password is already taken. Please choose a different one."

    else:
        return render_template("register.html")


@app.route("/home/<username>", methods=["GET"])
def home(username):
    return render_template("home.html", username=username)


@app.route("/logout")
def logout():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
