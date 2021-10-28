from models import *

session = Session()
user1 = UserCreation(username="petro228",
                     firstName="Peter",
                     lastName="Dada",
                     email="petro.dada.hnm@lpnu.ua",
                     password="drowssap",
                     phone="88005553535",
                     userStatus=1,
                     TempId = 1)
user2 = User(id = 1,
                     username="petro228",
                     firstName="Peter",
                     lastName="Dada",
                     email="petro.dada.hnm@lpnu.ua",
                     password="drowssap",
                     phone="88005553535",
                     userStatus="1",
                     UserCreation_TempId=user1.TempId)
session.add(user1)
session.commit()
session.add(user2)
session.commit()
user3 = UserCreation(username="Peret1337",
                     firstName="Peret",
                     lastName="Nene",
                     email="Peret.Nene.hnm@lpnu.ua",
                     password="psadasd",
                     phone="88005553535",
                     userStatus=2,
                     TempId = 2)

user4 = User(id = 2,
                     username="Peret1337",
                     firstName="Peret",
                     lastName="Nene",
                     email="Peret.Nene.hnm@lpnu.ua",
                     password="psadasd",
                     phone="88005553535",
                     userStatus="2",
                     UserCreation_TempId=user3.TempId)

session.add(user3)
session.commit()
session.add(user4)
session.commit()

user5 = StudentCreation(
                    TempId ="1",
                    name = "Peter",
                    lastName = "Dada",
                    avarageMark = 88,
                    idOfUser = "1")
user6 = StudentCreation(
                    TempId ="2",
                    name = "Peret",
                    lastName = "Nene",
                    avarageMark = 20,
                    idOfUser = "2")


user7 = Student(
                    id = 1,
                    name = "Peter",
                    lastName = "Dada",
                    avarageMark = 88,
                    User_id = user2.id,
                    StudentCreation_TempId = user5.TempId)

user8 = Student(
                    id = 2,
                    name = "Peret",
                    lastName = "Nene",
                    avarageMark = 20,
                    User_id = user4.id,
                    StudentCreation_TempId = user6.TempId)

session.add(user5)
session.commit()
session.add(user6)
session.commit()
session.add(user7)
session.commit()
session.add(user8)
session.commit()
#print(session.query(User).all()[0])

#alembic upgrade head