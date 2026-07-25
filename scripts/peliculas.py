import json
import re
import requests

URL = "https://apps2026.online/Peli/budtv.php"

texto = requests.get(URL, timeout=30).text
lineas = texto.splitlines()

peliculas = {}

i = 0
while i < len(lineas):
    linea = lineas[i].strip()

    if linea.startswith("#EXTINF"):
        info = linea

        url = ""
        j = i + 1
        while j < len(lineas):
            if lineas[j].startswith("http"):
                url = lineas[j].strip().split("#EXTGRP:")[0]
                break
            j += 1

        logo = re.search(r'tvg-logo="([^"]+)"', info)
        audio = re.search(r'audio-track="([^"]+)"', info)

        nombre = info.split(",", 1)[1].strip()

        if "|" in nombre:
            ano, titulo = nombre.split("|", 1)
        else:
            ano = ""
            titulo = nombre

        pelicula = {
            "titulo": titulo.strip(),
            "ano": ano.strip(),
            "logo": logo.group(1) if logo else "",
            "url": url,
            "audio": audio.group(1).lower() if audio else ""
        }

        clave = titulo.strip().lower()

        if clave not in peliculas:
            peliculas[clave] = pelicula
        else:
            if peliculas[clave]["audio"] != "spa" and pelicula["audio"] == "spa":
                peliculas[clave] = pelicula

        i = j

    i += 1

resultado = []

for pelicula in peliculas.values():
    pelicula.pop("audio", None)
    resultado.append(pelicula)

resultado.sort(
    key=lambda x: (
        int(x["ano"]) if x["ano"].isdigit() else 0,
        x["titulo"].lower()
    ),
    reverse=True
)

with open("peliculas.json", "w", encoding="utf-8") as f:
    json.dump(resultado, f, ensure_ascii=False, indent=2)

print(f"Películas guardadas: {len(resultado)}")
