import datetime
import json

import flask
import flask_login
from flask import render_template, Blueprint, redirect, url_for, flash, request, abort, app, current_app
from flask_login import current_user, login_user, logout_user
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError

from agil import db, bcrypt, ts, login_manager
from agil.Chef.utils import generate
from agil.Main.models.form import LoginForm, ForgetForm, ResetLoginForm
from agil.Main.utils import FormatString, days_between, login_details, send_details_login, send_reset_email, \
    send_confirmation_email, addMonth
from agil.models.History import LogUser
from agil.models.User import User

approot = Blueprint('approot', __name__)


@login_manager.user_loader
def load_user(id):
    if id is not None:
        return User.query.get(id)
    return None


@approot.before_request
def before_request():
    flask.session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=20)
    flask.session.modified = True
    flask.g.user = flask_login.current_user


@login_manager.unauthorized_handler
def unauthorized():
    logout_user()
    return redirect(url_for('approot.login'))


@approot.route('/', methods=['GET', 'POST'])
@approot.route('/index', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.roleUser == 0:
            return redirect(url_for('chef.index'))
        elif current_user.roleUser == 1:
            return redirect(url_for('admin.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(emailUser=form.Email.data).filter(or_(User.cinUser == FormatString(form.Cin.data), User.codeUser == FormatString(form.Cin.data))).first()
        if user:
            day = days_between(user.expiryCompte)
            x = login_details()
            His = LogUser(srcIp=x["Ip"], dateAttempt=x["Date"], descAttempt=x["Description"], idUser=user.idUser)
            if bcrypt.check_password_hash(user.passUser, form.Password.data) and user.nbrAttempts > 0 and int(user.etatCompte) == 1 and day:
                login_user(user, remember=False)
                try:
                    His.statusAttempt = 1
                    db.session.add(His)
                    db.session.commit()
                    send_details_login(user)
                except SQLAlchemyError:
                    flash("Erreur inconnue due au serveur", 'error')
                    db.session.rollback()
                    return redirect(url_for('approot.login'))

                if form.Password.data == "0000":
                    flash("Veuillez réinitialiser votre mot de passe", 'success')
                    if user.roleUser == 0:
                        return redirect(url_for('chef.resetLogin'))
                    elif user.roleUser == 1:
                        return redirect(url_for('admin.resetLogin'))

                next_page = request.args.get('next')
                flash('Vous êtes connecté avec succès', 'success')
                if next_page:
                    return redirect(next_page)
                else:
                    if user.roleUser == 0:
                        return redirect(url_for('chef.index'))
                    elif user.roleUser == 1:
                        return redirect(url_for('admin.index'))
            else:
                if day:
                    try:
                        if user.nbrAttempts >= 1:
                            user.nbrAttempts -= 1
                            flash('Veuillez vérifier vos informations d\'identification', 'error')
                            if user.nbrAttempts == 0:
                                user.etatCompte = 0
                        else:
                            if user.roleUser == 0:
                                flash('Le compte est verrouillé. Veuillez contacter l\'administrateur', 'error')
                            elif user.roleUser == 1:
                                flash('Veuillez réinitialiser votre mot de passe pour déverrouiller le compte', 'error')
                        His.statusAttempt = 0
                        db.session.add(His)
                        db.session.commit()
                    except SQLAlchemyError:
                        db.session.rollback()
                        flash("Erreur inconnue due au serveur", 'error')
                else:
                    try:
                        user.etatCompte = 0
                        user.nbrAttempts = 0
                        His.statusAttempt = 0
                        db.session.add(His)
                        db.session.commit()
                    except SQLAlchemyError:
                        db.session.rollback()
                        flash("Erreur inconnue due au serveur", 'error')
                    else:
                        if user.roleUser == 0:
                            flash('Le compte est verrouillé. Veuillez contacter l\'administrateur', 'error')
                        elif user.roleUser == 1:
                            flash('Veuillez réinitialiser votre mot de passe pour déverrouiller le compte', 'error')

                send_details_login(user)
                return redirect(url_for('approot.login'))
        else:
            flash('Veuillez vérifier vos informations d\'identification', 'error')
    return render_template('./main/index.html', form=form)


@approot.route('/forget', methods=['GET', 'POST'])
def forget():
    if current_user.is_authenticated:
        return redirect(url_for('main.login'))
    form = ForgetForm()
    if form.validate_on_submit():
        cin = FormatString(form.Cin.data)
        user = User.query.filter(User.emailUser == cin).first()
        if user:
            if not days_between(user.expiryCompte) or user.nbrAttempts < 1:
                try:
                    user.etatCompte = 0
                    user.nbrAttempts = 0
                    db.session.commit()
                except SQLAlchemyError:
                    db.session.rollback()
                    flash("Erreur inconnue due au serveur", 'error')
            try:
                token = ts.dumps(FormatString(form.Cin.data), salt="2Po[=}L=uP9[1Vb-cod2Wo}s#Rp:94Zh^O8")
                user.resetTokenUser = token
                if user.roleUser == 0:
                    if user.nbrAttempts < 1 or user.etatCompte < 1:
                        flash('Votre compte est verrouillé. Veuillez contacter l\'administrateur!', 'error')
                        return redirect(url_for('approot.login'))
                flash('Vérifiez votre boîte aux lettres pour réinitialiser votre mot de passe', 'success')
                db.session.commit()
                send_reset_email(user)
            except SQLAlchemyError:
                flash("Erreur inconnue due au serveur", 'error')
                db.session.rollback()
            else:
                return redirect(url_for('approot.login'))

        else:
            flash("Veuillez vérifier vos informations d'identification", 'error')
            return redirect(url_for('approot.forget'))

    return render_template('./main/forget/forget.html', title='Forget Password', form=form)


@approot.route('/generate', methods=['GET', 'POST'])
def generatePass():
    if request.method == 'POST':
        Str = generate()
        return json.dumps({"Password": Str}).encode('utf8')
    return ''


@approot.route('/reset/<token>', methods=['GET', 'POST'])
def reset(token):
    form = ResetLoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.login'))
    try:
        cin = ts.loads(token, salt="2Po[=}L=uP9[1Vb-cod2Wo}s#Rp:94Zh^O8", max_age=900)  # 15 min
        user = User.query.filter(User.emailUser == cin).first()
        if user:
            if form.validate_on_submit():
                try:
                    day = days_between(user.expiryCompte)
                    hashed_password = bcrypt.generate_password_hash(form.Password.data).decode('utf-8')
                    user.passUser = hashed_password
                    if user.resetTokenUser == token:
                        if user.roleUser == 1:
                            if day:
                                user.etatCompte = 1
                                if user.etatCompte <= 1 or user.nbrAttempts <= 1:
                                    user.nbrAttempts = 3
                            else:
                                if user.etatCompte == 0 or user.nbrAttempts == 0:
                                    user.expiryCompte = addMonth()
                                    user.etatCompte = 1
                                    user.nbrAttempts = 3
                            flash('Votre mot de passe a été mis à jour ! Ce compte est déverrouillé! Vous pouvez maintenant vous connecter','success')
                        elif user.roleUser == 0 and day:
                            flash('Votre mot de passe a été mis à jour !', 'success')
                        else:
                            abort(404)
                    else:
                        abort(404)
                    user.resetTokenUser = '0'
                    db.session.commit()
                    send_confirmation_email(user)
                except SQLAlchemyError:
                    flash("Erreur inconnue due au serveur", 'error')
                    db.session.rollback()
                else:
                    return redirect(url_for('approot.login'))
        else:
            abort(404)
    except:
        abort(404)
    return render_template('./main/forget/reset.html', title='Reset Password', form=form)
