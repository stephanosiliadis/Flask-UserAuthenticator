from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(64))
    password = db.Column(db.String(64))

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
        used_password = User.query.filter_by(password=password).first()

        if used_password is not None:
            return redirect(f"/home/{username}")

        else:
            return "No user found with that credentials..."

    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        used_password = User.query.filter_by(password=password).first()

        if used_password is None:
            user = User(username=username, email=email, password=password)
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
