from flask import Flask, render_template, request, session, redirect, url_for
import random
import time

app = Flask(__name__)
app.secret_key = "supersecretkey"

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

@app.route("/")
def menu():
    return render_template("menu.html")

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

    return render_template("resultado.html",
                           correcto=correcto,
                           correcta=escalas[escala_nombre][grado - 1],
                           tiempo=round(tiempo, 2))
@app.route("/resultados")
def resultados():
    preguntas = session.get("preguntas", 0)
    aciertos = session.get("aciertos", 0)
    fallos = session.get("fallos", 0)
    return render_template("resultados.html",
                           preguntas=preguntas,
                           aciertos=aciertos,
                           fallos=fallos)

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