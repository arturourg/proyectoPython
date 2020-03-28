import requests
import json
from flask import Flask, render_template, jsonify, request
from flaskext.mysql import MySQL
import pymysql
import pymysql.cursors


app = Flask(__name__)
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_DB"]  = "farmacias"

mysql = MySQL(app)
mysql.connect_args["autocommit"] = True
mysql.connect_args["cursorclass"] = pymysql.cursors.DictCursor


@app.route('/actualizaFarmacias')
def actualiza():
	url = "https://farmanet.minsal.cl/index.php/ws/getLocales"
	r  =  requests.get(url)
	cursor = mysql.get_db().cursor()
	cursor.execute("TRUNCATE farmacia")
	
	c = 0
	for objeto in json.loads(r.text[1:]):
		try:
			lat = float(objeto["local_lat"])
			lng = float(objeto["local_lng"])
			sql = "INSERT INTO farmacia (nombre_farmacia, direccion, ciudad, latitud, longitud, telefono)"
			sql+= " VALUES (%s,%s,%s,%s,%s,%s)"
			cursor.execute(sql,(objeto["local_nombre"],objeto["local_direccion"],objeto["comuna_nombre"],lat,lng,objeto["local_telefono"]))
			c+=1
		except Exception as e:
			print(e)
			continue
	return (f"Se han insertado {c} registros", 200)
		
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