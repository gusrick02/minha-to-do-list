from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("tarefas.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        texto TEXT NOT NULL,
        feito INTEGER NOT NULL
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    conn = get_db()

    tarefas = conn.execute(
        "SELECT * FROM tarefas"
    ).fetchall()

    conn.close()

    return render_template("index.html", tarefas=tarefas)

@app.route("/add", methods=["POST"])
def add():

    tarefa = request.form.get("tarefa")

    conn = get_db()

    conn.execute(
        "INSERT INTO tarefas (texto, feito) VALUES (?, ?)",
        (tarefa, 0)
    )

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/toggle/<int:id>")
def toggle(id):

    conn = get_db()

    tarefa = conn.execute(
        "SELECT feito FROM tarefas WHERE id=?",
        (id,)
    ).fetchone()

    novo_estado = 0 if tarefa["feito"] else 1

    conn.execute(
        "UPDATE tarefas SET feito=? WHERE id=?",
        (novo_estado, id)
    )

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM tarefas WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")
app.run(debug=True, use_reloader=False)