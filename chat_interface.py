import streamlit as st
from datetime import datetime
from typing import Dict, Optional, Any

DEFAULT_USER_CONFIG = {
    "username": "Usuario",
    "avatar_user": "👤",
    "avatar_bot": "🛒",
    "welcome_message": "😊 Hola! Soy Supermarket.AI, pero puedes llamarme Rita.Puedo ayudarte con productos, precios y disponibilidad.\n\n¡Pregunta lo que necesites!",
    "theme_color": "#4CAF50",
}

DEFAULT_DEV_CONFIG = {
    "max_display_messages": 50,
    "input_placeholder": "Escribe tu consulta...",
    "enable_examples": True,
    "example_queries": [
        "¿Cuánto cuesta la leche?",
        "¿Hay pollo disponible?",
        "Necesito frutas frescas",
        "¿Qué verduras tenéis?",
    ],
}


class ChatInterface:
    def __init__(self, user_config: Optional[Dict[str, Any]] = None, dev_config: Optional[Dict[str, Any]] = None):
        print("Inicializando ChatInterface")
        self.user_config = {**DEFAULT_USER_CONFIG, **(user_config or {})}
        self.dev_config = {**DEFAULT_DEV_CONFIG, **(dev_config or {})}
    
    def apply_theme(self):
        print(f"Aplicando tema: {self.user_config['theme_mode']} con color {self.user_config['theme_color']}")
        if self.user_config["theme_mode"] == "dark":
            background = "#0E1117"
            text_color = "#FAFAFA"
        else:
            background = "#FFFFFF"
            text_color = "#000000"
        
        st.markdown(f"""
            <style>
                .main {{
                    background-color: {background};
                    color: {text_color};
                }}
                .stButton>button {{
                    background-color: {self.user_config['theme_color']};
                    color: white;
                    border-radius: 8px;
                    border: none;
                }}
                .stButton>button:hover {{
                    background-color: #333333;
                }}
                .stTextInput>div>div>input {{
                    border-radius: 8px;
                    border: 1px solid {self.user_config['theme_color']};
                }}
                .stChatMessage {{
                    border-radius: 12px;
                    padding: 8px 16px;
                }}
            </style>
        """, unsafe_allow_html=True)

    def init_session_state(self):
        print("Inicializando session state")
        if "messages" not in st.session_state:
            st.session_state.messages = []
            st.session_state.messages.append({
                "role": "assistant",
                "content": self.user_config["welcome_message"],
                "timestamp": datetime.now()
            })
            print("Session state inicializado con mensaje de bienvenida")

    def render_sidebar(self):
        print("Renderizando sidebar")
        with st.sidebar:
            st.header("🏪 Opciones del Chat")
            username = st.text_input("Tu nombre:", value=self.user_config.get("username", ""))
            if username != self.user_config["username"]:
                print(f"Actualizando nombre de usuario a {username}")
                self.user_config["username"] = username
        
            st.markdown("---")
            st.subheader("📊 Estadísticas")
            num_user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
            st.metric("Mensajes enviados", num_user_msgs)

            if st.session_state.messages:
                duration = datetime.now() - st.session_state.messages[0]["timestamp"]
                mins = int(duration.total_seconds() / 60)
                st.metric("Duración", f"{mins} min")

            st.markdown("---")

            if st.button("🗑️ Limpiar Chat"):
                print("Botón limpiar chat presionado")
                self.clear_chat()
        
    def render_chat_window(self):
        print("Renderizando ventana de chat")
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.messages[-self.dev_config["max_display_messages"]:]:
                print(f"Mostrando mensaje: {msg}")
                self.display_message(msg, is_user=(msg["role"] == "user"))

    def render_user_input(self) -> Optional[str]:
        print("Renderizando input del usuario")
        st.markdown("---")
        with st.form(key="chat_form", clear_on_submit=True):
            cols = st.columns([5, 1])
            user_input = cols[0].text_input("", placeholder=self.dev_config["input_placeholder"])
            send = cols[1].form_submit_button("Enviar 📤")
            if send and user_input.strip():
                print(f"Entrada del usuario: {user_input.strip()}")
                return user_input.strip()
        return None
   
    def display_message(self, message: Dict[str, Any], is_user: bool = True):
        avatar = self.user_config["avatar_user"] if is_user else self.user_config["avatar_bot"]
        role = "user" if is_user else "assistant"
        print(f"Mostrando mensaje de {'usuario' if is_user else 'asistente'}: {message}")
        with st.chat_message(role, avatar=avatar):
            st.markdown(message["content"])

    def add_message(self, content: str, role: str):
        print(f"Añadiendo mensaje: {content} con rol {role}")
        st.session_state.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now()
        })

    def clear_chat(self):
        print("Limpiando chat")
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant",
            "content": self.user_config["welcome_message"],
            "timestamp": datetime.now()
        })
        print("Chat limpio e inicializado con mensaje de bienvenida")