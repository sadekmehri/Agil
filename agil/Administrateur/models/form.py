import re
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, FloatField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError, InputRequired, length

from agil.Chef.models.form import ReligionField
from agil.Chef.utils import validation, verifDate
from agil.Main.utils import FormatString, days_between
from agil.models.Carburant import Carburant
from agil.models.Delegation import Delegation
from agil.models.Employee import Employee
from agil.models.Groupe import Groupe
from agil.models.Role import Role
from agil.models.Station import Station
from agil.models.User import User
from agil.models.Ville import Ville


class ResetLoginForm(FlaskForm):
    Password = PasswordField('Password', validators=[DataRequired()])


class TypeCarburant(FlaskForm):
    Type = StringField('Nom Carburant :', validators=[DataRequired(), Length(min=3, max=30), Regexp(regex=r'^[a-zA-Z ]+$', message='Seules les lettres sont autorisées')])
    Prix = FloatField('Prix Carburant :', id="price", validators=[DataRequired()])

    def validate_Type(self, field):
        validation(field.data)
        Gp = Carburant.query.filter_by(NomCarburant=field.data).first()
        if Gp:
            raise ValidationError('Le carburant existe déjà. Veuillez choisir une option valide.')

    def validate_Prix(self, field):
        if float(field.data) <= 0:
            raise ValidationError('Le prix doit être > 0 .')


class UpdateCarburant(TypeCarburant):
    def validate_Type(self, field):
        validation(field.data)


class StationService(FlaskForm):
    Ville = SelectField('Ville :', id="ville", coerce=int, validators=[DataRequired()])
    Nom = StringField('Nom Station : ', id="St", validators=[DataRequired(), Length(min=5, max=50),Regexp(regex=r'^[a-zA-Z\-\:\_ ]+$', message='Seules les lettres sont autorisées')])
    Del = ReligionField('Delegation : ', id="delg", coerce=int, validators=[DataRequired()], choices=[])
    Adr = StringField('Adresse Station :', validators=[DataRequired(), Length(min=5, max=50), Regexp(regex=r'^[a-zA-Z0-9\-\:\_ ]+$', message='Uniquement lettres et chiffres')])

    def validate_Nom(self, field):
        validation(field.data)

    def validate_Adr(self, field):
        validation(field.data)

    def validate_Delg(self, field):
        Gp = Delegation.query.filter_by(idDelegation=field.data).first()
        if not Gp:
            raise ValidationError('Veuillez choisir une option valide .')

    def fill_choice_Del(self, string):
        Type = Delegation.query.with_entities(Delegation.idDelegation, Delegation.nomDelegation).join(Ville).filter(Ville.idVille == string).all()
        self.Del.choices = ([(0, '-- sélectionnez une option --')]) + ([i for i in Type])

    def fill_choice_ville(self):
        Type = list(Ville.query.with_entities(Ville.idVille, Ville.NomVille).all())
        self.Ville.choices = ([(0, '-- sélectionnez une option --')]) + ([i for i in Type])

    def validate_Ville(self, field):
        Gp = Ville.query.filter_by(idVille=field.data).first()
        if not Gp:
            raise ValidationError('Veuillez choisir une option valide .')


class ComptesChef(FlaskForm):
    Code = StringField('Code Chef : ', id="chef", validators=[DataRequired(), Length(min=5, max=30)])
    Nom = StringField('Nom : ', id="Nom", validators=[DataRequired(), Length(min=3, max=30),Regexp(regex=r'^[a-zA-Z ]+$', message='Seules les lettres sont autorisées')])
    Prenom = StringField('Prenom : ', id="Prenom", validators=[DataRequired(), Length(min=3, max=30),Regexp(regex=r'^[a-zA-Z ]+$', message='Seules les lettres sont autorisées')])
    Cin = StringField('Cin : ', id="Cin", validators=[DataRequired(),Length(8)])
    Date = StringField('Date De Naissance : ', id="Date", validators=[DataRequired()])
    Email = EmailField('Email : ', id="Email", validators=[DataRequired()])
    Tel = StringField('Telephone : ', id="Tel", validators=[DataRequired(), Length(8),Regexp(regex=r'^[0-9]+$', message='Seuls les chiffres sont autorisés')])
    Station = SelectField("Station ", id="station", coerce=int, validators=[DataRequired()])

    def validate_Code(self, field):
        validation(field.data)
        Gp = User.query.filter_by(codeUser=FormatString(field.data)).first()
        if Gp:
            raise ValidationError('Le code existe déjà! Veuillez en choisir un autre.')

    def validate_Date(self, field):
        if not (verifDate(field.data) and not days_between(field.data)):
            raise ValidationError('Veuillez choisir une date valide.')

    def validate_Nom(self, field):
        validation(field.data)

    def validate_Prenom(self, field):
        validation(field.data)
        Gp = User.query.filter(User.nomUser == FormatString(self.Nom.data).capitalize(),User.prenomUser == FormatString(field.data).capitalize()).first()
        if Gp:
            raise ValidationError('L\'utilisateur existe déjà! Veuillez en choisir un autre.')

    def validate_Email(self,field):
        if re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', field.data) is None:
            raise ValidationError('Email invalide! Veuillez en choisir un autre.')

        Gp = User.query.filter_by(emailUser=FormatString(field.data)).first()
        if Gp:
            raise ValidationError('L\'email existe déjà! Veuillez en choisir un autre.')

    def validate_Cin(self, field):
        Gp = User.query.filter_by(cinUser=FormatString(field.data)).first()
        if Gp:
            raise ValidationError('Cin existe déjà.')

    def validate_Tel(self, field):
        Gp = User.query.filter_by(telUser=FormatString(field.data)).first()
        if Gp:
            raise ValidationError('Le téléphone existe déjà! Veuillez en choisir un autre.')

    def fill_choice_St(self):
        Type = Station.query.with_entities(Station.idStation, Station.NomStation).all()
        self.Station.choices = ([(0, '-- sélectionnez une option --')]) + ([i for i in Type])

    def validate_Station(self, field):
        Gp = Station.query.filter_by(idStation=field.data).first()
        if not Gp:
            raise ValidationError('Veuillez choisir une option valide.')


class ComptesChefUpd(ComptesChef):
    Etat = SelectField("Etat Compte ", id="station", coerce=str, validators=[DataRequired()], choices=[('-1', '-- sélectionnez une option --'),('0',"Bloqué"),('1',"Active")])

    def validate_Email(self,field):
        if re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', field.data) is None:
            raise ValidationError('Email invalide! Veuillez en choisir un autre.')

    def validate_Etat(self, field):
        if not 1>= int(field.data) >= 0:
            raise ValidationError('Veuillez choisir une option valide.')

    def validate_Cin(self,field):
        pass

    def validate_Prenom(self,field):
        pass

    def validate_Code(self,field):
        pass

    def validate_Tel(self,field):
        pass


class EmpStation(FlaskForm):
    Code = StringField('Code :', id="codeEmp", validators=[DataRequired()])
    Cin = StringField('Cin :', id="Cin", validators=[DataRequired(), length(8), Regexp(regex=r'^[0-9]{8}$', message='Seuls les chiffres sont autorisés')])
    Nom = StringField('Nom :', id="Nom", validators=[DataRequired(), length(min=3, max=25), Regexp(regex=r'^[A-Za-z ]+$', message='Seules les lettres sont autorisées')])
    Prenom = StringField('Prenom :', id="Prenom", validators=[DataRequired(), length(min=3, max=25), Regexp(regex=r'^[A-Za-z ]+$', message='Seules les lettres sont autorisées')])
    Tel = StringField('Telephone :', id="Tel", validators=[DataRequired(), length(8), Regexp(regex=r'^[0-9]{8}$', message='Seuls les chiffres sont autorisés')])
    Date = StringField('Date de Naissance :', id="Date", validators=[DataRequired()])
    Groupe = SelectField('Groupe :', coerce=int, validators=[InputRequired()])
    Sal = StringField('Salaire :', id="Sal", validators=[DataRequired()])
    Role = SelectField('Role :', coerce=int, validators=[InputRequired()])
    Stat = SelectField('Station :', coerce=int, validators=[InputRequired()])

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

    def validate_Stat(self, field):
        Gp = Station.query.filter_by(idStation=field.data).first()
        if not Gp:
            raise ValidationError('Veuillez choisir une option valide.')

    def fill_choice_stat(self):
        Gp = list(Station.query.with_entities(Station.idStation, Station.NomStation).all())
        self.Stat.choices = ([(0, '-- sélectionnez une option --')]) + ([i for i in Gp])

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
    Groupe = SelectField('Station :', coerce=int, validators=[InputRequired()])

    def validate_Groupe(self, field):
        Gp = Station.query.filter_by(idStation=field.data).first()
        if not Gp:
            raise ValidationError('Veuillez choisir une option valide.')

    def fill_choice_groupe(self):
        Gp = list(Station.query.with_entities(Station.idStation, Station.NomStation).all())
        self.Groupe.choices = ([(0, '-- sélectionnez une option --')]) + ([i for i in Gp])