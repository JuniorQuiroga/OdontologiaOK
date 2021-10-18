from flask import Flask, json, jsonify, request, redirect
from flask_cors import CORS
from flaskext.mysql import MySQL
from config import config
import uuid
from http import cookies


app = Flask(__name__)
cors = CORS(app)
mysql = MySQL()
mysql.init_app(app)

# conecta con la base de datos y devuelve un cursor para hacer consultas
def get_cursor():
    con = mysql.connect()
    return con.cursor()


# genera un token unico para cada usuario
# al generarse se compara con todos los que se encuentren en la base de datos hasta el momento
# si está repetido, se vuelve a llamar a la función repitiendo el ciclo
def gen_token():
    token = str(uuid.uuid4())

    # pide todos los tokens de la base de datos y las almacena
    # devuelve una tupla => tokens_db[n][0] n+=1
    cursor = get_cursor()
    cursor.execute("select uuid from Paciente")
    tokens_db = cursor.fetchall()
    
    # si el token esta en la tupla se llama a si mismo
    # sino devuelve el token
    if token in tokens_db:
        gen_token()
    else:
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
            consulta = "Insert into Paciente(uuid,nombre,apellido,email,contrasenia,dni,telefono,direccion) values ('{0}','{1}','{2}','{3}','{4}',{5},{6},'{7}')".format(
                                                                                            gen_token(),
                                                                                            request.json['nombre'],
                                                                                            request.json['apellido'],
                                                                                            request.json['email'],
                                                                                            request.json['contrasenia'],
                                                                                            request.json['dni'],
                                                                                            request.json['telefono'],
                                                                                            request.json['direccion'])
        else:
            consulta = "Insert into Paciente(uuid,nombre,apellido,email,contrasenia,dni,telefono,direccion,obraSocial) values ('{0}','{1}','{2}','{3}','{4}',{5},{6},'{7}',{8})".format(
                                                                                            gen_token(),
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
            return jsonify({'mensaje':'Error (Insert): {0}'.format(ex)})



# Obras sociales -------------------------------------------------------
# retorna la lista de nombres de las obras sociales junto con su id
# para poder mostrarlos en la lista de opciones en la web
@app.route('/get_social', methods=['Get'])
def get_obra_social():
    # conecta con la BD y crear un cursor para hacer consultas
    cursor = get_cursor()
    consulta = "select idObraSocial, nombre from Obra_Social"
    cursor.execute(consulta)

    # gurda los datos de la consulata en una tupla
    # se envia a tuple_json() para crear un json  
    datos = cursor.fetchall()

    # crea un diccionario con todos los datos de la tupla
    obras_sociales = []
    for fila in datos:
        obras_sociales.append({'idObraSocial':fila[0],'nombre':fila[1]})

    return jsonify(obras_sociales)



# Login -------------------------------------------------------
@app.route('/login', methods=['post'])
def Login():
    print (request.json["email"],request.json["contrasenia"])
    try:
        # conecta con la BD y crear un cursor para hacer consultas
        cursor = get_cursor()
        consulta = "select uuid from Paciente where email = '{0}' and contrasenia = '{1}'".format(request.json["email"],request.json["contrasenia"])
        cursor.execute(consulta)

        # gurda los datos de la consulata en una tupla
        # se envia a tuple_json() para crear un json  
        datos = cursor.fetchone()
        print(datos)
        

        if datos != None:
            cookie = cookies.SimpleCookie()
            cookie["uuid"] = datos[0]
            
            return json.dumps({'loged':True}), 200, {'ContentType':'application/json'} 

        # crea un diccionario con todos los datos de la tupla
        obras_sociales = []
        for fila in datos:
            obras_sociales.append({'idObraSocial':fila[0],'nombre':fila[1]})

        return jsonify(obras_sociales)

    except Exception as ex:
            return jsonify({'mensaje':'Error (Insert): {0}'.format(ex)})



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
