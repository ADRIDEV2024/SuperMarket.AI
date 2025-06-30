from typing import List, Dict, Any, Optional


class ConversationHandler:

    def __init__(self):
        self.history: List[Dict[str, Any]] = []

    def add_message(self, sender: str, message: str) -> None:
        """
        Agrega un mensaje al historial de la conversación.

        :param sender: 'user' o 'bot'
        :param message: Texto del mensaje
        """
        self.history.append({
            "sender": sender,
            "message": message
        })

    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Obtiene el historial de la conversación.

        :param limit: Número máximo de mensajes a devolver (opcional)
        :return: Lista de mensajes
        """
        if limit is not None:
            return self.history[-limit:]
        return self.history

    def clear_history(self) -> None:
        """
        Limpia el historial de la conversación.
        """
        self.history.clear()

    def last_user_message(self) -> Optional[str]:
        """
        Obtiene el último mensaje enviado por el usuario.

        :return: Texto del último mensaje del usuario o None si no existe
        """
        for entry in reversed(self.history):
            if entry["sender"] == "user":
                return entry["message"]
        return None

    def last_bot_message(self) -> Optional[str]:
        """
        Obtiene el último mensaje enviado por el bot.

        :return: Texto del último mensaje del bot o None si no existe
        """
        for entry in reversed(self.history):
            if entry["sender"] == "bot":
                return