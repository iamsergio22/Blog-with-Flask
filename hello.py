from flask import flash, Flask, render_template

# Crear una instancia de Flask
app = Flask(__name__)

# Crear una ruta a un decorador


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/user/<name>')
def user(name):
    pizzas=["peperonni","carne","queso",87]
    return render_template("user.html",name=name,pizzas=pizzas)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404



if __name__ == '__main__':
    app.run(port=3000,debug=True)
