import os
from dotenv import load_dotenv
import openai
import logging

# Cargar variables de entorno
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Inicializar cliente de OpenAI
openai.api_key = OPENAI_API_KEY


class ChatbotEngine:
    def __init__(self, openai_client, product_data=None, bot_name="Chatbot", system_prompt=None):
        self.openai_client = openai_client
        self.product_data = product_data
        self.bot_name = bot_name
        self.system_prompt = system_prompt or "Eres un chatbot comercial experto en alimentos y supermercados. Ayuda a los clientes a encontrar productos, precios y promociones."
        self.conversation_history = []

    def add_to_history(self, user_message, bot_response):
        """
        Agrega un intercambio de mensajes al historial de conversación.
        """
        self.conversation_history.append({"user": user_message, "bot": bot_response})

    def get_response_openai(self, user_message):
        """
        Envía el mensaje del usuario y el historial a la API de OpenAI y devuelve la respuesta.
        """
        try:
            messages = [{"role": "system", "content": self.system_prompt}]
            for msg in self.conversation_history:
                messages.append({"role": "user", "content": msg["user"]})
                messages.append({"role": "assistant", "content": msg["bot"]})
            messages.append({"role": "user", "content": user_message})

            response = self.openai_client.create_chat_completion(
                messages=messages,
                max_tokens=300,
                temperature=0.5,
            )
            bot_message = response["choices"][0]["message"]["content"]
            self.add_to_history(user_message, bot_message)
            return bot_message.strip()

        except Exception as e:
            logging.error(f"Error al obtener respuesta de OpenAI: {e}")
            return "Lo siento, hubo un problema al procesar tu solicitud."

    def reset_history(self):
        self.conversation_history = []

    def save_history(self, user, bot, conversation_history):
        conversation_history.append({"user": user, "bot": bot})


def main(user_message, conversation_history=[], bot_response=None):
    print("¡Bienvenido a tu chatbot ideal para realizar la cesta de la compra :) ! Escribe 'salir' para terminar.\n")
    while True:
        user_message = input("Tú: ")
        if user_message.lower() in ["salir", "exit", "quit"]:
            print("¡Gracias por usar el chatbot! Hasta pronto.")
            break
        bot_response = get_response_openai(user_message, conversation_history)
        print(f"Bot: {bot_response}\n")
        save_history(user_message, bot_response)


if __name__ == "__main__":

    main(user_message, conversation_history=[], bot_response=None)

