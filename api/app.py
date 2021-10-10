from flask import Flask , jsonify, request
from flask_cors import CORS,cross_origin
from flaskext.mysql import MySQL
from config import config

app = Flask(__name__)
cors = CORS(app)
mysql = MySQL(  )
mysql.init_app(app)


#consulta especialidades
@app.route('/especialidades/', methods=["GET"])
def VerEspecialidades():
        try:
                con = mysql.connect()
                cursor = con.cursor()
                consulta = "select * from Especialidad"
                cursor.execute(consulta)
                datos = cursor.fetchall()

                #conversion de tupla a Json
                #diccionario que guarda lo devuelto por la base de datos
                especialidades = []
                for fila in datos:
                        #da formato a los datos de la tupla
                        espe = {'idEspecialidad':fila[0],'nombre':fila[1]}
                        #la agrega al diccionario
                        especialidades.append(espe)
                        
                #convierte el diccionario en Json
                return jsonify({'especialidades':especialidades,'mensaje':"especialidades mostradas."})
                
        except Exception as ex:
                return jsonify({'mensaje':'Error (Get): {0}'.format(ex)})

# consultar dato especifico por URL 
# 0.0.0.0:5000/especialidades/1 => especialidad con id == 1
@app.route('/especialidades/<codigo>', methods=["GET"])
def VerEspecialidad(codigo):
        try:
                con = mysql.connect()
                cursor = con.cursor()
                consulta = "select * from Especialidad where idEspecialidad = {0}".format(codigo)
                cursor.execute(consulta)
                datos = cursor.fetchone()

                if datos != None:
                        espe = {'idEspecialidad':datos[0],'nombre':datos[1]}
                        return jsonify({'especialidades':espe,'mensaje':"especialidades mostradas."})
                else:
                        return jsonify({'mensaje':'Especialidad no encontrado'})
        except Exception as ex:
                return jsonify({'mensaje':'Error (Get One): {0}'.format(ex)})

# ingresar una especialidad
@app.route('/especialidades', methods=["POST"])
def GuardarEspecialidad():
        try:
                con = mysql.connect()
                cursor = con.cursor()
                #request.json['idEspecialidad'],
                consulta = "insert into Especialidad(nombre) values  ('{0}')".format(request.json['nombre'])
                cursor.execute(consulta)
                con.commit()
                return jsonify({'mensaje':'Especialidad registrada exitosamente'})

        except Exception as ex:
                return jsonify({'mensaje':'Error (Insert): {0}'.format(ex)})

# borrar una especialidad
@app.route('/especialidades/<codigo>', methods=["DELETE"])
def BorrarEspecialidad(codigo):
        try:
                con = mysql.connect()
                cursor = con.cursor()
                consulta = "delete from Especialidad where idEspecialidad = '{0}'".format(codigo)
                cursor.execute(consulta)
                con.commit()
                return jsonify({'mensaje':'Especialidad borrada exitosamente'})

        except Exception as ex:
                return jsonify({'mensaje':'Error (Delete): {0}'.format(ex)})

# actualiza una especialidad
@app.route('/especialidades/<codigo>', methods=["PUT"])
def ActualizarEspecialidad(codigo):
        try:
                con = mysql.connect()
                cursor = con.cursor()
                consulta = "update Especialidad set nombre  = '{0}' where idEspecialidad = '{1}'".format(request.json['nombre'],codigo)
                cursor.execute(consulta)
                con.commit()
                return jsonify({'mensaje':'Especialidad actualizada exitosamente'})

        except Exception as ex:
                return jsonify({'mensaje':'Error (Update): {0}'.format(ex)})



#en caso de error 404 muestra esto
def NotFoundView(error):
        return "<h1> La pagina no existe we</h1>",404

if __name__ == "__main__":
        #importa un archivo de configuracion
        app.config.from_object(config['development'])
        app.config['CORS_HEADERS'] = 'Content-Type'
        
        #en caso de error 404 llama a NotFoundView()
        app.register_error_handler(404,NotFoundView)

        app.run(host="0.0.0.0")
