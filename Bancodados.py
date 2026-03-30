import sqlite3

def inicializar():
    conn = sqlite3.connect("games.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jogos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            estoque INTEGER NOT NULL,
            valor REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()

    print("Banco inicializado!")


if __name__ == "__main__":
    inicializar()