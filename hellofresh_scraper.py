import requests
import sys
import os
from datetime import datetime
from bs4 import BeautifulSoup
import time
import json

def print_debug(mensaje):
    print(mensaje, flush=True)
    with open('debug.log', 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now()}: {mensaje}\n")

def obtener_detalles_receta(url):
    print_debug(f"\nObteniendo receta: {url}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Crear directorio para recetas si no existe
        if not os.path.exists('recetas'):
            os.makedirs('recetas')
        
        # Obtener título de la receta
        titulo = soup.find('h1').text.strip() if soup.find('h1') else "Receta sin título"
        
        # Crear nombre de archivo válido
        nombre_archivo = "".join(x for x in titulo if x.isalnum() or x in (' ','-','_')).rstrip()
        ruta_archivo = os.path.join('recetas', f"{nombre_archivo}.html")
        
        # Guardar la página HTML
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print_debug(f"Receta guardada: {nombre_archivo}")
        return True
        
    except Exception as e:
        print_debug(f"Error al obtener receta: {str(e)}")
        return False

def main():
    print_debug("=== Iniciando descarga de recetas ===")
    
    # Leer enlaces de recetas
    with open('enlaces_recetas.txt', 'r', encoding='utf-8') as f:
        enlaces = [line.strip() for line in f if 'recipes' in line and not line.endswith('/recipes')]
    
    total_recetas = len(enlaces)
    print_debug(f"Total de recetas a descargar: {total_recetas}")
    
    # Descargar cada receta
    recetas_descargadas = 0
    for i, url in enumerate(enlaces, 1):
        print_debug(f"\nProcesando receta {i}/{total_recetas}")
        if obtener_detalles_receta(url):
            recetas_descargadas += 1
        time.sleep(1)  # Pausa entre descargas
    
    print_debug(f"\n=== Descarga completada ===")
    print_debug(f"Recetas descargadas: {recetas_descargadas}/{total_recetas}")

if __name__ == "__main__":
    main()
    input("\nPresiona Enter para salir...") 