#-*- coding:utf-8 -*-


import datetime

from string import strip

from flask import render_template, flash, redirect, session, url_for, request, g 
from flask.ext.login import login_user, logout_user, current_user, login_required 

from models import User, Post, ROLE_USER, ROLE_ADMIN
from app import app, db, lm
from forms import LoginForm, SignUpForm, AboutMeForm,PublishBlogForm


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@app.route('/index')
def index():
    user = 'Man'
    posts = [
        {
            'author': {'nickname': 'John'},

            'body': 'Beautiful day in Portland!'
        },

        {
            'author': {'nickname': 'Susan'},

            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template(
        "index.html",
        title="Home",
        user=user,
        posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # 验证用户是否被验证
    if current_user.is_authenticated:
        return redirect('index')
    # 注册验证
    form = LoginForm()
    if form.validate_on_submit():
        user = User.login_check(request.form.get('user_name'))
        if user:
            login_user(user)
            user.last_seen = datetime.datetime.now()

            try:
                db.session.add(user)
                db.session.commit()
            except:
                flash("The Database error!")
                return redirect('/login')

            flash('Your name: ' + request.form.get('user_name'))
            flash('remember me? ' + str(request.form.get('remember_me')))
            return redirect(url_for("index", user_id=current_user.id))
        else:
            flash('Login failed, Your name is not exist!')
            return redirect('/login')

    return render_template(
        "login.html",
        title="Sign In",
        form=form)

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    user = User()
    if form.validate_on_submit():
        user_name = request.form.get('user_name')
        user_email = request.form.get('user_email')

        register_check = User.query.filter(db.or_(
            User.nickname == user_name, User.email == user_email)).first()
        if register_check:
            flash("error: The user's name or email already exists!")
            return redirect('/sign-up')

        if len(user_name) and len(user_email):
            user.nickname = user_name
            user.email = user_email
            user.role = ROLE_USER
            try:
                db.session.add(user)
                db.session.commit()
            except:
                flash("The Database error!")
                return redirect('/sign-up')

            flash("Sign up successful!")
            return redirect('/index')

    return render_template(
        "sign_up.html",
        form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<int:user_id>', methods=["POST", "GET"])
@login_required
def users(user_id):
    form = AboutMeForm()
    user = User.query.filter(User.id == user_id).first()
    if not user:
        flash("The user is not exist.")
        redirect("/index")
    blogs = user.posts.all()
    return render_template(
        "user.html",
        form=form,
        user=user,
        blogs=blogs)

@app.route('/publish/<int:user_id>', methods=["POST", "GET"])
@login_required
def publish(user_id):
    form = PublishBlogForm()
    posts = Post()
    if form.validate_on_submit():
        blog_body = request.form.get("body")
        if not len(strip(blog_body)):
            flash("The content is necessray!")
            return redirect(url_for("publish", user_id=user_id))
        posts.body = blog_body
        posts.timestamp = datetime.datetime.now()
        posts.user_id = user_id

        try:
            db.session.add(posts)
            db.session.commit()
        except:
            flash("Database error!")
            return redirect(url_for("publish", user_id=user_id))

        flash("Publish Successful!")
        return redirect(url_for("publish", user_id=user_id))

    return render_template(
        "publish.html",
        form=form)

@app.route('/test/<int:user_id>',methods=['GET','POST'])
def test(user_id):
    form = AboutMeForm()
    user = User.query.filter(User.id == user_id).first()
    blogs = user.posts.all()
    return render_template('test.html',form=form,user=user,blogs=blogs)

@app.route('/test')
def test1():
    return render_template('index1.html')
