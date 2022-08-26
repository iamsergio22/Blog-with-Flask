from .entities.User import User

class ModelUser():
    
    @classmethod
    def login(self,conn,user):
        try:
            cur=conn.cursor()
            cur.execute("SELECT id, nombre, password1 FROM users WHERE nombre='{}'".format(user.username))
            row=cur.fetchone()
            if row != None:
                user=User(row[0],row[1],User.check_password(row[2],user.password))
                return user
            else:
                return None
        except Exception as ex: 
            raise Exception(ex)
        
    @classmethod
    def get_by_id(self,conn,user):
        try:
            cur=conn.cursor()
            cur.execute("SELECT id, nombre, password1 FROM users WHERE id='{}'".format(id))
            row=cur.fetchone()
            if row != None:
                user=User(row[0],row[1],None)
                return user
            else:
                return None
        except Exception as ex: 
            raise Exception(ex)
    