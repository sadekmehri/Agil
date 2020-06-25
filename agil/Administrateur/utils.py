from wtforms import ValidationError
from agil.Chef.utils import currentDate, days_calc
from agil.Main.utils import FormatString
from agil.models.Employee import Employee
from agil.models.User import User


def get_carburant_data(records):
    recordObject = []
    if records:
        for record in records:
            recordObject.append((record.idCarburant, record.NomCarburant, "{} TND".format(record.PrixCarburant)))
    return recordObject


def get_station_data(records):
    recordObject = []
    if records:
        for record in records:
            recordObject.append((record.idStation, record.NomStation, record.AdrStation,record.Delegation.nomDelegation, record.Delegation.Ville.NomVille))
    return recordObject


def remplire_field_station(form, St):
    form.Nom.data = St.NomStation
    form.Adr.data = St.AdrStation
    form.Del.data = St.idDelegation
    form.Ville.data = St.Delegation.idVille


def get_field_station(form, St):
    St.NomStation = form.Nom.data.capitalize()
    St.AdrStation = form.Adr.data.capitalize()
    St.idDelegation = form.Del.data


def remplire_field_carburant(form, Carburant):
    form.Type.data = Carburant.NomCarburant
    form.Prix.data = Carburant.PrixCarburant


def get_field_carburant(form, Carburant):
    Carburant.NomCarburant = FormatString(form.Type.data).capitalize()
    Carburant.PrixCarburant = form.Prix.data


def get_account_data(records):
    recordObject = []
    if records:
        for record in records:
            recordObject.append((record.idUser, record.codeUser, record.nomUser,record.prenomUser, record.emailUser,
                                 record.expiryCompte,record.Station.NomStation,record.etatCompte))
    return recordObject


def remplire_field_account(form, user):
    form.Code.data = user.codeUser
    form.Nom.data = user.nomUser
    form.Prenom.data = user.prenomUser
    form.Cin.data = user.cinUser
    form.Date.data = user.dateUser
    form.Email.data = user.emailUser
    form.Tel.data = user.telUser
    form.Station.data = user.idStation
    form.Etat.data = str(user.etatCompte)


def verifIdendity(user,otherUser):
    if user and otherUser:

        if user.cinUser != otherUser.cinUser:
            emp = User.query.filter(User.cinUser == otherUser.cinUser).first()
            if emp:
                raise ValidationError("Cin existe déjà, veuillez réessayer")

        if user.codeUser != otherUser.codeUser:
            emp = User.query.filter(User.codeUser == otherUser.codeUser).first()
            if emp:
                raise ValidationError("Code chef existe déjà, veuillez réessayer")

        if user.emailUser != otherUser.emailUser:
            emp = User.query.filter(User.emailUser == otherUser.emailUser).first()
            if emp:
                raise ValidationError("L'e-mail existe déjà, veuillez réessayer")

        if user.telUser != otherUser.telUser:
            emp = User.query.filter(User.telUser == otherUser.telUser).first()
            if emp:
                raise ValidationError("Le téléphone existe déjà, veuillez réessayer")

        if user.prenomUser != otherUser.prenomUser or user.nomUser != otherUser.nomUser:
            Gp = User.query.filter(User.nomUser == otherUser.nomUser,User.prenomUser == otherUser.prenomUser).first()
            if Gp:
                raise ValidationError("L'utilisateur existe déjà, veuillez réessayer")
    else:
        raise ValidationError("Erreur, veuillez réessayer")


def get_field_account(form, user):
    user.codeUser = form.Code.data
    user.nomUser = FormatString(form.Nom.data).capitalize()
    user.prenomUser = FormatString(form.Prenom.data).capitalize()
    user.cinUser = form.Cin.data
    user.dateUser = form.Date.data
    user.emailUser = form.Email.data
    user.telUser = form.Tel.data
    user.idStation = form.Station.data
    user.etatCompte = str(form.Etat.data)


def get_empStation_data(records):
    recordObject = []
    if records:
        for record in records:
            recordObject.append((record.idEmp, record.codeEmp, record.cinEmp, record.nomEmp, record.prenomEmp, record.Role.NomRole, record.Station.NomStation))
    return recordObject


def remplire_field_employee(form, emp):
    form.Cin.data = emp.cinEmp
    form.Code.data = emp.codeEmp
    form.Date.data = emp.dateEmp
    form.Tel.data = emp.telEmp
    form.Groupe.data = emp.idGroupe
    form.Role.data = emp.idRole
    form.Nom.data = emp.nomEmp
    form.Prenom.data = emp.prenomEmp
    form.Stat.data = emp.idStation
    form.Sal.data = emp.salEmp


def get_field_employee(form, emp):
    emp.cinEmp = form.Cin.data
    emp.codeEmp = form.Code.data
    emp.dateEmp = form.Date.data
    emp.telEmp = form.Tel.data
    emp.idGroupe = form.Groupe.data
    emp.idRole = form.Role.data
    emp.nomEmp = form.Nom.data.capitalize()
    emp.prenomEmp = form.Prenom.data.capitalize()
    emp.idStation = form.Stat.data
    emp.salEmp = form.Sal.data


def verifIdendityEmpStation(user,otherUser):

    if user and otherUser:

        if user.cinEmp != otherUser.cinEmp:
            emp = Employee.query.filter(Employee.cinEmp == otherUser.cinEmp).first()
            if emp:
                raise ValidationError("Cin existe déjà, veuillez réessayer")

        if user.codeEmp != otherUser.codeEmp:
            emp = Employee.query.filter(Employee.codeEmp == otherUser.codeEmp).first()
            if emp:
                raise ValidationError("Code Employé existe déjà, veuillez réessayer")

        if user.telEmp != otherUser.telEmp:
            emp = Employee.query.filter(Employee.telEmp == otherUser.telEmp).first()
            if emp:
                raise ValidationError("Le téléphone existe déjà, veuillez réessayer")

        if user.prenomEmp != otherUser.prenomEmp or user.nomEmp != otherUser.nomEmp:
            Gp = Employee.query.filter(Employee.nomEmp == otherUser.nomEmp, Employee.prenomEmp == otherUser.prenomEmp).first()
            if Gp:
                raise ValidationError("Employé existe déjà, veuillez réessayer")
    else:
        raise ValidationError("Erreur, veuillez réessayer")


def get_account_data_setting(records):
    recordObject = []
    if records:
        recordObject.append((records.codeUser,records.cinUser,records.emailUser,records.nomUser,records.prenomUser,
                             records.telUser,str(records.dateUser),str(records.expiryCompte), records.Station.NomStation,
                             "{} Jour(s)".format(days_calc(currentDate(),records.expiryCompte))))
    return recordObject
