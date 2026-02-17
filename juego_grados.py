import random

escalas = {
    "C": ["C", "D", "E", "F", "G", "A", "B"],
    "D": ["D", "E", "F#", "G", "A", "B", "C#"],
    "E": ["E", "F#", "G#", "A", "B", "C#", "D#"],
    "G": ["G", "A", "B", "C", "D", "E", "F#"],
    "A": ["A", "B", "C#", "D", "E", "F#", "G#"],
    "B": ["B", "C#", "D#", "E", "F#", "G#", "A#"],
    "F": ["F", "G", "A", "Bb", "C", "D", "E"],
    "Bb": ["Bb", "C", "D", "Eb", "F", "G", "A"],
    "Eb": ["Eb", "F", "G", "Ab", "Bb", "C", "D"],
    "Ab": ["Ab", "Bb", "C", "Db", "Eb", "F", "G"],
    "Db": ["Db", "Eb", "F", "Gb", "Ab", "Bb", "C"],
    "Gb": ["Gb", "Ab", "Bb", "Cb", "Db", "Eb", "F"],
    "Am": ["A", "B", "C", "D", "E", "F", "G"],
    "Bm": ["B", "C#", "D", "E", "F#", "G", "A"],
    "C#m": ["C#", "D#", "E", "F#", "G#", "A", "B"],
    "Dm": ["D", "E", "F", "G", "A", "Bb", "C"],
    "Em": ["E", "F#", "G", "A", "B", "C", "D"],
    "F#m": ["F#", "G#", "A", "B", "C#", "D", "E"],
    "G#m": ["G#", "A#", "B", "C#", "D#", "E", "F#"]
}

def formato_grado(numero):
    formatos = {
        1: "1er grado",
        2: "2do grado",
        3: "3er grado",
        4: "4to grado",
        5: "5to grado",
        6: "6to grado",
        7: "7mo grado"
    }
    return formatos.get(numero, "")

def generar_pregunta():
    escala_nombre = random.choice(list(escalas.keys()))
    escala = escalas[escala_nombre]
    grado = random.randint(1, 7)

    return {
        "escala": escala_nombre,
        "grado": grado,
        "texto_grado": formato_grado(grado),
        "respuesta_correcta": escala[grado - 1]
    }