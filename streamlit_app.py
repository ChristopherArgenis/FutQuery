import streamlit as st

# Título y descripción
st.set_page_config(page_title="FutQuery", layout="wide")
st.title("⚽ FutQuery")
st.markdown("""
Consulta y explora datos de fútbol con SQL.  
**FutQuery** es una herramienta interactiva donde puedes aprender y practicar SQL  
usando una base de datos normalizada construida a partir de datos reales de FIFA.

---

""")

# Tabs principales
tab1, tab2 = st.tabs(["📚 Ejemplos", "🛠️ Ejecutor"])

with tab1:
    st.header("📚 Ejemplos de consultas SQL")
    st.markdown("""
Aquí puedes ver ejemplos de sentencias SQL aplicadas sobre la base de datos de fútbol.  
Cada consulta viene acompañada de la tabla resultante, para que entiendas cómo funciona.

_Pronto mostraremos algunas consultas útiles..._
""")

with tab2:
    st.header("🛠️ Ejecutor SQL")
    st.markdown("""
Escribe tu propia sentencia SQL y obtén el resultado directamente.  
Debajo, puedes ver una lista de las tablas disponibles y cuántos registros tiene cada una.
""")
    # Placeholder para más adelante
    st.info("El ejecutor estará disponible cuando la base de datos esté lista.")
