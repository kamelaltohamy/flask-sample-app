from flask import flash, render_template, url_for, redirect, g
from flask_login import  login_user,logout_user, current_user, login_required
from app import app, db
from app import User
from app import flask_bcrypt
from forms import LoginForm, SnapForm
from app import Snap
@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('listing'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            flash('No such User exists')
            return render_template('login.html',form=form)
        if (not flask_bcrypt.check_password_hash(user.password,form.password.data)):
            flash("Invalid Password.")
            return render_template('login.html',form=form)
        login_user(user,remember=True)
        flash("you have logged in successfully.")
        return redirect(url_for('listing'))
    
    return render_template('login.html', form=form)


@app.route('/logout',methods=['GET'])
def logout():
    logout_user(user)
    return redirect(url_for('listing'))


@app.route('/hello')
def hello():
    return 'Hello your name!!'




@app.route('/snaps',methods=['GET'])
def listing():
    snaps = Snap.query.order_by(Snap.created_on.desc()).limit(20).all()
    return render_template('snaps_all.html',snaps=snaps)

@app.route('/snaps/add',methods=['GET','POST'])
@login_required
def add():
    form = SnapForm()
    if form.validate_on_submit():
        user_id = current_user.id
        snap = Snap(user_id=user_id,name=form.name.data,content=form.content.data,extension=form.extension.data)
        db.session.add(snap)
        try :
            db.session.commit()
        except exc.SQLAlchemyError:
            current_app.exception('Could not save new snap!!')
            flash(" something went wrong while posting your snap!")
            flash("try again")
    else:
        return render_template('snaps_add.html',form=form)
    return redirect(url_for('listing'))
