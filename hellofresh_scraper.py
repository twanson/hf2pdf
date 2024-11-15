import requests
import sys
import os
from datetime import datetime
from bs4 import BeautifulSoup

def print_debug(mensaje):
    print(mensaje, flush=True)
    with open('debug.log', 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now()}: {mensaje}\n")

def obtener_enlaces_recetas(html):
    print_debug("Analizando HTML en busca de recetas...")
    soup = BeautifulSoup(html, 'html.parser')
    enlaces = []
    
    # Buscar todos los enlaces
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and 'recipes' in href and 'hellofresh.es' in href:
            enlaces.append(href)
            print_debug(f"Receta encontrada: {href}")
    
    return enlaces

def main():
    print_debug("=== Inicio del programa ===")

    try:
        print_debug("1. Verificando directorio actual...")
        directorio_actual = os.getcwd()
        print_debug(f"Directorio actual: {directorio_actual}")

        print_debug("\n2. Intentando acceder a HelloFresh...")
        url = "https://www.hellofresh.es/recipes"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
        }
        
        response = requests.get(url, headers=headers)
        print_debug(f"Código de respuesta: {response.status_code}")
        
        print_debug("\n3. Buscando enlaces de recetas...")
        enlaces_recetas = obtener_enlaces_recetas(response.text)
        
        print_debug(f"\nTotal de enlaces encontrados: {len(enlaces_recetas)}")
        
        # Guardar enlaces en un archivo
        with open('enlaces_recetas.txt', 'w', encoding='utf-8') as f:
            for enlace in enlaces_recetas:
                f.write(enlace + '\n')
        
        print_debug("\n4. Enlaces guardados en 'enlaces_recetas.txt'")

    except Exception as e:
        print_debug(f"\nERROR: {str(e)}")
        print_debug(f"Tipo de error: {type(e)}")

    print_debug("\n=== Fin del programa ===")

if __name__ == "__main__":
    main()
    input("\nPresiona Enter para salir...") 