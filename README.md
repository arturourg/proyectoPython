# Vacunatorio Coelemu

	<h3>ENUNCIADO TRABAJO</h3>

Vacunatorio Coelemu requiere un sistema para manejar sus pacientes e inventario de vacunas. El proyecto Realiza lo siguiente:<br>
<br>
- Listar todos los pacientes<br>
- Crear pacientes<br>
- Listar vacunas<br>
- Crear vacunas<br>
- Listar pacientes que han recibido una vacuna específica<br>
- Listar vacunas que ha recibido un paciente<br>
- Registrar vacuna a un paciente (vacunar paciente)<br>
</div>

# Para Ejecutar la aplicación:


## Requisitos:

Tener instalado python3, pip, GIT y MySQL.

# Instalación de la aplicación:

Primero debe tener el proyecto en su computadora, para esto lo puede clonar o bien descargar desde GitHub.

Al tener el proyecto en su equipo, debe realizar la instalación de las dependencias necesarias para que se pueda ejecutar la aplicación correctamente. Para esto abra una consola y ubiquese en la dirección que tiene almacenado el proyecto y ejecute los siguientes comandos:

```bash
pip install -U pip
pip install -r requirements.txt
```


# Configuración de la Base de datos:

Para ejecutar esta aplicación debe tener una base de datos local que puede ejecutar con xampp o algún programa similar.
Los datos que debe tener la base de datos son:

Nombre de la base de datos: vacunatorio
Usuario base de datos: root
(No tiene contraseña) 

Ahora debe crear la base de datos, para esto ejecute el SQL llamado: create_database.sql y con este crea la base de datos y el modelo de esta (incluye tres tablas: paciente, recibe, vacuna.)

Luego, para tener algunos datos de prueba debe ejecutar el archivo llamado: insert.sql
con este script tendrá algunos datos de prueba.


# Ejecutar aplicación:

Estando situado en donde se encuentra el proyecto, abra una consola y ejecute el siguiente comando:

```bash
python vacunatorio.py
```
Con esto se iniciará un servidor local en el puerto 5000, para poder acceder a la aplicacion
desde su navegador ingrese a la dirección -> 127.0.0.1:5000


# Este proyecto fue realizado por:

* **César Mora - Estudiante de Ingeniería civil en informática UBB**
* **Arturo Urra - Estudiante de Ingeniería civil en informática UBB**
