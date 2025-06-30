import unicodedata
import re


def clean_text(text):
    """Limpia y normaliza un texto para procesamiento."""
    text = text.lower().strip()
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    text = re.sub(r'[^\w\s]', '', text)  # Elimina signos de puntuación
    text = re.sub(r'\s+', ' ', text)     # Espacios múltiples a uno solo
    return text


def clean_product_name(name):
    """Normaliza el nombre de un producto."""
    if not name:
        return ""
    name = name.strip()
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return clean_text(name)


def clean_product_data(product_list):
    """Limpia una lista de productos (dicts)."""
    cleaned = []
    for product in product_list:
        product_clean = product.copy()
        product_clean['nombre'] = clean_product_name(product['nombre'])
        cleaned.append(product_clean)
    return cleaned


def clean_price(price):

    if isinstance(price, str):
        price = price.replace(',', '.').strip()
    try:
        return float(price)
    except ValueError:
        return 0.0  # Retorna 0.0 si no se puede convertir a float
    