# -*- coding: utf-8 -*-
"""
ANÁLISIS DE DATOS DE INFOBAE AMÉRICA
Script para visualizar datos recolectados del scraping
"""

# =============================================================================
# 1. IMPORTAR LIBRERÍAS
# =============================================================================
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import re
import os
from datetime import datetime

# =============================================================================
# 2. CONFIGURACIÓN INICIAL
# =============================================================================
# Crear carpeta para guardar gráficos (si no existe)
os.makedirs('graficos', exist_ok=True)

# Configuración de estilos para matplotlib
plt.style.use('ggplot')
plt.rcParams['figure.dpi'] = 150  # Aumentar resolución
plt.rcParams['savefig.bbox'] = 'tight'

# =============================================================================
# 3. CARGA Y PREPROCESAMIENTO DE DATOS
# =============================================================================
try:
    df = pd.read_csv('infobae_noticias.csv')
    print("\n✅ Datos cargados correctamente")
    print(f"📊 Total de noticias: {len(df)}")
    
    # Preprocesamiento de texto
    df['titulo_limpio'] = df['titulo'].apply(lambda x: re.sub(r'[^\w\s]', '', x.lower()))
    text = ' '.join(df['titulo_limpio'])
    
    # Convertir fecha si existe
    if 'fecha_extraccion' in df.columns:
        df['fecha_extraccion'] = pd.to_datetime(df['fecha_extraccion'])
    
except Exception as e:
    print(f"\n❌ Error al cargar datos: {str(e)}")
    exit()

# =============================================================================
# 4. FUNCIONES PARA VISUALIZACIÓN
# =============================================================================
def generar_wordcloud(texto):
    """Genera y guarda nube de palabras"""
    print("\nGenerando nube de palabras...")
    try:
        wordcloud = WordCloud(
            width=1200,
            height=600,
            background_color='white',
            colormap='viridis',
            max_words=200
        ).generate(texto)
        
        plt.figure(figsize=(15, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Palabras más frecuentes en titulares - Infobae América', pad=20, fontsize=14)
        
        # Guardar con marca de tiempo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"graficos/wordcloud_{timestamp}.png"
        plt.savefig(filename)
        print(f"✅ Wordcloud guardado como: {filename}")
        plt.close()
        
    except Exception as e:
        print(f"❌ Error al generar wordcloud: {str(e)}")

def grafico_longitud_titulos(df):
    """Histograma de longitud de titulares"""
    print("\nAnalizando longitud de titulares...")
    try:
        df['longitud'] = df['titulo'].apply(len)
        
        plt.figure(figsize=(12, 6))
        plt.hist(df['longitud'], bins=20, color='#3498db', edgecolor='#2980b9')
        
        plt.xlabel('Cantidad de caracteres', fontsize=12)
        plt.ylabel('Frecuencia', fontsize=12)
        plt.title('Distribución de longitud de titulares', fontsize=14)
        plt.grid(True, alpha=0.3)
        
        # Líneas de referencia
        mean_len = df['longitud'].mean()
        plt.axvline(mean_len, color='#e74c3c', linestyle='--', 
                   label=f'Media: {mean_len:.1f} chars')
        plt.legend()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"graficos/longitud_titulos_{timestamp}.png"
        plt.savefig(filename)
        print(f"✅ Gráfico de longitud guardado como: {filename}")
        plt.close()
        
    except Exception as e:
        print(f"❌ Error en gráfico de longitud: {str(e)}")

def top_palabras(df, n=15):
    """Gráfico de barras con palabras más frecuentes"""
    print("\nCalculando palabras más frecuentes...")
    try:
        # Contar palabras excluyendo stopwords en español
        stopwords = {'de', 'la', 'el', 'en', 'y', 'a', 'los', 'las', 'del', 'que', 'con'}
        words = [word for word in re.findall(r'\b\w+\b', text) 
                if word not in stopwords and len(word) > 3]
        
        word_counts = Counter(words).most_common(n)
        
        plt.figure(figsize=(12, 6))
        plt.barh(
            [w[0] for w in word_counts],
            [w[1] for w in word_counts],
            color='#2ecc71'
        )
        
        plt.xlabel('Frecuencia', fontsize=12)
        plt.title(f'Top {n} palabras en titulares (excluyendo stopwords)', fontsize=14)
        plt.gca().invert_yaxis()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"graficos/top_palabras_{timestamp}.png"
        plt.savefig(filename)
        print(f"✅ Top {n} palabras guardado como: {filename}")
        plt.close()
        
    except Exception as e:
        print(f"❌ Error en top palabras: {str(e)}")

def analisis_temporal(df):
    """Gráficos temporales si hay datos suficientes"""
    if 'fecha_extraccion' not in df.columns:
        print("\n⚠ No hay datos temporales para analizar")
        return
        
    print("\nAnalizando patrones temporales...")
    try:
        # Extraer hora y día
        df['hora'] = df['fecha_extraccion'].dt.hour
        df['dia'] = df['fecha_extraccion'].dt.date
        
        # Gráfico por horas
        plt.figure(figsize=(12, 6))
        df['hora'].value_counts().sort_index().plot(
            kind='bar', 
            color='#9b59b6',
            title='Distribución de noticias por hora del día'
        )
        plt.xlabel('Hora del día')
        plt.ylabel('Número de noticias')
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"graficos/distribucion_horas_{timestamp}.png"
        plt.savefig(filename)
        print(f"✅ Distribución por horas guardada como: {filename}")
        plt.close()
        
    except Exception as e:
        print(f"❌ Error en análisis temporal: {str(e)}")

# =============================================================================
# 5. EJECUCIÓN DE ANÁLISIS
# =============================================================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("ANÁLISIS DE DATOS DE INFOBAE AMÉRICA")
    print("="*60)
    
    # Ejecutar todas las visualizaciones
    generar_wordcloud(text)
    grafico_longitud_titulos(df)
    top_palabras(df, n=15)
    analisis_temporal(df)
    
    print("\n" + "="*60)
    print(f"🎉 Análisis completado! Gráficos guardados en /graficos/")
    print("="*60)