import streamlit as st
import sqlite3
import pandas as pd

# Conexion a la base de datos
conn = sqlite3.connect("fifa2015.db")
cursor = conn.cursor()

# Configuración de la app
st.set_page_config(page_title="FutQuery", layout="wide")

# Título y descripción
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
            "sql": "SELECT alias, pais FROM Jugador INNER JOIN Pais ON Jugador.pais_id = Pais.id LIMIT 10;",
            "descripcion": "Consulta para ver los nombres de los jugadores y el país al que pertenecen. Útil para conocer la diversidad de nacionalidades."
        },
        {
            "titulo": "Top 5 jugadores con mayor valoración general",
            "sql": "SELECT alias, valoracion FROM Jugador INNER JOIN J_Indicador ON Jugador.id = J_Indicador.jugador_id ORDER BY overall DESC LIMIT 5;",
            "descripcion": "Identifica a los jugadores mejor valorados según su media general."
        },
        {
            "titulo": "Club con más jugadores",
            "sql": "SELECT club, COUNT(*) AS cantidad FROM Club INNER JOIN J_Info ON Club.id = J_Info.club_id GROUP BY club_name ORDER BY cantidad DESC LIMIT 1;",
            "descripcion": "Nos permite saber qué club tiene más jugadores en la base de datos."
        },
        {
            "titulo": "Promedio de altura por nacionalidad",
            "sql": "SELECT pais, AVG(height_cm) AS altura_promedio FROM Jugador INNER JOIN Pais ON Jugador.pais_id = Pais.id GROUP BY nationality_name ORDER BY altura_promedio DESC LIMIT 10;",
            "descripcion": "Analiza el promedio de estatura por país."
        },
        {
            "titulo": "Jugadores zurdos con mayor pase",
            "sql": "SELECT alias, pase FROM Jugador INNER JOIN J_Indicador ON Jugador.id = J_Indicador.jugador_id WHERE preferred_foot = 'Left' ORDER BY passing DESC LIMIT 10;",
            "descripcion": "Explora jugadores zurdos con mejores capacidades de pase."
        },
        {
            "titulo": "Jugadores con mejor agilidad",
            "sql": "SELECT alias, agilidad FROM Jugador INNER JOIN J_Indicador ON Jugador.id = J_Indicador.jugador_id ORDER BY movement_agility DESC LIMIT 10;",
            "descripcion": "Muestra los jugadores más ágiles según su estadística de agilidad."
        },
        {
            "titulo": "Valor promedio de mercado por club",
            "sql": "SELECT club, AVG(valuacion) AS valor_promedio FROM Club INNER JOIN J_Info ON Club.id = J_Info.club_id INNER JOIN Finanzas ON Finanzas.id = J_Info.finanzas_id GROUP BY club_name ORDER BY valor_promedio DESC LIMIT 10;",
            "descripcion": "Compara el valor promedio de los jugadores en los clubes."
        },
        {
            "titulo": "Distribución de jugadores por pie preferido",
            "sql": "SELECT pie_preferido, COUNT(*) AS cantidad FROM Jugador GROUP BY pie_preferido;",
            "descripcion": "Conoce cuántos jugadores son diestros o zurdos."
        },
        {
            "titulo": "Relación entre potencial y edad",
            "sql": "SELECT edad, AVG(potencial) AS potencial_promedio FROM Jugador INNER JOIN J_Indicador ON Jugador.id = J_Indicador.jugador_id GROUP BY age ORDER BY edad;",
            "descripcion": "Evalúa cómo varía el potencial según la edad."
        },
        {
            "titulo": "Jugadores con más control de balón",
            "sql": "SELECT alias, control_balon FROM Jugador INNER JOIN J_Indicador ON Jugador.id = J_Indicador.jugador_id ORDER BY skill_ball_control DESC LIMIT 10;",
            "descripcion": "Muestra los jugadores con mayor control del balón."
        }
    ]

    for ejemplo in ejemplos:
        with st.expander(ejemplo["titulo"]):
            st.markdown(f"**Descripción:** {ejemplo['descripcion']}")
            st.code(ejemplo['sql'], language="sql")
            try:
                resultado = pd.read_sql_query(ejemplo['sql'], conn)
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
