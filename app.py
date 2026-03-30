from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

BANCO = "games.db"


def get_db():
    conn = sqlite3.connect(BANCO)
    conn.row_factory = sqlite3.Row
    return conn


def query_db(comando, args=(), fetch=False):
    conn = get_db()
    cur = conn.cursor()

    resposta = None

    try:
        cur.execute(comando, args)

        if fetch:
            resposta = cur.fetchall()
        else:
            conn.commit()

    except Exception as erro:
        return {"erro": str(erro)}

    finally:
        conn.close()

    return resposta

@app.route("/games", methods=["GET"])
def listar_games():
    dados = query_db("SELECT * FROM jogos", fetch=True)
    return jsonify([dict(g) for g in dados])

@app.route("/games/<int:game_id>", methods=["GET"])
def buscar_game(game_id):
    resultado = query_db(
        "SELECT * FROM jogos WHERE id = ?",
        (game_id,),
        fetch=True
    )

    if not resultado:
        return jsonify({"erro": "Game não encontrado"}), 404

    return jsonify(dict(resultado[0]))

@app.route("/games", methods=["POST"])
def criar_game():
    body = request.get_json()

    if not body:
        return jsonify({"erro": "JSON inválido"}), 400

    query_db(
        "INSERT INTO jogos (titulo, estoque, valor) VALUES (?, ?, ?)",
        (body["titulo"], body["estoque"], body["valor"])
    )

    return jsonify({"mensagem": "Game cadastrado"}), 201

@app.route("/games/<int:game_id>", methods=["PUT"])
def atualizar_game(game_id):
    body = request.get_json()

    existe = query_db(
        "SELECT id FROM jogos WHERE id = ?",
        (game_id,),
        fetch=True
    )

    if not existe:
        return jsonify({"erro": "Game não encontrado"}), 404

    query_db(
        "UPDATE jogos SET titulo=?, estoque=?, valor=? WHERE id=?",
        (body["titulo"], body["estoque"], body["valor"], game_id)
    )

    return jsonify({"mensagem": "Game atualizado"})

@app.route("/games/<int:game_id>", methods=["DELETE"])
def deletar_game(game_id):
    item = query_db(
        "SELECT titulo FROM jogos WHERE id = ?",
        (game_id,),
        fetch=True
    )

    if not item:
        return jsonify({"erro": "Game não encontrado"}), 404

    query_db("DELETE FROM jogos WHERE id = ?", (game_id,))

    return jsonify({"mensagem": f"{item[0]['titulo']} removido"})

if __name__ == "__main__":
    app.run(debug=True)