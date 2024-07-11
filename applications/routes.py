from applications import app, db
from applications.forms import RegisterForm, LoginForm,CheckupForm
from flask import render_template, redirect, url_for, flash, request
from applications.models import User
from flask_login import login_user, logout_user, login_required,current_user



@app.route('/')
@app.route('/home')
def home_page():
    return render_template("home.html",username=current_user)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        with app.app_context():
            attempted_user=User.query.filter_by(username=form.username.data).first()
            if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
                login_user(attempted_user)
                flash(f'You have successfully logged in as : {attempted_user.username}' , category='success')
                return redirect(url_for('dashboard'))
            else:
                flash(f'Username and password do not match ! Please try again', category='error')
                print("Username and password do not match ! Please try again")
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET','POST'])
def sign_up():
    form=RegisterForm()
    if form.validate_on_submit():
        with app.app_context():
            user_data=User(username=form.username.data,
                        email_address=form.email_address.data,
                        password=form.password1.data)
            
            db.session.add(user_data)
            db.session.commit()
            login_user(user_data)
        
        return redirect(url_for('dashboard'))
    
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='error')
    
    return render_template('signup.html', form=form)


@app.route('/checkup',methods=['GET','POST'])
def check_up():
    myform=CheckupForm()
    if myform.validate_on_submit():
        # Access form data
        username=myform.username.data
        gender=myform.gender.data
        age=myform.age.data
        address=myform.address.data

        pincode = myform.pincode.data
        hypertension = myform.hypertension.data
        previousHeartDisease = myform.previousHeartDisease.data
        smoking_History = myform.smoking_History.data
        weight = myform.weight.data
        height = myform.height.data
        hba1clvl = myform.hba1clvl.data
        blood_glucose = myform.blood_glucose.data
        email = myform.email.data
        phone = myform.phone.data

        if len(username) < 2:
            flash("Username must be greater than 4 characters.", category='error')
        elif (age) >= 150:
            flash("Age value exceeded", category='error')
        elif (height)>3:
            flash("Invalid Height Input.", category='error')
        elif (blood_glucose) > 700:
            flash("invalid blood glucose level", category='error')
        else:
            flash("Form Submited!", category='success')
            redirect(url_for('check_up'))
    return render_template('checkup.html',form=myform)



@app.route('/logout')
@login_required
def logout():
    print("Logout")
    logout_user()
    return redirect(url_for('home_page'))

