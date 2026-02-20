from flask import Flask, render_template, request, session, redirect, url_for
import random
import time
import os
import json
from datetime import date

app = Flask(__name__)
app.secret_key = "supersecretkey"

SCORES_FILE = os.path.join(os.path.dirname(__file__), "scores.json")

escalas = {
    "C": ["C", "D", "E", "F", "G", "Am", "B"],
    "D": ["D", "E", "F#", "G", "A", "Bm", "C#"],
    "E": ["E", "F#", "G#", "A", "B", "C#m", "D#"],
    "G": ["G", "A", "B", "C", "D", "Em", "F#"],
    "A": ["A", "B", "C#", "D", "E", "F#m", "G#"],
    "B": ["B", "C#", "D#", "E", "F#", "G#m", "A#"],
    "F": ["F", "G", "A", "Bb", "C", "Dm", "E"],
    "Bb": ["Bb", "C", "D", "Eb", "F", "Gm", "A"],
    "Eb": ["Eb", "F", "G", "Ab", "Bb", "Cm", "D"],
    "Ab": ["Ab", "Bb", "C", "Db", "Eb", "Fm", "G"],
    "Db": ["Db", "Eb", "F", "Gb", "Ab", "Bbm", "C"],
    "Gb": ["Gb", "Ab", "Bb", "Cb", "Db", "Ebm", "F"],
    "Am": ["Am", "B", "C", "D", "E", "F", "G"],
    "Bm": ["Bm", "C#", "D", "E", "F#", "G", "A"],
    "C#m": ["C#m", "D#", "E", "F#", "G#", "A", "B"],
    "Dm": ["Dm", "E", "F", "G", "A", "Bb", "C"],
    "Em": ["Em", "F#", "G", "A", "B", "C", "D"],
    "F#m": ["F#m", "G#", "A", "B", "C#", "D", "E"],
    "G#m": ["G#m", "A#", "B", "C#", "D#", "E", "F#"]
}

def formato_grado(n):
    return ["1er grado","2do grado","3er grado","4to grado","5to grado","6to grado","7mo grado"][n-1]

# ── Puntajes ─────────────────────────────────────────────────────────────────

def load_scores():
    """Carga los puntajes del día. Si el archivo es de otro día, devuelve lista vacía."""
    today = str(date.today())
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data.get("date") == today:
                return data["scores"]
        except (json.JSONDecodeError, KeyError):
            pass
    return []

def save_score(nombre_jugador, score, aciertos, preguntas):
    """Guarda el puntaje del jugador. Solo reemplaza si el nuevo puntaje es mayor."""
    today = str(date.today())
    scores = load_scores()
    # Si ya existe una entrada para este jugador, solo reemplazar si mejora su puntaje
    existente = next((s for s in scores if s["nombre"].lower() == nombre_jugador.lower()), None)
    if existente is not None:
        if score <= existente["score"]:
            return  # No reemplazar: el puntaje existente es igual o mejor
        scores = [s for s in scores if s["nombre"].lower() != nombre_jugador.lower()]
    scores.append({
        "nombre": nombre_jugador,
        "score": score,
        "aciertos": aciertos,
        "preguntas": preguntas
    })
    scores.sort(key=lambda x: x["score"], reverse=True)
    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump({"date": today, "scores": scores}, f, ensure_ascii=False, indent=2)

# ── Rutas ─────────────────────────────────────────────────────────────────────

@app.route("/")
def menu():
    return render_template("menu.html")

@app.route("/nombre", methods=["GET", "POST"])
def nombre():
    if request.method == "POST":
        nombre_jugador = request.form.get("nombre", "").strip()
        # Bromas ocultas
        bromas = {
            "cielo": "Raquel",
            "anyeelina": "Adriana",
        }
        nombre_jugador = bromas.get(nombre_jugador.lower(), nombre_jugador)
        if nombre_jugador:
            session["nombre"] = nombre_jugador
        return redirect(url_for("reiniciar"))
    return render_template("nombre.html")

@app.route("/jugar")
def jugar():
    escala_nombre = random.choice(list(escalas.keys()))
    grado = random.randint(1, 7)

    session["escala"] = escala_nombre
    session["grado"] = grado
    session["inicio"] = time.time()

    # Inicializar estadísticas si no existen
    if "preguntas" not in session:
        session["preguntas"] = 0
    if "aciertos" not in session:
        session["aciertos"] = 0
    if "fallos" not in session:
        session["fallos"] = 0

    return render_template("juego.html",
                           escala=escala_nombre,
                           grado_texto=formato_grado(grado))

@app.route("/responder", methods=["POST"])
def responder():
    respuesta = request.form["respuesta"].strip().lower().replace(' ', '')
    escala_nombre = session["escala"]
    grado = session["grado"]

    tiempo = time.time() - session["inicio"]
    correcta = escalas[escala_nombre][grado - 1].lower().replace(' ', '')

    correcto = respuesta == correcta

    # Actualizar estadísticas
    session["preguntas"] = session.get("preguntas", 0) + 1
    if correcto:
        session["aciertos"] = session.get("aciertos", 0) + 1
    else:
        session["fallos"] = session.get("fallos", 0) + 1

    return render_template("respuesta.html",
                           correcto=correcto,
                           correcta=escalas[escala_nombre][grado - 1],
                           tiempo=round(tiempo, 2))

@app.route("/resultados")
def resultados():
    preguntas = session.get("preguntas", 0)
    aciertos = session.get("aciertos", 0)
    fallos = session.get("fallos", 0)
    nombre_jugador = session.get("nombre", "")
    score = aciertos * 1

    if nombre_jugador and preguntas > 0:
        save_score(nombre_jugador, score, aciertos, preguntas)

    return render_template("resultados.html",
                           preguntas=preguntas,
                           aciertos=aciertos,
                           fallos=fallos,
                           score=score,
                           nombre=nombre_jugador)

@app.route("/tabla")
def tabla():
    scores = load_scores()
    return render_template("tabla.html", scores=scores)

@app.route("/about")
def about():
    with open("logo.txt", "r", encoding="utf-8") as f:
        contenido = f.read()

    frames = [f.strip() for f in contenido.split("...") if f.strip()]

    return render_template("about.html", frames=frames)

@app.route("/reiniciar")
def reiniciar():
    session["preguntas"] = 0
    session["aciertos"] = 0
    session["fallos"] = 0
    return redirect(url_for("jugar"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)