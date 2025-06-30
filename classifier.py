import re


class IntentClassifier:
    """
    Clasificador de intenciones basado en reglas simples.
    Detecta la intención del usuario y extrae entidades relevantes.
    """

    def __init__(self, product_data=None):
        self.product_data = product_data  # Lista o dict de productos para búsqueda de entidades
        self.intent_entities = {
            "greeting": {"entities": []},
            "farewell": {"entities": []},
            "price_query": {"entities": ["product"]},
            "product_search": {"entities": ["products"]},
            "information_query": {"entities": []},
            "help_request": {"entities": []},
            # Intención por defecto
            "fallback": {"entities": []}
        }

    def _detect_intent(self, message):
        """
        Método auxiliar para detectar la intención del mensaje.
        Aquí se pueden agregar más intenciones según sea necesario.
        """
        return "fallback"  # Por defecto, si no se reconoce la intención

    def classify(self, user_message):
        """
        Analiza el mensaje del usuario y devuelve la intención y las entidades extraídas.
        """
        message = user_message.lower().strip()
        intent = "fallback" 
        entities = {}

        # 1. Saludo
        if re.search(r"\b(hola|buenos días|buenas tardes|buenas noches|hey|saludos)\b", message):
            intent = "greeting"
            return intent, entities

        # 2. Despedida
        if re.search(r"\b(adiós|hasta luego|nos vemos|chao|bye|salir|gracias)\b", message):
            intent = "farewell"
            return intent, entities

        # 3. Consulta de precio
        if re.search(r"(cuánto vale|precio de|cuánto cuesta|coste de)", message):
            intent = "price_query"
            product = self._extract_product(message)
            if product:
                entities["product"] = product
            return intent, entities

        # 4. Búsqueda de producto
        if re.search(r"(tienes|hay|busco|encuentro|ofreces|venden|productos de)", message):
            intent = "product_search"
            products = self._extract_products(message)
            if products:
                entities["products"] = products
            return intent, entities
        
        # 5. Consulta de información general
        if re.search(r"(qué es|cuéntame|dime|información sobre)", message):
            intent = "information_query"
            return intent, entities
        
        if re.search(r"(ayuda|necesito ayuda|asistencia)", message):
            intent = "help_request"
            return intent, entities
        
        if re.search(r"(no entiendo|no sé|no comprendo)", message):
            intent = "fallback"
            return intent, entities
        
        return intent, entities

    def _extract_product(self, message):
        """
        Busca el nombre de un producto en el mensaje usando los datos de productos.
        """
        if not self.product_data:
            return None
        for product in self.product_data:
            if product["nombre"].lower() in message:
                return product
        return None

    def _extract_products(self, message):
        """
        Busca todos los productos mencionados en el mensaje.
        """
        found = []

        if not self.product_data:
            return found
        for product in self.product_data:
            if product["nombre"].lower() in message:
                found.append(product)
        return found

    def add_product_data(self, product_data):
       
        self.product_data = product_data