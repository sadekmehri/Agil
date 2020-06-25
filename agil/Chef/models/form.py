from datetime import datetime

from flask_login import current_user
from flask_wtf import FlaskForm
from sqlalchemy import asc, or_
from wtforms import StringField, FloatField, SelectField, PasswordField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, Regexp, InputRequired, ValidationError, length

from agil.Chef.utils import validation, verifDate, days_between, date_check, days_calc
from agil.Main.utils import FormatString
from agil.models.Absence import Absence
from agil.models.Carburant import Carburant
from agil.models.Citerne import Citerne
from agil.models.Conge import TypeConge, Conge
from agil.models.Employee import Employee
from agil.models.Groupe import Groupe
from agil.models.Lavage import Lavage
from agil.models.Pompe import Pompe
from agil.models.PompeCiterne import PompeCiterne
from agil.models.Role import Role
from agil.models.Station import Station
from agil.models.Voie import Voie


class ReligionField(SelectField):

    def pre_validate(self, form):
        for v, _ in self.choices:
            if self.data == v:
                break
            else:
                pass


class ToDoForm(FlaskForm):
    Date = StringField("Date :", validators=[DataRequired()])
    Task = TextAreaField("Event :", render_kw={"rows": 4, "cols": 50}, validators=[DataRequired(), Length(min=3, max=75)])

    def validate_Date(self, field):
        if not verifDate(str(field.data)) or not date_check(str(field.data)):
            raise ValidationError('Veuillez choisir une date valide.')

    def validate_Task(self, field):
        validation(field.data)


class ToDoFormUpd(ToDoForm):
    Id = HiddenField("Id :", validators=[InputRequired()])

    class Meta:
        csrf = False


class ResetLoginForm(FlaskForm):
    Password = PasswordField('Password', validators=[DataRequired()])


class DateRecette(FlaskForm):
    Date = StringField('Date :')

    def validate_Date(self, field):
        if not (verifDate(field.data) and not days_between(field.data)):
            raise ValidationError('Veuillez choisir une date valide.')


class Recette(FlaskForm):
    Matricule = StringField('Matricule Voiture :', id="matricule", validators=[DataRequired()])
    Debut = StringField('Heure Debut : ', id="anytime-time", validators=[DataRequired()])
    Fin = StringField('Heure Fin : ', id="anytime-time1", validators=[DataRequired()])
    Type = SelectField('Type Lavage :', coerce=int, validators=[InputRequired()])
    kilometrage = StringField('kilométrage :', id="km", validators=[DataRequired()])
    Prix = FloatField('Prix :', id="price", validators=[DataRequired()])
    Date = StringField('Date :', id="Date", validators=[DataRequired()])
    Groupe = SelectField('Groupe :', coerce=int, validators=[InputRequired()])

    def validate_Prix(self, field):
        if float(field.data) <= 0:
            raise ValidationError('La valeur du prix doit être > 0.')

    def validate_Date(self, field):
        if not (verifDate(field.data) and not days_between(field.data)):
            raise ValidationError('Veuillez choisir une date valide.')

    def validate_Fin(form, field):
        FMT = '%H:%M'
        tdelta = datetime.strptime(field.data, FMT) - datetime.strptime(form.Debut.data, FMT)
        if tdelta.days < 0:
            raise ValidationError('L\'heure de fin doit être > Heure de début')

    def validate_Type(self, field):
        Type = Lavage.query.filter_by(idLavage=field.data).first()
        if not Type:
            raise ValidationError('Veuillez choisir une option valide.')

    def validate_Groupe(self, field):
        Gp = Groupe.query.filter_by(idGroupe=field.data).first()
        if not Gp:
            raise ValidationError('Veuillez choisir une option valide.')

    def fill_choice_type_lavage(self):
        type = list(Lavage.query.with_entities(Lavage.idLavage, Lavage.TypeLavage).all())
        self.Type.choices = ([(0, '-- sélectionnez une option --')]) + ([i for i in type])

    def fill_choice_groupe(self):
        Gp = list(Groupe.query.with_entities(Groupe.idGroupe, Groupe.NomGroupe).all())
        self.Groupe.choices = ([(0, '-- sélectionnez une option --')]) + ([i for i in Gp])


class Citernes(FlaskForm):
    Code = StringField('Code Citerne :', id="code",validators=[DataRequired(), Regexp(regex=r'^[a-zA-Z0-9]*$', message='erreur')])
    Car = SelectField('Carburant :', coerce=int, validators=[InputRequired()])
    Volume = FloatField('Volume Citerne :', id="citerne", validators=[DataRequired()])
    Min = StringField('Stock Min :', id="min", validators=[DataRequired()])

    def validate_Code(self, field):
        Type = Citerne.query.filter_by(NomCiterne=field.data).filter(Citerne.idStation == current_user.idStation).first()
        if Type:
            raise ValidationError('Nom Citerne existe déjà.')

    def validate_Car(self, field):
        Type = Carburant.query.filter_by(idCarburant=field.data).first()
        if not Type:
            raise ValidationError('Veuillez choisir une option valide.')

    def fill_choice_carburant(self):
        Gp = list(Carburant.query.with_entities(Carburant.idCarburant, Carburant.NomCarburant).all())
        self.Car.choices = ([(0, '-- sélectionnez une option --')]) + ([i for i in Gp])

    def validate_Volume(self, field):
        if float(field.data) <= 0:
            raise ValidationError('La valeur du volume doit être > 0.')

    def validate_Min(self, field):
        if float(field.data.replace(' %', '')) <= 0:
            raise ValidationError('La valeur minimale doit être > 0.')


class UpdCiternes(FlaskForm):
    Act = FloatField('Volume Actuelle :', id="volAct", validators=[DataRequired()])
    Etat = SelectField('Etat Citerne :', coerce=str, validators=[DataRequired()],choices=[('-1', '-- sélectionnez une option --'), ("0", 'Panne'), ("1", 'Active')])
    Code = StringField('Code Citerne :', id="code",validators=[DataRequired(), Regexp(regex=r'^[a-zA-Z0-9]*$', message='erreur')])
    Car = StringField('Carburant :')
    Volume = FloatField('Volume Citerne :', id="citerne", validators=[DataRequired()])
    Min = StringField('Stock Min :', id="min", validators=[DataRequired()])

    def validate_Volume(self, field):
        if float(field.data) <= 0:
            raise ValidationError('La valeur du volume doit être > 0.')

    def validate_Min(self, field):
        if float(field.data.replace(' %', '')) <= 0:
            raise ValidationError('La valeur minimale doit être > 0.')

    def validate_Etat(self, field):
        if not 1 >= int(field.data) >= 0:
            raise ValidationError('Veuillez choisir une option valide.')

    def validate_Act(form, field):
        if form.Volume.data - field.data < 0:
            raise ValidationError('Le volume actuel doit être <= Volume du citerne')


class Pompes(FlaskForm):
    Code = StringField('Code Pompe :', id="code", validators=[DataRequired(), Regexp(regex=r'^[A-Za-z0-9]*$', message='Uniquement lettres et chiffres')])

    def validate_Code(self, field):
        Gp = Pompe.query.filter_by(NomPompe=field.data).filter(Pompe.idStation == current_user.idStation).first()
        if Gp:
            raise ValidationError('Pompe existe déjà.')


class UpdPompes(Pompes):
    Etat = SelectField('Etat Pompe :', coerce=str, validators=[DataRequired()],choices=[("-1", '-- sélectionnez une option --'), ("0", 'Panne'), ("1", 'Active')])

    def validate_Etat(self, field):
        if not 1 >= int(field.data) >= 0:
            raise ValidationError('Veuillez choisir une option valide.')

    def validate_Code(form, field):
        pass


class PompeCiternes(FlaskForm):
    Code = SelectField('Code Pompe :', coerce=int, validators=[InputRequired()])
    Cit = SelectField('Nom Citerne :', id="cit", coerce=int, validators=[InputRequired()])
    Type = ReligionField('Type Carburant', id="type", coerce=int, choices=[(0, '-- sélectionnez une option --')])

    def validate_Cit(form, field):
        Gp = Citerne.query.filter_by(idCiterne=field.data).filter(Citerne.idStation == current_user.idStation, Citerne.EtatCiterne == 1).first()
        if not Gp:
            raise ValidationError('Veuillez choisir une option valide.')

        Gp = PompeCiterne.query.filter_by(idCiterne=field.data, idPompe=form.Code.data).filter(Citerne.idStation == current_user.idStation).first()
        if Gp:
            raise ValidationError('La liaison existe déjà.')

    def validate_Code(self, field):
        Gp = Pompe.query.filter_by(idPompe=field.data).filter(Pompe.idStation == current_user.idStation,Pompe.EtatPompe == 1).first()
        if not Gp:
            raise ValidationError('Veuillez choisir une option valide.')

    def fill_choice_Cit(self):
        Gp = list(Citerne.query.with_entities(Citerne.idCiterne, Citerne.NomCiterne).filter(
            Citerne.idStation == current_user.idStation,
            Citerne.EtatCiterne == 1).order_by(asc(Citerne.NomCiterne)).all())
        self.Cit.choices = ([(0, '-- sélectionnez une option --')]) + ([i for i in Gp])

    def fill_choice_Code(self):
        # idStation will be replaced after
        Gp = list(Pompe.query.with_entities(Pompe.idPompe, Pompe.NomPompe).filter(Pompe.idStation == current_user.idStation,Pompe.EtatPompe == 1).order_by(asc(Pompe.NomPompe)).all())
        self.Code.choices = ([(0, '-- sélectionnez une option --')]) + ([i for i in Gp])


class UpdPompeCiternes(PompeCiternes):

    def validate_Cit(form, field):
        Gp = Citerne.query.filter_by(idCiterne=field.data).filter(Citerne.idStation == current_user.idStation,Citerne.EtatCiterne == 1).first()
        if not Gp:
            raise ValidationError('Veuillez choisir une option valide.')


class RecetteCar(FlaskForm):
    Pmp = SelectField('Pompe :', coerce=int, id="pmp", validators=[InputRequired()])
    Cit = ReligionField('Citerne :', coerce=int, id="cit", choices=[(0, '-- select an option --')],validators=[InputRequired()])
    Car = ReligionField('Carburant :', coerce=int, id="car", choices=[(0, '-- select an option --')],validators=[InputRequired()])
    Voie = ReligionField('Voie :', coerce=int, validators=[InputRequired()])
    IndDebut = StringField('Indice Debut :', id="deb",validators=[DataRequired(), Regexp(regex=r'^[0-9]*$', message='Seuls les chiffres')])
    IndFin = StringField('Indice Fin :', id="fin",validators=[DataRequired(), Regexp(regex=r'^[0-9]*$', message='Seuls les chiffres')])
    Prix = StringField('Prix : (1 litre)', id="prix")
    Groupe = SelectField('Groupe :', coerce=int, validators=[InputRequired()])
    Date = StringField('Date :', id="Date", validators=[DataRequired()])

    def validate_Date(self, field):
        if not (verifDate(field.data) and not days_between(field.data)):
            raise ValidationError('Veuillez choisir une date valide.')

    def validate_Groupe(self, field):
        Gp = Groupe.query.filter_by(idGroupe=field.data).first()
        if not Gp:
            raise ValidationError('Veuillez choisir une option valide.')

    def fill_choice_groupe(self):
        Gp = list(Groupe.query.with_entities(Groupe.idGroupe, Groupe.NomGroupe).all())
        self.Groupe.choices = ([(0, '-- sélectionnez une option --')]) + ([i for i in Gp])

    def validate_Voie(self, field):
        Gp = Voie.query.filter_by(idVoie=field.data).first()
        if not Gp:
            raise ValidationError('Veuillez choisir une option valide.')

    def fill_choice_Voie(self):
        Gp = list(Voie.query.with_entities(Voie.idVoie, Voie.nomVoie).all())
        self.Voie.choices = ([(0, '-- sélectionnez une option --')]) + ([i for i in Gp])

    def validate_Pmp(self, field):
        Gp = Pompe.query.filter_by(idPompe=field.data).filter(Pompe.idStation == current_user.idStation,Pompe.EtatPompe == 1).first()
        if not Gp:
            raise ValidationError('Veuillez choisir une option valide.')

    def fill_choice_Pmp(self):
        Gp = list(Pompe.query.with_entities(Pompe.idPompe, Pompe.NomPompe).filter(Pompe.idStation == current_user.idStation,Pompe.EtatPompe == 1).order_by(asc(Pompe.NomPompe)).all())
        self.Pmp.choices = ([(0, '-- sélectionnez une option --')]) + ([i for i in Gp])

    def validate_Car(self, field):
        Type = Carburant.query.filter_by(idCarburant=field.data).first()
        if not Type:
            raise ValidationError('Veuillez choisir une option valide.')

    def validate_Cit(self, field):
        Type = Citerne.query.filter_by(idCiterne=field.data).filter(Citerne.idStation == current_user.idStation).first()
        if not Type:
            raise ValidationError('Veuillez choisir une option valide.')

    def validate_IndFin(form, field):
        if float(field.data) - float(form.IndDebut.data) <= 0:
            raise ValidationError('Indice Fin devrait être > Indice Debut.')
        Cit = Citerne.query.filter_by(idCiterne=form.Cit.data).filter(Citerne.idStation == current_user.idStation).first()
        if Cit:
            if Cit.Val_Act_Citerne < float(form.IndFin.data) - float(form.IndDebut.data):
                raise ValidationError("C'est au-dessus du volume réel de Citerne {} : {} L".format(Cit.NomCiterne,Cit.Val_Act_Citerne))
        else:
            raise ValidationError("Quelque chose s'est mal passé.")

    def validate_IndDeb(self, field):
        if field.data <= 0:
            raise ValidationError('Indice Debut devrait être > 0.')

    def validate_Prix(self, field):
        if field.data != "":
            if float(field.data) <= 0:
                raise ValidationError('Le prix d\'un litre doit être> 0')


class RecetteFilter(FlaskForm):
    Grp = ReligionField('Groupe :', coerce=int, choices=[(0, '-- sélectionnez une option --')], validators=[InputRequired()])
    Dat = StringField('Date :', id="input-daterange")

    def fill_choice_groupe(self):
        Gp = list(Groupe.query.with_entities(Groupe.idGroupe, Groupe.NomGroupe).all())
        self.Grp.choices = ([(0, '-- sélectionnez une option --')]) + ([i for i in Gp])

    def validate_Dat(self, field):
        if field.data != "":
            if not (verifDate(field.data) and not days_between(field.data)):
                raise ValidationError('Veuillez choisir une date valide.')

    def validate_Grp(self, field):
        if field.data != 0:
            Gp = Groupe.query.filter_by(idGroupe=field.data).first()
            if not Gp:
                raise ValidationError('Veuillez choisir une date valide.')


class CarFilter(FlaskForm):
    Mat = StringField('Matricule Voiture :', id="Mat", validators=[DataRequired()])


class ExpensesForm(FlaskForm):
    Date = StringField("Date :",id="Date", validators=[DataRequired()])
    Cat = StringField("Catégorie :", validators=[DataRequired(), Length(min=3, max=20)])
    Desc = TextAreaField("Description :", render_kw={"rows": 4, "cols": 50}, validators=[DataRequired(), Length(min=3, max=75)])
    Mont = StringField("Montant :",id="Mont", validators=[DataRequired()])

    def validate_Date(self, field):
        if not (verifDate(field.data) and not days_between(field.data)):
            raise ValidationError('Veuillez choisir une date valide.')

    def validate_Cat(self, field):
        validation(field.data)

    def validate_Desc(self, field):
        validation(field.data)

    def validate_Mont(self, field):
        if float(field.data) <= 0:
            raise ValidationError('Montant doit être supérieur à 0')


class ExpenseFilter(FlaskForm):
    Dat = StringField('Date :', id="input-daterange")

    def validate_Dat(self, field):
        if field.data != "":
            if not (verifDate(field.data) and not days_between(field.data)):
                raise ValidationError('Veuillez choisir une date valide.')


class EmpStation(FlaskForm):
    Code = StringField('Code :', id="codeEmp", validators=[DataRequired()])
    Cin = StringField('Cin :', id="Cin", validators=[DataRequired(),length(8),Regexp(regex=r'^[0-9]{8}$', message='Seuls les chiffres sont autorisés')])
    Nom = StringField('Nom :', id="Nom", validators=[DataRequired(),length(min=3,max=25),Regexp(regex=r'^[A-Za-z ]+$', message='Seules les lettres sont autorisées')])
    Prenom = StringField('Prenom :', id="Prenom", validators=[DataRequired(),length(min=3,max=25), Regexp(regex=r'^[A-Za-z ]+$', message='Seules les lettres sont autorisées')])
    Tel = StringField('Telephone :', id="Tel", validators=[DataRequired(), length(8), Regexp(regex=r'^[0-9]{8}$', message='Seuls les chiffres sont autorisés')])
    Date = StringField('Date de Naissance :', id="Date", validators=[DataRequired()])
    Sal = StringField('Salaire :', id="Sal", validators=[DataRequired()])
    Groupe = SelectField('Groupe :', coerce=int, validators=[InputRequired()])
    Role = SelectField('Role :', coerce=int, validators=[InputRequired()])

    def validate_Groupe(self, field):
        Gp = Groupe.query.filter_by(idGroupe=field.data).first()
        if not Gp:
            raise ValidationError('Veuillez choisir une option valide.')

    def validate_Code(self, field):
        Gp = Employee.query.filter_by(codeEmp=FormatString(field.data)).first()
        if Gp:
            raise ValidationError('Le code employé existe déjà.')

    def validate_Cin(self, field):
        Gp = Employee.query.filter_by(cinEmp=FormatString(field.data)).first()
        if Gp:
            raise ValidationError('Cin employé existe déjà.')

    def validate_Tel(self, field):
        Gp = Employee.query.filter_by(telEmp=FormatString(field.data)).first()
        if Gp:
            raise ValidationError('Le téléphone existe déjà.')

    def fill_choice_groupe(self):
        Gp = list(Groupe.query.with_entities(Groupe.idGroupe, Groupe.NomGroupe).all())
        self.Groupe.choices = ([(0, '-- sélectionnez une option --')]) + ([i for i in Gp])

    def validate_Role(self, field):
        Gp = Role.query.filter_by(idRole=field.data).first()
        if not Gp:
            raise ValidationError('Veuillez choisir une option valide.')

    def fill_choice_role(self):
        Gp = list(Role.query.with_entities(Role.idRole, Role.NomRole).all())
        self.Role.choices = ([(0, '-- sélectionnez une option --')]) + ([i for i in Gp])

    def validate_Nom(self, field):
        validation(field.data)

    def validate_Prenom(self, field):
        validation(field.data)
        Gp = Employee.query.filter(Employee.nomEmp == FormatString(self.Nom.data).capitalize(),Employee.prenomEmp == FormatString(field.data).capitalize()).first()
        if Gp:
            raise ValidationError('L\'employé existe déjà! Veuillez en choisir un autre.')

    def validate_Date(self, field):
        if not (verifDate(field.data) and not days_between(field.data)):
            raise ValidationError('Veuillez choisir une date valide.')

    def validate_Sal(self, field):
        if float(field.data) <= 0:
            raise ValidationError('Salaire doit être > 0.')


class UpdEmpStation(EmpStation):

    def validate_Code(self, field):
        pass

    def validate_Cin(self, field):
        pass

    def validate_Tel(self, field):
        pass

    def validate_Prenom(self, field):
        pass


class EmployeeFilter(FlaskForm):
    Groupe = SelectField('Groupe :', coerce=int, validators=[InputRequired()])

    def validate_Groupe(self, field):
        Gp = Groupe.query.filter_by(idGroupe=field.data).first()
        if not Gp:
            raise ValidationError('Veuillez choisir une option valide.')

    def fill_choice_groupe(self):
        Gp = list(Groupe.query.with_entities(Groupe.idGroupe, Groupe.NomGroupe).all())
        self.Groupe.choices = ([(0, '-- sélectionnez une option --')]) + ([i for i in Gp])


class AbsenceForm(FlaskForm):
    Date = StringField("Date :",id="Date", validators=[DataRequired()])
    Code = StringField("Code ou Cin Employé :",id="Code", validators=[DataRequired()])
    Name = StringField("Nom :",id="Name")
    Prenom = StringField("Prenom :", id="Prenom")
    Groupe = StringField("Groupe :", id="Groupe")
    Desc = TextAreaField("Description :", id="Desc", render_kw={"rows": 4, "cols": 50}, validators=[DataRequired(), Length(min=3, max=75)])

    def validate_Date(self, field):
        if not (verifDate(field.data) and not days_between(field.data)):
            raise ValidationError('Veuillez choisir une date valide.')

    def validate_Code(form, field):
        validation(field.data)
        Gp = Employee.query.filter(or_(Employee.codeEmp == FormatString(field.data), Employee.cinEmp == FormatString(field.data)),Employee.idStation == current_user.idStation).first()
        if not Gp:
            raise ValidationError('L\'employé n\'existe pas! Veuillez saisir un autre code.')
        Ab = Absence.query.join(Employee, Employee.idEmp == Absence.idEmp) \
            .join(Station, Station.idStation == Employee.idStation) \
            .filter(Employee.idStation == current_user.idStation, Absence.idStation == current_user.idStation, Employee.idEmp == Gp.idEmp,Absence.DateAbsence == FormatString(form.Date.data)).first()
        if Ab:
            raise ValidationError("Vous avez ajouté cet employé à la liste.")

    def validate_Desc(self, field):
        validation(field.data)


class UpdAbsenceForm(AbsenceForm):

    def validate_Code(self, field):
        pass


class AbsenceFilter(FlaskForm):
    Code = StringField('Code ou Cin Employé :',id="Code")

    def validate_Code(self, field):
        validation(field.data)
        Gp = Employee.query.filter(or_(Employee.codeEmp == FormatString(field.data), Employee.cinEmp == FormatString(field.data))).first()
        if not Gp:
            raise ValidationError('L\'employé n\'existe pas! Veuillez saisir un autre code.')


class CongeForm(FlaskForm):
    DatDeb = StringField("Date Sortie :",id="DateDeb", validators=[DataRequired()])
    DatFin = StringField("Date Retour :", id="DateFin", validators=[DataRequired()])
    Code = StringField("Code ou Cin Employé :",id="Code", validators=[DataRequired()])
    Name = StringField("Nom :",id="Name")
    Prenom = StringField("Prenom :", id="Prenom")
    Groupe = StringField("Groupe :", id="Groupe")
    Type = SelectField('Type du congé :',id="Type", coerce=int, validators=[InputRequired()])
    Desc = TextAreaField("Description :", id="Desc", render_kw={"rows": 4, "cols": 50}, validators=[DataRequired(), Length(min=3, max=75)])

    def validate_Code(form, field):
        validation(field.data)
        Gp = Employee.query.filter(or_(Employee.codeEmp == FormatString(field.data), Employee.cinEmp == FormatString(field.data)),Employee.idStation == current_user.idStation).first()
        if not Gp:
            raise ValidationError('L\'employé n\'existe pas! Veuillez saisir un autre code.')
        Gp = Conge.query.join(Employee, Employee.idEmp == Conge.idEmp) \
            .join(Station, Station.idStation == Employee.idStation) \
            .filter(or_(Employee.codeEmp == FormatString(field.data), Employee.cinEmp == FormatString(field.data)),Employee.idStation == current_user.idStation) \
            .filter(Conge.idStation == current_user.idStation,Conge.DateDebConge >= FormatString(form.DatDeb.data)).all()
        Test = True
        for record in Gp:
            if ((days_calc(record.DateDebConge, FormatString(form.DatDeb.data)) >= 0 and days_calc(FormatString(form.DatFin.data), record.DateFinConge) >= 0 )
                or (not((days_calc(FormatString(form.DatDeb.data),record.DateDebConge) > 0 and days_calc(FormatString(form.DatFin.data),record.DateDebConge) >= 0 )
                or (days_calc(record.DateFinConge,FormatString(form.DatDeb.data)) > 0 and days_calc(record.DateFinConge,FormatString(form.DatFin.data)) > 0 )))) :
                Test = False
            if not Test:
                raise ValidationError('L\'employé est en congé ! Veuillez saisir une autre date.')

    def validate_Desc(self, field):
        validation(field.data)

    def validate_Type(self, field):
        Gp = TypeConge.query.filter_by(idTypeConge=field.data).first()
        if not Gp:
            raise ValidationError('Veuillez choisir une option valide.')

    def fill_choice_type(self):
        Gp = list(TypeConge.query.with_entities(TypeConge.idTypeConge,TypeConge.typeConge).all())
        self.Type.choices = ([(0, '-- sélectionnez une option --')]) + ([i for i in Gp])

    def validate_DatDeb(self, field):
        if not (verifDate(field.data)):
            raise ValidationError('Veuillez choisir une date valide.')

    def validate_DatFin(form, field):
        if not (verifDate(field.data) and days_calc(form.DatDeb.data, field.data) >=1):
            raise ValidationError('Date retour devrait être > date retour.')


class UpdCongeForm(CongeForm):
    def validate_Code(form, field):
        validation(field.data)
        Gp = Employee.query.filter(or_(Employee.codeEmp == FormatString(field.data), Employee.cinEmp == FormatString(field.data)),Employee.idStation == current_user.idStation).first()
        if not Gp:
            raise ValidationError('L\'employé n\'existe pas! Veuillez saisir un autre code.')


class CongeFormFilter(FlaskForm):
    DatDeb = StringField("Date Sortie Debut :",id="DateDeb", validators=[DataRequired()])
    DatFin = StringField("Date Sortie Fin :", id="DateFin", validators=[DataRequired()])

    def validate_DatDeb(self, field):
        if not (verifDate(field.data)):
            raise ValidationError('Veuillez choisir une date valide.')

    def validate_DatFin(form, field):
        if not (verifDate(field.data) and days_calc(form.DatDeb.data, field.data) >=1):
            raise ValidationError('Date fin devrait être > date debut.')


class SettingsInfo(FlaskForm):
    Code = StringField('Code :', id="Code")
    Cin = StringField('Cin :', id="Cin", validators=[DataRequired(),length(8),Regexp(regex=r'^[0-9]{8}$', message='Seuls les chiffres sont autorisés')])
    Nom = StringField('Nom :', id="Nom", validators=[DataRequired(),length(min=3,max=25),Regexp(regex=r'^[A-Za-z ]+$', message='Seules les lettres sont autorisées')])
    Prenom = StringField('Prenom :', id="Prenom", validators=[DataRequired(),length(min=3,max=25), Regexp(regex=r'^[A-Za-z ]+$', message='Seules les lettres sont autorisées')])
    Tel = StringField('Telephone :', id="Tel", validators=[DataRequired(), length(8), Regexp(regex=r'^[0-9]{8}$', message='Seuls les chiffres sont autorisés')])
    Date: StringField = StringField('Date de Naissance :', id="Date", validators=[DataRequired()])
    Email = StringField('Email :', id="Email")

    def validate_Date(self, field):
        if not (verifDate(field.data) and not days_between(field.data)):
            raise ValidationError('Veuillez choisir une date valide.')

    def validate_Nom(self, field):
        validation(field.data)

    def validate_Prenom(self, field):
        validation(field.data)
