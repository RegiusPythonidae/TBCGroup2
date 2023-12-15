from flask import render_template, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from os import path

from forms import AddProductForm, RegisterForm, LoginForm
from models import Product, ProductCategory, User
from ext import app


library = "Flask 2,0"

role = "mod"


@app.route("/")
def index():
    products = Product.query.all()
    return render_template("index.html", products=products, role=role)


@app.route("/search/<string:name>")
def search(name):
    products = Product.query.filter(Product.name.ilike(f"%{name}%")).all()
    return render_template("search.html", products=products)


@app.route("/category/<int:category_id>")
def category(category_id):
    products = Product.query.filter(Product.category_id == category_id).all()
    return render_template("index.html", products=products)


@app.route("/product/<int:product_id>")
def view_product(product_id):
    chosen_product = Product.query.get(product_id)
    if not chosen_product:
        return render_template("404.html")
    return render_template("product.html", product=chosen_product, role=role)


@app.route("/edit_product/<int:product_id>", methods=["POST", "GET"])
@login_required
def edit_product(product_id):
    chosen_product = Product.query.get(product_id)
    if not chosen_product:
        return render_template("404.html")

    if current_user.role != "admin":
        return redirect("/")

    form = AddProductForm(name=chosen_product.name, price=chosen_product.price, img=chosen_product.img)
    if form.validate_on_submit():
        chosen_product.name = form.name.data
        chosen_product.price = form.price.data
        chosen_product.img = form.img.data.filename

        file_directory = path.join(app.root_path, "static", form.img.data.filename)
        form.img.data.save(file_directory)

        chosen_product.save()

    return render_template("add_product.html", form=form)


@app.route("/delete_product/<int:product_id>")
@login_required
def delete_product(product_id):
    chosen_product = Product.query.get(product_id)
    if not chosen_product:
        return render_template("404.html")

    if current_user.role != "admin":
        return redirect("/")

    chosen_product.delete()
    return redirect("/")


@app.route("/add_product", methods=["POST", "GET"])
@login_required
def add_product():
    if current_user.role != "admin":
        return redirect("/")

    form = AddProductForm()
    if form.validate_on_submit():
        new_product = Product(name=form.name.data, price=form.price.data, img=form.img.data.filename)
        new_product.create()

        file_directory = path.join(app.root_path, "static", form.img.data.filename)
        form.img.data.save(file_directory)
        return redirect("/")
    return render_template("add_product.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter(User.username == form.username.data).first()
        if existing_user:
            flash("მომხმარებელი უკვე არსებობს")
        else:
            new_user = User(username=form.username.data, password=form.password.data, role="normal")
            new_user.create()
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")

    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route("/about")
def about():
    language = "Python"
    return render_template("about.html")