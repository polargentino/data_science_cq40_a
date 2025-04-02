# -*- coding: utf-8 -*-
"""
ANÁLISIS AVANZADO DE NOTICIAS DE INFOBAE AMÉRICA
Incluye:
- Visualizaciones básicas (wordcloud, histogramas)
- Análisis de sentimiento
- Extracción de entidades (personas/lugares)
- Generación de reporte PDF
"""

# =============================================================================
# SECCIÓN 1: IMPORTAR LIBRERÍAS (Todas las necesarias)
# =============================================================================
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import re
import os
from datetime import datetime
from textblob import TextBlob  # Para análisis de sentimiento
import spacy  # Para extraer entidades nombradas
from fpdf import FPDF  # Para generar reportes

# =============================================================================
# SECCIÓN 2: CONFIGURACIÓN INICIAL (Estilos y carpetas)
# =============================================================================
# Crear carpeta para gráficos
os.makedirs('graficos', exist_ok=True)

# Configuración de estilos matplotlib
plt.style.use('ggplot')
plt.rcParams['figure.dpi'] = 300  # Alta resolución
plt.rcParams['font.size'] = 12

# Cargar modelo de lenguaje español para spaCy
try:
    nlp = spacy.load("es_core_news_sm")
except:
    print("⚠ Modelo spaCy no encontrado. Ejecuta: python -m spacy download es_core_news_sm")

# =============================================================================
# SECCIÓN 3: FUNCIONES DE ANÁLISIS (Cada una con su propósito)
# =============================================================================
def cargar_datos():
    """Carga y preprocesa los datos desde el CSV"""
    try:
        df = pd.read_csv('infobae_noticias.csv')
        print("\n✅ Datos cargados correctamente")
        print(f"📊 Total de noticias: {len(df)}")
        
        # Limpieza básica de texto
        df['titulo_limpio'] = df['titulo'].apply(
            lambda x: re.sub(r'[^\w\s]', '', x.lower())
        )
        
        # Convertir fecha si existe
        if 'fecha_extraccion' in df.columns:
            df['fecha_extraccion'] = pd.to_datetime(df['fecha_extraccion'])
        
        return df
    
    except Exception as e:
        print(f"\n❌ Error al cargar datos: {str(e)}")
        exit()

def generar_wordcloud(texto):
    """Genera una nube de palabras desde el texto"""
    try:
        wordcloud = WordCloud(
            width=1200,
            height=600,
            background_color='white',
            colormap='viridis',
            max_words=200,
            collocations=False  # Evita frases comunes
        ).generate(texto)
        
        plt.figure(figsize=(15, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Palabras más frecuentes en titulares', pad=20)
        
        filename = f"graficos/wordcloud_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(filename, bbox_inches='tight')
        plt.close()
        return filename
    
    except Exception as e:
        print(f"❌ Error al generar wordcloud: {str(e)}")
        return None

def analizar_longitud_titulos(df):
    """Histograma de la longitud de los titulares"""
    try:
        df['longitud'] = df['titulo'].apply(len)
        
        plt.figure(figsize=(12, 6))
        n, bins, patches = plt.hist(
            df['longitud'], 
            bins=20, 
            color='#3498db', 
            edgecolor='#2980b9'
        )
        
        # Destacar la media
        mean_len = df['longitud'].mean()
        plt.axvline(mean_len, color='#e74c3c', linestyle='--', 
                   label=f'Media: {mean_len:.1f} caracteres')
        
        plt.xlabel('Longitud (caracteres)')
        plt.ylabel('Frecuencia')
        plt.title('Distribución de longitud de titulares')
        plt.legend()
        
        filename = f"graficos/longitud_titulos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(filename)
        plt.close()
        return filename
    
    except Exception as e:
        print(f"❌ Error en gráfico de longitud: {str(e)}")
        return None

def top_palabras(df, n=15):
    """Gráfico de las palabras más frecuentes (excluyendo stopwords)"""
    try:
        stopwords = {
            'de', 'la', 'el', 'en', 'y', 'a', 'los', 'las', 
            'del', 'que', 'con', 'por', 'para'
        }
        
        words = [
            word for word in re.findall(r'\b\w+\b', ' '.join(df['titulo_limpio'])) 
            if word not in stopwords and len(word) > 3
        ]
        
        word_counts = Counter(words).most_common(n)
        
        plt.figure(figsize=(12, 6))
        bars = plt.barh(
            [w[0] for w in word_counts],
            [w[1] for w in word_counts],
            color='#2ecc71'
        )
        
        # Añadir etiquetas de valor
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 0.5, bar.get_y() + bar.get_height()/2,
                    f'{int(width)}', ha='left', va='center')
        
        plt.xlabel('Frecuencia')
        plt.title(f'Top {n} palabras en titulares')
        plt.gca().invert_yaxis()
        
        filename = f"graficos/top_palabras_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(filename)
        plt.close()
        return filename
    
    except Exception as e:
        print(f"❌ Error en top palabras: {str(e)}")
        return None

def analizar_sentimiento(df):
    """Calcula la polaridad del sentimiento en titulares"""
    try:
        df['sentimiento'] = df['titulo'].apply(
            lambda x: TextBlob(x).sentiment.polarity
        )
        
        plt.figure(figsize=(12, 6))
        plt.hist(
            df['sentimiento'], 
            bins=20, 
            color='#f39c12', 
            edgecolor='#e67e22',
            alpha=0.7
        )
        
        # Resaltar neutral (0) y extremos (-1, 1)
        for pos in [-1, 0, 1]:
            plt.axvline(pos, color='red', linestyle=':', alpha=0.5)
        
        plt.xlabel('Polaridad (-1 = Negativo, 1 = Positivo)')
        plt.ylabel('Frecuencia')
        plt.title('Distribución de Sentimiento en Titulares')
        
        filename = f"graficos/sentimiento_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(filename)
        plt.close()
        return filename
    
    except Exception as e:
        print(f"❌ Error en análisis de sentimiento: {str(e)}")
        return None

def extraer_entidades(df):
    """Identifica personas y lugares mencionados"""
    try:
        personas = []
        lugares = []
        
        for doc in nlp.pipe(df['titulo'].astype(str), batch_size=50):
            for ent in doc.ents:
                if ent.label_ == "PER":
                    personas.append(ent.text)
                elif ent.label_ == "LOC":
                    lugares.append(ent.text)
        
        # Gráfico para personas
        if personas:
            top_personas = Counter(personas).most_common(10)
            plt.figure(figsize=(12, 6))
            plt.barh(
                [p[0] for p in top_personas],
                [p[1] for p in top_personas],
                color='#9b59b6'
            )
            plt.title('Personas más mencionadas')
            plt.gca().invert_yaxis()
            
            filename_p = f"graficos/personas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(filename_p)
            plt.close()
        else:
            filename_p = None
        
        # Gráfico para lugares
        if lugares:
            top_lugares = Counter(lugares).most_common(10)
            plt.figure(figsize=(12, 6))
            plt.barh(
                [l[0] for l in top_lugares],
                [l[1] for l in top_lugares],
                color='#1abc9c'
            )
            plt.title('Lugares más mencionados')
            plt.gca().invert_yaxis()
            
            filename_l = f"graficos/lugares_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(filename_l)
            plt.close()
        else:
            filename_l = None
        
        return filename_p, filename_l
    
    except Exception as e:
        print(f"❌ Error al extraer entidades: {str(e)}")
        return None, None

def generar_reporte(graficos):
    """Crea un PDF con todos los gráficos generados"""
    try:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Portada
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Reporte de Análisis: Infobae América', 0, 1, 'C')
        pdf.ln(10)
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 10, 
                      f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                      f"Total noticias analizadas: {len(df)}")
        
        # Añadir cada gráfico
        for img in graficos:
            if img and os.path.exists(img):
                pdf.add_page()
                pdf.image(img, x=10, y=10, w=180)
        
        # Guardar PDF
        pdf.output("reporte_analisis.pdf")
        print("\n✅ Reporte generado: 'reporte_analisis.pdf'")
    
    except Exception as e:
        print(f"❌ Error al generar PDF: {str(e)}")

# =============================================================================
# SECCIÓN 4: EJECUCIÓN PRINCIPAL (Orquesta todo el análisis)
# =============================================================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("ANÁLISIS AVANZADO DE INFOBAE AMÉRICA")
    print("="*60)
    
    # Cargar datos
    df = cargar_datos()
    text = ' '.join(df['titulo_limpio'])
    
    # Lista para almacenar gráficos generados
    graficos_generados = []
    
    # Ejecutar análisis
    print("\n🔍 Ejecutando análisis...")
    graficos_generados.append(generar_wordcloud(text))
    graficos_generados.append(analizar_longitud_titulos(df))
    graficos_generados.append(top_palabras(df))
    graficos_generados.append(analizar_sentimiento(df))
    
    # Análisis avanzado (opcional)
    personas_img, lugares_img = extraer_entidades(df)
    if personas_img:
        graficos_generados.append(personas_img)
    if lugares_img:
        graficos_generados.append(lugares_img)
    
    # Filtrar gráficos no generados
    graficos_generados = [g for g in graficos_generados if g is not None]
    
    # Generar reporte final
    generar_reporte(graficos_generados)
    
    print("\n" + "="*60)
    print("🎉 ¡Análisis completado con éxito!")
    print(f"📂 Gráficos guardados en: {os.path.abspath('graficos')}")
    print(f"📄 Reporte PDF generado: 'reporte_analisis.pdf'")
    print("="*60)