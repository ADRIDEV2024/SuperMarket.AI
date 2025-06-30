import streamlit as st


def show_settings_panel():
    st.sidebar.header("Chatbot Settings")

    language = st.sidebar.selectbox(
        "Idioma del chatbot",
        options=["Español", "Inglés"],
        index=0
    )

    detail = st.sidebar.radio(
        "Nivel de detalle en las respuestas",
        options=["Short", "Verbose"],
        index=1
    )

    view_products = st.sidebar.radio(
        "Vista de productos",
        options=["List", "Grid"],
        index=0
    )

    notifications = st.sidebar.checkbox(
        "Recibir notificaciones de promociones y ofertas",
        value=True
    )

    market = st.sidebar.selectbox(
        "Supermercado preferido",
        options=["Todos", "Mercadona", "DIA", "Carrefour", "Alcampo"],
        index=0
    )

    return {
        "Idioma": language,
        "Detalle": detail,
        "Vista_Productos": view_products,
        "Notificaciones": notifications,
        "Supermercado": market
    }
