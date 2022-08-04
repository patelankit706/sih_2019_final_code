
import os
import secrets
from flask import Flask,render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import LoginForm, LabsReport,GenerateUID,RegistrationForm,GenerateForm
from flaskblog.models import User,Seller,Buyer,Lab,Report
from flaskblog.pseudorandom import uidGenerator,image
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime



@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        if current_user.typeUser <=2:
            return redirect(url_for('user'))
        if current_user.typeUser >=3:
            return redirect(url_for('admin'))
    return render_template('home.html')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.typeUser <=2:
            return redirect(url_for('user'))
        if current_user.typeUser >=3:
            return redirect(url_for('admin'))
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            if current_user.typeUser <=2:
                return redirect(url_for('user'))
            if current_user.typeUser >=3:
                return redirect(url_for('admin'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)




@app.route("/user")
@login_required
def user():
    if current_user.typeUser <= 2:
        return render_template('user.html')
    return redirect(url_for('login'))


@app.route("/admin")
@login_required
def admin():
    if current_user.typeUser ==3:
        a=len(User.query.filter_by(typeUser=0).all())
        return render_template('admin.html',leng=a)
    elif current_user.typeUser == 4:
        a=len(User.query.filter_by(typeUser=1).all())
        return render_template('admin.html',leng=a)
    elif current_user.typeUser == 5:
        a=len(User.query.filter_by(typeUser=2).all())
        return render_template('admin.html',leng=a)
    elif current_user.typeUser<3:
        flash('You are not admin', 'danger')
        return redirect(url_for('login'))

@app.route("/viewUser/<int:iD>")
@login_required
def viewUser(iD):
    if current_user.typeUser ==3:
        a=len(User.query.filter_by(typeUser=0).all())
        return render_template('viewUser.html',leng=a)
    elif current_user.typeUser == 4:
        a=len(User.query.filter_by(typeUser=1).all())
        return render_template('viewUser.html',leng=a)
    elif current_user.typeUser == 5:
        a=len(User.query.filter_by(typeUser=2).all())
        return render_template('viewUser.html',leng=a)
    elif current_user.typeUser<3:
        flash('You are not admin', 'danger')
        return redirect(url_for('login'))


@app.route("/adminDel/<int:iD>")
@login_required
def adminDel(iD):
    if current_user.typeUser ==3:
        a=User.query.filter_by(typeUser=0).all()
        a=a[iD]
        db.session.delete(a)
        db.session.commit()
        flash('Successfully deleted', 'success')
        return redirect(url_for('admin'))
    elif current_user.typeUser ==4:
        a=User.query.filter_by(typeUser=1).all()
        a=a[iD]
        db.session.delete(a)
        db.session.commit()
        flash('Successfully deleted', 'success')
        return redirect(url_for('admin'))
    elif current_user.typeUser ==5:
        a=User.query.filter_by(typeUser=2).all()
        a=a[iD]
        db.session.delete(a)
        db.session.commit()
        flash('Successfully deleted', 'success')
        return redirect(url_for('admin'))
    else:
        flash('You are not admin', 'danger')
        return redirect(url_for('login'))



@app.route("/adminAdd",methods=['GET', 'POST'])
@login_required
def adminAdd():
    form=RegistrationForm()
    if form.validate_on_submit():
        if current_user.typeUser==3:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user =User(username=form.username.data, email=form.email.data, password=hashed_password,typeUser=0)
            seller=Seller(sID=form.username.data)
            db.session.add_all([user,seller])
            db.session.commit()
            flash('User Created', 'success')
            return redirect(url_for('admin'))
        if current_user.typeUser==4:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user =User(username=form.username.data, email=form.email.data, password=hashed_password,typeUser=1)
            buyer=Buyer(bID=form.username.data)
            db.session.add_all([user,buyer])
            db.session.commit()
            flash('User Created', 'success')
            return redirect(url_for('admin'))
        if current_user.typeUser==5:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user =User(username=form.username.data, email=form.email.data, password=hashed_password,typeUser=2)
            lab=Lab(lID=form.username.data)
            db.session.add_all([user,lab])
            db.session.commit()
            flash('User Created', 'success')
            return redirect(url_for('admin'))
        else:
            flash('You are not admin', 'danger')
            return redirect(url_for('login'))
    return render_template('register.html',form=form)


@app.route("/viewReport")
@login_required
def viewReport():
    if current_user.typeUser == 0 :
        leng=len(Report.query.filter_by(sID=current_user.username).all())
        return render_template('viewReport.html',leng=leng)
    if current_user.typeUser == 1:
        leng=len(Report.query.filter_by(bID=current_user.username).all())
        return render_template('viewReport.html',leng=leng)
    return redirect(url_for('login'))


@app.route("/displayReport/<int:iD>")
@login_required
def displayReport(iD):
    if current_user.typeUser == 0:
        a=Report.query.filter_by(sID=current_user.username).all()
        form = a[iD]
        return render_template('displayReport.html',form=form)
    if current_user.typeUser == 1:
        a=Report.query.filter_by(bID=current_user.username).all()
        form = a[iD]
        return render_template('displayReport.html',form=form)
    return redirect(url_for('login'))




@app.route("/labsReport",methods=['GET', 'POST'])
@login_required
def labsReport():
    if current_user.typeUser == 2:
        form=LabsReport()
        if form.validate_on_submit():
            report=Report.query.filter_by(uID=form.uID.data).first()
            if report and report.validityFlag:
                report.netCalorificValue=form.netCalorificValue.data
                report.grossCalorificValue=form.grossCalorificValue.data
                report.validityFlag=False
                report.lID=current_user.username
                report.testDate=datetime.now()
                db.session.commit()
                flash('Report successfully added', 'success')
                return redirect(url_for('user'))
            flash('UID invalid', 'danger')
        return render_template('labsReport.html',form=form)
    return redirect(url_for('login'))


@app.route("/generateUID",methods=['GET', 'POST'])
@login_required
def generateUID():
    if current_user.typeUser == 0:
        form=GenerateUID()
        if form.validate_on_submit():
            a=uidGenerator()
            image(a)
            if Report.query.filter_by(uID=a).all():
                flash('Unsuccessful', 'danger')
            else:
                report=Report(uID=a, sID=current_user.username, bID=form.bID.data)
                db.session.add(report)
                db.session.commit()
                return render_template('viewUID.html',uID=a)
                flash('Uid generated', 'success')
        return render_template('generateUID.html',form=form)
    return redirect(url_for('login'))

@app.route("/enterCode",methods=['GET', 'POST'])
@login_required
def enterCode():
    if current_user.typeUser == 2:
        form=GenerateForm()
        if form.validate_on_submit():
            a=Report.query.filter_by(uID=form.uID.data).first()
            if a and a.validityFlag:
                return redirect(url_for('labsReport'))
        return render_template('enterCode.html',form=form)
    flash('Report corresponging to this uid not allowed', 'danger')
    return redirect(url_for('login'))
