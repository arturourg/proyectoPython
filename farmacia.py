import requests
import json
from flask import Flask, render_template, jsonify, request
from flaskext.mysql import MySQL
import pymysql
import pymysql.cursors

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


app = Flask(__name__)
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_DB"]  = "vacunatorio"

app.config['SECRET_KEY'] = 'c5f44a801f29abe08ec730b800ba33c3'

mysql = MySQL(app)
mysql.connect_args["autocommit"] = True
mysql.connect_args["cursorclass"] = pymysql.cursors.DictCursor


#insertPaciente
@app.route('/paciente/add', methods=["GET","POST"])
def addPaciente():
	cursor = mysql.get_db().cursor()

	if request.method == "GET":
		nombre = request.args.get('nombre', default = "", type = str)
		apellidos = request.args.get('apellidos', default = "", type = str)
		rut = request.args.get('rut', default = "", type = str)
		nacimiento = request.args.get('nacimiento', default = "", type = str)

		if nombre != "" and apellidos != "" and rut != "" and nacimiento !="":
			try:
				sql = "INSERT INTO PACIENTE (NOMBRE, APELLIDOS, RUT, FECHA_NACIMIENTO)"
				sql+= " VALUES (%s,%s,%s,%s)"
				cursor.execute(sql,(nombre,apellidos,rut, nacimiento))
			except Exception as e:
				print(e)

	if request.method == "POST":
		nombre = request.form['nombre']
		apellidos =request.form['apellidos']
		rut = request.form['rut']
		nacimiento = request.form['nacimiento']

		if nombre != "" and apellidos != "" and rut != "" and nacimiento !="":
			try:
				sql = "INSERT INTO PACIENTE (NOMBRE, APELLIDOS, RUT, FECHA_NACIMIENTO)"
				sql+= " VALUES (%s,%s,%s,%s)"
				cursor.execute(sql,(nombre, apellidos, rut, nacimiento))
			except Exception as e:
				print(e)
	
	return render_template('addPaciente.html', title='Registro de pacientes')


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

@app.route('/farmaciasJson')
def farmacias_json():
	cursor = mysql.get_db().cursor()
	cursor.execute("SELECT * FROM farmacia")
	return jsonify(cursor.fetchall())


@app.route('/farmacias', methods=["GET","POST"])
def farmacias():
	cursor = mysql.get_db().cursor()
	
	if request.method == "GET":
		ciudad = request.args.get('ciudad', default = "", type = str)
		farmacia = request.args.get('farmacia', default = "", type = str)

	if request.method == "POST":
		ciudad = request.form["ciudad"]
		farmacia = request.form["farmacia"]
		
	sql = "SELECT * FROM farmacia"
	cursor.execute(sql)
	
	if farmacia!="" and ciudad!="":
		sql+=" WHERE nombre_farmacia = %s AND ciudad= %s"
		cursor.execute(sql, (farmacia.upper(),ciudad.upper()))
	elif ciudad!="":
		sql +=" WHERE ciudad = %s"
		cursor.execute(sql, (ciudad.upper(),))
	elif farmacia!="":
		sql+=" WHERE nombre_farmacia = %s"
		cursor.execute(sql, (farmacia.upper(),))

	farmacias_ = cursor.fetchall()
	return render_template("farmacias.html",farmacies = farmacias_, ciudad = ciudad, farmacia = farmacia)

if __name__ == "__main__":
	app.run(debug=True)