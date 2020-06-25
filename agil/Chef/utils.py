from agil.Main.utils import FormatString
from agil.models.Employee import Employee
from agil.models.User import User
from wtforms import ValidationError
from datetime import datetime
import collections
import string
import secrets


def truncate(st, width):
    if len(st) > width:
        st = st[:width] + ' ...'
    return st


def currentDateTime():
    import datetime
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def verifDate(Date):
    import datetime
    try:
        isValid = True
        inputDate = FormatString(Date)
        year, month, day = inputDate.split('-')
        datetime.datetime(int(year), int(month), int(day))
    except ValueError:
        isValid = False

    return isValid


def currentDate():
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d")


def days_between(d2):
    Test = False
    d1 = datetime.strptime(str(currentDate()), "%Y-%m-%d")
    d2 = datetime.strptime(str(d2), "%Y-%m-%d")
    if (d2 - d1).days > 0:
        Test = True
    return Test


def date_check(d2):
    Test = False
    d1 = datetime.strptime(str(currentDate()), "%Y-%m-%d")
    d2 = datetime.strptime(str(d2), "%Y-%m-%d")
    if (d2 - d1).days >= 0:
        Test = True
    return Test


def days_calc(d1,d2):
    d1 = datetime.strptime(str(d1), "%Y-%m-%d")
    d2 = datetime.strptime(str(d2), "%Y-%m-%d")
    return (d2 - d1).days


def addDay():
    import datetime
    return datetime.datetime.strptime(currentDate(), "%Y-%m-%d") + datetime.timedelta(days=7)


def generate():
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(15))


def validation(String):
    j = i = 0
    st = String.strip()
    lg = len(st)
    while True and (i < lg):
        if st[i] == " " and st[i + 1] == " ":
            j += 2
        if j == 2:
            raise ValidationError('Un seul espace entre chaque mot.')
        i += 1


def remplire_field_recetteLavage(form, RLavage):
    form.Matricule.data = RLavage.MatriculeVoiture
    form.Date.data = RLavage.DateLavage
    form.Debut.data = RLavage.HeureDebut
    form.Fin.data = RLavage.HeureFin
    form.Type.data = RLavage.idLavage
    form.kilometrage.data = RLavage.Kilometrage
    form.Prix.data = RLavage.PrixLavage
    form.Groupe.data = RLavage.idGroupe


def get_field_recetteLavage(form, RLavage):
    RLavage.MatriculeVoiture = form.Matricule.data
    RLavage.DateLavage = form.Date.data
    RLavage.HeureDebut = form.Debut.data
    RLavage.HeureFin = form.Fin.data
    RLavage.idLavage = form.Type.data
    RLavage.Kilometrage = form.kilometrage.data
    RLavage.PrixLavage = form.Prix.data
    RLavage.idGroupe = form.Groupe.data


def get_recette_lavage_data(records):
    recordObject = []
    if records:
        for record in records:
            recordObject.append(
                (record.idRecetteLavage, record.MatriculeVoiture, "{}".format(record.DateLavage),record.Groupe.NomGroupe,
                 record.HeureDebut, record.HeureFin, "{} Km".format(record.Kilometrage), record.Lavage.TypeLavage,
                 "{} TND".format(record.PrixLavage)))
    return recordObject


def get_citerne_data(records):
    recordObject = []
    if records:
        for record in records:
            recordObject.append(
                (record.idCiterne, record.NomCiterne, record.VolumeCiterne, record.Val_Act_Citerne,
                 "{} %".format(record.Min_Val_Citerne), record.EtatCiterne, record.Carburant.NomCarburant))
    return recordObject


def remplire_field_one_citerne(form, Cit):
    form.Code.data = Cit.NomCiterne
    form.Car.data = Cit.Carburant.NomCarburant
    form.Volume.data = Cit.VolumeCiterne
    form.Min.data = Cit.Min_Val_Citerne
    form.Act.data = Cit.Val_Act_Citerne


def get_field_citerne(form, Cit):
    Cit.NomCiterne = form.Code.data
    Cit.VolumeCiterne = form.Volume.data
    Cit.Min_Val_Citerne = form.Min.data.replace(' %', '')
    Cit.EtatCiterne = form.Etat.data


def remplire_field_citerne(form, Cit):
    form.Code.data = Cit.NomCiterne
    form.Car.data = Cit.Carburant.NomCarburant
    form.Volume.data = Cit.VolumeCiterne
    form.Min.data = Cit.Min_Val_Citerne
    form.Act.data = Cit.Val_Act_Citerne
    form.Etat.data = str(Cit.EtatCiterne)


def get_pompe_data(records):
    recordObject = []
    if records:
        for record in records:
            recordObject.append((record.idPompe, record.NomPompe, record.EtatPompe))
    return recordObject


def get_field_pompe(form, Pmp):
    Pmp.NomPompe = form.Code.data
    Pmp.EtatPompe = form.Etat.data


def remplire_field_pompe(form, Pmp):
    form.Code.data = Pmp.NomPompe
    form.Etat.data = str(Pmp.EtatPompe)


def get_pompe_citerne_data(records):
    recordObject = []
    if records:
        for record in records:
            recordObject.append((record.id_citerne_has_pompe, record.Pompe.NomPompe, record.Citerne.NomCiterne,record.Citerne.Carburant.NomCarburant))
    return recordObject


def get_field_pompe_citerne(form, Pmp):
    Pmp.idPompe = form.Code.data
    Pmp.idCiterne = form.Cit.data


def remplire_field_pompe_citerne(form, Pmp):
    form.Code.data = Pmp.idPompe
    form.Cit.data = Pmp.idCiterne


def get_recette_carburant_data(records):
    recordObject = []
    if records:
        for record in records:
            recordObject.append(
                (record.idRecetteCarburant, record.Pompe.NomPompe, record.Citerne.NomCiterne,
                 '{} ({} {})'.format(record.Citerne.Carburant.NomCarburant, record.prixLitre, "TND/L"),
                 record.Voie.nomVoie, record.DateCarb, "{} - {}".format(int(record.indiceDeb),int(record.indiceFin)), record.Groupe.NomGroupe))
    return recordObject


def get_field_recetteCarb(form, RCarb):
    RCarb.idPompe = form.Pmp.data
    RCarb.idCiterne = form.Cit.data
    RCarb.idVoie = form.Voie.data
    RCarb.indiceDeb = form.IndDebut.data
    RCarb.indiceFin = form.IndFin.data
    RCarb.idGroupe = form.Groupe.data
    RCarb.PrixLitre = form.Prix.data
    RCarb.DateCarb = form.Date.data


def remplire_field_recetteCarb(form, RCarb):
    form.Pmp.data = RCarb.idPompe
    form.Voie.data = RCarb.idVoie
    form.IndDebut.data = int(RCarb.indiceDeb)
    form.IndFin.data = int(RCarb.indiceFin)
    form.Groupe.data = RCarb.idGroupe
    form.Prix.data = RCarb.prixLitre
    form.Date.data = RCarb.DateCarb


def FilterDataCarburant(data):
    src = collections.defaultdict(list)
    if data:
        for record in data:
            hello = {
                "Pompe": record.Pompe.NomPompe,
                "Groupe": record.Groupe.NomGroupe,
                "Citerne": record.Citerne.NomCiterne,
                "Voie": record.Voie.nomVoie,
                "Carburant": record.Citerne.Carburant.NomCarburant,
                "IndDepart": record.indiceDeb,
                "IndFin": record.indiceFin,
                "Litre": record.indiceFin - record.indiceDeb,
                "Prix": record.prixLitre,
                "Vente": (record.indiceFin - record.indiceDeb) * record.prixLitre,
                "Date": str(record.DateCarb)
            }
            if record.Pompe.NomPompe in src:
                src[record.Pompe.NomPompe].append(hello)
            else:
                src[record.Pompe.NomPompe] = [hello]

    return src


def get_employee_data(records):
    recordObject = []
    if records:
        for record in records:
            recordObject.append(
                (record.idEmp, record.codeEmp, record.cinEmp, record.nomEmp, record.prenomEmp, record.dateEmp,
                 record.Role.NomRole, record.Groupe.NomGroupe, '{} {}'.format(record.salEmp, "TND")))
    return recordObject


def FilterDataLavage(data):
    src = collections.defaultdict(list)
    if data:
        for record in data:
            hello = {
                "Groupe": record.Groupe.NomGroupe,
                "TypeLavage": record.Lavage.TypeLavage,
                "MatriculeVoiture": record.MatriculeVoiture,
                "HeureDebut": str(record.HeureDebut),
                "HeureFin": str(record.HeureFin),
                "DateLavage": str(record.DateLavage),
                "PrixLavage": float(record.PrixLavage),
            }
            if str(record.DateLavage) in src:
                src[str(record.DateLavage)].append(hello)
            else:
                src[str(record.DateLavage)] = [hello]

    return src


def FilterDataLavageVoiture(data):
    src = collections.defaultdict(list)
    if data:
        for record in data:
            hello = {
                "Groupe": record.Groupe.NomGroupe,
                "TypeLavage": record.Lavage.TypeLavage,
                "MatriculeVoiture": record.MatriculeVoiture,
                "HeureDebut": str(record.HeureDebut),
                "HeureFin": str(record.HeureFin),
                "DateLavage": str(record.DateLavage),
                "PrixLavage": float(record.PrixLavage),
            }
            if record.MatriculeVoiture in src:
                src[record.MatriculeVoiture].append(hello)
            else:
                src[record.MatriculeVoiture] = [hello]

    return src


def get_to_do_data(records):
    recordObject = []
    if records:
        for record in records:
            recordObject.append({
                "Id": record.idListUser,
                "Description": truncate(record.objListUser, 30),
                "Date": str(record.dateListUser),
                "Seen": record.stateListUser,
                "Deleted": record.delListUser
            })

    return recordObject


def get_expenses_data(records):
    recordObject = []
    if records:
        for record in records:
            recordObject.append(
                (record.idExpenses, record.dateExpenses, record.catExpenses, truncate(record.descExpenses, 30),
                 "{} TND".format(record.amExpenses))
            )
    return recordObject


def get_field_expenses(form, Exp):
    Exp.dateExpenses = form.Date.data
    Exp.catExpenses = FormatString(form.Cat.data)
    Exp.amExpenses = form.Mont.data
    Exp.descExpenses = FormatString(form.Desc.data)


def remplire_field_expenses(form, Exp):
    form.Date.data = Exp.dateExpenses
    form.Cat.data = Exp.catExpenses
    form.Mont.data = Exp.amExpenses
    form.Desc.data = Exp.descExpenses


def FilterDataExpenses(data):
    src = collections.defaultdict(list)
    if data:
        for record in data:
            hello = {
                "category": record.catExpenses,
                "Description": record.descExpenses,
                "Amount": record.amExpenses,
                "Date": str(record.dateExpenses)
            }
            if str(record.dateExpenses) in src:
                src[str(record.dateExpenses)].append(hello)
            else:
                src[str(record.dateExpenses)] = [hello]

    return src


def get_empStation_data(records):
    recordObject = []
    if records:
        for record in records:
            recordObject.append((record.idEmp, record.codeEmp, record.cinEmp, record.nomEmp, record.prenomEmp, record.Role.NomRole, record.Groupe.NomGroupe))
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


def get_absence_data(records):
    recordObject = []
    if records:
        for record in records:
            recordObject.append(
                (record.idAbsence, record.Employee.codeEmp, record.Employee.nomEmp,record.Employee.prenomEmp, record.Employee.cinEmp, record.Groupe.NomGroupe, record.DateAbsence))
    return recordObject


# Get data form update Absence field (Chef Station)
def get_field_absence(form, Abc):
    Abc.DateAbsence = FormatString(form.Date.data)
    Abc.DescAbsence = FormatString(form.Desc.data)


def remplire_field_absence(form, Abc):
    form.Date.data = Abc.DateAbsence
    form.Desc.data = Abc.DescAbsence
    form.Code.data = Abc.Employee.codeEmp


def FilterDataAbsence(data):
    src = collections.defaultdict(list)
    if data:
        for record in data:
            hello = {
                "Groupe": record.Groupe.NomGroupe,
                "Station": record.Station.NomStation,
                "Code": record.Employee.codeEmp,
                "Cin": record.Employee.cinEmp,
                "Nom": record.Employee.nomEmp,
                "Date": str(record.DateAbsence),
                "Prenom": record.Employee.prenomEmp
            }
            if str(record.DateAbsence) in src:
                src[str(record.DateAbsence)].append(hello)
            else:
                src[str(record.DateAbsence)] = [hello]

    return src


def FilterDataAbsenceEmployee(data):
    src = collections.defaultdict(list)
    if data:
        for record in data:
            hello = {
                "Groupe": record.Groupe.NomGroupe,
                "Code": record.Employee.codeEmp,
                "Cin": record.Employee.cinEmp,
                "Nom": record.Employee.nomEmp,
                "Date": str(record.DateAbsence),
                "Prenom": record.Employee.prenomEmp,
                "Station": record.Station.NomStation
            }
            if record.Station.NomStation in src:
                src[record.Station.NomStation].append(hello)
            else:
                src[record.Station.NomStation] = [hello]

    return src


def get_conge_data(records):
    recordObject = []
    if records:
        for record in records:
            recordObject.append(
                (record.idConge,record.Employee.codeEmp,record.Employee.cinEmp,record.Employee.nomEmp,record.Employee.prenomEmp,record.Groupe.NomGroupe,
                 record.TypeConge.typeConge,"{} - {}".format(record.DateDebConge,record.DateFinConge)))
    return recordObject


def get_field_conge(form, Abc):
    Abc.DateDebConge = FormatString(form.DatDeb.data)
    Abc.DateFinConge = FormatString(form.DatFin.data)
    Abc.DescConge = FormatString(form.Desc.data)
    Abc.idTypeConge = form.Type.data


def remplire_field_conge(form, Abc):
    form.DatDeb.data = Abc.DateDebConge
    form.DatFin.data = Abc.DateFinConge
    form.Desc.data = Abc.DescConge
    form.Code.data = Abc.Employee.codeEmp
    form.Type.data = Abc.idTypeConge


def FilterDataConge(data):
    src = collections.defaultdict(list)
    if data:
        for record in data:
            hello = {
                "Groupe": record.Groupe.NomGroupe,
                "Station": record.Station.NomStation,
                "Code": record.Employee.codeEmp,
                "Cin": record.Employee.cinEmp,
                "Nom": record.Employee.nomEmp,
                "Prenom": record.Employee.prenomEmp,
                "TypeConge": record.TypeConge.typeConge,
                "Date": "{} - {}".format(str(record.DateDebConge),str(record.DateFinConge)),
                "Nbr": days_calc(record.DateDebConge,record.DateFinConge)
            }
            if record.Station.NomStation in src:
                src[record.Station.NomStation].append(hello)
            else:
                src[record.Station.NomStation] = [hello]

    return src


def get_conge_employee_data(records):
    recordObject = []
    if records:
        for record in records:
            recordObject.append({
                "Station": record.Station.NomStation,
                "Groupe": record.Groupe.idGroupe,
                "TypeConge": record.TypeConge.typeConge,
                "DateSortie": str(record.DateDebConge),
                "DateRetour": str(record.DateFinConge),
                "Nbr": days_calc(record.DateDebConge,record.DateFinConge)
            })
    return recordObject


def get_absence_employee_data(records):
    recordObject = []
    if records:
        for record in records:
            recordObject.append({
                "Date": str(record.DateAbsence),
                "Groupe": record.Groupe.idGroupe,
                "Station": record.Station.NomStation
            })
    return recordObject


def get_account_data(records):
    recordObject = []
    if records:
        recordObject.append((records.codeUser,records.cinUser,records.emailUser,records.nomUser,records.prenomUser,
                             records.telUser,str(records.dateUser),str(records.expiryCompte), records.Station.NomStation,
                             "{} Jour(s)".format(days_calc(currentDate(),records.expiryCompte))))
    return recordObject


def verifIdenditySettings(user,otherUser):
    if user and otherUser:

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


def get_field_account_settings(form, user):
    user.nomUser = FormatString(form.Nom.data).capitalize()
    user.prenomUser = FormatString(form.Prenom.data).capitalize()
    user.dateUser = form.Date.data
    user.telUser = form.Tel.data


def get_notification_data(records):
    recordObject = []
    if records:
        for record in records:
            recordObject.append({
                "Id": record.comment_id,
                "Description": truncate(record.comment_text, 60),
                "Date": pretty_date(record.comment_date),
                "Seen": record.comment_status,
                "Titre": record.comment_subject
            })
            
    return recordObject


def pretty_date(time):
    from datetime import datetime
    now = datetime.now()
    if not time:
        time = now
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(int(round((second_diff / 60),0))) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(int(round((second_diff / 3600),0))) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(int(round((day_diff / 7),0))) + " weeks ago"
    if day_diff < 365:
        return str(int(round((day_diff / 30),0))) + " months ago"

    return str(int(round((day_diff / 365),0))) + " years ago"
