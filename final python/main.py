from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bim_market.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

class Products(db.Model):
    __tablename__ = "Products"
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    picture_data = db.Column(db.LargeBinary, nullable=True) 
    picture_mimetype = db.Column(db.String, nullable=True)

# Routes
@app.route("/")
def home():
    id = session.get('user_id')
    return render_template("base.html", is_authenticated='user_id' in session, id=id)

@app.route("/product")
def product():
    product = Products.query.all()
    return render_template("product.html", product=product)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Проверка совпадения паролей
        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for("register"))

        # Проверка существующего пользователя
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("Username or email is already taken.", "error")
            return redirect(url_for("register"))

        # Хеширование пароля и сохранение нового пользователя
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        # Проверяем наличие данных
        if not email or not password:
            flash("Email and password are required.", "error")
            return redirect(url_for("login"))

        # Проверяем, существует ли пользователь
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            # Устанавливаем данные в сессии
            session['user_id'] = user.id
            session['username'] = user.username
            session['email'] = user.email
            flash("Login successful!", "success")
            return redirect(url_for("profile"))  # Перенаправляем на профиль
        else:
            flash("Invalid email or password.", "error")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))

@app.route("/profile")
def profile():
    # Проверяем, вошел ли пользователь
    if 'user_id' not in session:
        flash("You need to log in to view this page.", "error")
        return redirect(url_for("login"))

    # Данные пользователя доступны в сессии
    username = session.get('username')
    email = session.get('email')
    return render_template("profile.html", username=username, email=email)

@app.route("/order")
def order():
    return render_template("order.html")

@app.route("/cart/<int:product_id>", methods=["POST","GET"])
def cart(product_id):
    prod = Products.query.filter_by(product_id=product_id).all()
    if 'user_id' not in session:
        flash("You need to log in to view this page.", "error")
        return redirect(url_for("login"))
    return render_template("cart.html",prod=prod)

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if 'user_id' not in session:
        flash("You need to log in to view this page.", "error")
        return redirect(url_for("login"))
    if request.method == "POST":
        address = request.form.get('address')
        payment = request.form.get('payment')
        flash("Order placed successfully!", "success")
        return redirect(url_for("checkout"))
    return render_template("checkout.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        flash("Your message has been sent!", "success")
    return render_template("contact.html")
@app.route("/admin")
def admin():
    return render_template("admin.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
