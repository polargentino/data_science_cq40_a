"""
Este script extrae títulos y subtítulos de noticias de la página de Infobae América. Voy a explicar las partes principales:

Importación de bibliotecas:

requests: Para hacer la solicitud HTTP a la página web
BeautifulSoup: Para analizar y extraer información del HTML
pandas: Para estructurar los datos
datetime: Para registrar la fecha y hora de extracción


Función scrape_infobae_america():

Realiza una solicitud a la página de Infobae América
Usa un User-Agent para simular un navegador real (ayuda a evitar bloqueos)
Extrae los títulos (elementos h2 con clase story-card-hl)
Extrae los subtítulos (elementos h3 con clase story-card-deck)
Crea un DataFrame con los datos extraídos


Funciones auxiliares:

save_data(): Guarda los datos en un archivo CSV
print_news(): Muestra las noticias extraídas en un formato legible


Bloque principal:

Ejecuta el scraping
Muestra los resultados
Guarda los datos en un archivo CSV



Para ejecutar este script, necesitarás tener instaladas las bibliotecas:pip install requests beautifulsoup4 pandas
Este es un buen punto de partida. Si quieres mejorarlo, podrías:

Extraer también los enlaces a las noticias
Capturar imágenes relacionadas
Implementar un sistema para evitar duplicados si ejecutas el script varias veces
Crear una función para extraer el contenido completo de cada noticia

¿Hay alguna funcionalidad específica que te gustaría añadir o modificar?(Fuente: Claude3.7 Sonnet)
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_infobae_america():
    """
    Extrae títulos y subtítulos de noticias de Infobae América
    
    Returns:
        pandas.DataFrame: DataFrame con los títulos, subtítulos y fecha de extracción
    """
    # URL objetivo
    url = "https://www.infobae.com/america/"
    
    # Headers para simular un navegador real
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        # Realizar la solicitud HTTP
        response = requests.get(url, headers=headers)
        
        # Verificar si la solicitud fue exitosa
        if response.status_code != 200:
            print(f"Error al acceder a la página: Código {response.status_code}")
            return None
            
        # Parsear el contenido HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscar los elementos de las noticias
        # Buscamos los títulos principales (h2 con la clase story-card-hl)
        titles = soup.find_all("h2", class_="story-card-hl")
        
        # Buscamos los subtítulos (h3 con la clase story-card-deck)
        subtitles = soup.find_all("h3", class_="story-card-deck")
        
        # Preparar listas para almacenar los datos
        news_data = []
        
        # Extraer títulos
        for title in titles:
            if title.text.strip():
                news_data.append({
                    "titulo": title.text.strip(),
                    "subtitulo": "",
                    "fecha_extraccion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
        
        # Intentar asociar subtítulos con títulos
        # Nota: Esto es una aproximación ya que la estructura exacta puede variar
        for i, subtitle in enumerate(subtitles):
            if i < len(news_data):
                news_data[i]["subtitulo"] = subtitle.text.strip()
        
        # Crear un DataFrame con los datos
        df = pd.DataFrame(news_data)
        
        return df
        
    except Exception as e:
        print(f"Error durante el scraping: {str(e)}")
        return None

def save_data(df, filename="infobae_noticias.csv"):
    """
    Guarda los datos en un archivo CSV
    
    Args:
        df (pandas.DataFrame): DataFrame con los datos a guardar
        filename (str): Nombre del archivo CSV
    """
    if df is not None and not df.empty:
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Datos guardados en {filename}")
    else:
        print("No hay datos para guardar")

def print_news(df):
    """
    Imprime las noticias extraídas en un formato legible
    
    Args:
        df (pandas.DataFrame): DataFrame con las noticias
    """
    if df is not None and not df.empty:
        print("\n=== ÚLTIMAS NOTICIAS DE INFOBAE AMÉRICA ===\n")
        
        for i, row in df.iterrows():
            print(f"NOTICIA {i+1}:")
            print(f"Título: {row['titulo']}")
            if row['subtitulo']:
                print(f"Subtítulo: {row['subtitulo']}")
            print("-" * 50)
    else:
        print("No se encontraron noticias")

if __name__ == "__main__":
    print("Iniciando scraping de Infobae América...")
    
    # Extraer datos
    news_df = scrape_infobae_america()
    
    # Imprimir noticias
    print_news(news_df)
    
    # Guardar datos
    save_data(news_df)
    
    print("\nProceso completado!") # Salidas: 
#     Iniciando scraping de Infobae América...

# === ÚLTIMAS NOTICIAS DE INFOBAE AMÉRICA ===

# NOTICIA 1:
# Título: El mensaje de Zelensky tras la tensa reunión con Trump
# Subtítulo: El presidente de Ucrania publicó un comentario en la red social X luego del acalorado encuentro con el mandatario estadounidense
# --------------------------------------------------
# NOTICIA 2:
# Título: Tras la discusión, Zelensky abandonó la Casa Blanca sin firmar el acuerdo con EEUU
# Subtítulo: El ucraniano le mostró fotos de las atrocidades cometidas por el ejército ruso y, refiriéndose a Vladimir Putin, dijo que no debería haber “ningún compromiso con un asesino en nuestro territorio”
# --------------------------------------------------
# NOTICIA 3:
# Título: Gene Hackman y Betsy Arakawa habrían muerto semanas antes de ser encontrados, informó la policía
# --------------------------------------------------
# NOTICIA 4:
# Título: Tensa reunión de Trump con Zelensky en la Casa Blanca: “O llegamos a un acuerdo o estamos fuera”
# --------------------------------------------------
# NOTICIA 5:
# Título: El papa Francisco sufrió una crisis “aislada” respiratoria
# --------------------------------------------------
# NOTICIA 6:
# Título: Murió Miguel Piñera, hermano del ex presidente chileno Sebastián, a los 70 años
# --------------------------------------------------
# NOTICIA 7:
# Título: Uno de los rehenes israelíes de Hamas liberados habló sobre su cautivero: “Hay momentos en los que simplemente te desmayas”
# --------------------------------------------------
# NOTICIA 8:
# Título: Gracias al veloz avance de la IA, la Singularidad podría alcanzarse en solo un año, advierten expertos
# --------------------------------------------------
# NOTICIA 9:
# Título: Rafael Caro Quintero: el día que 14 marinos murieron tras participar en operativo para detener al capo de la droga
# --------------------------------------------------
# NOTICIA 10:
# Título: Qué dijo un joven Caro Quintero cuando le preguntaron sobre su extradición a Estados Unidos
# --------------------------------------------------
# NOTICIA 11:
# Título: La heladería favorita del papa Francisco en Roma no es italiana, sino argentina: “Hace 8 años que cada 15 días nos encarga helado”
# --------------------------------------------------
# NOTICIA 12:
# Título: Alineación de 7 planetas: cómo ver esta noche el fenómeno astronómico que no se repetirá hasta dentro de 467 años
# --------------------------------------------------
# NOTICIA 13:
# Título: Esta es la bebida que ayuda a eliminar la placa dental y el sarro de los dientes de una forma rápida
# --------------------------------------------------
# NOTICIA 14:
# Título: El uso de perros en competencias de trineos en Alaska desata críticas por denuncias de maltrato y abandono
# --------------------------------------------------
# NOTICIA 15:
# Título: Veterana actriz porno que se acostó con 300 hombres en un día despotrica contra Bonnie Blue y Lilly Phillips en OnlyFans: “Solo están copiando lo que hicimos antes”
# --------------------------------------------------
# NOTICIA 16:
# Título: La erupción del Vesubio convirtió el cerebro de un hombre en vidrio: por qué y cómo ocurrió
# --------------------------------------------------
# NOTICIA 17:
# Título: Caro Quintero y Vicente Carrillo Fuentes se declaran no culpables ante juez de NY; esta es la fecha de su próxima audiencia
# --------------------------------------------------
# NOTICIA 18:
# Título: Otra joven asegura ser Madeleine McCann y dice tener pruebas de ADN para respaldarlo
# --------------------------------------------------
#NOTICIA 19:
# Título: Misterio en la muerte de Michelle Trachtenberg: su familia no permitió la autopsia
# --------------------------------------------------
# NOTICIA 20:
# Título: Nueva purga de Xi Jinping en el gobierno chino: echó al ministro de Industria y Tecnología de la Información
# --------------------------------------------------
# NOTICIA 21:
# Título: Quiénes son los narcos mexicanos entregados a EEUU que podrían ser condenados a pena de muerte
# --------------------------------------------------
# NOTICIA 22:
# Título: El asesinato de “Kiki” Camarena: el delito que EEUU jamás le perdonó a Caro Quintero
# --------------------------------------------------
# NOTICIA 23:
# Título: Jack Nicholson revela de qué gran actriz de Hollywood copió las claves de su estilo de actuación
# --------------------------------------------------
# NOTICIA 24:
# Título: Un fotógrafo ruso encontró un extraño pez con forma de alien y generó revuelo en redes
# --------------------------------------------------
# NOTICIA 25:
# Título: Cuáles son los efectos secundarios y las contraindicaciones del consumo de la manzanilla
# --------------------------------------------------
# NOTICIA 26:
# Título: Sheinbaum apuesta a una negociación política con Trump para suspender la aplicación de los aranceles a México
# --------------------------------------------------
# NOTICIA 27:
# Título: La Justicia electoral de Ecuador suspendió los derechos de participación política de la vicepresidenta Verónica Abad
# --------------------------------------------------
# NOTICIA 28:
# Título: Encapuchados asaltaron a los guardias de una base naval en Chile: les robaron fusiles, municiones y chalecos
# --------------------------------------------------
# NOTICIA 29:
# Título: Índice global de The Economist: Uruguay y Costa Rica son las únicas “democracias plenas” de América Latina
# --------------------------------------------------
# NOTICIA 30:
# Título: Qué sucede cuando un astronauta se enferma en el espacio
# --------------------------------------------------
# NOTICIA 31:
# Título: La insólita carrera que se celebrará en Australia: ciclistas desnudos recorrerán la ciudad
# --------------------------------------------------
# NOTICIA 32:
# Título: El impacto inmediato de reducir el azúcar: beneficios para la salud y estrategias efectivas
# --------------------------------------------------
# NOTICIA 33:
# Título: Corea del Norte lanzó un misil de crucero “estratégico” para mostrar “la preparación de los medios de operación nuclear”
# --------------------------------------------------
# NOTICIA 34:
# Título: De la neumonía a las rutinas controladas: la evolución de la salud del papa Francisco en 4 claves
# --------------------------------------------------
# NOTICIA 35:
# Título: Chuck Norris no dudó al identificar su mejor película: “Me llevaron a un nivel superior”
# --------------------------------------------------
# NOTICIA 36:
# Título: Starmer convoca una cumbre en Londres sobre Ucrania con 12 líderes europeos, Pedro Sánchez entre ellos
# --------------------------------------------------
# NOTICIA 37:
# Título: La agencia atómica de la ONU advirtió que el sarcófago de Chernobyl sufre incendios latentes tras el ataque de un dron ruso
# --------------------------------------------------
# NOTICIA 38:
# Título: Soldados norcoreanos capturados en Ucrania revelaron detalles de cómo los llevaron a combatir: “No sabía que iba a Rusia”
# --------------------------------------------------
# NOTICIA 39:
# Título: Israel anunció la muerte de un miembro de Hezbollah en un bombardeo en Líbano
# --------------------------------------------------
# NOTICIA 40:
# Título: Egipto anunció el inicio del diálogo entre Israel y Hamas sobre la segunda fase de la tregua en Gaza
# --------------------------------------------------
# NOTICIA 41:
# Título: El jefe del Ejército israelí asumió su responsabilidad por los fallos de seguridad antes y durante el 7 de octubre de 2023
# --------------------------------------------------
# NOTICIA 42:
# Título: Marco Rubio elogió los aportes de México en la extradición de los narcos a Estados Unidos
# --------------------------------------------------
# NOTICIA 43:
# Título: Así es la cárcel en Nueva York donde Caro Quintero, “El Mayo” y “El Nini” están recluidos
# --------------------------------------------------
# NOTICIA 44:
# Título: ¿Por qué los precios de los huevos en EEUU siguen subiendo? La gripe aviar no es la única razón
# --------------------------------------------------
# NOTICIA 45:
# Título: Otro accidente para el Tesla Cybertruck: el vehículo cae en una piscina vacía y genera preocupaciones
# --------------------------------------------------
# NOTICIA 46:
# Título: María Corina Machado denunció que hombres no identificados intentaron ingresar a su vivienda en Caracas
# --------------------------------------------------
# NOTICIA 47:
# Título: Cómo el dinero del botín de guerra de la tortura en Venezuela llega a un equipo de la Copa Libertadores
# --------------------------------------------------
# NOTICIA 48:
# Título: Chile inició el proceso de extradición de “El Fresa” desde Estados Unidos por el crimen de Ronald Ojeda
# --------------------------------------------------
# NOTICIA 49:
# Título: Los Óscar son más globales que nunca pero la competencia de “película internacional” está rota
# --------------------------------------------------
# NOTICIA 50:
# Título: Cuáles son las probabilidades de que Karla Sofía Gascón gane el Oscar a Mejor Actriz por "Emilia Pérez"
# --------------------------------------------------
# NOTICIA 51:
# Título: El Tribunal Electoral de Bolivia rechazó la directiva del nuevo partido de Evo Morales
# --------------------------------------------------
# NOTICIA 52:
# Título: Chile firmó un acuerdo con Bolivia para “reconducir” a los migrantes que entren por la frontera norte
# --------------------------------------------------
# NOTICIA 53:
# Título: En el último mes, Estados Unidos deportó entre cinco y diez ciudadanos bolivianos
# --------------------------------------------------
# NOTICIA 54:
# Título: Show de Stephen Curry: 56 puntos, 12 triples y la inesperada reacción del público rival
# --------------------------------------------------
# NOTICIA 55:
# Título: La inédita anécdota que reveló Neymar con Lionel Messi: cómo le enseñó a patear penales
# --------------------------------------------------
# NOTICIA 56:
# Título: Messi, íntimo: su reacción cuando aparece su nombre en una canción, su futuro y cómo mutó su juego
# --------------------------------------------------
# NOTICIA 57:
# Título: Las dos insólitas banderas rojas en los test de pretemporada en la Fórmula 1
# --------------------------------------------------
# NOTICIA 58:
# Título: Hailee Steinfeld adelantó detalles sobre la película Pecadores: “No se parece a nada en lo que haya participado o visto”
# --------------------------------------------------
# NOTICIA 59:
# Título: Los actores mejor pagos de 2024, según Forbes
# --------------------------------------------------
# NOTICIA 60:
# Título: La nueva Miley Cyrus: “Antes era ‘la ex estrella de Disney rebelde’ y ahora quieren etiquetarme como la chica mala que encontró la paz”
# --------------------------------------------------
# NOTICIA 61:
# Título: Los secretos de Neverland: el icónico rancho de Michael Jackson recobra protagonismo con el rodaje de su biopic
# --------------------------------------------------
# NOTICIA 62:
# Título: ¿Cómo ganar masa muscular entrenando con el propio peso?
# --------------------------------------------------
# NOTICIA 63:
# Título: Comer nueces por la mañana podría ser el secreto para un cerebro más ágil
# --------------------------------------------------
# NOTICIA 64:
# Título: Cómo se contagia el sarampión y quiénes deben vacunarse para evitar esta enfermedad que puede ser mortal
# --------------------------------------------------
# NOTICIA 65:
# Título: Así es el robot humanoide con ‘músculos’ y ‘huesos’ que podría salir pronto al mercado
# --------------------------------------------------
# NOTICIA 66:
# Título: Estas son las mejores frases para enviar por WhatsApp en el Día de la Mujer
# --------------------------------------------------
# NOTICIA 67:
# Título: Músicos contra la IA: Radiohead, Gorillaz, Jamiroquai, The Clash y más anuncian lanzamiento especial
# --------------------------------------------------
# NOTICIA 68:
# Título: Gex Trilogy confirma su lanzamiento para mediados de este año
# --------------------------------------------------
# NOTICIA 69:
# Título: Blades of Fire será el nuevo juego de MercurySteam, estudio detrás de Metroid Dread
# -------------------------------------------------
# NOTICIA 70:
# Título: Terminator 2D: No Fate llevará la icónica película al gaming retro en septiembre
# --------------------------------------------------
# NOTICIA 71:
# Título: The Assessment: el thriller protagonizado por Elizabeth Olsen y Alicia Vikander lanza su primer adelanto
# --------------------------------------------------
# NOTICIA 72:
# Título: Así llegó Caro Quintero a EEUU: las primeras imágenes del narco tras ser entregado
# --------------------------------------------------
# NOTICIA 73:
# Título: El Cristo Redentor de Brasil se iluminó con el rostro del papa Francisco en un mensaje de apoyo por su recuperación
# --------------------------------------------------
# NOTICIA 74:
# Título: Petro presentó al nuevo gabinete para la recta final de su Gobierno: Francia Márquez se va y empieza era de Benedetti
# --------------------------------------------------
# NOTICIA 75:
# Título: La hija de Gene Hackman sospecha que el actor y su esposa murieron envenenados en su casa
# --------------------------------------------------
# NOTICIA 76:
# Título: Nicaragua se retiró del Consejo de DDHH de la ONU tras un informe que denuncia la “maquinaria de represión” del régimen
# --------------------------------------------------
# NOTICIA 77:
# Título: Murió a los 113 años Rose Girone, la sobreviviente del Holocausto más longeva
# --------------------------------------------------
# Datos guardados en infobae_noticias.csv

# Proceso completado!


# ¡Excelente! Me alegra que el script haya funcionado perfectamente. Has extraído con éxito 77 noticias de Infobae América, incluyendo títulos y subtítulos cuando estaban disponibles.
# Algunos aspectos destacables del resultado:

# El script pudo capturar los títulos principales relacionados con eventos actuales como la reunión entre Zelensky y Trump.
# Logró asociar correctamente los subtítulos con sus títulos correspondientes.
# Los datos se guardaron exitosamente en un archivo CSV, lo que te permitirá trabajar con ellos en otras aplicaciones o realizar análisis posteriores.

# Este es un buen primer paso en tu aventura de web scraping. Ahora tienes un conjunto de datos estructurado con el que puedes trabajar.
# ¿Te gustaría continuar desarrollando este script? Algunas ideas para mejorar serían:

# Extraer las URLs de cada noticia para poder acceder al contenido completo
# Añadir categorías o etiquetas de las noticias
# Implementar algún tipo de análisis de sentimiento sobre los títulos
# Configurar el script para que se ejecute automáticamente cada cierto tiempo

# ¿Qué te gustaría explorar a continuación?