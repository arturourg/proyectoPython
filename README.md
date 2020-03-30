# proyectoPython

	<h3><span class="glyphicon glyphicon-th-list"></span> ENUNCIADO TRABAJO</h3>
</div>
Estimados:<br>
<br>
Adjunto a uds un wireframe con la funcionalidad básica del proyecto. (pueden hacer click en los botones del pdf)<br>
<br>
Vacunatorio Coelemu requiere un sistema para manejar sus pacientes e inventario de vacunas. El proyecto debe poder:<br>
<br>
- Listar todos los pacientes<br>
- Crear pacientes<br>
- Listar vacunas<br>
- Crear vacunas<br>
- Listar pacientes que han recibido una vacuna específica<br>
- Listar vacunas que ha recibido un paciente<br>
- Registrar vacuna a un paciente (vacunar paciente)<br>
<br>
Entidades:<br>
- Paciente (nombre, rut, fecha_nacimiento)<br>
- Vacuna (nombre_enfermedad)<br>
<br>
Relaciones:<br>
- Paciente&nbsp; ---(0,n)---Recibe---(0,n)---N&nbsp; &nbsp;Vacuna<br>
<br>
Consideraciones:<br>
- Cada que se agregue una nueva vacuna, o se vacune un paciente en específico, se deberá registrar de manera automática la fecha de registro, la que después será mostrado en los listados.<br>
- El sistema deberá utilizar una base de datos mysql, flask y jinja. Está prohibido utilizar otra forma de servidor HTTP o base de datos. Incumplir esto resultará en la nota mínima, es decir, 1.<br>
- No se aceptarán correos después del plazo, cualquiera fuera de plazo será evaluado con nota 1.<br>
- El proyecto deberá ser subido a un repositorio github, que deberá contener:<br>
&nbsp; &nbsp; &nbsp; &nbsp; - Código completo del proyecto<br>
&nbsp; &nbsp; &nbsp; &nbsp; - Archivo README con las instrucciones de instalación y desplegado<br>
&nbsp; &nbsp; &nbsp; &nbsp; - Archivo requirements.txt con todas las dependencias utilizadas por pip<br>
&nbsp; &nbsp; &nbsp; &nbsp; - Script sql con la estructura de la base de datos, junto con datos de pruebas en todas las tablas.<br>
- Cada archivo .py o .html del proyecto deberá tener comentado el nombre de los integrantes <br>
- Al entregar el proyecto, solo se deberá enviar un correo a <a href="mailto:x.zenteno.a@gmail.com" target="_blank"><span class="il">x.zenteno.a@gmail.com</span></a> con la url del repositorio github y los nombres de los integrantes, nada más. No aceptará ni menos considerará el código adjuntado al correo.<br>
- El código no podrá estar comprimido ni compactado en un rar, zip, gzip, tar, etc. Incumplir esto resultará en la nota mínima.