'''
Proyecto final de Python
Integrantes:
-César Mora
-Arturo Urra
'''


#Bibliotecas importadas
import requests
import json
import pymysql
import pymysql.cursors
from flask import Flask, render_template, jsonify, request, redirect, session, url_for
from flaskext.mysql import MySQL
from datetime import datetime


#CONFIGURACION BD
app = Flask(__name__)
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_DB"]  = "vacunatorio"

mysql = MySQL(app)
mysql.connect_args["autocommit"] = True
mysql.connect_args["cursorclass"] = pymysql.cursors.DictCursor

#RAIZ	
@app.route('/')
def hello():
	return render_template('inicio.html')



#FUNCION PARA LISTAR PACIENTES
@app.route('/listar_pacientes', methods=["GET","POST"])
def paciente2():
	cursor = mysql.get_db().cursor()
	sql = "SELECT * FROM `paciente`"
	cursor.execute(sql)

	if request.method == "POST":
		
		if request.form.get("selec",None):
			selec = request.form["selec"]
			sql2="SELECT p.RUT,p.NOMBRE,p.APELLIDOS,p.FECHA_NACIMIENTO,v.NOMBRE_ENFERMEDAD,r.FECHA_VACUNA FROM paciente p,recibe r,vacuna v where p.RUT=r.RUT and r.NOMBRE_ENFERMEDAD=v.NOMBRE_ENFERMEDAD and p.RUT=%s"
			cursor.execute(sql2,(selec,))
			vacuna_del_paciente_ = cursor.fetchall()
			return render_template("mostrar_vacunas.html",vacuna_del_paciente = vacuna_del_paciente_)

		elif request.form.get("vacunar", None):
			vacunar = request.form["vacunar"]
			print("hola")
			return redirect(url_for('.vacunarPaciente',vacunar = vacunar, **request.args))

	paciente_ = cursor.fetchall()
	return render_template("listar_paciente.html",lista_paci = paciente_) 



#FUNCION PARA LISTAR VACUNAS
@app.route('/listar_vacunas', methods=["GET","POST"])
def vacunas():
	cursor = mysql.get_db().cursor()
	
	if request.method == "GET":
		enfermedad_python = request.args.get('NOMBRE_ENFERMEDAD', default = "", type = str)

	if request.method == "POST":
		enfermedad_python = request.form["NOMBRE_ENFERMEDAD"]
		print(enfermedad_python)
	sql = "SELECT NOMBRE_ENFERMEDAD, FECHA_REGISTRO FROM `vacuna`"
	cursor.execute(sql)
	
	if enfermedad_python!="":
		sql+=" WHERE NOMBRE_ENFERMEDAD = %s"
		cursor.execute(sql, (enfermedad_python.upper()))

	vacuna_ = cursor.fetchall()
	return render_template("listar_vacunas.html",lista_vacu = vacuna_)



#FUNCION PARA AGREGAR NUEVO PACIENTE
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
				sql = "INSERT INTO PACIENTE (RUT, NOMBRE, APELLIDOS, FECHA_NACIMIENTO)"
				sql+= " VALUES (%s,%s,%s,%s)"
				cursor.execute(sql,(rut, nombre, apellidos, nacimiento))
			except Exception as e:
				print(e)

	if request.method == "POST":
		nombre = request.form['nombre']
		apellidos =request.form['apellidos']
		rut = request.form['rut']
		nacimiento = request.form['nacimiento']

		if nombre != "" and apellidos != "" and rut != "" and nacimiento !="":
			try:
				sql = "INSERT INTO PACIENTE (RUT, NOMBRE, APELLIDOS,  FECHA_NACIMIENTO)"
				sql+= " VALUES (%s,%s,%s,%s)"
				cursor.execute(sql,(rut, nombre, apellidos, nacimiento))
			except Exception as e:
				print(e)
	
	return render_template('addPaciente.html', title='Registro de pacientes')



#FUNCION PARA AGREGAR NUEVA VACUNA
@app.route('/vacuna/add', methods=["GET","POST"])
def addVacuna():
	cursor = mysql.get_db().cursor()

	if request.method == "GET":
		enfermedad = request.args.get('enfermedad', default = "", type = str)

		if enfermedad != "":
			try:
				sql = "INSERT INTO VACUNA (FECHA_REGISTRO, NOMBRE_ENFERMEDAD)"
				sql+= " VALUES (%s, %s)"
				cursor.execute(sql,(datetime.today().strftime('%y-%m-%d'), enfermedad, ))
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



#FUNCION PARA AGREGAR VACUNA A PACIENTE
@app.route('/vacunar_paciente', methods=["GET","POST"])
def vacunarPaciente():
	rut_a_vacunar = request.args.get('vacunar')
	cursor = mysql.get_db().cursor()
	cursor2 = mysql.get_db().cursor()

	print(rut_a_vacunar)
	print(request.form.get('nombre_enfermedad'))

	if request.method == "POST":
		#INSERTAR VACUNA
		if rut_a_vacunar != "" and request.form.get('nombre_enfermedad') != "":
			enfermedad = request.form.get('nombre_enfermedad')
			
			try:
				query_insert_vacuna = "INSERT INTO recibe (FECHA_VACUNA, NOMBRE_ENFERMEDAD, RUT)"
				query_insert_vacuna+= " VALUES (%s, %s, %s)" 
				cursor.execute(query_insert_vacuna, (datetime.today().strftime('%Y-%m-%d'), enfermedad, rut_a_vacunar,))
			except Exception as e:
				print(e)

		query_select_paciente="SELECT RUT, NOMBRE, APELLIDOS, FECHA_NACIMIENTO FROM paciente where RUT=%s" #PACIENTES
		cursor.execute(query_select_paciente, (rut_a_vacunar,))
		vacuna_del_paciente_ = cursor.fetchall()

		sql2 = "SELECT NOMBRE_ENFERMEDAD FROM VACUNA" #VACUNAS
		cursor2.execute(sql2 )
		vacunas_ = cursor2.fetchall()

		return render_template("vacunar_paciente.html", paciente = vacuna_del_paciente_, lista_vacu = vacunas_ )

	elif rut_a_vacunar != "":
		#MOSTRAR DATOS PACIENTES
		query_select_paciente="SELECT RUT, NOMBRE, APELLIDOS, FECHA_NACIMIENTO FROM paciente where RUT=%s" #PACIENTES
		cursor.execute(query_select_paciente, (rut_a_vacunar,))
		vacuna_del_paciente_ = cursor.fetchall()

		#MOSTRAR VACUNAS
		sql2 = "SELECT NOMBRE_ENFERMEDAD FROM VACUNA" #VACUNAS
		cursor2.execute(sql2 )
		vacunas_ = cursor2.fetchall()

		return render_template("vacunar_paciente.html", paciente = vacuna_del_paciente_, lista_vacu = vacunas_ )
	

if __name__ == "__main__":
	app.run(debug=True)