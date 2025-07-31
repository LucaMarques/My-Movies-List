from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from models import db, Episodio, Filme

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

@app.route('/series/<int:filme_id>')
def series(filme_id):
    filme = Filme.query.get_or_404(filme_id)
    episodios = filme.episodios

    if episodios:
        media = sum(ep.avaliacao for ep in episodios) / len(episodios)
        media = round(media, 1)
    else:
        media = None

    return render_template('film-page.html', filme=filme, episodios=episodios, media = media)


# Formulário de novo episódio
@app.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        titulo = request.form["titulo"]
        numero = request.form["numero"]
        avaliacao = float(request.form["avaliacao"])
        filme_id = int(request.form["filme_id"])

        novo_episodio = Episodio(titulo=titulo, numero=numero, avaliacao=avaliacao, filme_id = filme_id)
        db.session.add(novo_episodio)
        db.session.commit()

        return redirect(url_for("series", filme_id=filme_id))
    
    filmes = Filme.query.all()
    return render_template("novo.html", filmes=filmes)

@app.route('/novo_filme', methods=['GET', 'POST'])
def novo_filme():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']

        novo_filme = Filme(titulo=titulo, descricao=descricao)
        db.session.add(novo_filme)
        db.session.commit()

        return redirect(url_for('novo'))

    return render_template("novo_filme.html")


