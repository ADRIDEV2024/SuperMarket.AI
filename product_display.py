import streamlit as st


def display_product_list(product_list):
   
    if not product_list:
        st.info("No se encontraron productos para mostrar.")
        return

    for product in product_list:
        with st.container():
            cols = st.columns([1, 3])
            # Imagen del producto (opcional)
            if product.get("image"):
                cols[0].image(product["image"], width=80)
            else:
                cols[0].empty()
            # Detalles del producto
            cols[1].markdown(f"**{product['name'].title()}**")
            cols[1].markdown(f"Price: ${product['price']}")
            if product.get("description"):
                cols[1].markdown(f"*{product['description']}*")
            # Botón para añadir al carrito (ejemplo)
            if st.button(f"Añadir {product['name']} al carrito", key=product['name']):
                st.success(f"{product['name'].title()} añadido al carrito.")


def display_product_detail(product):
    """
    Muestra los detalles ampliados de un producto.
    """
    st.header(product['name'].title())
    if product.get("image"):
        st.image(product["image"], width=200)
    st.markdown(f"**Precio:** ${product['price']}")
    if product.get("description"):
        st.markdown(f"**Descripción:** {product['description']}")
    # Puedes añadir más detalles aquí (ingredientes, valor nutricional, etc.)

# Ejemplo de uso:
# if __name__ == "__main__":
#     productos = [
#         {"nombre": "manzana", "precio": 1.2, "imagen": "https://via.placeholder.com/80", "descripcion": "Manzana roja fresca"},
#         {"nombre": "pan", "precio": 0.8, "descripcion":