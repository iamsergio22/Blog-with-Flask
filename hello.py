from flask import flash, Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Crear una instancia de Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = "mi super clave secrssseta"

# crear una clase form
class NamerForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Crear una ruta a un decorador
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/user/<name>')
def user(name):
    return render_template("user.html", name=name)


@app.route('/name', methods=['GET','POST'])
def name():
    name = None
    form = NamerForm()
    # validaciones
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Fom submiteed succesfully")
    return render_template("name.html", name=name, form=form)





# ------------------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


if __name__ == '__main__':
    app.run(port=3000, debug=True)
