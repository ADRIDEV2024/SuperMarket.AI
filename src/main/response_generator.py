
class ResponseGenerator:
    def __init__(self, product_data=None, bot_name="Chatbot"):
        self.product_data = product_data
        self.bot_name = bot_name

    def generate_greeting_response(self):
        return f"¡Hola! Soy {self.bot_name}, ¿en qué puedo ayudarte hoy con tu compra?"

    def generate_farewell_response(self):
        return "¡Gracias por contar conmigo! Si necesitas algo más, aquí estaré."

    def generate_product_search_response(self, product_list):
        if not product_list:
            return "Parece que no he encontrado productos que coincidan con tu búsqueda :(."
        response = "Estos son los productos que encontré:\n"
        for product in product_list:
            response += f"- {product['nombre']} (${product['precio']})\n"
        return response

    def generate_price_response(self, product):
        if not product:
            return "No he encontrado el producto que buscas."
        return f"El precio de {product['nombre']} es ${product['precio']}."

    def generate_fallback_response(self):
        return "Lo siento, no entendí tu solicitud. ¿Puedes reformularla?"

    def generate_response(self, intent, entities=None, context=None):
        if intent == "greeting":
            return self.generate_greeting_response()
        elif intent == "farewell":
            return self.generate_farewell_response()
        elif intent == "product_search":
            products = entities.get("products", []) if entities else []
            return self.generate_product_search_response(products)
        elif intent == "price_query":
            product = entities.get("product") if entities else None
            return self.generate_price_response(product)
        else:
            return self.generate_fallback_response()