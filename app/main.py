from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from models import db, Ator, Filme, Atuacao, Episodio

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
    
    elenco = [
        {"nome": atuacao.ator.nome, "personagem": atuacao.personagem}
        for atuacao in filme.atuacoes
    ]

    if episodios:
        media = sum(ep.avaliacao for ep in episodios) / len(episodios)
        media = round(media, 1)
    else:
        media = None

    return render_template('film-page.html', filme=filme, episodios=episodios, elenco=elenco, media = media)


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
        temporada = request.form['temporada']
        ano = request.form['ano']

        novo_filme = Filme(titulo=titulo, descricao=descricao, temporada = temporada, ano = ano)
        db.session.add(novo_filme)
        db.session.commit()

        return redirect(url_for('novo'))

    return render_template("novo_filme.html")

@app.route('/novo-ator', methods=['GET', 'POST'])
def novo_ator():
    filmes = Filme.query.all()
    atores = Ator.query.all()

    if request.method == 'POST':
        acao = request.form.get("acao")

        if acao == "criar":
            nome = request.form["nome"]
            data_nascimento_str = request.form["data_nascimento"]
            data_nascimento = datetime.strptime(data_nascimento_str, "%Y-%m-%d").date()

            filmes_ids = request.form.getlist("filmes")
            personagem = request.form["personagem"]

            novo_ator = Ator(nome=nome, data_nascimento=data_nascimento)
            db.session.add(novo_ator) 
            
            
            for filme_id in filmes_ids:
                atuacao = Atuacao(ator=novo_ator, filme_id=int(filme_id), personagem=personagem)
                db.session.add(atuacao)

            db.session.commit()

            return redirect(url_for("novo_ator"))

        elif acao == "adicionar_filme":
            ator_id = int(request.form["ator_existente"])
            ator = Ator.query.get_or_404(ator_id)

            ids_filmes = request.form.getlist("novos_filmes")
            personagem = request.form.get("personagem")

            for filme in ids_filmes:
                filme_id = int(filme)
                atuacao_existente = Atuacao.query.filter_by(ator_id=ator_id, filme_id=filme_id).first()

                if not atuacao_existente:
                    nova_atuacao = Atuacao(
                        ator_id=ator_id,
                        filme_id=filme_id,
                        personagem=personagem
                    )
                    db.session.add(nova_atuacao)

            db.session.commit()
            return redirect(url_for("novo_ator"))

    return render_template("novo_ator.html", filmes=filmes, atores=atores)

