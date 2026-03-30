from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco agora via SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Instância do ORM (substitui sqlite3)
db = SQLAlchemy(app)

# Model representa a tabela "jogos"
class Game(db.Model):
    __tablename__ = 'jogos'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    estoque = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.Float, nullable=False)

    # Converte objeto em JSON
    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "estoque": self.estoque,
            "valor": self.valor
        }


# Criação automática do banco/tabela
with app.app_context():
    db.create_all()


# GET - listar todos
@app.route("/games", methods=["GET"])
def listar_games():
    # 🔹 Antes: SELECT * FROM jogos
    # 🔹 Agora: ORM
    games = Game.query.all()
    return jsonify([g.to_dict() for g in games])


# GET por ID
@app.route("/games/<int:game_id>", methods=["GET"])
def buscar_game(game_id):

    game = Game.query.get(game_id)

    if not game:
        return jsonify({"erro": "Game não encontrado"}), 404

    return jsonify(game.to_dict())


# POST - criar
@app.route("/games", methods=["POST"])
def criar_game():

    body = request.get_json()

    if not body:
        return jsonify({"erro": "JSON inválido"}), 400

    novo_game = Game(
        titulo=body.get("titulo"),
        estoque=body.get("estoque"),
        valor=body.get("valor")
    )
    # ORM
    db.session.add(novo_game)
    db.session.commit()

    return jsonify({
        "mensagem": "Game cadastrado",
        "id": novo_game.id
    }), 201

# PUT - atualizar
@app.route("/games/<int:game_id>", methods=["PUT"])
def atualizar_game(game_id):

    game = Game.query.get(game_id)

    if not game:
        return jsonify({"erro": "Game não encontrado"}), 404

    body = request.get_json()

    # Atualização sem SQL
    game.titulo = body.get("titulo", game.titulo)
    game.estoque = body.get("estoque", game.estoque)
    game.valor = body.get("valor", game.valor)

    db.session.commit()

    return jsonify({"mensagem": "Game atualizado"})


# DELETE
@app.route("/games/<int:game_id>", methods=["DELETE"])
def deletar_game(game_id):

    game = Game.query.get(game_id)

    if not game:
        return jsonify({"erro": "Game não encontrado"}), 404

    titulo = game.titulo

    db.session.delete(game)
    db.session.commit()

    return jsonify({"mensagem": f"{titulo} removido"})


if __name__ == "__main__":
    app.run(debug=True)