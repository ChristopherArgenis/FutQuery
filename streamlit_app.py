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
tab1, tab2 = st.tabs(["🧠 Ejemplos", "🛠️ Ejecutor SQL"])

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