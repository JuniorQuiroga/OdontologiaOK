from itertools import cycle
from flask import Flask, json, jsonify, request, Response
from flask_cors import CORS
from flaskext.mysql import MySQL
from config import config
import uuid

import traceback
import smtplib
import random
import string
import re

app = Flask(__name__)
cors = CORS(app,supports_credentials=True)
mysql = MySQL()
mysql.init_app(app)

# conecta con la base de datos y devuelve un cursor para hacer consultas
def get_cursor():
    con = mysql.connect()
    return con.cursor()

# recibe un usuario, crea un token, lo sube a la base de datos y lo retorna
def gen_token(usuario,tipo):
    con = mysql.connect()
    cursor = con.cursor()

    # genera una clave unica
    token = str(uuid.uuid4())
    
    # si es paciente ingresa la clave en la tabla correspondiente
    # sino en la de medicos
    if tipo == 'paciente':
        cursor.execute("insert into Token  (idPaciente,token) values ({0}, '{1}') ".format(usuario,token))
    else: 
        cursor.execute("insert into Token_Medico  (idMedico,token) values ({0}, '{1}') ".format(usuario,token))
    con.commit()

    # retorna la clave
    return token




# recibe un usuario, crea un token, lo sube a la base de datos y lo retorna
def gen_token(usuario,tipo):
    con = mysql.connect()
    cursor = con.cursor()

    # genera una clave unica
    token = str(uuid.uuid4())
    
    # si es paciente ingresa la clave en la tabla correspondiente
    # sino en la de medicos
    if tipo == 'paciente':
        cursor.execute("insert into Token  (idPaciente,token) values ({0}, '{1}') ".format(usuario,token))
    else: 
        cursor.execute("insert into Token_Medico  (idMedico,token) values ({0}, '{1}') ".format(usuario,token))
    con.commit()

    # retorna la clave
    return token



@app.route('/mandarCodigo', methods=['POST']) #manda un codigo al mail que se ingrese
def mandarCodigo():
    length_of_string = 8 #genera un codigo alfanumerico random de 8 caracteres
    codigo=(''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length_of_string)))

    gmail_user = 'mailCentroOdontologico@gmail.com' #mail desde el que mandamos el mail
    gmail_password = 'papaya_2003'

    mail= request.json['email']
    sent_from = gmail_user
    to = mail
    subject = 'Codigo de recuperacion'
    body = "Su codigo es: "+codigo

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)#se loguea en gmail
        server.sendmail(sent_from, to, email_text)#manda el mail
        server.close()

        try:
            cursor = get_cursor()
            consulta = "select idMedico from Medico where email = '{0}'".format(request.json["email"])
            cursor.execute(consulta)

            # gurda la respuesta de la consulata en una tupla y se convierte en un JSON
            datos = cursor.fetchone()
            print(datos)
            response = Response()
            if(datos != None):
                # se rellena la respuesta con 
                # el token correspondiente en un header
                # un indicador de que se logueo con exito y que es un medico
                response.headers['set-cookie']= "mail="+mail+"; Max-Age=3600; Path=/"
                #response.headers['set-cookie']="codigo="+codigo+"; Max-Age=3600; Path=/"
                response.headers['ContentType']= 'application/json'
                response.response = json.dumps({'mail':mail})#,{'codigo':codigo})
                response.status_code = 200
            else:
                consulta = "select idPaciente from Paciente where email = '{0}'".format(request.json["email"])
                cursor.execute(consulta)
                datos=cursor.fetchone()

                # si se reciben datos se considera que es un paciente
                if(datos != None):
                    # se rellena la respuesta con 
                    # el token correspondiente en un header
                    # un indicador de que se logueo con exito y que es un paciente
                    response.headers['set-cookie']= "mail="+mail+","+codigo+";Max-Age=3600; Path=/"
                                            
                    response.headers['ContentType']= 'application/json'
                    response.response = json.dumps({'mail':mail,'codigo':codigo})
                    response.status_code = 200
                else:
                    # se indica que no se logueo y un codigo de autenticacion fallida
                    response.headers['ContentType']= 'application/json'
                    response.response = json.dumps({'mail':mail})
                    response.status_code = 401
            return response

        except Exception as ex:
            traceback.print_exc()
            return jsonify({'mensaje':'Error al guardar coockie'})   

    except Exception as ex:
        traceback.print_exc()
        return jsonify({'mensaje':'Error al mandar el mail'})
#Actualiza la contrasenia-------------------------------------------
@app.route('/cambiar/<codigo>', methods=['PUT'])
def ActualizarContrasenia(codigo):
    try:
        con = mysql.connect()
        cursor = con.cursor()
        mail= codigo.split("_")[0]
        contra= codigo.split("_")[1]    
        consulta = "update Paciente set contrasenia  = '"+contra+"' where email = '"+mail+"'"
        cursor.execute(consulta)
        con.commit()
        return jsonify({'mensaje':'Contrasenia actualizada exitosamente'})
    
    except Exception as ex:
        traceback.print_exc()  
        return jsonify({'mensaje':'Error actualizar contrasenia'})



# Obras sociales -------------------------------------------------------
# retorna la lista de nombres de las obras sociales junto con su id
# para poder mostrarlos en la lista de opciones en la web
@app.route('/get_social', methods=['get'])
def get_obra_social():
    try:
        # conecta con la BD y crear un cursor para pedir las obras sociales
        cursor = get_cursor()
        consulta = "select idObraSocial, nombre from Obra_Social"
        cursor.execute(consulta)

        # guarda la respuesta de la consulata y se convierte en un JSON
        datos = cursor.fetchall()

        # crea una lista para almacenar todos los datos recibidos
        obras_sociales = []
        for fila in datos:
            obras_sociales.append({'idObraSocial':fila[0],'nombre':fila[1]})

        # se devuelve un JSON con toda la informacion recibida al frontend
        return jsonify(obras_sociales)

    except Exception as ex:
            traceback.print_exc()
            return jsonify({'mensaje':'Error (login): obraSocial fallida'}),500



# Registrarse ----------------------------------------------------------
# maneja las peticiones de registro 
# recibe un JSON con los datos del formulario de la web y los inserta en la base de datos 
@app.route('/register', methods=['post'])
def register():
    try:
        # conecta con la BD y crea un cursor
        con = mysql.connect()
        cursor = con.cursor()

        # si no tiene obra social se carga el resto de datos y se omite ese atributo
        if request.json['obra_social'] == "false":
            consulta = "Insert into Paciente(nombre,apellido,email,contrasenia,dni,telefono,direccion) values ('{0}','{1}','{2}','{3}',{4},{5},'{6}')".format(
                                                                                            request.json['nombre'],
                                                                                            request.json['apellido'],
                                                                                            request.json['email'],
                                                                                            request.json['contrasenia'],
                                                                                            request.json['dni'],
                                                                                            request.json['telefono'],
                                                                                            request.json['direccion'])
        else:
            consulta = "Insert into Paciente(nombre,apellido,email,contrasenia,dni,telefono,direccion,obraSocial) values ('{0}','{1}','{2}','{3}',{4},{5},'{6}','{7}')".format(
                                                                                            request.json['nombre'],
                                                                                            request.json['apellido'],
                                                                                            request.json['email'],
                                                                                            request.json['contrasenia'],
                                                                                            request.json['dni'],
                                                                                            request.json['telefono'],
                                                                                            request.json['direccion'],
                                                                                            request.json['obra_social'])
        cursor.execute(consulta)
        con.commit()
        
        # devuelve un mensaje en formato JSON
        return jsonify({'mensaje':'Paciente registrado exitosamente'})

    # en caso de error devuelve un mensaje en formato JSON
    except Exception as ex:
            traceback.print_exc()
            return jsonify({'mensaje':'Error (Register): registro fallido'}),500



# Login -------------------------------------------------------
@app.route('/login', methods=['post'])
def Login():
    try:
        # conecta con la BD y crear un cursor para hacer consultas
        # se verifica si la cuenta y la contrasenia son de un medico
        cursor = get_cursor()
        consulta = "select idMedico from Medico where email = '{0}' and contrasenia = '{1}'".format(request.json["email"],request.json["contrasenia"])
        cursor.execute(consulta)

        # gurda la respuesta de la consulata en una tupla y se convierte en un JSON
        datos = cursor.fetchone()

        response = Response() #crea una respuesta para el frontend

        # si se reciben datos se entiende que es un medico
        if(datos != None):
            # se rellena la respuesta con 
            # el token correspondiente en un header
            # un indicador de que se logueo con exito y que es un medico
            response.headers['set-cookie']= "token="+gen_token(datos[0],"medico")+"; Max-Age=3600; Path=/"
            response.headers['ContentType']= 'application/json'
            response.response = json.dumps({'loged':True, 'paciente':False})
            response.status_code = 200

        else:
            # se verifica si la cuenta y la contrasenia son de un paciente
            consulta = "select idPaciente from Paciente where email = '{0}' and contrasenia = '{1}'".format(request.json["email"],request.json["contrasenia"])
            cursor.execute(consulta)
            datos=cursor.fetchone()
            
            # si se reciben datos se considera que es un paciente
            if(datos != None):
                # se rellena la respuesta con 
                # el token correspondiente en un header
                # un indicador de que se logueo con exito y que es un paciente
                response.headers['set-cookie']= "token="+gen_token(datos[0],"paciente")+"; Max-Age=3600; Path=/"
                response.headers['ContentType']= 'application/json'
                response.response = json.dumps({'loged':True, 'paciente':True})
                response.status_code = 200
            else:
                # se indica que no se logueo y un codigo de autenticacion fallida
                response.headers['ContentType']= 'application/json'
                response.response = json.dumps({'loged':False})
                response.status_code = 401
        return response

    except Exception as ex:
            traceback.print_exc()
            return jsonify({'mensaje':'Error (login): login fallido'}),500
 


# SACAR TURNO ########################################################## 
# Especialidades para turno --------------------------------------------
@app.route('/get_especialidad', methods=['get'])
def get_especialidad():
    try:
        # conecta con la BD y crear un cursor para pedir las especialidades
        cursor = get_cursor()
        consulta = "select idEspecialidad, nombre from Especialidad"
        cursor.execute(consulta)
        datos = cursor.fetchall() # guarda la respuesta de la consulata

        # crea una lista y guarda la lista de especialidades
        especialidades = []
        for fila in datos:
            especialidades.append({'id':fila[0],'nombre':fila[1]})

        # se envian las especialidades al frontend en un JSON
        return jsonify(especialidades)

    except Exception as ex:
            traceback.print_exc()
            return jsonify({'mensaje':'Error (SacarEspecialidad): especialidad fallida'}),500



# Medico para turno --------------------------------------------
@app.route('/get_medico/<codigo>', methods=['get'])
def get_medico(codigo):
    try:
        # conecta con la BD y crear un cursor para pedir los medicos de una especialidad especifica
        cursor = get_cursor()
        consulta = "select idMedico, nombre from Medico where especialidad={0}".format(codigo)
        cursor.execute(consulta)
        datos = cursor.fetchall() # guarda los datos recibidos

        # crea una lista y guarda los datos recibidos 
        especialidades = []
        for fila in datos:
            especialidades.append({'id':fila[0],'nombre':fila[1]})

        # se envia al frontend en forma de JSON
        return jsonify(especialidades),200

    except Exception as ex:
            traceback.print_exc()
            return jsonify({'mensaje':'Error (SacarTurnoMedico): medico fallido'}),500

# Registra el turno --------------------------------------------
@app.route('/sacar_turno', methods=['post'])
def sacar_turno():
    try:
        # conecta con la BD y crear un cursor para hacer consultas
        con = mysql.connect()
        cursor = con.cursor()

        # guarda el header de autenticacion 
        # usa este para pedir la id del paciente en la BD
        auth = request.headers['Authorization']

        #intenta sacar un turno con el token de paciente
        try:
            cursor.execute("select idPaciente from Token where token = '{0}'".format(auth))
            paciente = cursor.fetchone()[0]

            if paciente!= None:
                # inserta un turno nuevo en la BD
                consulta = """insert into Turno (paciente,medico,fechaAgenda,fechaTurno,motivo,requisitos) 
                                        values ({0},{1},'{2} {3}:00',now(),'{4}',"ninguno") """.format(
                                            paciente,
                                            request.json["medico"],
                                            request.json["fecha"],
                                            request.json["hora"],
                                            request.json["motivo"]
                                            )
        except:
            #intenta sacar un turno con el token de medico
            try:
                cursor.execute("select idMedico from Token_Medico where token = '{0}'".format(auth))
                med = cursor.fetchone()[0]

                if med!= None:
                    # auth - dni fecha hora motivo requisitos
                    cursor.execute("select idPaciente from Paciente where dni = '{0}'".format(request.json["dni"]))
                    paciente = cursor.fetchone()[0]


                    # inserta un turno nuevo en la BD
                    consulta = """insert into Turno (paciente,medico,fechaAgenda,fechaTurno,motivo,requisitos) 
                                            values ({0},{1},'{2} {3}:00',now(),'{4}','{5}') """.format(
                                                paciente,
                                                med,
                                                request.json["fecha"],
                                                request.json["hora"],
                                                request.json["motivo"],
                                                request.json["requisitos"]
                                                )
            except Exception as ex:
                traceback.print_exc()
                return jsonify({'mensaje':'No se pudo encontrar ni medico ni paciente'}),500

            cursor.execute(consulta)
            con.commit()
        
            return jsonify({'mensaje':"turno registrado"}),200
        

    except Exception as ex:
            traceback.print_exc()
            return jsonify({'mensaje':'Error al registrar turno'}),500


# Horas para turno --------------------------------------------
@app.route('/get_hora/<codigo>', methods=['get'])
def get_hora(codigo):
    try:
        # diccionario que guarda todas las horas disponibles del dia
        horas={
        "09:00":"0",
        "09:30":"0",
        "10:00":"0",
        "10:30":"0",
        "11:00":"0",
        "11:30":"0",
        "12:00":"0",
        "12:30":"0",
        "13:00":"0",
        "13:30":"0",
        "14:00":"0",
        "14:30":"0",
        "15:00":"0",
        "15:30":"0",
        "16:00":"0",
        "16:30":"0",
        "17:00":"0",
        "17:30":"0",
        "18:00":"0",
        }
        auth = request.headers['Authorization']
        # conecta con la BD y crear un cursor para hacer consultas
        cursor = get_cursor()

        # informacion recibida del frontend en forma de string con formato a-m-d-medico
        codigo_s = codigo.split("_")

        # intenta hacer un select con el codigo dividido sino usa el codigo y la autorizacion
        try:
            #devuelve los horarios ocupados  del dia y doctor especificado
            consulta="select extract(hour from fechaAgenda),extract(minute from fechaAgenda)  from Turno where medico={1} and date(fechaAgenda) ='{0}';".format(codigo_s[0],codigo_s[1])
        except:
            try:
                cursor.execute("select idMedico from Token_Medico where token = '{0}'".format(auth))
                med = cursor.fetchone()[0]
                consulta="select extract(hour from fechaAgenda),extract(minute from fechaAgenda)  from Turno where medico={1} and date(fechaAgenda) ='{0}';".format(codigo,med)
            except Exception as ex:
                traceback.print_exc()
                return jsonify({'mensaje':'Error (ver hora medico): medico hora'}),500

        cursor.execute(consulta)
        # gurda la respuesta de la consulta 
        datos = cursor.fetchall()
        

        # lista para almacenar las horas ocupadas
        horasO=[]
        #pasamos la tupla datos a la lista horasO
        for fila in datos: 
            horasO.append(fila)

        #quitamos del diccionario horas las horasO recuperadas de la BD
        for turno in horasO: 
            if len(str(turno[0]))==1:
                if turno[1] == 0:
                    horas.pop("0{0}:{1}0".format(turno[0],turno[1]))
                else:
                    horas.pop("0{0}:{1}".format(turno[0],turno[1]))
            else:
                if turno[1] == 0:
                    horas.pop("{0}:{1}0".format(turno[0],turno[1]))
                else:
                    horas.pop("{0}:{1}".format(turno[0],turno[1]))

        # lista final con las horas desocupadas 
        desocupadas = []
        for hora in horas.keys():
            desocupadas.append({'id':hora,'nombre':hora})

        # devuelve al frontend las horas desocupadas indicando que todo salio bien
        return jsonify(desocupadas),200

    except Exception as ex:
            traceback.print_exc()
            return jsonify({'mensaje':'Error (SacarTurnoHora): hora fallida'}),500



# Paciente - Ver turnos --------------------------------------------------
@app.route('/get_turno_paciente', methods=['get'])
def get_turnos_paciente():
    try:
        # conecta con la BD y crear un cursor para pedir los medicos de una especialidad especifica
        cursor = get_cursor()

        auth = request.headers['Authorization']
        print(auth)
        cursor.execute("select idPaciente from Token where token = '{0}'".format(auth))
        paciente = cursor.fetchone()
    
        #if paciente != None:
        try:
            turnos_paciente = []
            consulta = "select idTurno,fechaAgenda,motivo,requisitos from Turno where paciente = {0}".format(paciente[0])
            cursor.execute(consulta)
            datos = cursor.fetchall() # guarda los datos recibidos

            # crea una lista y guarda los datos recibidos 
            for fila in datos:
                turnos_paciente.append({'idTurno':fila[0],'fecha':fila[1],'motivo':fila[2],'requisitos':fila[3]})

        except Exception as ex:
            traceback.print_exc()
        
        # se envia al frontend en forma de JSON
        return jsonify(turnos_paciente),200
        
    except Exception as ex:
            traceback.print_exc()
            return jsonify({'mensaje':'Error (VerTurnosPaciente): no se pudieron mostrar los turnos'}),500



@app.route('/cancelar_turno_paciente/<codigo>', methods=['delete'])
def cancelar(codigo):
    try:
        # conecta con la BD y crear un cursor para pedir los medicos de una especialidad especifica
        con = mysql.connect()
        cursor = con.cursor()
        
        cursor.execute("DELETE FROM Turno WHERE idTurno = '{}'".format(codigo))
        con.commit()
        con.close()
        
        # se envia al frontend en forma de JSON
        return jsonify({'mensaje':'Turno cancelado'}),200
        
    except Exception as ex:
            traceback.print_exc()
            return jsonify({'mensaje':'Error (cancelar turno paciente): no se pudo cancelar el turno'}),500

@app.route('/editar_turno/<codigo>', methods=['put'])
def edit_turno(codigo):
    try:
        # turno fecha hora
        codigo_s = codigo.split("_")
        print(codigo_s)
        # conecta con la BD y crear un cursor para pedir los medicos de una especialidad especifica
        con = mysql.connect()
        cursor = con.cursor()

        cursor.execute("update Turno set fechaAgenda = '{0} {1}' where idTurno = '{2}'".format(codigo_s[0],codigo_s[1],codigo_s[2]))
        con.commit()
        con.close()
        return jsonify({'mensaje':'turno editado con exito'}),200

    except Exception as ex:
        traceback.print_exc()
        return jsonify({'mensaje':'Error (editar turno): no se pudo editar el turno'}),500



# Medico - Ver turnos --------------------------------------------------
@app.route('/get_turno_medico', methods=['get'])
def get_turnos_medico():
    try:
        # conecta con la BD y crear un cursor para pedir los medicos de una especialidad especifica
        cursor = get_cursor()

        auth = request.headers['Authorization']
        print(auth)
        cursor.execute("select idMedico from Token_Medico where token = '{0}'".format(auth))
        medico = cursor.fetchone()

        #if paciente != None:
        try:
            turnos_medico = []
            consulta = "select idTurno,fechaAgenda,motivo,requisitos from Turno where medico = {0}".format(medico[0])
            cursor.execute(consulta)
            datos = cursor.fetchall() # guarda los datos recibidos

            # crea una lista y guarda los datos recibidos 
            for fila in datos:
                turnos_medico.append({'idTurno':fila[0],'fecha':fila[1],'motivo':fila[2],'requisitos':fila[3]})

        except Exception as ex:
            traceback.print_exc()
            return jsonify({"mensaje":"Error (VerTurnosMedico): al recopilar turnos"}),500
        
        # se envia al frontend en forma de JSON
        return jsonify(turnos_medico),200
        
    except Exception as ex:
            traceback.print_exc()
            return jsonify({'mensaje':'Error (VerTurnosMedico): no se pudieron mostrar los turnos'}),500



# Registra el turno como medico
@app.route('/sacar_turno_medico', methods=['post'])
def sacar_turno_medico():
    try:
        # conecta con la BD y crear un cursor para hacer consultas
        con = mysql.connect()
        cursor = con.cursor()

        # guarda el header de autenticacion 
        # usa este para pedir la id del paciente en la BD
        auth = request.headers['Authorization']
        print(auth)
        cursor.execute("select idMedico from Token_Medico where token = '{0}'".format(auth))
        medico = cursor.fetchone()

        cursor.execute("select idPaciente from Paciente where dni = '{0}'".format(request.json["dni"]))
        paciente = cursor.fetchone()


        if medico!= None:
            # inserta un turno nuevo en la BD
            consulta = """insert into Turno (paciente,medico,fechaAgenda,fechaTurno,motivo,requisitos) 
                                    values ({0},{1},'{2} {3}:00',now(),'{4}','{5}') """.format(
                                        paciente[0],
                                        medico[0],
                                        request.json["fecha"],
                                        request.json["hora"],
                                        request.json["motivo"],
                                        request.json["requisitos"]
                                        )
            
            cursor.execute(consulta)
            con.commit()
        
            return jsonify({'mensaje':"turno registrado"}),200
        else:
            traceback.print_exc()
            return jsonify({'mensaje':"Error al registrar turno - no se encuentra medico"}),500

    except Exception as ex:
            traceback.print_exc()
            return jsonify({'mensaje':'Error al registrar turno'}),500



@app.route('/get_horas_modificar/<codigo>', methods=['get'])
def horas_modificar(codigo):
    try:
        codigo_s = codigo.split("_")
        # diccionario que guarda todas las horas disponibles del dia
        horas={
        "09:00":"0",
        "09:30":"0",
        "10:00":"0",
        "10:30":"0",
        "11:00":"0",
        "11:30":"0",
        "12:00":"0",
        "12:30":"0",
        "13:00":"0",
        "13:30":"0",
        "14:00":"0",
        "14:30":"0",
        "15:00":"0",
        "15:30":"0",
        "16:00":"0",
        "16:30":"0",
        "17:00":"0",
        "17:30":"0",
        "18:00":"0",
        }
        
        # conecta con la BD y crear un cursor para hacer consultas
        cursor = get_cursor()
        #devuelve los horarios ocupados  del dia y doctor especificado
        consulta="""SELECT extract(hour FROM fechaAgenda),extract(minute FROM fechaAgenda) FROM Turno 
                    WHERE medico = (SELECT medico from Turno WHERE idTurno = {0}) && date(fechaAgenda) = '{1}'""".format(codigo_s[0],codigo_s[1])
        cursor.execute(consulta)
        # gurda la respuesta de la consulta 
        datos = cursor.fetchall()
        
        # lista para almacenar las horas ocupadas
        horasO=[]
        #pasamos la tupla datos a la lista horasO
        for fila in datos: 
            horasO.append(fila)

        

        #quitamos del diccionario horas las horasO recuperadas de la BD
        for turno in horasO: 
            if len(str(turno[0]))==1:
                if turno[1] == 0:
                    horas["0{0}:{1}0".format(turno[0],turno[1])] = "1"
                else:
                    horas["0{0}:{1}".format(turno[0],turno[1])] = "1"
            else:
                if turno[1] == 0:
                    horas["{0}:{1}0".format(turno[0],turno[1])] = "1"
                else:
                    horas["{0}:{1}".format(turno[0],turno[1])] = "1"

        # lista final con las horas desocupadas 
        desocupadas = []
        i = 0
        for hora in horas.keys():
            desocupadas.append({'id':hora,'nombre':hora,'ocupado':horas[hora]})
            i+=1

        # devuelve al frontend las horas desocupadas indicando que todo salio bien
        return jsonify(desocupadas),200

    except Exception as ex:
            traceback.print_exc()
            return jsonify({'mensaje':'Error (Get hora turno modificar): no se pudo devolver la hora'}),500


# ERROR 404 ------------------------------------------------------------
def NotFoundView(error):
    return "<h1>La pagina a la que intenta acceder no existe</h1>",404



# MAIN -----------------------------------------------------------------
if __name__ == "__main__":
    #importa un archivo de configuracion
    app.config.from_object(config['develop'])
    
    #en caso de error 404 llama a NotFoundView()
    app.register_error_handler(404,NotFoundView)

    app.run(host="0.0.0.0")
