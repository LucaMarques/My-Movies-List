from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from models import db, Episodio

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meu_banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# Garante que as tabelas existem
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/series')
def series():
    episodios = Episodio.query.all()
    return render_template('film-page.html', episodios=episodios)

# Formulário de novo episódio
@app.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        titulo = request.form["titulo"]
        numero = request.form["numero"]
        avaliacao = float(request.form["avaliacao"])

        novo_episodio = Episodio(titulo=titulo, numero=numero, avaliacao=avaliacao)
        db.session.add(novo_episodio)
        db.session.commit()

        return redirect(url_for("series"))

'''
@app.route('/novo_filme', methods=['GET', 'POST'])
def novo_filme():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']

        novo_filme = Filme(titulo=titulo, descricao=descricao)
        db.session.add(novo_filme)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template("novo.html")
'''

