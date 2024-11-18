from flask import Flask, render_template, request, redirect, url_for, flash



app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route("/")
def home():
    return render_template("base.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def reg():
    return render_template("register.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/product")
def product():
    return render_template("product.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        
        
        flash('Your message has been sent successfully!', 'success')
        
        
        
    return render_template("contact.html")


@app.route("/search")
def search():
    return render_template("search.html")


@app.route("/cart")
def cart():
    return render_template("cart.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        address = request.form.get('address')
        payment = request.form.get('payment')
        flash("Thank you! :3")

        return redirect(url_for('checkout'))
        
    return render_template("checkout.html")


@app.route("/order")
def order():
    return render_template("order.html")


@app.route("/faq")
def faq():
    return render_template("faq.html")


if __name__ == "__main__":
    app.run(debug=True)