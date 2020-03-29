import requests
import json
from flask import Flask, render_template, jsonify, request
from flaskext.mysql import MySQL
import pymysql
import pymysql.cursors


app = Flask(__name__)
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_DB"]  = "vacunatorio"

mysql = MySQL(app)
mysql.connect_args["autocommit"] = True
mysql.connect_args["cursorclass"] = pymysql.cursors.DictCursor

	
@app.route('/')
def hello():
	url = "https://farmanet.minsal.cl/index.php/ws/getLocales"
	r  =  requests.get(url)
	diccionario = {}
	for objeto in json.loads(r.text[1:]):
		llave_region = f"region_{objeto['fk_region']}" 
		if llave_region not in diccionario:
			diccionario[llave_region] = []
		if objeto["comuna_nombre"] not in diccionario[llave_region]:
			diccionario[llave_region].append(objeto["comuna_nombre"])
	return render_template('plantilla.html', regiones=diccionario)



@app.route('/listar_vacunas', methods=["GET","POST"])
def vacunas():
	cursor = mysql.get_db().cursor()
	
	if request.method == "GET":
		NOMBRE_ENFERMEDAD = request.args.get('NOMBRE_ENFERMEDAD', default = "", type = str)

	if request.method == "POST":
		NOMBRE_ENFERMEDAD = request.form["NOMBRE_ENFERMEDAD"]

	sql = "SELECT NOMBRE_ENFERMEDAD FROM `vacuna`"
	cursor.execute(sql)

	
	if NOMBRE_ENFERMEDAD!="":
		sql+=" WHERE NOMBRE_ENFERMEDAD = %s"
		cursor.execute(sql, (NOMBRE_ENFERMEDAD.upper()))


	vacuna_ = cursor.fetchall()
	print("aqui")
	print(vacuna_)
	return render_template("listar_vacunas.html",lista_vacu = vacuna_)


@app.route('/listar_pacientes', methods=["GET","POST"])
def paciente():
	cursor = mysql.get_db().cursor()
	
	if request.method == "GET":
		RUT = request.args.get('RUT', default = "", type = str)
		NOMBRE = request.args.get('NOMBRE', default = "", type = str)
		APELLIDOS = request.args.get('APELLIDOS', default = "", type = str)
		FECHA_NACIMIENTO = request.args.get('FECHA_NACIMIENTO', default = "", type = str)

	if request.method == "POST":
		RUT = request.form["RUT"]
		NOMBRE = request.form["NOMBRE"]
		APELLIDOS = request.form["APELLIDOS"]
		FECHA_NACIMIENTO = request.form["FECHA_NACIMIENTO"]

	sql = "SELECT * FROM `paciente`"
	cursor.execute(sql)

	paciente_ = cursor.fetchall()
	print("aqui")
	print(paciente_)
	return render_template("listar_pacientes.html",lista_paci = paciente_,RUT=RUT, NOMBRE=NOMBRE, APELLIDOS=APELLIDOS,FECHA_NACIMIENTO=FECHA_NACIMIENTO) 



if __name__ == "__main__":
	app.run(debug=True)