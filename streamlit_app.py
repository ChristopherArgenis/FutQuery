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

    ejemplos = {
        "Jugadores y sus nacionalidades": "SELECT short_name, nationality_name FROM Jugador INNER JOIN Pais ON Jugador.pais_id = Pais.id LIMIT 10;",
        "Top 5 jugadores con mayor valoración": "SELECT short_name, overall FROM Jugador INNER JOIN J_Indicador ON Jugador.id = J_Indicador.jugador_id ORDER BY overall DESC LIMIT 5;",
        "Club con más jugadores": "SELECT club_name, COUNT(*) as cantidad FROM Club INNER JOIN J_Info ON Club.id = J_Info.club_id GROUP BY club_name ORDER BY cantidad DESC LIMIT 1;"
    }

    consulta_seleccionada = st.selectbox("Selecciona una consulta de ejemplo:", list(ejemplos.keys()))
    sql = ejemplos[consulta_seleccionada]

    st.code(sql, language="sql")

    try:
        resultado = pd.read_sql_query(sql, conn)
        st.dataframe(resultado)
    except Exception as e:
        st.error(f"Error al ejecutar la consulta: {e}")

# TAB 2: Ejecutor SQL
with tab2:
    st.subheader("✍️ Escribe tu propia consulta SQL")

    # Mostrar nombres de tablas y registros
    st.markdown("### Tablas disponibles")
    tablas = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    for (tabla,) in tablas:
        total = cursor.execute(f"SELECT COUNT(*) FROM {tabla}").fetchone()[0]
        st.markdown(f"- `{tabla}` ({total} registros)")

    consulta_usuario = st.text_area("Escribe tu consulta SQL aquí:", height=150)

    if st.button("Ejecutar consulta"):
        try:
            resultado = pd.read_sql_query(consulta_usuario, conn)
            st.dataframe(resultado)
        except Exception as e:
            st.error(f"❌ Error al ejecutar la consulta: {e}")