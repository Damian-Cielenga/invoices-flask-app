from flask import Flask, render_template, request, redirect, flash, url_for, send_from_directory, abort
from flask_login import login_user, login_required, logout_user, current_user
from flask_app import app, bcrypt
from flask_app.forms import LoginForm, ResetForm
from flask_app.models import User
import os 

@app.route("/", methods=["GET", "POST"])
def login():
    # authenticated users will be redirected to dashboard 
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        # filter user from user table
        user = User.query.filter_by(username=form.username.data).first()
        # compare input password with hashed password
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            # redirect to login page if not logged in
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("dashboard"))
        else:
            flash("Login Unsuccessful. Please try again", "danger")
    return render_template("login.html", form=form)

@app.route("/reset", methods=["GET", "POST"])
def reset():
    form = ResetForm()
    # resend password
    if form.validate_on_submit():
        flash("E-mail send successfully", "success")
        return redirect(url_for("reset"))
    return render_template("reset.html", form=form)

@app.route("/login")
def home():
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard(): 
    # path = app.config["DOWNLOAD_FOLDER"] + current_user.username    
    # unsorted_files =  os.listdir(path)             
    # files = sorted(unsorted_files, key=lambda x: x, reverse=True)
    # return render_template("dashboard.html", files=files)
    return render_template("dashboard.html")
    

@app.route("/downloads/<file_name>")
@login_required
def download_file(file_name):
    if current_user.is_authenticated:
        try:
            return send_from_directory(app.config["DOWNLOAD_FOLDER"] + current_user.username, file_name, as_attachment=False)
        except FileNotFoundError:
            abort(404)