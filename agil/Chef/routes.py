import json
from functools import wraps

from flask import render_template, Blueprint, redirect, url_for, flash, request, current_app, jsonify
from flask_login import current_user, logout_user
from sqlalchemy import desc, or_, func, and_
from sqlalchemy.exc import SQLAlchemyError
from wtforms import ValidationError

from agil import db, bcrypt
from agil.Chef.models.form import Recette, Pompes, DateRecette, PompeCiternes, Citernes, UpdCiternes, UpdPompes, \
    UpdPompeCiternes, RecetteCar, RecetteFilter, CarFilter, ResetLoginForm, ToDoForm, ToDoFormUpd, ExpensesForm, \
    ExpenseFilter, EmpStation, UpdEmpStation, AbsenceForm, UpdAbsenceForm, AbsenceFilter, CongeForm, CongeFormFilter, \
    UpdCongeForm, EmployeeFilter, SettingsInfo
from agil.Chef.utils import remplire_field_recetteLavage, get_field_recetteLavage, get_recette_lavage_data, \
    get_citerne_data, remplire_field_one_citerne, get_field_citerne, remplire_field_citerne, get_pompe_data, \
    get_field_pompe, remplire_field_pompe, get_pompe_citerne_data, get_field_pompe_citerne, \
    remplire_field_pompe_citerne, get_recette_carburant_data, get_field_recetteCarb, remplire_field_recetteCarb, \
    FilterDataLavage, FilterDataCarburant, days_between, generate, \
    currentDate, addDay, get_to_do_data, verifDate, get_expenses_data, remplire_field_expenses, get_field_expenses, \
    FilterDataExpenses, get_empStation_data, remplire_field_employee, get_field_employee, verifIdendityEmpStation, \
    get_absence_data, get_field_absence, remplire_field_absence, FilterDataAbsence, \
    FilterDataAbsenceEmployee, get_conge_data, get_field_conge, remplire_field_conge, days_calc, FilterDataConge, \
    get_conge_employee_data, FilterDataLavageVoiture, get_absence_employee_data, get_account_data, \
    verifIdenditySettings, get_field_account_settings, currentDateTime, get_notification_data, pretty_date
from agil.Main.utils import send_details_logout, FormatString, addMonth
from agil.models.Absence import Absence
from agil.models.Citerne import Citerne
from agil.models.Comment import Comment
from agil.models.Conge import Conge
from agil.models.Employee import Employee
from agil.models.Expenses import Expenses
from agil.models.Pompe import Pompe
from agil.models.PompeCiterne import PompeCiterne
from agil.models.RecetteCarburant import RecetteCarburant
from agil.models.RecetteLavage import RecetteLavage
from agil.models.Station import Station
from agil.models.ToDo import ToDo
from agil.models.User import User
from agil.models.Voie import Voie


chef = Blueprint('chef', __name__)


def login_required():
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()
            if not days_between(current_user.expiryCompte) or int(current_user.nbrAttempts) < 1 or int(current_user.etatCompte) < 1:
                ur = User.query.filter_by(idUser=current_user.idUser).filter(User.roleUser == 0).first()
                if ur:
                    try:
                        ur.etatCompte = 0
                        ur.nbrAttempts = 0
                        db.session.commit()
                        flash('Le compte est verrouillé. Veuillez contacter l\'administrateur', 'error')
                    except SQLAlchemyError:
                        db.session.rollback()
                return current_app.login_manager.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


@chef.route('/chef/reset', methods=['GET', 'POST'])
@login_required()
def resetLogin():
    form = ResetLoginForm()
    if current_user.is_authenticated:
        if not bcrypt.check_password_hash(current_user.passUser, "0000"):
            return redirect(url_for('chef.index'))
        else:
            if form.validate_on_submit():
                user = User.query.filter(or_(User.cinUser == current_user.cinUser, User.codeUser == current_user.codeUser)).first_or_404()
                if user:
                    try:
                        hashed_password = bcrypt.generate_password_hash(form.Password.data).decode('utf-8')
                        user.passUser = hashed_password
                        db.session.commit()
                        flash('Votre mot de passe a été mis à jour avec succès', 'success')
                        return redirect(url_for('chef.index'))
                    except SQLAlchemyError:
                        db.session.rollback()
                        flash("Erreur inconnue due au serveur", 'error')

                    return redirect(url_for('chef.resetLogin'))

    return render_template('./chef/reset/reset.html', form=form, title="Reset Password")


@chef.route('/chef/generate', methods=['GET', 'POST'])
@login_required()
def generatePass():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        if request.method == 'POST':
            Str = generate()
            return json.dumps({"Password": Str}).encode('utf8')
    return ''


@chef.route('/chef/', methods=['GET', 'POST'])
@chef.route('/chef/index', methods=['GET', 'POST'])
@login_required()
def index():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    form = ToDoForm()
    formUpd = ToDoFormUpd()
    return render_template('./chef/index.html', form=form, formUpd=formUpd)


@chef.route('/chef/CiterneFetch', methods=['GET', 'POST'])
@login_required()
def indexCitFetch():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        recordObject = [{"Id": 0, "NomCit": "-- sélectionnez une option --"}]
        records = Citerne.query.filter(Citerne.idStation == current_user.idStation).all()
        if records:
            for record in records:
                recordObject.append({
                    "Id": record.idCiterne,
                    "MinVal": record.Min_Val_Citerne,
                    "Volume": record.VolumeCiterne,
                    "ValAct": record.Val_Act_Citerne,
                    "NomCit": "{} : {}".format(record.NomCiterne, record.Carburant.NomCarburant)
                })

        return json.dumps(recordObject).encode('utf8'), 200


@chef.route('/chef/CiterneInfo', methods=['GET', 'POST'])
@login_required()
def indexCitInfo():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        recordObject = []
        if request.method == 'POST':
            id = FormatString(request.json['id'])
            record = Citerne.query.filter(Citerne.idStation == current_user.idStation, Citerne.idCiterne == id).first()
            if record:
                recordObject.append({
                    "Id": record.idCiterne,
                    "Volume": record.VolumeCiterne,
                    "ValAct": record.Val_Act_Citerne
                })
            else:
                recordObject.append({
                    "Volume": 1,
                    "ValAct": 0
                })

        return json.dumps(recordObject).encode('utf8'), 200


@chef.route('/chef/dateDepense', methods=['GET', 'POST'])
@login_required()
def dateDepense():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        recordObject = []
        if request.method == 'POST':
            startDate = request.form["startDate"]
            endDate = request.form["endDate"]
            if (startDate is None) or (endDate is None):
                return jsonify(data={"Msg": "Erreur"}), 201
            else:
                startDate = FormatString(startDate)
                endDate = FormatString(endDate)

                Str = "SELECT DATE_FORMAT(dateExpenses,'%Y-%m-%d') AS Date ,dateExpenses,sum(amExpenses) As Prix " \
                      "FROM expenses join station using(idStation) " \
                      "WHERE idStation = {} AND dateExpenses  BETWEEN '{}' AND '{}' " \
                      "GROUP BY Date ,YEAR(Date) ORDER BY dateExpenses".format(current_user.idStation,startDate,endDate)

                result = db.session.execute(Str)
                if result:
                    for record in result:
                        recordObject.append({
                            "Date": str(record["Date"]),
                            "Prix": float(record["Prix"])
                        })

        return json.dumps(recordObject).encode('utf8'), 200


@chef.route('/chef/toDo/Fetch', methods=['GET', 'POST'])
@login_required()
def fetchToDo():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        if request.method == 'POST':
            records = ToDo.query.filter(ToDo.idUser == current_user.get_id())
            date = FormatString(request.json['date'])
            if date == "":
                records = records.filter(and_(ToDo.dateListUser >= currentDate(), ToDo.dateListUser <= addDay())).order_by(desc(ToDo.dateListUser), desc(ToDo.idListUser)).all()
            else:
                if verifDate(date):
                    records = records.filter(ToDo.dateListUser == date).order_by(desc(ToDo.idListUser)).all()
                else:
                    return jsonify(data={"Msg": "Erreur Date Format"}), 201
            return json.dumps(get_to_do_data(records)).encode('utf8'), 200

        return ''


@chef.route('/chef/toDo/FetchSingle', methods=['GET', 'POST'])
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


@chef.route('/chef/toDo/Add', methods=['GET', 'POST'])
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


@chef.route('/chef/toDo/MarkAsDone', methods=['GET', 'POST'])
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


@chef.route('/chef/toDo/MarkAsUndone', methods=['GET', 'POST'])
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


@chef.route('/chef/toDo/Restore', methods=['GET', 'POST'])
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


@chef.route('/chef/toDo/UpdateToDO', methods=['GET', 'POST'])
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


@chef.route('/chef/toDo/PreDelete', methods=['GET', 'POST'])
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


@chef.route('/chef/toDo/Delete', methods=['GET', 'POST'])
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


@chef.route('/chef/dateCarburant', methods=['GET', 'POST'])
@login_required()
def dateCarburant():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        recordObject = []
        if request.method == 'POST':
            startDate = request.form["startDate"]
            endDate = request.form["endDate"]
            if (startDate is None) or (endDate is None):
                return jsonify(data={"Msg": "Erreur"}), 201
            else:
                startDate = FormatString(startDate)
                endDate = FormatString(endDate)

                Str = "SELECT DATE_FORMAT(DateCarb,'%Y-%m-%d') AS Date ,DateCarb,sum(prixLitre*(indiceFin-indiceDeb)) As Prix " \
                      "FROM recettecarburant join station using(idStation) " \
                      "WHERE idStation = {} AND DateCarb  BETWEEN '{}' AND '{}' " \
                      "GROUP BY Date ,YEAR(Date) ORDER BY DateCarb".format(current_user.idStation, startDate, endDate)

                result = db.session.execute(Str)
                if result:
                    for record in result:
                        recordObject.append({
                            "Date": str(record["Date"]),
                            "Prix": float(record["Prix"])
                        })

        return json.dumps(recordObject).encode('utf8'), 200


@chef.route('/chef/dateLavage', methods=['GET', 'POST'])
@login_required()
def dateLavage():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        recordObject = []
        if request.method == 'POST':
            startDate = request.form["startDate"]
            endDate = request.form["endDate"]
            if (startDate is None) or (endDate is None):
                return jsonify(data={"Msg": "Erreur"}), 201
            else:
                startDate = FormatString(startDate)
                endDate = FormatString(endDate)

                Str = "SELECT DATE_FORMAT(DateLavage,'%Y-%m-%d') AS Date ,DateLavage,sum(PrixLavage) As Prix " \
                      "FROM recettelavage join station using(idStation) " \
                      "WHERE idStation = {} AND DateLavage  BETWEEN '{}' AND '{}' " \
                      "GROUP BY Date ,YEAR(Date) ORDER BY DateLavage".format(current_user.idStation, startDate, endDate)

                result = db.session.execute(Str)
                if result:
                    for record in result:
                        recordObject.append({
                            "Date": str(record["Date"]),
                            "Prix": float(record["Prix"])
                        })

        return json.dumps(recordObject).encode('utf8'), 200


"""" Recette Lavage """


@chef.route('/chef/recette/lavage/dataLavage', methods=['GET', 'POST'])
@login_required()
def dataLavage():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        now = currentDate()
        form = RecetteFilter()
        if form.validate_on_submit():
            data = RecetteLavage.query.filter(RecetteLavage.idStation == current_user.idStation)
            Dat = FormatString(form.Dat.data)
            Grp = int(form.Grp.data)

            if Grp == 0:
                if Dat == "":
                    data = data.filter(RecetteLavage.DateLavage == now)
                else:
                    data = data.filter(RecetteLavage.DateLavage >= Dat)
            else:
                if Dat == "":
                    data = data.filter(RecetteLavage.idGroupe == Grp, RecetteLavage.DateLavage == now)
                else:
                    data = data.filter(RecetteLavage.idGroupe == Grp, RecetteLavage.DateLavage >= Dat)

            data = data.order_by(desc(RecetteLavage.DateLavage),RecetteLavage.idGroupe,desc(RecetteLavage.idRecetteLavage)).all()
            return json.dumps(FilterDataLavage(data)).encode('utf8'), 200

        return jsonify(data=form.errors), 201


@chef.route('/chef/recette/lavage/voiture', methods=['GET', 'POST'])
@login_required()
def dataVoiture():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        form = CarFilter()
        if form.validate_on_submit():
            Mat = FormatString(form.Mat.data)
            Str = RecetteLavage.query.filter_by(MatriculeVoiture=Mat).filter(RecetteLavage.idStation == current_user.idStation).order_by(desc(RecetteLavage.DateLavage),RecetteLavage.idGroupe,desc(RecetteLavage.idRecetteLavage)).all()
            return json.dumps(FilterDataLavageVoiture(Str)).encode('utf8'), 200

        return jsonify(data=form.errors), 201


@chef.route('/chef/lavage/recette/voiture/imprimer', methods=['GET', 'POST'])
@login_required()
def imprimer_voiture():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    form = CarFilter()
    return render_template('./chef/recette/lavage/voiture.html', title="Imprimer Voiture", form=form)


@chef.route('/chef/lavage/recette/imprimer', methods=['GET', 'POST'])
@login_required()
def imprimer_recette_lavage():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    form = RecetteFilter()
    form.fill_choice_groupe()
    return render_template('./chef/recette/lavage/imprimer.html', title="Imprimer Recette Lavage", form=form)


@chef.route('/chef/lavage/recette/', methods=['GET', 'POST'])
@chef.route('/chef/lavage/recette/consulter', methods=['GET', 'POST'])
@login_required()
def consulter_recette_lavage():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    form = DateRecette()
    records = RecetteLavage.query.filter(RecetteLavage.idStation == current_user.idStation, RecetteLavage.DateLavage == currentDate())

    if form.validate_on_submit():
        Str = FormatString(form.Date.data)
        if Str:
            records = RecetteLavage.query.filter(RecetteLavage.idStation == current_user.idStation, RecetteLavage.DateLavage >= Str)

    elif request.method == 'GET':
        Str = request.args.get('Date')
        if Str:
            records = RecetteLavage.query.filter(RecetteLavage.idStation == current_user.idStation, RecetteLavage.DateLavage == FormatString(Str))

    records = records.order_by(desc(RecetteLavage.DateLavage),desc(RecetteLavage.idGroupe),desc(RecetteLavage.idRecetteLavage)).all()
    return render_template('./chef/recette/lavage/consulter.html', form=form, title="Consulter Recette Lavage", data=get_recette_lavage_data(records))


@chef.route('/chef/lavage/recette/ajouter', methods=['GET', 'POST'])
@login_required()
def ajouter_recette_lavage():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    form = Recette()
    form.fill_choice_type_lavage()
    form.fill_choice_groupe()
    if form.validate_on_submit():
        try:
            Rlavage = RecetteLavage(MatriculeVoiture=form.Matricule.data, Kilometrage=form.kilometrage.data,HeureDebut=form.Debut.data,DateLavage=FormatString(form.Date.data),
                                    HeureFin=form.Fin.data, PrixLavage=form.Prix.data, idLavage=form.Type.data,idGroupe=form.Groupe.data, idStation=current_user.idStation)
            db.session.add(Rlavage)
            db.session.commit()
        except SQLAlchemyError:
            flash("Erreur inconnue due au serveur", 'error')
            db.session.rollback()
        else:
            flash("Recette Lavage a été ajoutée avec succès", 'success')
        return redirect(url_for('chef.consulter_recette_lavage', Date=FormatString(form.Date.data), _external=True))

    return render_template('./chef/recette/lavage/ajouter.html', form=form, title="Ajouter Recette Lavage")


@chef.route('/chef/lavage/recette/<int:id>/modifier', methods=['GET', 'POST'])
@login_required()
def modifier_recette_lavage(id):
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    RLavage = RecetteLavage.query.filter_by(idRecetteLavage=id).filter(RecetteLavage.idStation == current_user.idStation).first_or_404()
    form = Recette()
    form.fill_choice_type_lavage()
    form.fill_choice_groupe()
    if form.validate_on_submit():
        try:
            get_field_recetteLavage(form, RLavage)
            db.session.commit()
        except SQLAlchemyError:
            flash("Erreur inconnue due au serveur", 'error')
            db.session.rollback()
            return redirect(url_for('chef.modifier_recette_lavage', id=RLavage.idRecetteLavage, _external=True))
        else:
            flash("Recette Lavage a été mise à jour avec succès", 'success')
        return redirect(url_for('chef.consulter_recette_lavage', Date=FormatString(form.Date.data), _external=True))
    elif request.method == 'GET':
        remplire_field_recetteLavage(form, RLavage)

    return render_template('./chef/recette/lavage/modifier.html', form=form, title="Modifier Recette Lavage")


@chef.route('/chef/lavage/recette/<int:id>/supprimer', methods=['GET', 'POST'])
@login_required()
def supprimer_recette_lavage(id):
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    RLavage = RecetteLavage.query.filter_by(idRecetteLavage=id).filter(RecetteLavage.idStation == current_user.idStation).first_or_404()
    try:
        db.session.delete(RLavage)
        db.session.commit()
    except SQLAlchemyError:
        flash("Erreur inconnue due au serveur", 'error')
        db.session.rollback()
    else:
        flash("Les données de la recette ont été supprimées avec succès", 'success')
    return redirect(url_for('chef.consulter_recette_lavage', Date=RLavage.DateLavage, _external=True))


"""" Recette Carburant """


@chef.route('/chef/carburant/recette/dataRecette', methods=['GET', 'POST'])
@login_required()
def dataRecette():
    recordObject = [{"id": 0, "name": '-- sélectionnez une option --'}]
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        if request.method == 'POST':
            user_id = request.form['id']
            user_id = FormatString(user_id)
            data = db.session.query(PompeCiterne) \
                .join(Citerne, Citerne.idCiterne == PompeCiterne.idCiterne) \
                .join(Pompe, Pompe.idPompe == PompeCiterne.idPompe) \
                .filter(Pompe.idPompe == user_id, Pompe.idStation == current_user.idStation, Citerne.idStation == current_user.idStation, Citerne.EtatCiterne == 1).all()
            if data:
                for record in data:
                    recordObject.append({
                        "id": record.Citerne.idCiterne,
                        "name": record.Citerne.NomCiterne
                    })

    return json.dumps(recordObject).encode('utf8')


@chef.route('/chef/recette/carburant/dataCarburant', methods=['GET', 'POST'])
@login_required()
def dataCarburant():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        now = currentDate()
        form = RecetteFilter()
        if form.validate_on_submit():
            data = RecetteCarburant.query.filter(RecetteCarburant.idStation == current_user.idStation)
            Dat = FormatString(form.Dat.data).strip()
            Grp = int(form.Grp.data)

            if Grp == 0:
                if Dat == "":
                    data = data.filter(RecetteCarburant.DateCarb == now)
                else:
                    data = data.filter(RecetteCarburant.DateCarb == Dat)
            else:
                if Dat == "":
                    data = data.filter(RecetteCarburant.idGroupe == Grp, RecetteCarburant.DateCarb == now)
                else:
                    data = data.filter(RecetteCarburant.idGroupe == Grp, RecetteCarburant.DateCarb == Dat)

            data = data.join(Voie).order_by(desc(RecetteCarburant.DateCarb),RecetteCarburant.idGroupe,RecetteCarburant.idPompe, Voie.nomVoie).all()
            return json.dumps(FilterDataCarburant(data),).encode('utf8'), 200

        return jsonify(data=form.errors), 201


@chef.route('/chef/carburant/recette/imprimer', methods=['GET', 'POST'])
@login_required()
def imprimer_recette_carburant():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    form = RecetteFilter()
    form.fill_choice_groupe()
    return render_template('./chef/recette/carburant/imprimer.html', title="Imprimer Recette Carburant", form=form)


@chef.route('/chef/carburant/recette', methods=['GET', 'POST'])
@chef.route('/chef/carburant/recette/consulter', methods=['GET', 'POST'])
@login_required()
def consulter_recette_carburant():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    records = RecetteCarburant.query.filter(RecetteCarburant.idStation == current_user.idStation, RecetteCarburant.DateCarb == currentDate()) \
        .join(Voie, Voie.idVoie == RecetteCarburant.idVoie)
    form = DateRecette()
    if form.validate_on_submit():
        Str = FormatString(form.Date.data)
        if Str:
            records = RecetteCarburant.query.filter(RecetteCarburant.idStation == current_user.idStation, RecetteCarburant.DateCarb >= Str) \
                .join(Voie, Voie.idVoie == RecetteCarburant.idVoie)

    elif request.method == 'GET':
        Str = request.args.get('Date')
        if Str:
            records = RecetteCarburant.query.filter(RecetteCarburant.idStation == current_user.idStation,RecetteCarburant.DateCarb == FormatString(Str)) \
                .join(Voie, Voie.idVoie == RecetteCarburant.idVoie)

    records = records.order_by(desc(RecetteCarburant.DateCarb),desc(RecetteCarburant.idGroupe),RecetteCarburant.idPompe, Voie.nomVoie).all()
    return render_template('./chef/recette/carburant/consulter.html', title="Recette Carburant", data=get_recette_carburant_data(records), form=form)


@chef.route('/chef/carburant/recette/ajouter', methods=['GET', 'POST'])
@login_required()
def ajouter_recette_carburant():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    form = RecetteCar()
    form.fill_choice_Pmp()
    form.fill_choice_groupe()
    form.fill_choice_Voie()
    if form.validate_on_submit():
        try:
            Price = form.Prix.data
            Cit = Citerne.query.filter_by(idCiterne=form.Cit.data).filter(Citerne.idStation == current_user.idStation).first_or_404()
            RCarb = RecetteCarburant(idPompe=form.Pmp.data, idCiterne=form.Cit.data, idVoie=form.Voie.data, idStation=current_user.idStation,
                                     idGroupe=form.Groupe.data, indiceDeb=form.IndDebut.data, indiceFin=form.IndFin.data,DateCarb=FormatString(form.Date.data))
            if Price == "":
                result = db.session.query(func.GetPrixCarburant(int(FormatString(str(form.Cit.data))))).all()
                if result:
                    for record in result:
                        Price = record[0]

            RCarb.prixLitre = Price
            val = float(form.IndFin.data) - float(form.IndDebut.data)
            Cit.Val_Act_Citerne -= val
            db.session.add(RCarb)
            Cit = Citerne.query.filter(Citerne.idCiterne == form.Cit.data,Citerne.idStation == current_user.idStation).first()
            if (float(Cit.VolumeCiterne) * float(Cit.Min_Val_Citerne))/100 >= float(Cit.Val_Act_Citerne):
                Com = Comment(comment_subject="Alerte Citerne {}".format(Cit.NomCiterne),comment_date=currentDateTime(),
                              comment_text="Votre attention s'il vous plaît, Volume actuelle Citerne {} : ({} Litres) Type Carburant : {} est égale à {} ".format(Cit.NomCiterne,Cit.VolumeCiterne,Cit.Carburant.NomCarburant,Cit.Val_Act_Citerne),idUser=current_user.idUser)
                db.session.add(Com)
            db.session.commit()
        except SQLAlchemyError:
            flash("Erreur inconnue due au serveur", 'error')
            db.session.rollback()
        else:
            flash("Recette Carburant a été ajoutée avec succès", 'success')
        return redirect(url_for('chef.consulter_recette_carburant',Date=FormatString(form.Date.data), _external=True))

    return render_template('./chef/recette/carburant/ajouter.html', form=form, title="Ajouter Recette Carburant")


@chef.route('/chef/carburant/recette/<int:id>/modifier', methods=['GET', 'POST'])
@login_required()
def modifier_recette_carburant(id):
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    RCarb = RecetteCarburant.query.filter_by(idRecetteCarburant=id).filter(RecetteCarburant.idStation == current_user.idStation).first_or_404()
    form = RecetteCar()
    form.fill_choice_Pmp()
    form.fill_choice_groupe()
    form.fill_choice_Voie()
    if form.validate_on_submit():
        Price = FormatString(str(form.Prix.data))
        if Price == "":
            result = db.session.query(func.GetPrixCarburant(int(FormatString(str(form.Cit.data))))).all()
            if result:
                for record in result:
                    Price = record[0]

        RCarb.prixLitre = Price
        try:
            Cit = Citerne.query.filter_by(idCiterne=RCarb.idCiterne).filter(Citerne.idStation == current_user.idStation).first_or_404()
            val = float(form.IndFin.data) - float(form.IndDebut.data)
            if Cit.Val_Act_Citerne < val:
                flash("C'est au-dessus du volume réel de Citerne", 'error')
                return redirect(url_for('chef.consulter_recette_carburant', Date=FormatString(form.Date.data), _external=True))

            Cit.Val_Act_Citerne += float(RCarb.indiceFin) - float(RCarb.indiceDeb)
            Cit = Citerne.query.filter_by(idCiterne=form.Cit.data).filter(Citerne.idStation == current_user.idStation).first_or_404()
            Cit.Val_Act_Citerne -= float(form.IndFin.data) - float(form.IndDebut.data)
            get_field_recetteCarb(form, RCarb)
            db.session.commit()
        except SQLAlchemyError:
            flash("Erreur inconnue due au serveur", 'error')
            db.session.rollback()
            return redirect(url_for('chef.consulter_recette_carburant', Date=RCarb.DateCarb, _external=True))

        else:
            flash("Recette Carburant a été mise à jour avec succès", 'success')
        return redirect(url_for('chef.consulter_recette_carburant', Date=FormatString(form.Date.data), _external=True))
    elif request.method == 'GET':
        remplire_field_recetteCarb(form, RCarb)
    return render_template('./chef/recette/carburant/modifier.html', form=form, title="Modifier Recette Carburant")


@chef.route('/chef/carburant/recette/<int:id>/supprimer', methods=['GET', 'POST'])
@login_required()
def supprimer_recette_carburant(id):
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    RCarb = RecetteCarburant.query.filter_by(idRecetteCarburant=id).filter(RecetteCarburant.idStation == current_user.idStation).first_or_404()
    try:
        Cit = Citerne.query.filter_by(idCiterne=RCarb.idCiterne).filter(Citerne.idStation == current_user.idStation).first_or_404()
        Cit.Val_Act_Citerne += float(RCarb.indiceFin) - float(RCarb.indiceDeb)
        db.session.delete(RCarb)
        db.session.commit()
    except SQLAlchemyError:
        flash("Erreur inconnue due au serveur", 'error')
        db.session.rollback()
    else:
        flash("Les données de recette ont été supprimées avec succès", 'success')
    return redirect(url_for('chef.consulter_recette_carburant', Date=RCarb.DateCarb, _external=True))


""" Employee """


@chef.route('/chef/employee/conge/record', methods=['GET', 'POST'])
@login_required()
def fetchCongeEmployee():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        if request.method == 'POST':
            idEmploye = request.form['id']
            startDate = request.form['startDate']
            endDate = request.form['endDate']
            if (startDate is None) or (endDate is None) or (idEmploye is None):
                return jsonify(data={"Msg": "Erreur"}), 201
            else:
                records = Conge.query.join(Employee, Employee.idEmp == Conge.idEmp) \
                    .join(Station, Station.idStation == Employee.idStation) \
                    .filter(Employee.idEmp == idEmploye,Employee.idStation == current_user.idStation) \
                    .filter(and_(Conge.DateDebConge >= startDate, Conge.DateDebConge <= endDate)) \
                    .order_by(desc(Conge.DateDebConge), desc(Conge.idConge)).all()
                return json.dumps(get_conge_employee_data(records)).encode('utf8'), 200

        return ''


@chef.route('/chef/employee/absence/record', methods=['GET', 'POST'])
@login_required()
def fetchAbsenceEmployee():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        if request.method == 'POST':
            idEmploye = request.form['id']
            startDate = request.form['startDate']
            endDate = request.form['endDate']
            if (startDate is None) or (endDate is None) or (idEmploye is None):
                return jsonify(data={"Msg": "Erreur"}), 201
            else:
                startDate = FormatString(startDate)
                endDate = FormatString(endDate)
                records = Absence.query.join(Employee, Employee.idEmp == Absence.idEmp) \
                    .join(Station, Station.idStation == Employee.idStation) \
                    .filter(Employee.idEmp == idEmploye,Employee.idStation == current_user.idStation) \
                    .filter(and_(Absence.DateAbsence >= startDate, Absence.DateAbsence <= endDate)) \
                    .order_by(desc(Absence.DateAbsence),desc(Absence.idAbsence)).all()
                return json.dumps(get_absence_employee_data(records)).encode('utf8'), 200

        return ''


@chef.route('/chef/employee/', methods=['GET', 'POST'])
@chef.route('/chef/employee/consulter', methods=['GET', 'POST'])
@login_required()
def consulter_employee_station():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    emp = Employee.query.filter(Employee.idStation == current_user.idStation)
    form = EmployeeFilter()
    form.fill_choice_groupe()
    if form.validate_on_submit():
        Str = FormatString(str(form.Groupe.data))
        if Str:
            emp = emp.filter(Employee.idGroupe == Str)

    elif request.method == 'GET':
        Str = request.args.get('idGroupe')
        if Str:
            emp = emp.filter(Employee.idGroupe == FormatString(str(Str)))

    emp = emp.order_by(Employee.idGroupe,desc(Employee.idEmp)).all()
    return render_template('./chef/employee/consulter.html', title="Consulter les Employés",form=form, data=get_empStation_data(emp))


@chef.route('/chef/employee/consulter/<int:id>/', methods=['GET', 'POST'])
@login_required()
def consulter_one_employee_station(id):
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    records = Employee.query.filter_by(idEmp=id).filter(Employee.idStation == current_user.idStation).first_or_404()
    return render_template('./chef/employee/one.html',records=records, data=records.idEmp, title="Consulter Profil d'employé")


@chef.route('/chef/employee/ajouter', methods=['GET', 'POST'])
@login_required()
def ajouter_employee_station():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    form = EmpStation()
    form.fill_choice_role()
    form.fill_choice_groupe()
    if form.validate_on_submit():
        try:
            emp = Employee(codeEmp=FormatString(form.Code.data),cinEmp=FormatString(form.Cin.data),nomEmp=FormatString(form.Nom.data).capitalize(),
                           prenomEmp=FormatString(form.Prenom.data).capitalize(),telEmp=FormatString(form.Tel.data),idGroupe=form.Groupe.data,
                           idRole=form.Role.data,dateEmp=FormatString(form.Date.data),salEmp=form.Sal.data,idStation=current_user.idStation)
            db.session.add(emp)
            db.session.commit()
        except SQLAlchemyError:
            flash("Erreur inconnue due au serveur", 'error')
            db.session.rollback()
        else:
            flash("Employé a été ajouté avec succès", 'success')
        return redirect(url_for('chef.consulter_employee_station',idGroupe=form.Groupe.data, _external=True))

    return render_template('./chef/employee/ajouter.html',form=form, title="Ajouter un Employé")


@chef.route('/chef/employee/<int:id>/modifier', methods=['GET', 'POST'])
@login_required()
def modifier_employee_station(id):
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    emp = Employee.query.filter_by(idEmp=id).filter(Employee.idStation == current_user.idStation).first_or_404()
    form = UpdEmpStation()
    form.fill_choice_role()
    form.fill_choice_groupe()
    if form.validate_on_submit():
        try:
            othEmp = Employee(codeEmp=FormatString(form.Code.data), cinEmp=FormatString(form.Cin.data), nomEmp=FormatString(form.Nom.data).capitalize(),
                              prenomEmp=FormatString(form.Prenom.data).capitalize(), telEmp=FormatString(form.Tel.data), idGroupe=form.Groupe.data,
                              idRole=form.Role.data, dateEmp=FormatString(form.Date.data), salEmp=form.Sal.data, idStation=current_user.idStation)
            verifIdendityEmpStation(emp, othEmp)
            get_field_employee(form, emp)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            flash('Erreur inconnue due au serveur', 'error')
        except ValidationError as e:
            flash(str(e), 'error')
            return redirect(url_for('chef.modifier_employee_station', id=emp.idEmp, _external=True))
        else:
            flash("Employé a été mis à jour avec succès", 'success')
        return redirect(url_for('chef.consulter_employee_station', idGroupe=form.Groupe.data, _external=True))
    elif request.method == 'GET':
        remplire_field_employee(form, emp)

    return render_template('./chef/employee/modifier.html',form=form,title="Modifier un Employé")


@chef.route('/chef/employee/<int:id>/supprimer', methods=['GET', 'POST'])
@login_required()
def supprimer_employee_station(id):
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    emp = Employee.query.filter_by(idEmp=id).filter(Employee.idStation == current_user.idStation).first_or_404()
    try:
        db.session.delete(emp)
        db.session.commit()
    except SQLAlchemyError:
        flash("Erreur inconnue due au serveur", 'error')
        db.session.rollback()
    else:
        flash("L'employé a été supprimé avec succès", 'success')
    return redirect(url_for('chef.consulter_employee_station', Groupe=emp.idGroupe, _external=True))


""" Citerne """


@chef.route('/chef/citerne/', methods=['GET', 'POST'])
@chef.route('/chef/citerne/consulter', methods=['GET', 'POST'])
@login_required()
def consulter_citerne():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    Cit = Citerne.query.filter(Citerne.idStation == current_user.idStation).order_by(desc(Citerne.idCiterne),Citerne.idCarburant).all()
    return render_template('./chef/citerne/consulter.html', title="Consulter les Citernes", data=get_citerne_data(Cit))


@chef.route('/chef/citerne/consulter/<int:id>/', methods=['GET', 'POST'])
@login_required()
def consulter_one_citerne(id):
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    Cit = Citerne.query.filter_by(idCiterne=id).filter(Citerne.idStation == current_user.idStation).first_or_404()
    form = UpdCiternes()
    remplire_field_one_citerne(form, Cit)
    return render_template('./chef/citerne/one.html', form=form, title="Consulter une Citerne")


@chef.route('/chef/citerne/ajouter', methods=['GET', 'POST'])
@login_required()
def ajouter_citerne():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    form = Citernes()
    form.fill_choice_carburant()
    if form.validate_on_submit():
        try:
            Cit = Citerne(NomCiterne=form.Code.data, VolumeCiterne=form.Volume.data, Val_Act_Citerne=form.Volume.data,
                          Min_Val_Citerne=form.Min.data.replace(' %', ''), idCarburant=form.Car.data, idStation=current_user.idStation)
            db.session.add(Cit)
            db.session.commit()
        except SQLAlchemyError:
            flash("Erreur inconnue due au serveur", 'error')
            db.session.rollback()
        else:
            flash("Citerne a été ajouté avec succès", 'success')
        return redirect(url_for('chef.consulter_citerne'))

    return render_template('./chef/citerne/ajouter.html', form=form, title="Ajouter une Citerne")


@chef.route('/chef/citerne/<int:id>/modifier', methods=['GET', 'POST'])
@login_required()
def modifier_citerne(id):
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    Cit = Citerne.query.filter_by(idCiterne=id).filter(Citerne.idStation == current_user.idStation).first_or_404()
    form = UpdCiternes()
    if form.validate_on_submit():
        if Cit.NomCiterne != form.Code.data:
            emp = Citerne.query.filter(Citerne.NomCiterne == form.Code.data, Citerne.idStation == current_user.idStation).first()
            if emp:
                flash("Le code Citerne existe déjà, veuillez réessayer", 'error')
                return redirect(url_for('chef.modifier_citerne', id=Cit.idCiterne, _external=True))
        try:
            get_field_citerne(form, Cit)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            flash("Erreur inconnue due au serveur", 'error')
        else:
            flash("Citerne a été mis à jour avec succès", 'success')
        return redirect(url_for('chef.consulter_citerne'))

    elif request.method == 'GET':
        remplire_field_citerne(form, Cit)

    return render_template('./chef/citerne/modifier.html', form=form, title="Modifier une Citerne")


@chef.route('/chef/citerne/<int:id>/supprimer', methods=['GET', 'POST'])
@login_required()
def supprimer_citerne(id):
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    Cit = Citerne.query.filter_by(idCiterne=id).filter(Citerne.idStation == current_user.idStation).first_or_404()
    try:
        db.session.delete(Cit)
        db.session.commit()
    except SQLAlchemyError:
        flash("Ce Citerne a déjà une liaison avec une Pompe", 'error')
        db.session.rollback()
    else:
        flash("Citerne a été supprimé avec succès", 'success')
    return redirect(url_for('chef.consulter_citerne'))


""" Pompe """


@chef.route('/chef/pompe/data', methods=['GET', 'POST'])
@login_required()
def dataPompe():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        recordObject = []
        if request.method == 'POST':
            user_id = request.form['id']
            user_id = FormatString(user_id)
            data = Citerne.query.filter_by(idCiterne=user_id, idStation=current_user.idStation).all()
            if not data:
                recordObject.append({"id": 0, "name": '-- sélectionnez une option --'})
            else:
                for record in data:
                    recordObject.append({
                        "id": record.idCarburant,
                        "name": record.Carburant.NomCarburant
                    })

        return json.dumps(recordObject).encode('utf8'), 200


@chef.route('/chef/pompe/', methods=['GET', 'POST'])
@chef.route('/chef/pompe/consulter', methods=['GET', 'POST'])
@login_required()
def consulter_pompe():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    Pmp = Pompe.query.filter(Pompe.idStation == current_user.idStation).order_by(desc(Pompe.idPompe)).all()
    return render_template('./chef/pompe/consulter.html', title="Consulter les Pompes", data=get_pompe_data(Pmp))


@chef.route('/chef/pompe/ajouter', methods=['GET', 'POST'])
@login_required()
def ajouter_pompe():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    form = Pompes()
    if form.validate_on_submit():
        try:
            Pmp = Pompe(NomPompe=FormatString(form.Code.data), idStation=current_user.idStation)
            db.session.add(Pmp)
            db.session.commit()
        except SQLAlchemyError:
            flash("Erreur inconnue due au serveur", 'error')
            db.session.rollback()
        else:
            flash("Pompe a été ajoutée avec succès", 'success')
        return redirect(url_for('chef.consulter_pompe'))

    return render_template('./chef/pompe/ajouter.html', form=form, title="Ajouter une Pompe")


@chef.route('/chef/pompe/<int:id>/modifier', methods=['GET', 'POST'])
@login_required()
def modifier_pompe(id):
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    Pmp = Pompe.query.filter_by(idPompe=id).filter(Pompe.idStation == current_user.idStation).first_or_404()
    form = UpdPompes()
    if form.validate_on_submit():
        if Pmp.NomPompe != form.Code.data:
            emp = Pompe.query.filter(Pompe.NomPompe == FormatString(form.Code.data), Pompe.idStation == current_user.idStation).first()
            if emp:
                flash("Le code Pompe existe déjà, veuillez réessayer", 'error')
                return redirect(url_for('chef.modifier_pompe', id=Pmp.idPompe, _external=True))
        try:
            get_field_pompe(form, Pmp)
            db.session.commit()
        except SQLAlchemyError:
            flash("Erreur inconnue due au serveur", 'error')
            db.session.rollback()
        else:
            flash("Data Pompe a été mis à jour avec succès", 'success')
        return redirect(url_for('chef.consulter_pompe'))
    elif request.method == 'GET':
        remplire_field_pompe(form, Pmp)
    return render_template('./chef/pompe/modifier.html', form=form, title="Modifier une Pompe")


@chef.route('/chef/pompe/<int:id>/supprimer', methods=['GET', 'POST'])
@login_required()
def supprimer_pompe(id):
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    Pmp = Pompe.query.filter_by(idPompe=id).filter(Pompe.idStation == current_user.idStation).first_or_404()
    try:
        db.session.delete(Pmp)
        db.session.commit()
    except SQLAlchemyError:
        flash("Erreur inconnue due au serveur", 'error')
        db.session.rollback()
    else:
        flash("Pompe a bien été supprimée", 'success')
    return redirect(url_for('chef.consulter_pompe'))


""" Pompe Citerne """


@chef.route('/chef/pompeciterne/', methods=['GET', 'POST'])
@chef.route('/chef/pompeciterne/consulter', methods=['GET', 'POST'])
@login_required()
def consulter_pompe_citerne():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    PmpCit = db.session.query(PompeCiterne) \
        .join(Citerne, Citerne.idCiterne == PompeCiterne.idCiterne) \
        .join(Pompe, Pompe.idPompe == PompeCiterne.idPompe) \
        .filter(Pompe.idStation == current_user.idStation, Citerne.idStation == current_user.idStation) \
        .order_by(PompeCiterne.idCiterne,PompeCiterne.idPompe).all()
    return render_template('./chef/pompeCiterne/consulter.html', title="Consulter les Liasons", data=get_pompe_citerne_data(PmpCit))


@chef.route('/chef/pompeciterne/ajouter', methods=['GET', 'POST'])
@login_required()
def ajouter_pompe_citerne():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    form = PompeCiternes()
    form.fill_choice_Code()
    form.fill_choice_Cit()
    if form.validate_on_submit():
        try:
            Pmp = PompeCiterne(idPompe=form.Code.data, idCiterne=form.Cit.data)
            db.session.add(Pmp)
            db.session.commit()
        except SQLAlchemyError:
            flash("Erreur inconnue due au serveur", 'error')
            db.session.rollback()
        else:
            flash("La liaison a été ajoutée avec succès", 'success')
        return redirect(url_for('chef.consulter_pompe_citerne'))

    return render_template('./chef/pompeCiterne/ajouter.html', form=form, title="Ajouter Liason")


@chef.route('/chef/pompeciterne/<int:id>/modifier', methods=['GET', 'POST'])
@login_required()
def modifier_pompe_citerne(id):
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    Pmp = db.session.query(PompeCiterne).filter_by(id_citerne_has_pompe=id) \
        .join(Citerne, Citerne.idCiterne == PompeCiterne.idCiterne) \
        .join(Pompe, Pompe.idPompe == PompeCiterne.idPompe) \
        .filter(Pompe.idStation == current_user.idStation, Citerne.idStation == current_user.idStation).first_or_404()
    form = UpdPompeCiternes()
    form.fill_choice_Code()
    form.fill_choice_Cit()
    if form.validate_on_submit():

        if (Pmp.idCiterne != form.Cit.data) or (Pmp.idPompe != form.Code.data):
            emp = db.session.query(PompeCiterne) \
                .join(Citerne, Citerne.idCiterne == PompeCiterne.idCiterne) \
                .join(Pompe, Pompe.idPompe == PompeCiterne.idPompe) \
                .filter(Citerne.idCiterne == form.Cit.data, Pompe.idPompe == form.Code.data,
                        Citerne.idStation == current_user.idStation, Pompe.idStation == current_user.idStation).first()
            if emp:
                flash("Liaison Pompe Citerne existe déjà, veuillez réessayer", 'error')
                return redirect(url_for('chef.modifier_pompe_citerne', id=Pmp.id_citerne_has_pompe, _external=True))

        try:
            get_field_pompe_citerne(form, Pmp)
            db.session.commit()
        except SQLAlchemyError:
            flash("Erreur inconnue due au serveur", 'error')
            db.session.rollback()
        else:
            flash("La liaison a été mise à jour avec succès", 'success')
        return redirect(url_for('chef.consulter_pompe_citerne'))
    elif request.method == 'GET':
        remplire_field_pompe_citerne(form, Pmp)
    return render_template('./chef/pompeCiterne/modifier.html', form=form, title="Modifier Liason")


@chef.route('/chef/pompeciterne/<int:id>/supprimer', methods=['GET', 'POST'])
@login_required()
def supprimer_pompe_citerne(id):
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    PmpCit = db.session.query(PompeCiterne).filter_by(id_citerne_has_pompe=id).join(Citerne).join(Pompe).filter(Pompe.idStation == current_user.idStation, Citerne.idStation == current_user.idStation).first_or_404()
    try:
        db.session.delete(PmpCit)
        db.session.commit()
    except SQLAlchemyError:
        flash("Erreur inconnue due au serveur", 'error')
        db.session.rollback()
    else:
        flash("La liaison a été supprimée avec succès", 'success')
    return redirect(url_for('chef.consulter_pompe_citerne'))


""" Liste Expenses """


@chef.route('/chef/expenses/imprimer/list', methods=['GET', 'POST'])
@login_required()
def dataExpenses():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        now = currentDate()
        form = ExpenseFilter()
        if form.validate_on_submit():
            data = Expenses.query.filter(Expenses.idStation == current_user.idStation)
            Dat = FormatString(form.Dat.data)
            if Dat == "":
                data = data.filter(Expenses.dateExpenses == now)
            else:
                data = data.filter(Expenses.dateExpenses >= Dat)

            data = data.order_by(desc(Expenses.dateExpenses),desc(Expenses.idExpenses)).all()
            return json.dumps(FilterDataExpenses(data)).encode('utf8'), 200

        return jsonify(data=form.errors), 201


@chef.route('/chef/expenses/imprimer', methods=['GET', 'POST'])
@login_required()
def imprimer_expenses():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    form = ExpenseFilter()
    return render_template('./chef/expenses/imprimer.html',form=form, title="Imprimer la liste du dépenses")


@chef.route('/chef/expenses/', methods=['GET', 'POST'])
@chef.route('/chef/expenses/consulter', methods=['GET', 'POST'])
@login_required()
def consulter_expenses():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    records = Expenses.query.filter(Expenses.idStation == current_user.idStation,Expenses.dateExpenses == currentDate())
    form = DateRecette()
    if form.validate_on_submit():
        Str = FormatString(form.Date.data)
        if Str:
            records = Expenses.query.filter(Expenses.idStation == current_user.idStation, Expenses.dateExpenses >= Str)

    elif request.method == 'GET':
        Str = request.args.get('Date')
        if Str:
            records = Expenses.query.filter(Expenses.idStation == current_user.idStation, Expenses.dateExpenses == FormatString(Str))
    records = records.order_by(desc(Expenses.dateExpenses), desc(Expenses.idExpenses)).all()
    return render_template('./chef/expenses/consulter.html', title="Consulter la liste du dépenses",form=form, data=get_expenses_data(records))


@chef.route('/chef/expenses/ajouter', methods=['GET', 'POST'])
@login_required()
def ajouter_expenses():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    form = ExpensesForm()
    if form.validate_on_submit():
        try:
            Exp = Expenses(dateExpenses=form.Date.data, amExpenses=form.Mont.data, catExpenses=FormatString(form.Cat.data), descExpenses=FormatString(form.Desc.data), idStation=current_user.idStation)
            db.session.add(Exp)
            db.session.commit()
        except SQLAlchemyError:
            flash("Erreur inconnue due au serveur", 'error')
            db.session.rollback()
        else:
            flash("Cela a été ajouté avec succès à la liste", 'success')
        return redirect(url_for('chef.consulter_expenses', Date=FormatString(form.Date.data), _external=True))

    return render_template('./chef/expenses/ajouter.html', form=form, title="Ajouter à la liste du dépense")


@chef.route('/chef/expenses/<int:id>/modifier', methods=['GET', 'POST'])
@login_required()
def modifier_expenses(id):
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    Exp = Expenses.query.filter_by(idExpenses=id).filter(Expenses.idStation == current_user.idStation).first_or_404()
    form = ExpensesForm()
    if form.validate_on_submit():
        try:
            get_field_expenses(form,Exp)
            db.session.commit()
        except SQLAlchemyError:
            flash("Erreur inconnue due au serveur", 'error')
            db.session.rollback()
            return redirect(url_for('chef.modifier_expenses', id=Exp.idExpenses, _external=True))
        else:
            flash("Cet element a été mise à jour avec succès", 'success')
        return redirect(url_for('chef.consulter_expenses', Date=FormatString(form.Date.data), _external=True))
    elif request.method == 'GET':
        remplire_field_expenses(form,Exp)

    return render_template('./chef/expenses/modifier.html',form=form, title="Modifier la liste du déponses")


@chef.route('/chef/expenses/<int:id>/supprimer', methods=['GET', 'POST'])
@login_required()
def supprimer_expenses(id):
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    Exp = Expenses.query.filter_by(idExpenses=id).filter(Expenses.idStation == current_user.idStation).first_or_404()
    try:
        db.session.delete(Exp)
        db.session.commit()
    except SQLAlchemyError:
        flash("Erreur inconnue due au serveur", 'error')
        db.session.rollback()
    else:
        flash("Cela a été supprimé avec succès de la liste", 'success')
    return redirect(url_for('chef.consulter_expenses',Date=Exp.dateExpenses, _external=True))


""" Absence """


@chef.route('/chef/absence/AddEmp', methods=['GET', 'POST'])
@login_required()
def addEmpAbsence():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        form = AbsenceForm()
        if form.validate_on_submit():
            try:
                do = Employee.query.filter(or_(Employee.codeEmp == FormatString(form.Code.data), Employee.cinEmp == FormatString(form.Code.data)),Employee.idStation == current_user.idStation).first()
                abc = Absence(DateAbsence=form.Date.data, DescAbsence=FormatString(form.Desc.data), idEmp=do.idEmp, idStation=current_user.idStation,idGroupe=do.Groupe.idGroupe)
                db.session.add(abc)
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                return jsonify(data={"Msg": "Erreur inconnue due au serveur"}), 202
            else:
                flash("L'absence a été ajoutée avec succès","success")
                return jsonify(data={"Msg": "L'absence a été ajoutée avec succès"}), 200

        return jsonify(data=form.errors), 201


@chef.route('/chef/FetchEmp', methods=['GET', 'POST'])
@login_required()
def fetchEmp():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        if request.method == 'POST':
            recordObject = []
            date = FormatString(request.form['id']).strip()
            if date == "" or date is None:
                return jsonify(data={"Msg": "Erreur Code Employée"}), 201
            else:
                records = Employee.query.filter(or_(Employee.codeEmp == date, Employee.cinEmp == date)).filter(Employee.idStation == current_user.idStation).first()
                if records:
                    recordObject.append({
                        "Nom": records.nomEmp,
                        "Prenom": records.prenomEmp,
                        "Groupe": records.Groupe.NomGroupe
                    })
                    return json.dumps(recordObject).encode('utf8'), 200
                else:
                    return jsonify(data={"Msg": "Erreur Code Employée"}), 201

        return ''


@chef.route('/chef/absence/', methods=['GET', 'POST'])
@chef.route('/chef/absence/consulter', methods=['GET', 'POST'])
@login_required()
def consulter_absence():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    form = DateRecette()
    records = Absence.query \
        .join(Employee, Employee.idEmp == Absence.idEmp) \
        .join(Station, Station.idStation == Employee.idStation) \
        .filter(Absence.idStation == current_user.idStation, Absence.DateAbsence == currentDate())

    if form.validate_on_submit():
        Str = FormatString(form.Date.data)
        if Str:
            records = Absence.query \
                .join(Employee, Employee.idEmp == Absence.idEmp) \
                .join(Station, Station.idStation == Employee.idStation) \
                .filter(Absence.idStation == current_user.idStation, Absence.DateAbsence >= Str)

    elif request.method == 'GET':
        Str = request.args.get('Date')
        if Str:
            records = Absence.query \
                .join(Employee, Employee.idEmp == Absence.idEmp) \
                .join(Station, Station.idStation == Employee.idStation) \
                .filter(Absence.idStation == current_user.idStation, Absence.DateAbsence == FormatString(Str))

    records = records.order_by(desc(Absence.DateAbsence),desc(Absence.idGroupe),desc(Absence.idAbsence)).all()

    return render_template('./chef/absence/consulter.html', form=form, data=get_absence_data(records), title="Consulter la liste d'absence")


@chef.route('/chef/absence/ajouter', methods=['GET', 'POST'])
@login_required()
def ajouter_absence():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    form = AbsenceForm()
    return render_template('./chef/absence/ajouter.html',form=form, title="Ajouter à la liste d'absence")


@chef.route('/chef/absence/<int:id>/modifier', methods=['GET', 'POST'])
@login_required()
def modifier_absence(id):
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    Abc = Absence.query.filter_by(idAbsence=id) \
        .join(Employee, Employee.idEmp == Absence.idEmp) \
        .join(Station, Station.idStation == Employee.idStation) \
        .filter(Employee.idStation == current_user.idStation, Absence.idStation == current_user.idStation).first_or_404()
    form = UpdAbsenceForm()
    if form.validate_on_submit():
        try:
            Emp = Absence.query.join(Employee, Employee.idEmp == Absence.idEmp) \
                .join(Station, Station.idStation == Employee.idStation) \
                .filter(Absence.DateAbsence == form.Date.data) \
                .filter(Employee.idStation == current_user.idStation)\
                .filter(or_(Employee.codeEmp == FormatString(form.Code.data), Employee.cinEmp == FormatString(form.Code.data)))\
                .first_or_404()
            if Emp:
                if Emp.Employee.codeEmp == Abc.Employee.codeEmp:
                    if Emp.DateAbsence != Abc.DateAbsence:
                        Nbr = Absence.query.join(Employee, Employee.idEmp == Absence.idEmp) \
                            .join(Station, Station.idStation == Employee.idStation) \
                            .filter(Employee.idStation == current_user.idStation, Employee.idEmp == Emp.Employee.idEmp,Absence.DateAbsence == Emp.DateAbsence).count()
                        if Nbr > 0:
                            raise ValidationError("Cet employé existe déjà dans la liste, veuillez réessayer")
                else:
                    Nbr = Absence.query.join(Employee, Employee.idEmp == Absence.idEmp) \
                        .join(Station, Station.idStation == Employee.idStation) \
                        .filter(Employee.idStation == current_user.idStation, Absence.DateAbsence == Emp.DateAbsence) \
                        .filter(or_(Employee.codeEmp == Emp.Employee.codeEmp, Employee.cinEmp == Emp.Employee.codeEmp)) \
                        .count()
                    if Nbr > 0:
                        raise ValidationError("Cet employé existe déjà dans la liste, veuillez réessayer")
            else:
                Emp = Employee.query.filter(or_(Employee.codeEmp == FormatString(form.Code.data), Employee.cinEmp == FormatString(form.Code.data)),Employee.idStation == current_user.idStation).first()
            Abc.idEmp = Emp.idEmp
            get_field_absence(form, Abc)
            db.session.commit()
        except SQLAlchemyError:
            flash("Erreur inconnue due au serveur", 'error')
            db.session.rollback()
            return redirect(url_for('chef.modifier_absence', id=Abc.idAbsence, _external=True))
        except ValidationError as e:
            flash(str(e), 'error')
            return redirect(url_for('chef.modifier_absence', id=Abc.idAbsence, _external=True))
        else:
            flash("L'absence a été mise à jour avec succès", 'success')
        return redirect(url_for('chef.consulter_absence', Date=FormatString(form.Date.data), _external=True))
    elif request.method == 'GET':
        remplire_field_absence(form, Abc)

    return render_template('./chef/absence/modifier.html', form=form, title="Modifier la liste d'absences ")


@chef.route('/chef/absence/<int:id>/supprimer', methods=['GET', 'POST'])
@login_required()
def supprimer_absence(id):
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    Abc = Absence.query.filter_by(idAbsence=id)\
        .join(Employee, Employee.idEmp == Absence.idEmp)\
        .join(Station, Station.idStation == Employee.idStation)\
        .filter(Employee.idStation == current_user.idStation,Absence.idStation == current_user.idStation).first_or_404()
    try:
        db.session.delete(Abc)
        db.session.commit()
    except SQLAlchemyError:
        flash("Erreur inconnue due au serveur", 'error')
        db.session.rollback()
    else:
        flash("Cela a été supprimé avec succès de la liste", 'success')
    return redirect(url_for('chef.consulter_absence', Date=Abc.DateAbsence, _external=True))


@chef.route('/chef/absence/imprimerListe/data', methods=['GET', 'POST'])
@login_required()
def dataAbsenceAll():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        now = currentDate()
        form = RecetteFilter()
        if form.validate_on_submit():
            data = Absence.query.join(Employee, Employee.idEmp == Absence.idEmp) \
                .join(Station, Station.idStation == Employee.idStation) \
                .filter(Absence.idStation == current_user.idStation)
            Dat = FormatString(form.Dat.data).strip()
            Grp = int(form.Grp.data)

            if Grp == 0:
                if Dat == "":
                    data = data.filter(Absence.DateAbsence == now)
                else:
                    data = data.filter(Absence.DateAbsence >= Dat)
            else:
                if Dat == "":
                    data = data.filter(Absence.idGroupe == Grp, Absence.DateAbsence == now)
                else:
                    data = data.filter(Absence.idGroupe == Grp, Absence.DateAbsence >= Dat)

            data = data.order_by(desc(Absence.DateAbsence),desc(Absence.idAbsence),Absence.idGroupe).all()
            return json.dumps(FilterDataAbsence(data)).encode('utf8'), 200

        return jsonify(data=form.errors), 201


@chef.route('/chef/absence/imprimerListe/data/employee', methods=['GET', 'POST'])
@login_required()
def dataAbsenceEmpAll():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        form = AbsenceFilter()
        if form.validate_on_submit():
            data = Absence.query.join(Employee, Employee.idEmp == Absence.idEmp) \
                .join(Station, Station.idStation == Employee.idStation) \
                .filter(or_(Employee.codeEmp == FormatString(form.Code.data), Employee.cinEmp == FormatString(form.Code.data)))\
                .order_by(desc(Absence.DateAbsence),desc(Absence.idAbsence),Absence.idGroupe).all()

            return json.dumps(FilterDataAbsenceEmployee(data)).encode('utf8'), 200

        return jsonify(data=form.errors), 201


@chef.route('/chef/absence/imprimer/liste', methods=['GET', 'POST'])
@login_required()
def imprimer_liste_absence():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    form = RecetteFilter()
    form.fill_choice_groupe()
    return render_template('./chef/absence/imprimer.html',form=form, title="Imprimer La liste d'absences")


@chef.route('/chef/absence/imprimer/employee', methods=['GET', 'POST'])
@login_required()
def imprimer_liste_absence_employee():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    form = AbsenceFilter()
    return render_template('./chef/absence/employee.html',form=form, title="Imprimer La liste d'absences Employé")


""" Congé """


@chef.route('/chef/conge/AddEmp', methods=['GET', 'POST'])
@login_required()
def addEmpConge():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        form = CongeForm()
        form.fill_choice_type()
        if form.validate_on_submit():
            try:
                do = Employee.query.filter(or_(Employee.codeEmp == FormatString(form.Code.data), Employee.cinEmp == FormatString(form.Code.data)),Employee.idStation == current_user.idStation).first_or_404()
                abc = Conge(DateDebConge=form.DatDeb.data,DateFinConge=form.DatFin.data,idTypeConge=form.Type.data,DescConge=FormatString(form.Desc.data), idEmp=do.idEmp, idStation=current_user.idStation,idGroupe=do.Groupe.idGroupe)
                db.session.add(abc)
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                return jsonify(data={"Msg": "Erreur inconnue due au serveur"}), 202
            else:
                flash("Le congé a été ajouté avec succès","success")
                return jsonify(data={"Msg": "Le congé a été ajouté avec succès"}), 200

        return jsonify(data=form.errors), 201


@chef.route('/chef/conge/', methods=['GET', 'POST'])
@chef.route('/chef/conge/consulter', methods=['GET', 'POST'])
@login_required()
def consulter_conge():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    records = Conge.query \
        .join(Employee, Employee.idEmp == Conge.idEmp) \
        .join(Station, Station.idStation == Employee.idStation) \
        .filter(Conge.idStation == current_user.idStation,Conge.DateDebConge <= addMonth())

    form = CongeFormFilter()
    if form.validate_on_submit():
        records = Conge.query \
            .join(Employee, Employee.idEmp == Conge.idEmp) \
            .join(Station, Station.idStation == Employee.idStation) \
            .filter(Conge.idStation == current_user.idStation)\
            .filter(and_(Conge.DateDebConge >= FormatString(form.DatDeb.data), Conge.DateDebConge <= FormatString(form.DatFin.data)))

    elif request.method == 'GET':
        Str = request.args.get('Date')
        if Str:
            records = Conge.query \
                .join(Employee, Employee.idEmp == Conge.idEmp) \
                .join(Station, Station.idStation == Employee.idStation) \
                .filter(Conge.idStation == current_user.idStation,and_(Conge.DateDebConge >= FormatString(Str), Conge.DateDebConge <= addMonth()))

    records = records.order_by(desc(Conge.DateDebConge),desc(Conge.idConge),desc(Conge.idGroupe)).all()
    return render_template('./chef/conge/consulter.html',data=get_conge_data(records),form=form,title="Consulter la liste du congé")


@chef.route('/chef/conge/ajouter', methods=['GET', 'POST'])
@login_required()
def ajouter_conge():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    form = CongeForm()
    form.fill_choice_type()
    return render_template('./chef/conge/ajouter.html',form=form, title="Ajouter à la liste du congé")


@chef.route('/chef/conge/<int:id>/modifier', methods=['GET', 'POST'])
@login_required()
def modifier_conge(id):
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    var = Conge.query.filter_by(idConge=id).join(Employee, Employee.idEmp == Conge.idEmp) \
        .join(Station, Station.idStation == Employee.idStation) \
        .filter(Conge.idStation == current_user.idStation, Employee.idStation == current_user.idStation) \
        .first_or_404()
    form = UpdCongeForm()
    form.fill_choice_type()
    if form.validate_on_submit():
        try:
            DatDeb = FormatString(form.DatDeb.data)
            DatFin = FormatString(form.DatFin.data)
            Code = FormatString(form.Code.data)
            Gp = Conge.query.join(Employee, Employee.idEmp == Conge.idEmp) \
                .join(Station, Station.idStation == Employee.idStation) \
                .filter(or_(Employee.codeEmp == Code, Employee.cinEmp == Code), Employee.idStation == current_user.idStation) \
                .filter(Conge.idStation == current_user.idStation, Conge.DateDebConge >= DatDeb).all()
            Test = True
            if var.Employee.codeEmp != Code:
                for record in Gp:
                    if ((days_calc(record.DateDebConge, DatDeb) >= 0 and days_calc(DatFin, record.DateFinConge) >= 0)
                            or (not ((days_calc(DatDeb, record.DateDebConge) > 0 and days_calc(DatFin, record.DateDebConge) >= 0)
                            or (days_calc(record.DateFinConge, DatDeb) > 0 and days_calc(record.DateFinConge, DatFin) > 0)))):
                        Test = False
                        if not Test:
                            raise ValidationError('L\'employé est en congé ! Veuillez saisir une autre date.')
            elif days_calc(var.DateDebConge,DatDeb) != 0 or days_calc(var.DateFinConge, DatFin) != 0:
                for record in Gp:
                    if ((days_calc(record.DateDebConge, DatDeb) >= 0 and days_calc(DatFin, record.DateFinConge) >= 0)
                            or (not ((days_calc(DatDeb, record.DateDebConge) > 0 and days_calc(DatFin, record.DateDebConge) >= 0)
                            or (days_calc(record.DateFinConge, DatDeb) > 0 and days_calc(record.DateFinConge, DatFin) > 0)))):
                        Test = False
                        if not Test:
                            raise ValidationError('L\'employé est en congé ! Veuillez saisir une autre date.')

            Emp = Employee.query.filter(or_(Employee.codeEmp == Code, Employee.cinEmp == Code),Employee.idStation == current_user.idStation).first_or_404()
            var.idEmp = Emp.idEmp
            get_field_conge(form, var)
            db.session.commit()
        except SQLAlchemyError:
            flash("Erreur inconnue due au serveur", 'error')
            db.session.rollback()
            return redirect(url_for('chef.modifier_conge', id=var.idConge, _external=True))
        except ValidationError as e:
            flash(str(e), 'error')
            return redirect(url_for('chef.modifier_conge', id=var.idConge, _external=True))
        else:
            flash("L'absence a été mise à jour avec succès", 'success')
        return redirect(url_for('chef.consulter_conge', Date=FormatString(form.DatDeb.data), _external=True))
    elif request.method == 'GET':
        remplire_field_conge(form, var)

    return render_template('./chef/conge/modifier.html',form=form, title="Modifier la liste du congé")


@chef.route('/chef/conge/<int:id>/supprimer', methods=['GET', 'POST'])
@login_required()
def supprimer_conge(id):
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    var = Conge.query.filter_by(idConge=id).join(Employee, Employee.idEmp == Conge.idEmp) \
        .join(Station, Station.idStation == Employee.idStation) \
        .filter(Conge.idStation == current_user.idStation,Employee.idStation == current_user.idStation) \
        .first_or_404()
    try:
        db.session.delete(var)
        db.session.commit()
    except SQLAlchemyError:
        flash("Erreur inconnue due au serveur", 'error')
        db.session.rollback()
    else:
        flash("Cela a été supprimé avec succès de la liste", 'success')
    return redirect(url_for('chef.consulter_conge',Date=var.DateDebConge, _external=True))


@chef.route('/chef/conge/imprimer/liste', methods=['GET', 'POST'])
@login_required()
def imprimer_liste_conge():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    form = CongeFormFilter()
    return render_template('./chef/conge/imprimer.html',form=form,title="Imprimer la liste du congé")


@chef.route('/chef/conge/imprimerListe/data', methods=['GET', 'POST'])
@login_required()
def dataCongeAll():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        form = CongeFormFilter()
        if form.validate_on_submit():
            records = Conge.query.join(Employee, Employee.idEmp == Conge.idEmp) \
                .join(Station, Station.idStation == Employee.idStation) \
                .filter(Conge.idStation == current_user.idStation) \
                .filter(and_(Conge.DateDebConge >= FormatString(form.DatDeb.data), Conge.DateDebConge <= FormatString(form.DatFin.data)))\
                .order_by(desc(Conge.DateDebConge),desc(Conge.idConge),Conge.idGroupe).all()
            return json.dumps(FilterDataConge(records)).encode('utf8'), 200

        return jsonify(data=form.errors), 201


@chef.route('/chef/conge/imprimer/employee', methods=['GET', 'POST'])
@login_required()
def imprimer_liste_conge_employee():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    form = AbsenceFilter()
    return render_template('./chef/conge/employee.html',form=form, title="Imprimer La liste de congé de l'Employé")


@chef.route('/chef/conge/imprimerListe/data/employee', methods=['GET', 'POST'])
@login_required()
def dataCongeEmpAll():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        form = AbsenceFilter()
        if form.validate_on_submit():
            records = Conge.query.join(Employee, Employee.idEmp == Conge.idEmp) \
                .join(Station, Station.idStation == Employee.idStation) \
                .filter(or_(Employee.codeEmp == FormatString(form.Code.data), Employee.cinEmp == FormatString(form.Code.data)))\
                .order_by(desc(Conge.DateDebConge),desc(Conge.idConge),Conge.idGroupe).all()

            return json.dumps(FilterDataConge(records)).encode('utf8'), 200

        return jsonify(data=form.errors), 201


""" Settings """


@chef.route('/chef/setting/propos', methods=['GET', 'POST'])
@login_required()
def setting():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    user = User.query.filter(User.idStation == current_user.idStation,User.roleUser == 0,User.emailUser == current_user.emailUser).first_or_404()
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
            return redirect(url_for('chef.setting'))
        except ValidationError as e:
            flash(str(e), 'error')
            return redirect(url_for('chef.setting'))
        else:
            flash("Les informations de l'utilisateur ont été mise à jour avec succès", 'success')
        return redirect(url_for('chef.setting'))

    return render_template('./chef/profile/propos.html',form=form, title="Consulter les détails du compte",data=get_account_data(user))


@chef.route('/chef/setting/historique', methods=['GET', 'POST'])
@login_required()
def settingHistorique():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    return render_template('./chef/profile/historique.html',title="Consulter l'historique de connexion")


@chef.route('/chef/setting/logindetails', methods=['GET', 'POST'])
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


@chef.route('/chef/setting/password', methods=['GET', 'POST'])
@login_required()
def settingPassword():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    form = ResetLoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.emailUser == current_user.emailUser).first_or_404()
        if user:
            try:
                hashed_password = bcrypt.generate_password_hash(form.Password.data).decode('utf-8')
                user.passUser = hashed_password
                db.session.commit()
                flash('Votre mot de passe a été mis à jour avec succès', 'success')
                return redirect(url_for('chef.setting'))
            except SQLAlchemyError:
                db.session.rollback()
                flash("Erreur inconnue due au serveur", 'error')

            return redirect(url_for('chef.settingPassword'))
    return render_template('./chef/profile/password.html',title="Modifier le mot de passe",form=form)


@chef.route('/chef/setting/generate', methods=['GET', 'POST'])
@login_required()
def dataPassSetting():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        if request.method == 'POST':
            Str = generate()
            return json.dumps({"Password": Str}).encode('utf8')
        return ""


@chef.route('/chef/setting/notification', methods=['GET', 'POST'])
@login_required()
def settingNotification():
    if current_user.is_authenticated and bcrypt.check_password_hash(current_user.passUser, "0000"):
        return redirect(url_for('chef.resetLogin'))
    return render_template('./chef/profile/notification.html',title="Consulter les notifications")


@chef.route('/chef/setting/notification/details', methods=['GET', 'POST'])
@login_required()
def dataNotificationDetails():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        if request.method == 'POST':
            recordObject = []
            startDate = request.form["startDate"]
            endDate = request.form["endDate"]
            if (startDate is None) or (endDate is None):
                return jsonify(data={"Msg": "Erreur"}), 201
            else:
                startDate = FormatString(startDate)+" 00:00:00"
                endDate = FormatString(endDate)+" 23:59:59"
                Str = "SELECT * FROM comments " \
                      "WHERE idUser = {} AND comment_date BETWEEN '{}' AND '{}' " \
                      "ORDER BY comment_date DESC".format(current_user.idUser, startDate,endDate)

                result = db.session.execute(Str)
                if result:
                    for record in result:
                        recordObject.append({
                            "Subject":  record["comment_subject"],
                            "Time": pretty_date(record["comment_date"]),
                            "Text":  record["comment_text"]
                        })

            return json.dumps(recordObject).encode('utf8'),200

        return ""


"""" Notification """


@chef.route('/chef/notification/count', methods=['GET', 'POST'])
@login_required()
def dataNotificationCount():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        if request.method == 'POST':
            record = Comment.query.filter(Comment.idUser == current_user.idUser,Comment.comment_status == 1).count()
            return jsonify(data={"Msg": record}), 200
        return ""


@chef.route('/chef/notification/fetch', methods=['GET', 'POST'])
@login_required()
def dataNotification():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        if request.method == 'POST':
            offset = 0
            start = 5
            id = request.form["id"]
            if id is None:
                return jsonify(data={"Msg": "Erreur"}), 201
            start += int(id)
            records = Comment.query.filter(Comment.idUser == current_user.idUser) \
                .order_by(desc(Comment.comment_date)).limit(start).offset(offset).all()
            return json.dumps(get_notification_data(records)).encode('utf8'), 200

        return ""


@chef.route('/chef/notification/delete', methods=['GET', 'POST'])
@login_required()
def dataNotificationDelete():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        if request.method == 'POST':
            id = request.form["id"]
            if id is None:
                return jsonify(data={"Msg": "Erreur"}), 201
            try:
                records = Comment.query.filter(Comment.idUser == current_user.idUser, Comment.comment_id == id).first()
                if records:
                    db.session.delete(records)
                    db.session.commit()
                else:
                    return jsonify(data={"Msg": "Erreur inconnue due au serveur"}), 201
            except SQLAlchemyError:
                db.session.rollback()
                return jsonify(data={"Msg": "Erreur inconnue due au serveur"}), 201
            else:
                return jsonify(data={"Msg": "Cette notification est supprimée avec succès"}), 200

        return ""


@chef.route('/chef/notification/seen', methods=['GET', 'POST'])
@login_required()
def dataNotificationSeen():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        if request.method == 'POST':
            id = request.form["id"]
            if id is None:
                return jsonify(data={"Msg": "Erreur"}), 201
            try:
                records = Comment.query.filter(Comment.idUser == current_user.idUser, Comment.comment_id == id,Comment.comment_status == 1).first()
                if records:
                    records.comment_status = 0
                    db.session.commit()
                else:
                    return jsonify(data={"Msg": "Cette notification est déjà lue"}), 201
            except SQLAlchemyError:
                db.session.rollback()
                return jsonify(data={"Msg": "Erreur inconnue due au serveur"}), 201
            else:
                return jsonify(data={"Msg": "Cette notification est correctement marquée comme vue"}), 200

        return ""


@chef.route('/chef/notification/done', methods=['GET', 'POST'])
@login_required()
def dataNotificationDone():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        if request.method == 'POST':
            try:
                records = Comment.query.filter(Comment.idUser == current_user.idUser,Comment.comment_status == 1).all()
                if records:
                    for record in records:
                        record.comment_status = 0
                    db.session.commit()
                else:
                    return jsonify(data={"Msg": "Toutes les notifications sont déjà lues"}), 201
            except SQLAlchemyError:
                db.session.rollback()
                return jsonify(data={"Msg": "Erreur inconnue due au serveur"}), 201
            else:
                return jsonify(data={"Msg": "Toutes les notifications sont correctement marquées comme lues"}), 200

        return ""


@chef.route('/chef/notification/deleteAll', methods=['GET', 'POST'])
@login_required()
def dataNotificationDeleteAll():
    if current_user.is_authenticated and not bcrypt.check_password_hash(current_user.passUser, "0000"):
        if request.method == 'POST':
            try:
                records = Comment.query.filter(Comment.idUser == current_user.idUser).all()
                if records:
                    for record in records:
                        db.session.delete(record)
                    db.session.commit()
                else:
                    return jsonify(data={"Msg": "Toutes les notifications sont déjà Supprimées"}), 201
            except SQLAlchemyError:
                db.session.rollback()
                return jsonify(data={"Msg": "Erreur inconnue due au serveur"}), 201
            else:
                return jsonify(data={"Msg": "Toutes les notifications sont correctement Supprimées"}), 200

        return ""


""" Log Out """


@chef.route('/chef/logout', methods=['GET', 'POST'])
@login_required()
def logout():
    send_details_logout(current_user)
    logout_user()
    return redirect(url_for('approot.login'))
