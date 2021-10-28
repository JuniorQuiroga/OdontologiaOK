from flask import Flask, json, jsonify, request, Response

from flask_cors import CORS
from flaskext.mysql import MySQL
from config import config
import uuid
from http import cookies
import traceback

app = Flask(__name__)
cors = CORS(app,supports_credentials=True)
mysql = MySQL()
mysql.init_app(app)

# conecta con la base de datos y devuelve un cursor para hacer consultas
def get_cursor():
    con = mysql.connect()
    return con.cursor()


# agarra un usuario, crea un token, lo sube a la base de datos y lo retorna
def gen_token(usuario):
    con = mysql.connect()
    cursor = con.cursor()

    token = str(uuid.uuid4())
    
    cursor.execute("insert into Token  (idPaciente,token) values ({0}, '{1}') ".format(usuario,token))
    con.commit()

    return token



# Registrarse ----------------------------------------------------------
# maneja las peticiones de registro 
# recibe un JSON con los datos del formulario de la web y los inserta en la base de datos 
@app.route('/register', methods=['Post'])
def register():
    try:
        # conecta con la BD y crea un cursor
        con = mysql.connect()
        cursor = con.cursor()

        if request.json['obra_social'] == "false":
            # se genera la consulata, se ejecuta y se confirma
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



# Obras sociales -------------------------------------------------------
# retorna la lista de nombres de las obras sociales junto con su id
# para poder mostrarlos en la lista de opciones en la web
@app.route('/get_social', methods=['Get'])
def get_obra_social():
    try:
        # conecta con la BD y crear un cursor para hacer consultas
        cursor = get_cursor()
        consulta = "select idObraSocial, nombre from Obra_Social"
        cursor.execute(consulta)

        # gurda la respuesta de la consulata en una tupla y se convierte en un JSON
        datos = cursor.fetchall()

        # crea un diccionario con todos los datos de la tupla
        obras_sociales = []
        for fila in datos:
            obras_sociales.append({'idObraSocial':fila[0],'nombre':fila[1]})

        return jsonify(obras_sociales)
    except Exception as ex:
            traceback.print_exc()
            return jsonify({'mensaje':'Error (login): obraSocial fallida'}),500



# Login -------------------------------------------------------
@app.route('/login', methods=['post'])
def Login():
    #print (request.json["email"],request.json["contrasenia"])
    
    try:
        # conecta con la BD y crear un cursor para hacer consultas
        cursor = get_cursor()
        consulta = "select idPaciente from Paciente where email = '{0}' and contrasenia = '{1}'".format(request.json["email"],request.json["contrasenia"])
        cursor.execute(consulta)

        # gurda la respuesta de la consulata en una tupla y se convierte en un JSON
        datos = cursor.fetchone()
        #print(datos)
        

        response = Response()
        if datos != None:
            response.headers['set-cookie']= "token="+gen_token(datos[0])+"; Max-Age=3600; Path=/"
            response.headers['ContentType']= 'application/json'
            response.response = json.dumps({'loged':True})
            response.status_code = 200

        else:
            response.headers['ContentType']= 'application/json'
            response.response = json.dumps({'loged':False})
            response.status_code = 401
        return response 

    except Exception as ex:
            traceback.print_exc()
            return jsonify({'mensaje':'Error (login): login fallido'}),500
 

# SACAR TURNO ########################################################## 
# Especialidades para turno --------------------------------------------
@app.route('/get_especialidad', methods=['Get'])
def get_especialidad():
    try:
        # conecta con la BD y crear un cursor para hacer consultas
        #con = mysql.connect(use)
        cursor = get_cursor()
        consulta = "select idEspecialidad, nombre from Especialidad"
        cursor.execute(consulta)

        # gurda la respuesta de la consulata en una tupla y se convierte en un JSON
        datos = cursor.fetchall()

        # crea un diccionario con todos los datos de la tupla
        especialidades = []
        for fila in datos:
            especialidades.append({'id':fila[0],'nombre':fila[1]})

        return jsonify(especialidades)

    except Exception as ex:
            traceback.print_exc()
            return jsonify({'mensaje':'Error (SacarEspecialidad): especialidad fallida'}),500



# Medico para turno --------------------------------------------
@app.route('/get_medico/<codigo>', methods=['Get'])
def get_medico(codigo):
    try:
        # conecta con la BD y crear un cursor para hacer consultas
        #con = mysql.connect(use)
        cursor = get_cursor()
        consulta = "select idMedico, nombre from Medico where especialidad={0}".format(codigo)
        cursor.execute(consulta)

        # gurda la respuesta de la consulata en una tupla
        datos = cursor.fetchall()

        # crea un diccionario con todos los datos de la tupla
        especialidades = []
        for fila in datos:
            especialidades.append({'id':fila[0],'nombre':fila[1]})

        return jsonify(especialidades),200

    except Exception as ex:
            traceback.print_exc()
            return jsonify({'mensaje':'Error (SacarTurnoMedico): medico fallido'}),500

@app.route('/sarasa', methods=['Get'])
def prueba():
    for header in request.headers:
        print(str(header))


# Horas para turno --------------------------------------------
@app.route('/get_hora/<codigo>', methods=['Get'])
def get_hora(codigo):
    try:
        dics={
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
        horasO=[]

        #a/m/d/ medico
        codigo_s = codigo.split("-")
        
        # conecta con la BD y crear un cursor para hacer consultas
        #con = mysql.connect(use)
        cursor = get_cursor()
        #devuelve los horarios ocupados
        consulta="select extract(hour from fechaAgenda),extract(minute from fechaAgenda)  from Turno where medico={3} and date(fechaAgenda) ='{0}/{1}/{2}';".format(codigo_s[0],codigo_s[1],codigo_s[2],codigo_s[3])
        #consulta = "SELECT EXTRACT(DAY FROM fechaAgenda) AS dia FROM Turno where medico={5} && fechaAgenda='{0}/{1}/{2} {3}:{4}'".format(codigo_s[0],codigo_s[1],codigo_s[2],codigo_s[3],codigo_s[4],codigo_s[5])
        cursor.execute(consulta)

        # gurda la respuesta de la consulata en una tupla 
        datos = cursor.fetchall()
        print(datos)
        for fila in datos: #pasamos la tupla datos a la lista horasO
            horasO.append(fila)

        for turno in horasO: #quitamos de dics las horasO
            if turno[1] == 0:
                dics.pop("{0}:{1}0".format(turno[0],turno[1]))
            else:
                dics.pop("{0}:{1}".format(turno[0],turno[1]))

        ocupadas = []
        for hora in dics.keys():
            ocupadas.append({'id':hora,'nombre':hora})

        return jsonify(ocupadas),200
        #return jsonify(datos)

    except Exception as ex:
            traceback.print_exc()
            return jsonify({'mensaje':'Error (SacarTurnoHora): hora fallida'}),500



# Registra el turno --------------------------------------------
@app.route('/sacar_turno', methods=['Post'])
def sacar_turno():
    try:
        # conecta con la BD y crear un cursor para hacer consultas
        con = mysql.connect()
        cursor = con.cursor()

        auth = request.headers.get('Autorization')
        cursor.execute("select idPaciente from Token where token = '{0}'".format(auth))
        paciente = cursor.fetchone()[0]

        consulta = """insert into Turno (paciente,medico,fechaAgenda,fechaTurno,motivo,requisitos) 
                                values ({0},{1},'{2}-{3}-{4} {5}:00',now(),'{6}',null) """.format(
                                    paciente,
                                    request.json["medico"],
                                    request.json["anio"],
                                    request.json["mes"],
                                    request.json["dia"],
                                    request.json["hora"],
                                    request.json["motivo"],
                                    )
        
        cursor.execute(consulta)
        con.commit()
        
        return jsonify({'mensaje':"turno registrado"}),200

    except Exception as ex:
            traceback.print_exc()
            return jsonify({'mensaje':'Error (SacarTurnoHora): hora fallida'}),500



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
