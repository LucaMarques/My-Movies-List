from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from models import db, Ator, Filme, Atuacao, Episodio, Genero

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
    atuacoes = filme.atuacoes

    return render_template('film-page.html', filme=filme, episodios=episodios, elenco=atuacoes)


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

@app.route('/novo-filme', methods=['GET', 'POST'])
def novo_filme():
    generos = Genero.query.all()
    filmes = Filme.query.all()

    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        temporada = request.form['temporada']
        ano = request.form['ano']  
        
        genero_ids = request.form.getlist("generos")  
        genero_ids = [int(gid) for gid in genero_ids]  

        novo_filme = Filme(titulo=titulo, descricao=descricao, temporada = temporada, ano = ano)
        
        generos_selecionados = Genero.query.filter(Genero.id.in_(genero_ids)).all()
        for genero in generos_selecionados:
            novo_filme.generos.append(genero)

        db.session.add(novo_filme)
        db.session.commit()

        return redirect(url_for('novo'))

    return render_template("novo_filme.html", generos = generos)

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
            return redirect(url_for("novo_filme"))

    return render_template("novo_ator.html", filmes=filmes, atores=atores)

@app.route('/novo-genero', methods=['GET', 'POST'])
def novo_genero():
    filmes = Filme.query.all()
    generos = Genero.query.all()

    if request.method == 'POST':
        acao = request.form.get("acao")

        if acao == "criar":
            nome = request.form["nome"]

            filmes_ids = request.form.getlist("filmes")
            filmes_selecionados = Filme.query.filter(Filme.id.in_(filmes_ids)).all()

            novo_genero = Genero(nome = nome)
            novo_genero.filmes = filmes_selecionados
            db.session.add(novo_genero) 
            
            db.session.commit()

            return redirect(url_for("novo_ator"))

        elif acao == "adicionar_genero":
            genero_id = int(request.form["genero_existente"])
            genero = Genero.query.get_or_404(genero_id)

            filmes_ids = request.form.getlist("novos_filmes")
            novos_filmes = Filme.query.filter(Filme.id.in_(filmes_ids)).all()

            for filme in novos_filmes:
                if filme not in genero.filmes:
                    genero.filmes.append(filme)

            db.session.commit()
            return redirect(url_for("novo_genero"))

    return render_template("novo_genero.html", filmes=filmes, generos = generos)