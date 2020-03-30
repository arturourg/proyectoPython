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
	return render_template('inicio.html')



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
	return render_template("listar_pacientes.html",lista_paci = paciente_,RUT=RUT, NOMBRE=NOMBRE, APELLIDOS=APELLIDOS,FECHA_NACIMIENTO=FECHA_NACIMIENTO) 


@app.route('/paciente_vacuna', methods=["GET","POST"])
def paciente2():
	cursor = mysql.get_db().cursor()
	cursor2 = mysql.get_db().cursor()
	
	if request.method == "GET":
		selec = request.args.get('selec', default = "", type = str)
		vacunar = request.args.get('vacunar', default = "", type = str)

	if request.method == "POST":
		selec = request.form["selec"]
		vacunar = request.form["vacunar"]

	sql = "SELECT * FROM `paciente`"
	cursor.execute(sql)
	if vacunar!="":
		sql2="SELECT DISTINCT p.RUT,p.NOMBRE,p.APELLIDOS,p.FECHA_NACIMIENTO,v.NOMBRE_ENFERMEDAD,r.FECHA_VACUNA FROM paciente p,recibe r,vacuna v where p.RUT=r.RUT and r.NOMBRE_ENFERMEDAD=v.NOMBRE_ENFERMEDAD and p.RUT=%s"
		cursor2.execute(sql2,(selec,))
		rut_a_vacunar_ = cursor2.fetchall()
		return render_template("vacunar_pacientes.html",rut_a_vacunar = rut_a_vacunar_)

	elif selec!="":
		sql2="SELECT p.RUT,p.NOMBRE,p.APELLIDOS,p.FECHA_NACIMIENTO,v.NOMBRE_ENFERMEDAD,r.FECHA_VACUNA FROM paciente p,recibe r,vacuna v where p.RUT=r.RUT and r.NOMBRE_ENFERMEDAD=v.NOMBRE_ENFERMEDAD and p.RUT=%s"
		cursor2.execute(sql2,(selec,))
		vacuna_del_paciente_ = cursor2.fetchall()
		return render_template("mostrar_vacunas_paciente.html",vacuna_del_paciente = vacuna_del_paciente_) 
	
	

	paciente_ = cursor.fetchall()
	return render_template("paciente_vacuna.html",lista_paci = paciente_) 



@app.route('/vacuna_paciente', methods=["GET","POST"])
def vacuna_paciente():
	cursor = mysql.get_db().cursor()
	cursor2 = mysql.get_db().cursor()
	
	if request.method == "GET":
		selec = request.args.get('selec', default = "", type = str)


	if request.method == "POST":
		selec = request.form["selec"]


	sql = "SELECT NOMBRE_ENFERMEDAD FROM `vacuna`"
	cursor.execute(sql)

	
	if selec!="":
		sql2="SELECT p.RUT,p.NOMBRE,p.APELLIDOS,p.FECHA_NACIMIENTO,v.NOMBRE_ENFERMEDAD,r.FECHA_VACUNA FROM paciente p,recibe r,vacuna v where p.RUT=r.RUT and r.NOMBRE_ENFERMEDAD=v.NOMBRE_ENFERMEDAD  and v.NOMBRE_ENFERMEDAD=%s"
		cursor2.execute(sql2,(selec,))
		vacuna_pacientes_ = cursor2.fetchall()
		return render_template("paciente_vacuna_mostrar.html",vacuna_pacientes = vacuna_pacientes_)


	vacuna_ = cursor.fetchall()
	return render_template("vacuna_paciente.html",lista_vacu = vacuna_)


<<<<<<< HEAD
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

#insertvacuna
@app.route('/vacuna/add', methods=["GET","POST"])
def addVacuna():
	cursor = mysql.get_db().cursor()

	if request.method == "GET":
		enfermedad = request.args.get('enfermedad', default = "", type = str)

		if enfermedad != "":
			try:
				sql = "INSERT INTO VACUNA (NOMBRE_ENFERMEDAD)"
				sql+= " VALUES (%s)"
				cursor.execute(sql,(enfermedad))
			except Exception as e:
				print(e)

	if request.method == "POST":
		enfermedad = request.form['enfermedad']

		if enfermedad != "":
			try:
				sql = "INSERT INTO VACUNA (NOMBRE_ENFERMEDAD)"
				sql+= " VALUES (%s)"
				cursor.execute(sql,(enfermedad))
			except Exception as e:
				print(e)
	
	return render_template('addVacuna.html', title='Nueva vacuna')

@app.route('/vacunar_paciente', methods=["GET","POST"])
def vacunarPaciente():
	cursor = mysql.get_db().cursor()
	cursor2 = mysql.get_db().cursor()

	if request.method == "GET":
		selec = request.args.get('selec', default = "", type = str)

	if request.method == "POST":
		selec = request.form["selec"]


	#if selec!="":	

		#return render_template("mostrar_vacunas_paciente.html",vacuna_del_paciente = vacuna_del_paciente_) 
	

	sql="SELECT RUT, NOMBRE, APELLIDOS, FECHA_NACIMIENTO FROM paciente where  RUT=5476546484"
	cursor.execute(sql)
	vacuna_del_paciente_ = cursor.fetchall()


	#MOSTRAR VACUNAS
	sql2 = "SELECT NOMBRE_ENFERMEDAD FROM VACUNA"
	cursor2.execute(sql2)
	vacunas_ = cursor.fetchall()


	return render_template("vacunar_paciente.html", paciente = vacuna_del_paciente_, lista_vacu = vacunas_)
	#vacuna_del_paciente_ = cursor.fetchall()
	#paciente_ = cursor.fetchall()
	#return render_template("vacunar_paciente.html", paciente = vacuna_del_paciente_) #RUT=RUT, NOMBRE=NOMBRE, APELLIDOS=APELLIDOS,FECHA_NACIMIENTO=FECHA_NACIMIENTO paciente = paciente_,


<<<<<<< HEAD
=======
=======
>>>>>>> aea4f61d4bcdf70485fdd99eeec05398d1da9797
>>>>>>> 16b5017f9b9a98ce5b2ab1390344ff4e53346599
if __name__ == "__main__":
	app.run(debug=True)

