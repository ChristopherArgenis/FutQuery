import streamlit as st
import sqlite3
import pandas as pd

# Conexión a la base de datos
conn = sqlite3.connect("fifa2015.db")
cursor = conn.cursor()

# Configuración de la app
st.set_page_config(page_title="FutQuery", layout="wide")

st.title("⚽ FutQuery")
st.markdown("""
**FutQuery** es una herramienta interactiva para explorar y consultar datos FIFA usando SQL.

- En la pestaña **Ejemplos**, puedes ver consultas SQL predefinidas y sus resultados.
- En la pestaña **Ejecutor SQL**, puedes escribir tus propias sentencias y explorar libremente la base de datos.
""")

# Tabs principales
tab1, tab2, tab3 = st.tabs(["🧠 Ejemplos", "🛠️ Ejecutor SQL", "🗂️ Acerca de..."])

# TAB 1: Ejemplos
with tab1:
    st.subheader("📌 Consultas SQL de ejemplo")

    ejemplos = [
        {
            "titulo": "Jugadores y sus nacionalidades",
            "sql": """
                SELECT Jugador.alias, Pais.Nombre
                FROM Jugador
                JOIN J_Info ON Jugador.id = J_Info.id
                JOIN Pais ON J_Info.id_pais = Pais.id
                LIMIT 10;
            """,
            "descripcion": "Muestra los jugadores y el país al que pertenecen."
        },
        {
            "titulo": "Top 5 jugadores con mayor valoración general",
            "sql": """
                SELECT Jugador.alias, Metricas.General
                FROM Jugador
                JOIN J_Indicador ON Jugador.id = J_Indicador.id
                JOIN Metricas ON J_Indicador.id_metricas = Metricas.id
                ORDER BY Metricas.General DESC
                LIMIT 5;
            """,
            "descripcion": "Jugadores con la mejor media general."
        },
        {
            "titulo": "Club con más jugadores",
            "sql": """
                SELECT Club.Nombre, COUNT(*) as cantidad
                FROM J_Info
                JOIN Club ON J_Info.id_club = Club.id
                GROUP BY Club.Nombre
                ORDER BY cantidad DESC
                LIMIT 1;
            """,
            "descripcion": "Club con más jugadores registrados en la base."
        },
        {
            "titulo": "Promedio de altura por nacionalidad",
            "sql": """
                SELECT Pais.Nombre, AVG(Jugador.Altura) as altura_promedio
                FROM Jugador
                JOIN J_Info ON Jugador.id = J_Info.id
                JOIN Pais ON J_Info.id_pais = Pais.id
                GROUP BY Pais.Nombre
                ORDER BY altura_promedio DESC
                LIMIT 10;
            """,
            "descripcion": "Altura promedio de jugadores por país."
        },
        {
            "titulo": "Jugadores zurdos con mayor pase",
            "sql": """
                SELECT Jugador.alias, Metricas.Pase
                FROM Jugador
                JOIN J_Indicador ON Jugador.id = J_Indicador.id
                JOIN Metricas ON J_Indicador.id_metricas = Metricas.id
                WHERE Jugador.Pie_preferente = 'Izquierdo'
                ORDER BY Metricas.Pase DESC
                LIMIT 10;
            """,
            "descripcion": "Jugadores zurdos con mayor habilidad de pase."
        },
        {
            "titulo": "Jugadores con mejor agilidad",
            "sql": """
                SELECT Jugador.alias, Habilidades.Agilidad
                FROM Jugador
                JOIN J_Indicador ON Jugador.id = J_Indicador.id
                JOIN Habilidades ON J_Indicador.id_habilidades = Habilidades.id
                ORDER BY Habilidades.Agilidad DESC
                LIMIT 10;
            """,
            "descripcion": "Muestra los jugadores más ágiles."
        },
        {
            "titulo": "Valor promedio de mercado por club",
            "sql": """
                SELECT Club.Nombre, AVG(Finanzas.Valuacion) as valor_promedio
                FROM J_Info
                JOIN Club ON J_Info.id_club = Club.id
                JOIN Finanzas ON J_Info.id_finanzas = Finanzas.id
                GROUP BY Club.Nombre
                ORDER BY valor_promedio DESC
                LIMIT 10;
            """,
            "descripcion": "Compara el valor promedio de mercado por club."
        },
        {
            "titulo": "Distribución por pie preferente",
            "sql": """
                SELECT Pie_preferente, COUNT(*) as cantidad
                FROM Jugador
                GROUP BY Pie_preferente;
            """,
            "descripcion": "Distribución entre diestros y zurdos."
        },
        {
            "titulo": "Relación entre potencial y edad",
            "sql": """
                SELECT Jugador.Edad, AVG(Metricas.Potencial) as potencial_promedio
                FROM Jugador
                JOIN J_Indicador ON Jugador.id = J_Indicador.id
                JOIN Metricas ON J_Indicador.id_metricas = Metricas.id
                GROUP BY Jugador.Edad
                ORDER BY Jugador.Edad;
            """,
            "descripcion": "Cómo varía el potencial con la edad."
        },
        {
            "titulo": "Jugadores con más control de balón",
            "sql": """
                SELECT Jugador.alias, Habilidades.'Control de Balon'
                FROM Jugador
                JOIN J_Indicador ON Jugador.id = J_Indicador.id
                JOIN Habilidades ON J_Indicador.id_habilidades = Habilidades.id
                ORDER BY Habilidades.'Control de Balon' DESC
                LIMIT 10;
            """,
            "descripcion": "Jugadores con mejor control de balón."
        },
    ]

    for ejemplo in ejemplos:
        with st.expander(ejemplo["titulo"]):
            st.markdown(f"**Descripción:** {ejemplo['descripcion']}")
            st.code(ejemplo["sql"], language="sql")
            try:
                resultado = pd.read_sql_query(ejemplo["sql"], conn)
                st.dataframe(resultado)
            except Exception as e:
                st.error(f"Error al ejecutar la consulta: {e}")

# TAB 2: Ejecutor SQL
with tab2:
    st.subheader("✍️ Escribe tu propia consulta SQL")
    col1, col2 = st.columns([2, 1])

    with col1:
        consulta_usuario = st.text_area("Escribe tu consulta SQL aquí:", height=200)
        if st.button("Ejecutar consulta"):
            try:
                resultado = pd.read_sql_query(consulta_usuario, conn)
                st.dataframe(resultado)
            except Exception as e:
                st.error(f"❌ Error al ejecutar la consulta: {e}")

    with col2:
        st.markdown("### 📋 Tablas disponibles")
        tablas = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        for (tabla,) in tablas:
            total = cursor.execute(f"SELECT COUNT(*) FROM {tabla}").fetchone()[0]
            st.markdown(f"- `{tabla}` ({total} registros)")

with tab3:
    st.markdown("### 🎓 Acerca de FutQuery")

    st.markdown("""
    #### 1. Objetivo del Proyecto
    Este proyecto tiene como objetivo principal servir como herramienta educativa para practicar y visualizar consultas SQL aplicadas a un conjunto de datos real. Utiliza información sobre jugadores de FIFA 2015 para explorar características individuales y relaciones como nacionalidad, club, posición y más.

    #### 2. Contexto y Aplicabilidad
    - **Propósito**: Analizar diversas características y relaciones de jugadores de FIFA 2015 usando SQL.
    - **Aplicación**: Útil para estudiantes, analistas de datos y fanáticos del fútbol interesados en aprender SQL de manera práctica e intuitiva.

    #### 3. Origen del Dataset
    - **Fuente**: Kaggle.
    - **Año de Referencia**: 2015.

    #### 4. Normalización y Diagrama Relacional
    - Se llevó a cabo un proceso de **normalización** del dataset original en múltiples tablas, buscando claridad semántica y eficiencia en las relaciones.
    - **Dificultades**: La principal complejidad fue estructurar correctamente las relaciones entre entidades como jugador, club, país, métricas, etc.

    #### 5. Generación del Nuevo Dataset
    El desarrollador realizó:
    - La normalización del dataset.
    - La creación de una base de datos con SQLAlchemy.
    - Un script de procesamiento para poblar las tablas.
    - La construcción de una aplicación interactiva para ejecutar queries que permiten generar nuevos datasets o vistas a partir de las relaciones.

    #### 6. Entregables del Proyecto
    - Dataset base con la información original.
    - Diagrama relacional normalizado.
    - Aplicación interactiva con dos vistas:
      - Ejemplos de consultas SQL.
      - Ejecutador personalizado de queries SQL.

    #### 7. Información del Estudiante
    - **Nombre**: Christopher Argenis Preciado Silva  
    - **Edad**: 20 años  
    - **Matrícula**: 376907

    #### 8. Conclusión del Proyecto
    Durante el desarrollo de este proyecto, se consolidaron múltiples aprendizajes adquiridos en clase, incluyendo la normalización de datos, la creación de relaciones entre tablas y la escritura de consultas SQL complejas. A nivel técnico, uno de los principales desafíos fue decidir cómo poblar correctamente las tablas normalizadas y cómo estructurar las relaciones entre ellas para que reflejaran adecuadamente la lógica del dominio.

    Uno de los mayores logros fue convertir este análisis en una aplicación web interactiva con Streamlit, que no solo sirve como repositorio de ejemplos sino también como un entorno para ejecutar consultas SQL personalizadas. El ejecutor SQL representa un valor añadido, permitiendo al usuario practicar libremente en una base de datos bien estructurada.

    Esta herramienta tiene un gran potencial práctico, especialmente como apoyo educativo para estudiantes y fanáticos del fútbol que deseen practicar SQL sobre un contexto familiar y atractivo. Finalmente, una mejora futura destacable sería incorporar un asistente con inteligencia artificial que interprete lenguaje natural y lo convierta automáticamente en sentencias SQL, haciendo la experiencia aún más accesible e innovadora.
    """)

    st.markdown("### 🗂️ Diagrama Relacional")
    st.image("tables_BD.png", caption="Diagrama Relacional de la Base de Datos Normalizada (FIFA 2015)", use_column_width=True)
