from app import mysql
from app.models.user import User
from app.utils.jwt_utils import generate_token, validate_token
import bcrypt

class UserController:
    def login(self, nick, password):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE nick_user=%s", (nick,))
        user = cur.fetchone()
        cur.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[5].encode('utf-8')):
            user_obj = User(user[0], user[1], user[2], user[3], '', '')
            token = generate_token(user_obj)
            return {'token': token,
                    'message': 'Inicio de Sesión Satisfactorio'}
        else:
            return {'message': 'Credenciales inválidas'}

    @validate_token
    def register(self, user):
        try:
            hashed_password = bcrypt.hashpw(user.get_password().encode('utf-8'), bcrypt.gensalt())
            hashed_password_str = hashed_password.decode('utf-8')  # Convertir la contraseña encriptada a string para almacenarla

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO user (name_user, lastname_user, rol_user, nick_user, passw_user) VALUES (%s, %s, %s, %s, %s)", (user.get_name(), user.get_lastname(), user.get_rol(), user.get_nick(), hashed_password_str))
            
            if cur.rowcount == 0:  # Verificar si se insertó alguna fila
                mysql.connection.rollback()
                cur.close()
                return {'message': 'Error al registrar el usuario'}, 400
            
            mysql.connection.commit()
            cur.close()
            return {'message': 'Usuario registrado correctamente'}, 200

        except Exception as e:
            mysql.connection.rollback()  # Deshacer cualquier cambio en caso de error
            return {'message': 'Error al registrar el usuario', 'error': str(e)}, 500

    @validate_token
    def get_users_controller():
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT id_user, name_user, lastname_user, rol_user, nick_user FROM user")
            users = cur.fetchall()
            cur.close()
            
            user_list = [{"id": user[0], "name": user[1], "lastname": user[2], "rol": user[3], "nick": user[4]} for user in users]
            return user_list, 200
        
        except Exception as e:
            return {'message': 'Error al obtener los usuarios', 'error': str(e)}, 500

    @validate_token
    def update_user_controller(user):
        try:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE user SET name_user = %s, lastname_user = %s, rol_user = %s, nick_user = %s WHERE id_user = %s", (user.get_name(), user.get_lastname(), user.get_rol(), user.get_nick(), user.get_id()))
            
            if cur.rowcount == 0:  # Verificar si se actualizó alguna fila
                mysql.connection.rollback()
                cur.close()
                return {'message': 'No se encontró el usuario o no se realizaron cambios'}, 404
            
            mysql.connection.commit()
            cur.close()
            return {'message': 'Usuario actualizado exitosamente'}, 200

        except Exception as e:
            mysql.connection.rollback()  # Deshacer cualquier cambio en caso de error
            return {'message': 'Error al actualizar el usuario', 'error': str(e)}, 500
        
    @validate_token
    def update_password_user(self, id_user, current_passw, new_passw):
        try:
            hashed_password = bcrypt.hashpw(new_passw.encode('utf-8'), bcrypt.gensalt())
            hashed_password_str = hashed_password.decode('utf-8')  # Convertir la contraseña encriptada a string para almacenarla

            if self.validate_current_password(id_user, current_passw):
                cur = mysql.connection.cursor()
                cur.execute("UPDATE user SET passw_user = %s WHERE id_user = %s", (hashed_password_str, id_user))

                if cur.rowcount == 0:
                    mysql.connection.rollback() # Deshacer cualquier cambio en caso de error
                    cur.close()
                    return {'message': 'No se encontró el usuario o no se realizaron cambios'}, 404
                
                mysql.connection.commit()
                cur.close()
                return {'message': 'Contraseña actualizado correctamente'}, 200
            
            else:
                return {'message': 'Contraseña actual incorrecta'}

        except Exception as e:
            mysql.connection.rollback()  # Deshacer cualquier cambio en caso de error
            return {'message': 'Error al actualizar la contraseña', 'error': str(e)}, 500

    def validate_current_password(id_user, password):
        cur = mysql.connection.cursor()
        cur.execute("SELECT passw_user FROM user WHERE id_user=%s", (id_user))
        user = cur.fetchone()
        cur.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
            return True
        else:
            return False
        
    @validate_token
    def update_passw_with_admin(id_user, new_password):
        try:
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            hashed_password_str = hashed_password.decode('utf-8')  # Convertir la contraseña encriptada a string para almacenarla

            cur = mysql.connection.cursor()
            cur.execute("UPDATE user SET passw_user = %s WHERE id_user = %s", (hashed_password_str, id_user))

            if cur.rowcount == 0:
                mysql.connection.rollback() # Deshacer cualquier cambio en caso de error
                cur.close()
                return {'message': 'No se encontró el usuario o no se realizaron cambios'}, 404
                
            mysql.connection.commit()
            cur.close()
            return {'message': 'Contraseña actualizado correctamente'}, 200
        except Exception as e:
            mysql.connection.rollback()  # Deshacer cualquier cambio en caso de error
            return {'message': 'Error al actualizar la contraseña', 'error': str(e)}, 500

    @validate_token
    def delete_user(id_user):
        try:
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM user WHERE id_user = %s", (id_user))
            
            if cur.rowcount == 0:  # Verificar si se eliminó alguna fila
                mysql.connection.rollback()
                cur.close()
                return {'message': 'Usuario no encontrado o no eliminado'}, 404
            
            mysql.connection.commit()
            cur.close()
            return {'message': 'Usuario eliminado correctamente'}, 200

        except Exception as e:
            mysql.connection.rollback()  # Deshacer cualquier cambio en caso de error
            return {'message': 'Error al eliminar el usuario', 'error': str(e)}, 500
            
        

