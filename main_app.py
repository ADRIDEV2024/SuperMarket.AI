import streamlit as st
import time
import random
from datetime import datetime
from utils import config

# Configuración inicial de la página
st.set_page_config(
    page_title="Supermarket.AI Assistant",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

PRODUCTS_DB = config.PRODUCTS_DATA_PATH


def init_state():

    if "mensajes" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "rol": "asistente",
            "contenido": "¡Hola! Soy Supermarket.AI, aunque me puedes llamar Rita. Puedo ayudarte ofreciéndote información sobre productos, precios, disponibilidad y recomendaciones. ¿En qué puedo ayudarte hoy?",
            "timestamp": datetime.now()
        })
    
    if "usuario_nombre" not in st.session_state:
        st.session_state.usuario_nombre = ""
    
    if "conversacion_activa" not in st.session_state:
        st.session_state.conversacion_activa = False


def search_products(query):
   
    consulta = query.lower().strip()
    if not consulta:
        return []
    
    products_finded = []
    
    for category, products in PRODUCTS_DB:
        for name, info in products:
            # Busca coincidencias en el nombre del producto o en su descripción
                      
            if (
                consulta in name.lower() or
                consulta in (info.get("descripcion") or "").lower() or
                consulta in category.lower()
            ):
                products_finded.append({
                    "name": name,
                    "category": category,
                    "price": info.get("price"),
                    "stock": info.get("stock"),
                    "description": info.get("description")
                })
    
    return products_finded 


def generate_bot_response(user_message):
    """
    Genera una respuesta del chatbot basada en el mensaje del usuario.
    Esta función simula el procesamiento de lenguaje natural y 
    proporciona respuestas contextualmente apropiadas.
    """
    mensaje = user_message.lower()
    
    # Saludos y despedidas
    if any(saludo in mensaje for saludo in ["hola", "buenos días", "buenas tardes", "buenas"]):
        return "¡Hola! Es un placer ayudarte. ¿Qué producto necesitas encontrar hoy?"
    
    if any(despedida in mensaje for despedida in ["adiós", "gracias", "hasta luego", "chao"]):
        return "¡De nada! Ha sido un placer ayudarte. ¡Que tengas un excelente día y disfrutes tus compras!"
    
    # Consultas sobre precios
    if "precio" in mensaje or "cuesta" in mensaje or "vale" in mensaje:
        productos = search_products(mensaje)
        if productos:
            respuesta = "Aquí tienes los precios que encontré:\n\n"
            for producto in productos[:3]:  # Limitar a 3 resultados para no saturar
                respuesta += f"🏷️ **{producto['name'].title()}**: {producto['price']}€\n"
                respuesta += f"   📝 {producto['description']}\n\n"
            return respuesta
        else:
            return "Lo siento, no encontré información de precios para ese producto. ¿Podrías ser más específico o probar con otro producto?"
    
    # Consultas sobre disponibilidad/stock
    if "hay" in mensaje or "stock" in mensaje or "disponible" in mensaje or "tenéis" in mensaje:
        productos = search_products(mensaje)
        if productos:
            respuesta = "Información de disponibilidad:\n\n"
            for producto in productos[:15]:
                estado_stock = "✅ Disponible" if producto['stock'] > 0 else "❌ Agotado"
                respuesta += f"{estado_stock} **{producto['name'].title()}**\n"
                respuesta += f"   📦 Stock: {producto['stock']} unidades\n"
                respuesta += f"   💰 Precio: {producto['price']}€\n\n"
            return respuesta
        else:
            return "No encontré ese producto en nuestro inventario. ¿Te refieres a algún producto similar?"
    
    # Búsqueda general de productos
    productos = search_products(mensaje)
    if productos:
        respuesta = f"Encontré {len(productos)} producto(s) relacionado(s):\n\n"
        for producto in productos[:15]:
            respuesta += f"🛒 **{producto['nombre'].title()}** ({producto['categoria'].title()})\n"
            respuesta += f"   📝 {producto['descripcion']}\n"
            respuesta += f"   💰 Precio: {producto['precio']}€\n"
            respuesta += f"   📦 Stock: {producto['stock']} unidades\n\n"
        
        if len(productos) > 15:
            respuesta += f"... y {len(productos) - 15} productos más. ¿Te gustaría que busque algo más específico?"
        
        return respuesta
    
    # Respuestas para consultas no reconocidas
    generic_responses = [
        "Interesante pregunta. ¿Podrías darme más detalles sobre qué producto específico necesitas?",
        "No estoy seguro de entender completamente. ¿Buscas información sobre algún producto en particular?",
        "Me gustaría ayudarte mejor. ¿Podrías reformular tu pregunta o mencionar un producto específico?",
        "¿Podrías ser más específico? Puedo ayudarte con precios, disponibilidad o información sobre productos."
    ]
    
    return random.choice(generic_responses)

def mostrar_mensaje(mensaje, es_usuario=True):
    """
    Muestra un mensaje en el chat con el formato apropiado.
    Diferencia visualmente entre mensajes del usuario y del asistente.
    """
    if es_usuario:
        with st.chat_message("user", avatar="👤"):
            st.write(mensaje["content"])
    else:
        with st.chat_message("assistant", avatar="🛒"):
            st.write(mensaje["content"])

def main():
    """
    Función principal que construye y maneja toda la interfaz de usuario.
    Organiza el layout, maneja las interacciones y coordina el flujo del chat.
    """
    init_state()
    
    st.title("🛒 Supermarket.AI, Rita te ayuda con tu cesta de la compra")
    st.markdown("---")
    
    with st.sidebar:
        st.header("🏪 Centro de Ayuda")
        
        st.subheader("👤 Información Personal")
        nombre_usuario = st.text_input("Tu nombre (opcional):", value=st.session_state.usuario_nombre)
        if nombre_usuario != st.session_state.usuario_nombre:
            st.session_state.usuario_nombre = nombre_usuario
        
        st.markdown("---")
        
        st.subheader("📊 Estadísticas del Chat")
        num_mensajes = len([m for m in st.session_state.mensajes if m["rol"] == "usuario"])
        st.metric("Mensajes enviados", num_mensajes)
        
        if st.session_state.mensajes:
            tiempo_conversacion = datetime.now() - st.session_state.mensajes[0]["timestamp"]
            minutos = int(tiempo_conversacion.total_seconds() / 60)
            st.metric("Tiempo de conversación", f"{minutos} min")
        
        st.markdown("---")
        
        st.subheader("💡 Ejemplos de Consultas")
        ejemplos = [
            "¿Cuánto cuesta la leche?",
            "¿Hay pollo disponible?",
            "Necesito frutas frescas",
            "¿Qué verduras tenéis?",
            "Precio del queso manchego"
        ]
        
        for ejemplo in ejemplos:
            if st.button(ejemplo, key=f"ejemplo_{ejemplo}"):
                st.session_state.mensajes.append({
                    "rol": "usuario",
                    "contenido": ejemplo,
                    "timestamp": datetime.now()
                })
                respuesta = generate_bot_response(ejemplo)
                st.session_state.mensajes.append({
                    "rol": "asistente",
                    "contenido": respuesta,
                    "timestamp": datetime.now()
                })
                st.rerun()  # Actualizar la interfaz
        
        st.markdown("---")
        
        # Botón para limpiar chat
        if st.button("🗑️ Limpiar Chat", type="secondary"):
            st.session_state.mensajes = []
            # Agregar mensaje de bienvenida nuevamente
            st.session_state.mensajes.append({
                "rol": "asistente",
                "contenido": "¡Hola! Soy tu asistente virtual del supermercado. Puedo ayudarte con información sobre productos, precios, disponibilidad y recomendaciones. ¿En qué puedo ayudarte hoy?",
                "timestamp": datetime.now()
            })
            st.rerun()
    
    # Área principal del chat
    st.subheader("💬 Conversación")
    
    # Contenedor para los mensajes del chat
    chat_container = st.container()
    
    with chat_container:
        # Mostrar todos los mensajes existentes
        for mensaje in st.session_state.mensajes:
            mostrar_mensaje(mensaje, es_usuario=(mensaje["rol"] == "usuario"))
    
    # Input del usuario en la parte inferior
    st.markdown("---")
    
    # Crear el formulario para el input del usuario
    with st.form(key="formulario_chat", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            mensaje_usuario = st.text_input(
                "Escribe tu consulta aquí...",
                placeholder="Ej: ¿Cuánto cuesta la leche? o ¿Hay manzanas disponibles?",
                key="input_usuario"
            )
        
        with col2:
            enviar = st.form_submit_button("Enviar 📤", type="primary")
    
    # Procesar el mensaje del usuario cuando se envía
    if enviar and mensaje_usuario.strip():
        # Agregar saludo personalizado si es el primer mensaje del usuario
        if st.session_state.usuario_nombre and len([m for m in st.session_state.mensajes if m["rol"] == "usuario"]) == 0:
            mensaje_con_nombre = f"Hola, soy {st.session_state.usuario_nombre}. {mensaje_usuario}"
        else:
            mensaje_con_nombre = mensaje_usuario
        
        # Agregar mensaje del usuario al historial
        st.session_state.mensajes.append({
            "rol": "usuario",
            "contenido": mensaje_con_nombre,
            "timestamp": datetime.now()
        })
        
        # Simular tiempo de procesamiento (opcional, para realismo)
        with st.spinner("El asistente está pensando..."):
            time.sleep(1)  # Simular tiempo de procesamiento
            
            # Generar y agregar respuesta del bot
            respuesta_bot = generate_bot_response(mensaje_con_nombre)
            st.session_state.mensajes.append({
                "rol": "asistente",
                "contenido": respuesta_bot,
                "timestamp": datetime.now()
            })
        
        # Actualizar la interfaz para mostrar los nuevos mensajes
        st.rerun()
  
    # Información adicional en la parte inferior
    st.markdown("---")
    
    # Footer con información útil
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("🕐 **Horario de atención**\nLun-Dom: 8:00 - 22:00")
    
    with col2:
        st.info("📞 **Contacto**\nTeléfono: 900 123 456\nEmail: info@supermercado.com")
    
    with col3:
        st.info("🏪 **Servicios**\n• Consulta de productos\n• Información de precios\n• Disponibilidad en tiempo real")


def run_app():
    """
    Ejecuta la aplicación Streamlit.
    Esta función es el punto de entrada para iniciar la aplicación.
    """
    main()


if __name__ == "__main__":
    run_app()
else:
    st.warning("Este módulo no debe ejecutarse directamente. Usa `streamlit run main_app.py` para iniciar la aplicación.")