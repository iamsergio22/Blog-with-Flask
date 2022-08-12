from flask import flash, Flask, render_template, request,url_for,redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_mysqldb import MySQL #Necesario para la conexion a DB
import mysql.connector #Necesario para la conexion a DB


# Crear una instancia de Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = "mi super clave secrssseta"

# Ventana por defecto/index
@app.route('/')
def index():
    return render_template("index.html")


# BASE DE DATOS ⬇️⬇️⬇️⬇️⬇️⬇️

# conexion a db
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    db='blog',
)

# INSERTAR EN BD
@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST': #Si a esta ruta se le envia algo atraves del metodo 'POST' entonces haga esto:
        nombre = request.form['nombre'] #la variable nombre va a ser igual a lo que haya en el name="nombre" del name.html 
        email = request.form['email']
        fecha=request.form['fecha']
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO users (nombre,correo,Fecha) VALUES (%s,%s,%s)', (nombre, email,fecha))
        conn.commit()        
        flash("User Registrado!!!")
        return redirect(url_for('name')) # Estoy redireccionando a la funcion name que tiene la vista name y tambien me consulta lo que hay en la base de datos.

# SEARCH TO DB 
@app.route('/name', methods=['GET', 'POST'])
def name():
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    data = cur.fetchall()
    conn.commit()       
    return render_template('name.html', users=data)





@app.route('/user/<name>')
def user(name):
    return render_template("user.html", name=name)





# ------------------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


if __name__ == '__main__':
    app.run(port=3000, debug=True)
