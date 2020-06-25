import json
from functools import wraps

from flask import render_template, Blueprint, redirect, url_for, flash, request, current_app, jsonify
from flask_login import current_user, logout_user
from sqlalchemy import or_, desc
from sqlalchemy.exc import SQLAlchemyError
from wtforms import ValidationError

from agil import db, bcrypt
from agil.Administrateur.models.form import ResetLoginForm, TypeCarburant, UpdateCarburant, StationService, ComptesChef, \
    ComptesChefUpd, EmpStation, UpdEmpStation, EmployeeFilter
from agil.Administrateur.utils import get_carburant_data, get_field_carburant, remplire_field_carburant, \
    get_station_data, get_field_station, remplire_field_station, remplire_field_account, \
    verifIdendity, get_field_account, verifIdendityEmpStation, get_field_employee, remplire_field_employee, \
    get_empStation_data, get_account_data, get_account_data_setting
from agil.Chef.models.form import ResetLoginForm, ToDoFormUpd, ToDoForm, SettingsInfo
from agil.Chef.utils import days_between, generate, verifDate, get_to_do_data, addDay, get_absence_employee_data, \
    get_conge_employee_data, get_field_account_settings, verifIdenditySettings
from agil.Main.utils import send_details_logout, FormatString, currentDate, addMonth
from agil.models.Absence import Absence
from agil.models.Carburant import Carburant
from agil.models.Conge import Conge
from agil.models.Delegation import Delegation
from agil.models.Employee import Employee
from agil.models.Station import Station
from agil.models.ToDo import ToDo
from agil.models.User import User
from agil.models.Ville import Ville

admin = Blueprint('admin', __name__)


def login_required():
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()
            if not days_between(current_user.expiryCompte) or current_user.nbrAttempts < 1 or current_user.etatCompte < 1:
                ur = User.query.filter_by(idUser=current_user.idUser).filter(User.roleUser == 1).first()
                if ur:
                    try:
                        ur.etatCompte = 0
                        ur.nbrAttempts = 0
                        db.session.commit()
                        flash('Veuillez réinitialiser votre mot de passe pour déverrouiller le compte', 'error')
                    except SQLAlchemyError:
                        db.session.rollback()
                return current_app.login_manager.unauthorized()
            return fn(*args, **kwargs)

        return decorated_view

    return wrapper


@admin.route('/administrateur/reset', methods=['GET', 'POST'])
@login_required()
def resetLogin():
    form = ResetLoginForm()
    if current_user.is_authenticated:
        if not bcrypt.check_password_hash(current_user.passUser, "0000"):
            return redirect(url_for('admin.index'))
        else:
            if form.validate_on_submit():
                user = User.query.filter(or_(User.cinUser == current_user.cinUser, User.codeUser == current_user.codeUser)).first_or_404()
                if user:
                    try:
                        hashed_password = bcrypt.generate_password_hash(form.Password.data).decode('utf-8')
                        user.passUser = hashed_password
                        db.session.commit()
                        flash('Votre mot de passe a été mis à jour avec succès', 'success')
                        return redirect(url_for('admin.index'))
                    except SQLAlchemyError:
                        db.session.rollback()
                        flash('Erreur inconnue due au serveur', 'error')
                    return redirect(url_for('admin.resetLogin'))
    return render_template('./admin/reset/reset.html', form=form, title="Reset Password")


@admin.route('/admin/generate', methods=['GET', 'POST'])
@login_required()
def generatePass():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        if request.method == 'POST':
            Str = generate()
            return json.dumps({"Password": Str}).encode('utf8')
    return ''


@admin.route('/administrateur/', methods=['GET', 'POST'])
@admin.route('/administrateur/index', methods=['GET', 'POST'])
@login_required()
def index():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('admin.resetLogin'))
    form = ToDoForm()
    formUpd = ToDoFormUpd()
    return render_template('./admin/index.html',form=form, formUpd=formUpd)


@admin.route('/administrateur/StationFetch', methods=['GET', 'POST'])
@login_required()
def indexStatFetch():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        recordObject = [{"Id": 0, "NomStat": "-- sélectionnez une option --"}]
        records = Station.query.all()
        if records:
            for record in records:
                recordObject.append({
                    "Id": record.idStation,
                    "NomStat": record.NomStation
                })

        return json.dumps(recordObject).encode('utf8'), 200


@admin.route('/administrateur/toDo/Fetch', methods=['GET', 'POST'])
@login_required()
def fetchToDo():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        if request.method == 'POST':
            records = ToDo.query.filter(ToDo.idUser == current_user.get_id())
            date = FormatString(request.json['date'])
            if date == "":
                records = records.filter(ToDo.dateListUser.between(currentDate(), addDay())).order_by(desc(ToDo.dateListUser), desc(ToDo.idListUser)).all()
            else:
                if verifDate(date):
                    records = records.filter(ToDo.dateListUser == date).order_by(desc(ToDo.idListUser)).all()
                else:
                    return jsonify(data={"Msg": "Error Date Format"}), 201
            return json.dumps(get_to_do_data(records)).encode('utf8'), 200

        return ''


@admin.route('/administrateur/toDo/FetchSingle', methods=['GET', 'POST'])
@login_required()
def fetchSingleToDo():
    recordObject = []
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        if request.method == 'POST':
            id = FormatString(request.json['id'])
            if id:
                record = ToDo.query.filter_by(idListUser=id).filter(ToDo.idUser == current_user.get_id()).first()
                if record:
                    recordObject.append({
                        "Id": record.idListUser,
                        "Description": record.objListUser,
                        "Date": str(record.dateListUser)
                    })
                return json.dumps(recordObject).encode('utf8'), 200
            else:
                return jsonify(data={"Msg": "Erreur inconnue due au serveur"}), 201

        return ''


@admin.route('/administrateur/toDo/Add', methods=['GET', 'POST'])
@login_required()
def addToDot():
    form = ToDoForm()
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        if form.validate_on_submit():
            try:
                do = ToDo(objListUser=FormatString(form.Task.data), dateListUser=FormatString(form.Date.data), idUser=current_user.get_id())
                db.session.add(do)
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                return jsonify(data={"Msg": "Erreur inconnue due au serveur"}), 202
            else:
                return jsonify(data={"Msg": "Un événement a été ajouté avec succès"}), 200

        return jsonify(data=form.errors), 201


@admin.route('/administrateur/toDo/MarkAsDone', methods=['GET', 'POST'])
@login_required()
def markAsDone():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        if request.method == 'POST':
            id = FormatString(request.json['id'])
            if id:
                do = ToDo.query.filter_by(idListUser=id).filter(ToDo.stateListUser == 1, ToDo.idUser == current_user.get_id()).first()
                if do:
                    try:
                        do.stateListUser = 0
                        db.session.commit()
                    except SQLAlchemyError:
                        db.session.rollback()
                        return jsonify(data={"Msg": "Erreur inconnue due au serveur"}), 201
                    else:
                        return jsonify(data={"Msg": "Terminé avec succès"}), 200
                else:
                    return jsonify(data={"Msg": "Erreur"}), 202
            else:
                return jsonify(data={"Msg": "Erreur"}), 202

        return ''


@admin.route('/administrateur/toDo/MarkAsUndone', methods=['GET', 'POST'])
@login_required()
def markAsUndone():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        if request.method == 'POST':
            id = FormatString(request.json['id'])
            if id:
                do = ToDo.query.filter_by(idListUser=id).filter(ToDo.stateListUser == 0, ToDo.idUser == current_user.get_id()).first()
                if do:
                    try:
                        do.stateListUser = 1
                        db.session.commit()
                    except SQLAlchemyError:
                        db.session.rollback()
                        return jsonify(data={"Msg": "Erreur inconnue due au serveur"}), 201
                    else:
                        return jsonify(data={"Msg": "Terminé avec succès"}), 200
                else:
                    return jsonify(data={"Msg": "Erreur"}), 202
            else:
                return jsonify(data={"Msg": "Erreur"}), 202

        return ''


@admin.route('/administrateur/toDo/Restore', methods=['GET', 'POST'])
@login_required()
def Restore():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        if request.method == 'POST':
            id = FormatString(request.json['id'])
            if id:
                do = ToDo.query.filter_by(idListUser=id).filter(ToDo.delListUser == 0, ToDo.idUser == current_user.get_id()).first()
                if do:
                    try:
                        do.delListUser = 1
                        db.session.commit()
                    except SQLAlchemyError:
                        db.session.rollback()
                        return jsonify(data={"Msg": "Erreur inconnue due au serveur"}), 201
                    else:
                        return jsonify(data={"Msg": "Terminé avec succès"}), 200
                else:
                    return jsonify(data={"Msg": "Erreur"}), 202
            else:
                return jsonify(data={"Msg": "Erreur"}), 202

        return ''


@admin.route('/administrateur/toDo/UpdateToDO', methods=['GET', 'POST'])
@login_required()
def updateToDot():
    form = ToDoFormUpd()
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        if form.validate_on_submit():
            id = FormatString(form.Id.data)
            if id:
                do = ToDo.query.filter_by(idListUser=id).filter(ToDo.idUser == current_user.get_id()).first()
                if do:
                    try:
                        do.objListUser = FormatString(form.Task.data)
                        do.dateListUser = FormatString(form.Date.data)
                        do.delListUser = 1
                        db.session.commit()
                    except SQLAlchemyError:
                        db.session.rollback()
                        return jsonify(data={"Msg": "Erreur inconnue due au serveur"}), 201
                    else:
                        return jsonify(data={"Msg": "Terminé avec succès"}), 200
                else:
                    return jsonify(data={"Msg": "Erreur"}), 202
            else:
                return jsonify(data={"Msg": "Erreur"}), 202

        return jsonify(data=form.errors), 201


@admin.route('/administrateur/toDo/PreDelete', methods=['GET', 'POST'])
@login_required()
def PreDelete():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        if request.method == 'POST':
            id = FormatString(request.json['id'])
            if id:
                do = ToDo.query.filter_by(idListUser=id).filter(ToDo.delListUser == 1, ToDo.idUser == current_user.get_id()).first()
                if do:
                    try:
                        do.delListUser = 0
                        db.session.commit()
                    except SQLAlchemyError:
                        db.session.rollback()
                        return jsonify(data={"Msg": "Erreur inconnue due au serveur"}), 201
                    else:
                        return jsonify(data={"Msg": "Terminé avec succès"}), 200
                else:
                    return jsonify(data={"Msg": "Erreur"}), 202
            else:
                return jsonify(data={"Msg": "Erreur"}), 202

        return ''


@admin.route('/administrateur/toDo/Delete', methods=['GET', 'POST'])
@login_required()
def Delete():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        if request.method == 'POST':
            id = FormatString(request.json['id'])
            if id:
                do = ToDo.query.filter_by(idListUser=id).filter(ToDo.idUser == current_user.get_id()).first()
                if do:
                    try:
                        db.session.delete(do)
                        db.session.commit()
                    except SQLAlchemyError:
                        db.session.rollback()
                        return jsonify(data={"Msg": "Erreur inconnue due au serveur"}), 201
                    else:
                        return jsonify(data={"Msg": "Terminé avec succès"}), 200
                else:
                    return jsonify(data={"Msg": "Erreur"}), 202
            else:
                return jsonify(data={"Msg": "Erreur"}), 202

        return ''


@admin.route('/administrateur/carburant', methods=['GET', 'POST'])
@admin.route('/administrateur/carburant/index', methods=['GET', 'POST'])
@login_required()
def consulter_carburant():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('admin.resetLogin'))
    return render_template('./admin/carburant/consulter.html', title="Liste du Carburant", data=get_carburant_data(Carburant.query.all()))


@admin.route('/administrateur/carburant/ajouter', methods=['GET', 'POST'])
@login_required()
def ajouter_carburant():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('admin.resetLogin'))
    form = TypeCarburant()
    if form.validate_on_submit():
        Carb = Carburant(NomCarburant=FormatString(form.Type.data), PrixCarburant=form.Prix.data)
        try:
            db.session.add(Carb)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            flash('Erreur inconnue due au serveur', 'error')
        else:
            flash("Le carburant a été ajouté avec succès", 'success')
        return redirect(url_for('admin.consulter_carburant'))

    return render_template('./admin/carburant/ajouter.html', form=form, title="Ajouter Carburant")


@admin.route('/administrateur/carburant/<int:id>/modifier', methods=['GET', 'POST'])
@login_required()
def modifier_carburant(id):
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('admin.resetLogin'))
    Carb = Carburant.query.filter_by(idCarburant=id).first_or_404()
    form = UpdateCarburant()
    if form.validate_on_submit():
        if Carb.NomCarburant != FormatString(form.Type.data):
            emp = Carburant.query.filter(Carburant.NomCarburant == FormatString(form.Type.data)).first()
            if emp:
                flash("Le carburant existe déjà, veuillez réessayer", 'error')
                return redirect(url_for('admin.modifier_carburant', id=Carb.idCarburant, _external=True))
        try:
            get_field_carburant(form, Carb)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            flash('Erreur inconnue due au serveur', 'error')
        else:
            flash("Les données de carburant ont été mis à jour avec succès", 'success')
            return redirect(url_for('admin.consulter_carburant'))
    elif request.method == 'GET':
        remplire_field_carburant(form, Carb)
    return render_template('./admin/carburant/modifier.html', form=form, title="Modifier Carburant")


@admin.route('/administrateur/carburant/<int:id>/supprimer', methods=['GET', 'POST'])
@login_required()
def supprimer_carburant(id):
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('admin.resetLogin'))
    Carb = Carburant.query.filter_by(idCarburant=id).first_or_404()
    try:
        db.session.delete(Carb)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        flash('Erreur inconnue due au serveur', 'error')
    else:
        flash("Les données de carburant ont été supprimées avec succès", 'success')
    return redirect(url_for('admin.consulter_carburant'))


@admin.route('/administrateur/station/data', methods=['GET', 'POST'])
@login_required()
def consulter():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        recordObject = []
        if request.method == 'POST':
            user_id = request.form['id']
            data = Delegation.query.with_entities(Delegation.idDelegation, Delegation.nomDelegation).filter_by(idVille=user_id).all()
            if data is not None:
                recordObject.append({"id": 0, "name": '-- sélectionnez une option --'})
                for record in data:
                    recordObject.append({
                        "id": record.idDelegation,
                        "name": record.nomDelegation
                    })

        return json.dumps(recordObject).encode('utf8')


@admin.route('/administrateur/station/statistique/lavage', methods=['GET', 'POST'])
@login_required()
def stat_lavage():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        recordObject = []
        if request.method == 'POST':
            idStation = request.form['idStation']
            startDate = request.form["startDate"]
            endDate = request.form["endDate"]
            if (idStation is None) or (startDate is None) or (endDate is None):
                return jsonify(data={"Msg": "Erreur"}), 201
            else:
                startDate = FormatString(startDate)
                endDate = FormatString(endDate)
                idStation = FormatString(idStation)

                Str = "SELECT DATE_FORMAT(DateLavage,' %D %M %Y') AS Date ,DateLavage,sum(PrixLavage) As Prix " \
                      "FROM recettelavage join station using(idStation) " \
                      "WHERE idStation = {} AND DateLavage  BETWEEN '{}' AND '{}' " \
                      "GROUP BY Date ,YEAR(Date) ORDER BY DateLavage ".format(idStation, startDate, endDate)

                result = db.session.execute(Str)
                if result:
                    for record in result:
                        recordObject.append({
                            "Date": str(record["Date"]),
                            "Prix": float(record["Prix"])
                        })
                else:
                    recordObject.append({
                        "Date": str(currentDate()),
                        "Prix": 0.0
                    })

        return json.dumps(recordObject).encode('utf8'),200


@admin.route('/administrateur/station/statistique/carburant', methods=['GET', 'POST'])
@login_required()
def stat_carburant():
    recordObject = []
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        if request.method == 'POST':
            idStation = request.form['idStation']
            startDate = request.form["startDate"]
            endDate = request.form["endDate"]
            if (idStation is None) or (startDate is None) or (endDate is None):
                return jsonify(data={"Msg": "Erreur"}), 201
            else:
                startDate = FormatString(startDate)
                endDate = FormatString(endDate)
                idStation = FormatString(idStation)

                Str = "SELECT DATE_FORMAT(DateCarb,' %D %M %Y') AS Date ,DateCarb,sum(prixLitre*(indiceFin-indiceDeb)) As Prix " \
                      "FROM recettecarburant join station using(idStation) " \
                      "WHERE idStation = {} AND DateCarb  BETWEEN '{}' AND '{}' " \
                      "GROUP BY Date ,YEAR(Date) ORDER BY DateCarb".format(idStation, startDate, endDate)

                result = db.session.execute(Str)
                if result:
                    for record in result:
                        recordObject.append({
                            "Date": str(record["Date"]),
                            "Prix": float(record["Prix"])
                        })

        return json.dumps(recordObject).encode('utf8'),200


@admin.route('/administrateur/station/statistique/revenue', methods=['GET', 'POST'])
@login_required()
def stat_revenue():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        recordObject = []
        if request.method == 'POST':
            idStation = request.form['idStation']
            startDate = request.form["startDate"]
            endDate = request.form["endDate"]
            if (idStation is None) or (startDate is None) or (endDate is None):
                return jsonify(data={"Msg": "Erreur"}), 201
            else:
                startDate = FormatString(startDate)
                endDate = FormatString(endDate)
                idStation = FormatString(idStation)

                Str = "SELECT Full, Date, Sum(Prix) as Prix FROM " \
                      "(( SELECT CONCAT(MONTHNAME(DateLavage), ' ', YEAR(DateLavage)) AS Full , DateLavage as Date , sum(PrixLavage) As Prix " \
                      "FROM recettelavage join  station using(idStation) WHERE idStation = {}  AND DateLavage BETWEEN '{}' AND '{}' " \
                      "GROUP BY MONTH(DateLavage) , YEAR(DateLavage)) " \
                      "union " \
                      "(SELECT CONCAT(MONTHNAME(DateCarb),' ', YEAR(DateCarb)) AS Full, DateCarb as Date , sum(prixLitre*(indiceFin - indiceDeb)) As Prix " \
                      "FROM recettecarburant join station using(idStation)  WHERE idStation = {} AND DateCarb BETWEEN '{}' AND '{}'" \
                      "GROUP BY MONTH(DateCarb), YEAR(DateCarb))) a " \
                      "GROUP BY Month(Date),Year(Date) ORDER BY Date".format(idStation, startDate, endDate, idStation, startDate, endDate)

                result = db.session.execute(Str)
                if result:
                    for record in result:
                        recordObject.append({
                            "Date": str(record["Full"]),
                            "Prix": float(record["Prix"])
                        })
        return json.dumps(recordObject).encode('utf8'),200


@admin.route('/administrateur/station/statistique/expenses', methods=['GET', 'POST'])
@login_required()
def stat_expenses():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        recordObject = []
        if request.method == 'POST':
            idStation = request.form['idStation']
            startDate = request.form["startDate"]
            endDate = request.form["endDate"]
            if (idStation is None) or (startDate is None) or (endDate is None):
                return jsonify(data={"Msg": "Erreur"}), 201
            else:
                startDate = FormatString(startDate)
                endDate = FormatString(endDate)
                idStation = FormatString(idStation)

                Str = "SELECT CONCAT(MONTHNAME(dateExpenses), ' ', YEAR(dateExpenses)) AS Full ,dateExpenses as Date, sum(amExpenses) As Prix "\
                      "FROM expenses join station using(idStation) "\
                      "WHERE idStation = {} AND dateExpenses  BETWEEN '{}' AND '{}'"\
                      "GROUP BY Month(Date),Year(Date) ORDER BY Date".format(idStation, startDate, endDate)

                result = db.session.execute(Str)
                if result:
                    for record in result:
                        recordObject.append({
                            "Date": str(record["Full"]),
                            "Prix": float(record["Prix"])
                        })

        return json.dumps(recordObject).encode('utf8'),200


@admin.route('/administrateur/station', methods=['GET', 'POST'])
@admin.route('/administrateur/station/index', methods=['GET', 'POST'])
@login_required()
def consulter_station():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('admin.resetLogin'))
    result = db.session.query(Station).join(Delegation, Delegation.idDelegation == Station.idDelegation).join(Ville, Ville.idVille == Delegation.idVille).all()
    return render_template('./admin/station/consulter.html', title="Liste du Station", data=get_station_data(result))


@admin.route('/administrateur/station/statistique/<int:id>/', methods=['GET', 'POST'])
@login_required()
def consulter_stat_station(id):
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('admin.resetLogin'))
    records = Station.query.filter_by(idStation=id).first_or_404()
    return render_template('./admin/station/statistique.html', title="Statistique Station", data=records.idStation)


@admin.route('/administrateur/station/ajouter', methods=['GET', 'POST'])
@login_required()
def ajouter_station():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('admin.resetLogin'))
    form = StationService()
    form.fill_choice_ville()
    if form.validate_on_submit():
        St = Station(NomStation=FormatString(form.Nom.data), AdrStation=FormatString(form.Adr.data), idDelegation=form.Del.data)
        try:
            db.session.add(St)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            flash('Erreur inconnue due au serveur', 'error')
        else:
            flash("La station a été ajoutée avec succès", 'success')
        return redirect(url_for('admin.consulter_station'))

    return render_template('./admin/station/ajouter.html', form=form, title="Ajouter une Station")


@admin.route('/administrateur/station/<int:id>/modifier', methods=['GET', 'POST'])
@login_required()
def modifier_station(id):
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('admin.resetLogin'))
    St = Station.query.filter_by(idStation=id).first_or_404()
    q = db.session.query(Station).join(Delegation, Delegation.idDelegation == Station.idDelegation).join(Ville, Ville.idVille == Delegation.idVille).filter(
        Station.idStation == id).first()
    form = StationService()
    form.fill_choice_Del(q.Delegation.idVille)
    form.fill_choice_ville()
    if form.validate_on_submit():
        if St.NomStation != FormatString(form.Nom.data).capitalize():
            emp = Station.query.filter(Station.NomStation == FormatString(form.Nom.data)).first()
            if emp:
                flash("Nom Station existe déjà, veuillez réessayer", 'error')
                return redirect(url_for('admin.modifier_station', id=St.idStation, _external=True))
        try:
            get_field_station(form, St)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            flash('Erreur inconnue due au serveur', 'error')
        else:
            flash("La station a été mise à jour avec succès", 'success')
        return redirect(url_for('admin.consulter_station'))
    elif request.method == 'GET':
        remplire_field_station(form, q)

    return render_template('./admin/station/modifier.html', form=form, title="Modifier une Station")


@admin.route('/administrateur/station/<int:id>/supprimer', methods=['GET', 'POST'])
@login_required()
def supprimer_station(id):
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('admin.resetLogin'))
    St = Station.query.filter_by(idStation=id).first_or_404()
    try:
        db.session.delete(St)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        flash("Erreur inconnue due au serveur", 'error')
    else:
        flash("Les données de la station ont été supprimées avec succès", 'success')
    return redirect(url_for('admin.consulter_station'))


@admin.route('/administrateur/compte/', methods=['GET', 'POST'])
@admin.route('/administrateur/compte/index', methods=['GET', 'POST'])
@login_required()
def conCompteChef():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('admin.resetLogin'))
    results = User.query.filter(User.roleUser == 0).all()
    return render_template('./admin/accounts/consulter.html', title="Consulter Les Comptes", data=get_account_data(results))


@admin.route('/administrateur/compte/ajouter', methods=['GET', 'POST'])
@login_required()
def ajtCompteChef():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('admin.resetLogin'))
    form = ComptesChef()
    form.fill_choice_St()
    if form.validate_on_submit():
        try:
            user = User(codeUser=form.Code.data,roleUser=0, cinUser=form.Cin.data, emailUser=form.Email.data,
                        nomUser=FormatString(form.Nom.data).capitalize(), prenomUser=FormatString(form.Prenom.data).capitalize(), telUser=form.Tel.data, createCompte=currentDate(),
                        dateUser=form.Date.data,expiryCompte=addMonth(), idStation=form.Station.data)
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            flash('Erreur inconnue due au serveur', 'error')
        else:
            flash("Le compte Chef a été ajouté avec succès", 'success')
        return redirect(url_for('admin.conCompteChef'))

    return render_template('./admin/accounts/ajouter.html', form=form, title="Ajouter un Compte")


@admin.route('/administrateur/compte/<int:id>/modifier', methods=['GET', 'POST'])
@login_required()
def modCompteChef(id):
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('admin.resetLogin'))
    user = User.query.filter_by(idUser=id).filter(User.roleUser == 0).first_or_404()
    form = ComptesChefUpd()
    form.fill_choice_St()
    if form.validate_on_submit():
        othUser = User(codeUser=form.Code.data, roleUser=0, cinUser=form.Cin.data, emailUser=form.Email.data,
                       nomUser=FormatString(form.Nom.data).capitalize(), prenomUser=FormatString(form.Prenom.data).capitalize(), telUser=form.Tel.data, dateUser=form.Date.data,
                       idStation=form.Station.data, etatCompte=form.Etat.data)
        try:
            verifIdendity(user, othUser)
            get_field_account(form, user)
            etat = int(user.etatCompte)
            if etat == 1:
                user.nbrAttempts = 3
                if not days_between(user.expiryCompte):
                    user.expiryCompte = addMonth()
                    user.passUser = f'$2b$12$VILP2t3.JdQzbSx4qZ7jn.8dzueDJYjx12pJMoj/4ORyFRzPHkFY6'
            elif etat == 0:
                user.nbrAttempts = 0
                user.passUser = f'$2b$12$VILP2t3.JdQzbSx4qZ7jn.8dzueDJYjx12pJMoj/4ORyFRzPHkFY6'
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            flash('Erreur inconnue due au serveur', 'error')
        except ValidationError as e:
            flash(str(e), 'error')
            return redirect(url_for('admin.modCompteChef', id=user.idUser, _external=True))
        else:
            flash("Le compte a été mis à jour avec succès", 'success')
        return redirect(url_for('admin.conCompteChef'))
    elif request.method == 'GET':
        remplire_field_account(form, user)
    return render_template('./admin/accounts/modifier.html', form=form, title="Modifier le Compte")


@admin.route('/administrateur/compte/<int:id>/supprimer', methods=['GET', 'POST'])
@login_required()
def suppCompteChef(id):
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('admin.resetLogin'))
    user = User.query.filter_by(idUser=id).filter(User.roleUser == 0).first_or_404()
    try:
        db.session.delete(user)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        flash('Erreur inconnue due au serveur', 'error')
    else:
        flash("Les données du compte ont été supprimées avec succès", 'success')
    return redirect(url_for('admin.conCompteChef'))


""" Employee """


@admin.route('/admin/employee/conge/record', methods=['GET', 'POST'])
@login_required()
def fetchCongeEmployee():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        if request.method == 'POST':
            idEmploye = request.form['id']
            if idEmploye:
                records = Conge.query.join(Employee, Employee.idEmp == Conge.idEmp) \
                    .join(Station, Station.idStation == Employee.idStation) \
                    .filter(Employee.idEmp == idEmploye).order_by(desc(Conge.DateDebConge), desc(Conge.idConge)).all()
                return json.dumps(get_conge_employee_data(records)).encode('utf8'), 200
            else:
                return jsonify(data={"Msg": "Erreur"}), 201

        return ''


@admin.route('/admin/employee/absence/record', methods=['GET', 'POST'])
@login_required()
def fetchAbsenceEmployee():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        if request.method == 'POST':
            idEmploye = request.form['id']
            if idEmploye:
                records = Absence.query.join(Employee, Employee.idEmp == Absence.idEmp) \
                    .join(Station, Station.idStation == Employee.idStation) \
                    .filter(Employee.idEmp == idEmploye)\
                    .order_by(desc(Absence.DateAbsence),desc(Absence.idAbsence)).all()
                return json.dumps(get_absence_employee_data(records)).encode('utf8'), 200
            else:
                return jsonify(data={"Msg": "Erreur"}), 201

        return ''


@admin.route('/administrateur/employee/', methods=['GET', 'POST'])
@admin.route('/administrateur/employee/consulter', methods=['GET', 'POST'])
@login_required()
def consulter_employee_station():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    emp = Employee.query
    form = EmployeeFilter()
    form.fill_choice_groupe()
    if form.validate_on_submit():
        Str = FormatString(str(form.Groupe.data))
        if Str:
            emp = emp.filter(Employee.idStation == Str)

    elif request.method == 'GET':
        Str = request.args.get('idStation')
        if Str:
            emp = emp.filter(Employee.idStation == FormatString(str(Str)))

    emp = emp.order_by(Employee.idGroupe, desc(Employee.idEmp)).all()
    return render_template('./admin/employee/consulter.html',form=form, title="Consulter les Employés",data=get_empStation_data(emp))


@admin.route('/admin/employee/consulter/<int:id>/', methods=['GET', 'POST'])
@login_required()
def consulter_one_employee_station(id):
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    records = Employee.query.filter_by(idEmp=id).first_or_404()
    return render_template('./admin/employee/one.html',records=records, data=records.idEmp, title="Consulter Profil d'employé")


@admin.route('/administrateur/employee/ajouter', methods=['GET', 'POST'])
@login_required()
def ajouter_employee_station():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('admin.resetLogin'))
    form = EmpStation()
    form.fill_choice_role()
    form.fill_choice_groupe()
    form.fill_choice_stat()
    if form.validate_on_submit():
        try:
            emp = Employee(codeEmp=FormatString(form.Code.data),cinEmp=FormatString(form.Cin.data),nomEmp=FormatString(form.Nom.data).capitalize(),
                           prenomEmp=FormatString(form.Prenom.data).capitalize(),telEmp=FormatString(form.Tel.data),idGroupe=form.Groupe.data,
                           idRole=form.Role.data,dateEmp=FormatString(form.Date.data),salEmp=form.Sal.data,idStation=form.Stat.data)
            db.session.add(emp)
            db.session.commit()
        except SQLAlchemyError:
            flash("Erreur inconnue due au serveur", 'error')
            db.session.rollback()
        else:
            flash("L'employé a été ajouté avec succès", 'success')
        return redirect(url_for('admin.consulter_employee_station',idStation=form.Stat.data, _external=True))

    return render_template('./admin/employee/ajouter.html',form=form, title="Ajouter un Employé")


@admin.route('/administrateur/employee/<int:id>/modifier', methods=['GET', 'POST'])
def modifier_employee_station(id):
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    emp = Employee.query.filter_by(idEmp=id).first_or_404()
    form = UpdEmpStation()
    form.fill_choice_role()
    form.fill_choice_groupe()
    form.fill_choice_stat()
    if form.validate_on_submit():
        try:
            othEmp = Employee(codeEmp=FormatString(form.Code.data), cinEmp=FormatString(form.Cin.data), nomEmp=FormatString(form.Nom.data).capitalize(),
                              prenomEmp=FormatString(form.Prenom.data).capitalize(), telEmp=FormatString(form.Tel.data), idGroupe=form.Groupe.data,
                              idRole=form.Role.data, dateEmp=FormatString(form.Date.data),salEmp=form.Sal.data, idStation=form.Stat.data)
            verifIdendityEmpStation(emp, othEmp)
            get_field_employee(form, emp)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            flash("Erreur inconnue due au serveur", 'error')
        except ValidationError as e:
            flash(str(e), 'error')
            return redirect(url_for('admin.modifier_employee_station', id=emp.idEmp, _external=True))
        else:
            flash("Employé a été mis à jour avec succès", 'success')
        return redirect(url_for('admin.consulter_employee_station',idStation=form.Stat.data, _external=True))
    elif request.method == 'GET':
        remplire_field_employee(form, emp)

    return render_template('./admin/employee/modifier.html',form=form,title="Modifier un Employé")


@admin.route('/administrateur/employee/<int:id>/supprimer', methods=['GET', 'POST'])
@login_required()
def supprimer_employee_station(id):
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('admin.resetLogin'))
    emp = Employee.query.filter_by(idEmp=id).first_or_404()
    try:
        db.session.delete(emp)
        db.session.commit()
    except SQLAlchemyError:
        flash("Erreur inconnue due au serveur", 'error')
        db.session.rollback()
    else:
        flash("L'employé a été supprimé avec succès", 'success')
    return redirect(url_for('admin.consulter_employee_station',idStation=emp.idStation, _external=True))


""" Settings """


@admin.route('/admin/setting/propos', methods=['GET', 'POST'])
@login_required()
def setting():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('admin.resetLogin'))
    user = User.query.filter(User.idStation == current_user.idStation,User.roleUser == 1,User.emailUser == current_user.emailUser).first_or_404()
    form = SettingsInfo()
    if form.validate_on_submit():
        try:
            othUser = User(codeUser=user.codeUser, roleUser=user.roleUser, cinUser=form.Cin.data,emailUser=user.emailUser,
                           nomUser=FormatString(form.Nom.data).capitalize(),prenomUser=FormatString(form.Prenom.data).capitalize(),
                           telUser=form.Tel.data, dateUser=form.Date.data, idStation=user.idStation,etatCompte=user.etatCompte)
            verifIdenditySettings(user, othUser)
            get_field_account_settings(form, user)
            db.session.commit()
        except SQLAlchemyError:
            flash("Erreur inconnue due au serveur", 'error')
            db.session.rollback()
            return redirect(url_for('admin.setting'))
        except ValidationError as e:
            flash(str(e), 'error')
            return redirect(url_for('admin.setting'))
        else:
            flash("Les informations de l'utilisateur ont été mise à jour avec succès", 'success')
        return redirect(url_for('admin.setting'))

    return render_template('./admin/profile/propos.html',form=form, title="Consulter les détails du compte",data=get_account_data_setting(user))


@admin.route('/admin/setting/historique', methods=['GET', 'POST'])
@login_required()
def settingHistorique():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('admin.resetLogin'))
    return render_template('./admin/profile/historique.html',title="Consulter l'historique de connexion")


@admin.route('/admin/setting/logindetails', methods=['GET', 'POST'])
@login_required()
def dataLoginDetails():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        if request.method == 'POST':
            recordObject = []
            startDate = request.form["startDate"]
            endDate = request.form["endDate"]
            if (startDate is None) or (endDate is None):
                return jsonify(data={"Msg": "Erreur"}), 201
            else:
                startDate = FormatString(startDate)
                endDate = FormatString(endDate)
                Str = "SELECT idLoginHist,srcIp, DATE_FORMAT(dateAttempt,'%Y-%m-%d') AS Date,dateAttempt,statusAttempt,descAttempt,idUser " \
                      "FROM loguser " \
                      "WHERE idUser = {} AND DATE_FORMAT(dateAttempt,'%Y-%m-%d') BETWEEN '{}' AND '{}' " \
                      "ORDER BY dateAttempt DESC".format(current_user.idUser, startDate,endDate)

                result = db.session.execute(Str)
                if result:
                    for record in result:
                        recordObject.append({
                            "Date":  str(record["dateAttempt"]),
                            "Etat": 'Succès' if (int(record["statusAttempt"]) == 1) else 'Échoué',
                            "Desc": record["descAttempt"],
                            "Ip": record["srcIp"]
                        })

            return json.dumps(recordObject).encode('utf8'),200

        return ""


@admin.route('/admin/setting/password', methods=['GET', 'POST'])
@login_required()
def settingPassword():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('admin.resetLogin'))
    form = ResetLoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.emailUser == current_user.emailUser).first_or_404()
        if user:
            try:
                hashed_password = bcrypt.generate_password_hash(form.Password.data).decode('utf-8')
                user.passUser = hashed_password
                db.session.commit()
                flash('Votre mot de passe a été mis à jour avec succès', 'success')
                return redirect(url_for('admin.setting'))
            except SQLAlchemyError:
                db.session.rollback()
                flash("Erreur inconnue due au serveur", 'error')

            return redirect(url_for('admin.settingPassword'))
    return render_template('./admin/profile/password.html',title="Modifier le mot de passe",form=form)


@admin.route('/admin/setting/generate', methods=['GET', 'POST'])
@login_required()
def dataPassSetting():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        if request.method == 'POST':
            Str = generate()
            return json.dumps({"Password": Str}).encode('utf8')
        return ""


""" Log Out """


@admin.route('/administrateur/logout', methods=['GET', 'POST'])
@login_required()
def logout():
    send_details_logout(current_user)
    logout_user()
    return redirect(url_for('approot.login'))
