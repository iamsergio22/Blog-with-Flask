from urllib.error import URLError
from flask import flash, Flask, render_template, request, url_for, redirect
from wtforms.validators import DataRequired
from flask_mysqldb import MySQL  # Necesario para la conexion a DB
import mysql.connector  # Necesario para la conexion a DB
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
# texto="x?1_aP-1M.4!eM"
# texto_encriptado=generate_password_hash(texto)
# print(texto_encriptado)
# print(check_password_hash(texto_encriptado,texto))


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
    # Si a esta ruta se le envia algo atraves del metodo 'POST' entonces haga esto:
    if request.method == 'POST':
        # la variable nombre va a ser igual a lo que haya en el name="nombre" del name.html
        nombre = request.form['nombre']
        email = request.form['email']
        fecha = request.form['fecha']
        password = request.form['password1']
        password2 = request.form['password2']
        if password2 == password:
            passwordFinal = generate_password_hash(password)
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO users (nombre,correo,password1,Fecha) VALUES (%s,%s,%s,%s)', (nombre, email, passwordFinal, fecha))
            conn.commit()
            flash("User Registrado!!!")
            # Estoy redireccionando a la funcion name que tiene la vista name y tambien me consulta lo que hay en la base de datos.
            return redirect(url_for('name'))
        else:
            flash("las claves no coinciden")
            return redirect(url_for('name'))

# SEARCH TO DB


@app.route('/name', methods=['GET', 'POST'])
def name():
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    data = cur.fetchall()
    conn.commit()
    return render_template('name.html', users=data)

# UPDATE TO DB


@app.route('/edit/<id>', methods=['POST', 'GET'])
def edit(id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id=%s", [id])
    info = cur.fetchall()
    return render_template('edit.html', info=info)


@app.route('/update/<id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        # la variable nombre va a ser igual a lo que haya en el name="nombre" del name.html
        nombre = request.form['nombre']
        email = request.form['email']
        fecha = request.form['fecha']
        cur = conn.cursor()
        cur.execute("""UPDATE users SET nombre=%s,correo=%s,Fecha=%s WHERE id=%s""",
                    (nombre, email, fecha, id))
        conn.commit()
        flash("user actualizado")
        return redirect(url_for('name'))
    else:
        flash("no se pudo realizar la edición")
        return redirect(url_for('name'))

# DELETE OF BD


@app.route('/delete/<id>')
def delete(id):
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id={0}".format(id))
    conn.commit()
    flash("registro eliminado")
    return redirect(url_for('name'))


# agregando post 
@app.route('/post')
def post():
    return render_template("add-post.html")

@app.route('/add-post', methods=['GET','POST'])
def addpost():
    if request.method=='POST':
        title=request.form['title']
        content=request.form['Content']
        author=request.form['author']
        slug=request.form['slug']
        fechaPubli=datetime.now()        
        cur=conn.cursor()
        cur.execute("INSERT INTO posts (title,content,author,slug,date_posted) VALUES (%s,%s,%s,%s,%s)",(title,content,author,slug,fechaPubli))
        conn.commit()
        flash("Post Publicado")
        return redirect(url_for("post"))
    else:
        flash("Hubo un error al publicar el post")
        return redirect(url_for("name"))
    
# ver post 
@app.route('/ShowPost')
def ShowPost():
    cur=conn.cursor()
    cur.execute("SELECT * FROM posts")
    data=cur.fetchall()
    posts=data
    print(posts)
    return render_template("post.html",post=posts)
    




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
