from .entities.User import User
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy


class ModelUser():

    @classmethod
    def login(cls, db, usuarios):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, email, password, name, role FROM usuarios WHERE email = '{}'".format(usuarios.email)
            #print(sql)

            cursor.execute(sql)
            row = cursor.fetchone()

            if row != None:
                hashed_password = row[2]
                #input_password = str(usuarios.password)
                if User.check_password(hashed_password, usuarios.password):
                    logged_user = User(row[0], row[1], hashed_password, row[3])
                    #print(row[2], usuarios.password)
                    return logged_user
            else:
                return None
        except Exception as ex:
            #print("Error: ", ex)
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, name, email, role FROM usuarios WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_by_email(cls, db, email):
        return db.session.query(cls).filter_by(email=email).first()
