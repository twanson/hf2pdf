from bs4 import BeautifulSoup
import pdfkit
import os
from datetime import datetime

def extraer_receta(soup):
    # Extraer título
    titulo = soup.find('h1').text.strip()
    
    # Extraer ingredientes
    ingredientes_enviados = []
    ingredientes_no_enviados = []
    ingredientes_container = soup.find('div', {'data-test-id': 'ingredients-list'})
    if ingredientes_container:
        for item in ingredientes_container.find_all('div', {'data-test-id': 'ingredient-item-shipped'}):
            texto = item.text.strip()
            # Mejorar formato de cantidades y alérgenos
            texto = texto.replace('gramo(s)', 'g ')
            texto = texto.replace('mililitro(s)', 'ml ')
            texto = texto.replace('unidad(es)', 'ud ')
            texto = texto.replace('sobre(s)', 'sobre ')
            texto = texto.replace('cucharada(s)', 'cda ')
            texto = texto.replace('pizca(s)', 'pizca ')
            if 'Contiene' in texto:
                partes = texto.split('(Contiene')
                texto = f"{partes[0].strip()} (Alérgenos:{partes[1]}"
            ingredientes_enviados.append(texto)
            
        for item in ingredientes_container.find_all('div', {'data-test-id': 'ingredient-item-not-shipped'}):
            texto = item.text.strip()
            texto = texto.replace('cucharada(s)', 'cda ')
            texto = texto.replace('unidad(es)', 'ud ')
            ingredientes_no_enviados.append(texto)
    
    # Extraer instrucciones
    instrucciones = []
    instrucciones_container = soup.find('div', {'data-test-id': 'instructions'})
    if instrucciones_container:
        pasos = instrucciones_container.find_all('div', {'data-test-id': 'instruction-step'})
        for paso in pasos:
            instrucciones.append(paso.text.strip())
    
    # Extraer imágenes
    imagenes = []
    hero_image = soup.find('div', {'data-test-id': 'recipe-hero-image'})
    if hero_image and hero_image.find('img'):
        imagenes.append(hero_image.find('img').get('src'))
    
    if instrucciones_container:
        for img in instrucciones_container.find_all('img'):
            imagenes.append(img.get('src'))
    
    return {
        'titulo': titulo,
        'ingredientes_enviados': ingredientes_enviados,
        'ingredientes_no_enviados': ingredientes_no_enviados,
        'instrucciones': instrucciones,
        'imagenes': imagenes
    }

def crear_html(receta):
    return f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            @page {{
                size: A4;
                margin: 1.5cm;
            }}
            body {{
                font-family: 'Segoe UI', Arial, sans-serif;
                line-height: 1.5;
                max-width: 100%;
                margin: 0 auto;
                padding: 0;
                color: #333;
            }}
            h1 {{
                color: #1a1a1a;
                text-align: center;
                font-size: 26px;
                margin: 20px 0;
                padding-bottom: 10px;
                border-bottom: 2px solid #e0e0e0;
            }}
            .imagen-principal {{
                text-align: center;
                margin: 25px 0;
                page-break-inside: avoid;
            }}
            .imagen-principal img {{
                max-width: 90%;
                border-radius: 10px;
                box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            }}
            .seccion {{
                background: #ffffff;
                padding: 25px;
                margin: 20px 0;
                border-radius: 12px;
                border: 1px solid #e0e0e0;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                page-break-inside: avoid;
            }}
            .paso {{
                background: #f8f9fa;
                padding: 20px 25px;
                margin: 15px 0;
                border-radius: 10px;
                page-break-inside: avoid;
                display: grid;
                grid-template-columns: 40px 1fr;
                gap: 15px;
                align-items: start;
            }}
            .paso-numero {{
                background: #2c3e50;
                color: white;
                width: 40px;
                height: 40px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                font-size: 18px;
            }}
            .paso-contenido {{
                flex: 1;
            }}
            .paso img {{
                max-width: 85%;
                border-radius: 8px;
                margin: 15px 0;
                grid-column: 1 / -1;
            }}
            .ingredientes-lista {{
                margin: 15px 0;
                padding: 0 15px;
            }}
            .ingredientes-enviados {{
                position: relative;
                padding-left: 20px;
            }}
            .ingredientes-enviados::before {{
                content: '';
                position: absolute;
                left: 0;
                top: 0;
                bottom: 0;
                width: 4px;
                background: linear-gradient(to bottom, #2ecc71, #27ae60);
                border-radius: 2px;
            }}
            .ingredientes-no-enviados {{
                position: relative;
                padding-left: 20px;
                margin-top: 20px;
            }}
            .ingredientes-no-enviados::before {{
                content: '';
                position: absolute;
                left: 0;
                top: 0;
                bottom: 0;
                width: 4px;
                background: linear-gradient(to bottom, #e74c3c, #c0392b);
                border-radius: 2px;
            }}
            .footer {{
                text-align: center;
                color: #666;
                font-size: 0.9em;
                margin-top: 30px;
                padding: 15px 0;
                border-top: 1px solid #eee;
            }}
            h2 {{
                color: #2c3e50;
                font-size: 22px;
                margin: 0 0 20px 0;
                padding-bottom: 10px;
                border-bottom: 2px solid #eee;
            }}
            h3 {{
                color: #34495e;
                font-size: 18px;
                margin: 0 0 15px 0;
                font-weight: 600;
            }}
            li {{
                margin: 10px 0;
                font-size: 14px;
                line-height: 1.6;
            }}
            p {{
                font-size: 14px;
                line-height: 1.6;
                margin: 0;
            }}
            ul {{
                margin: 0;
                padding-left: 20px;
                list-style-type: none;
            }}
            ul li::before {{
                content: '•';
                color: #3498db;
                font-weight: bold;
                display: inline-block;
                width: 1em;
                margin-left: -1em;
            }}
        </style>
    </head>
    <body>
        <h1>{receta['titulo']}</h1>
        
        <div class="imagen-principal">
            <img src="{receta['imagenes'][0]}" alt="Imagen principal">
        </div>
        
        <div class="seccion">
            <h2>Ingredientes</h2>
            
            <div class="ingredientes-lista ingredientes-enviados">
                <h3>📦 Ingredientes incluidos</h3>
                <ul>
                    {''.join(f'<li>{ingrediente}</li>' for ingrediente in receta['ingredientes_enviados'])}
                </ul>
            </div>
            
            <div class="ingredientes-lista ingredientes-no-enviados">
                <h3>🏠 Necesitarás en casa</h3>
                <ul>
                    {''.join(f'<li>{ingrediente}</li>' for ingrediente in receta['ingredientes_no_enviados'])}
                </ul>
            </div>
        </div>
        
        <div class="seccion">
            <h2>Preparación</h2>
            {''.join(
                f'<div class="paso">'
                f'<div class="paso-numero">{i+1}</div>'
                f'<div class="paso-contenido">'
                f'<p>{paso}</p>'
                f'{"<img src=\"" + receta["imagenes"][i+1] + "\" alt=\"Paso " + str(i+1) + "\">" if i+1 < len(receta["imagenes"]) else ""}'
                f'</div>'
                f'</div>'
                for i, paso in enumerate(receta['instrucciones'])
            )}
        </div>
        
        <div class="footer">
            <p>Receta generada el {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        </div>
    </body>
    </html>
    """

def main():
    print("=== Iniciando conversión de recetas a PDF ===")
    
    print("\nVerificando configuración...")
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    if not os.path.exists(path_wkhtmltopdf):
        print(f"❌ Error: No se encuentra wkhtmltopdf en {path_wkhtmltopdf}")
        return
    print("✅ wkhtmltopdf encontrado")
    
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    
    print("\nBuscando archivos HTML...")
    if not os.path.exists('recetas'):
        print("❌ Error: No se encuentra la carpeta 'recetas'")
        return
        
    archivos = [f for f in os.listdir('recetas') if f.endswith('.html')]
    total = len(archivos)
    
    if total == 0:
        print("❌ No se encontraron archivos HTML en la carpeta 'recetas'")
        return
    
    print(f"✅ Encontrados {total} archivos para procesar")
    
    print("\nCreando carpeta de salida...")
    if not os.path.exists('pdfs'):
        os.makedirs('pdfs')
        print("✅ Carpeta 'pdfs' creada")
    else:
        print("✅ Carpeta 'pdfs' ya existe")
    
    options = {
        'page-size': 'A4',
        'margin-top': '15mm',
        'margin-right': '15mm',
        'margin-bottom': '15mm',
        'margin-left': '15mm',
        'encoding': 'UTF-8',
        'enable-local-file-access': None,
        'print-media-type': None,
        'no-background': None
    }
    
    for i, archivo in enumerate(archivos, 1):
        nombre = os.path.splitext(archivo)[0]
        print(f"\n[{i}/{total}] Procesando: {nombre}")
        
        try:
            print("  ⌛ Leyendo archivo HTML...")
            with open(os.path.join('recetas', archivo), 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
            
            print("  ⌛ Extrayendo información...")
            receta = extraer_receta(soup)
            
            print("  ⌛ Generando HTML limpio...")
            html_limpio = crear_html(receta)
            
            print("  ⌛ Convirtiendo a PDF...")
            pdf_path = os.path.join('pdfs', f"{nombre}.pdf")
            pdfkit.from_string(html_limpio, pdf_path, options=options, configuration=config)
            
            print(f"  ✅ PDF generado: {pdf_path}")
            
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
    
    print("\n=== Conversión completada ===")
    print(f"PDFs generados: {total}")

if __name__ == "__main__":
    main()
    input("\nPresiona Enter para salir...")
