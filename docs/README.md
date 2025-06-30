# Supermarket.AI Assistant 🛒

¡Bienvenido a **Supermarket.AI Assistant**!  
Un chatbot inteligente bajo la potencia tecnológica de Openai con ChatGPT 4 y o2 diseñado para ayudarte a encontrar productos, comparar precios y obtener recomendaciones en supermercados (por el momento solo aquellos que se ubican en España) de manera rápida y sencillam, gracias a Rita,tu asistente que te guiará y te dará todo el feedback que necesites para cada consulta que tengas,¡Créeme que será de gran ayuda para tus próximas cestas de la compra!

---

##  🤔 ¿Qué puede hacer Rita por mí?

Supermarket.AI Assistant es un asistente conversacional basado en modelos de IA generativa GPT, especializado en productos de supermercado. Permite a los usuarios:

- Buscar productos por nombre, marca o categoría de comercios locales y grandes cadenas de supermercados.
- Consultar precios y promociones en tiempo real.
- Comparar precios entre diferentes supermercados de España.
- Obtener recomendaciones personalizadas.
- Recibir información sobre disponibilidad y ofertas especiales.

---

## 🧩 Características principales

- **Interfaz amigable:** Basada en [Streamlit](https://streamlit.io/) para una experiencia visual moderna y sencilla.
- **IA conversacional:** Utiliza modelos de OpenAI para comprender y responder preguntas en lenguaje natural.
- **Gestión de base de datos:** Soporte para múltiples fuentes de datos (MariaDB, CSV, JSON).
- **Panel de configuración:** Personaliza idioma, nivel de detalle, supermercado preferido y más.
- **Extensible:** Arquitectura modular para añadir nuevas funcionalidades fácilmente.

---

## 📦 Estructura del proyecto

```
Chatbot/
│
├── config/           # Configuración de la app y modelos
├── data/             # Bases de datos y datos de productos
├── docs/             # Documentación y guías
├── src/              # Código fuente principal
│   ├── api/          # Integración con APIs externas (OpenAI, etc.)
│   ├── data_proc/    # Procesamiento y gestión de datos
│   ├── gui/          # Interfaz gráfica (Streamlit)
│   ├── main/         # Lógica principal del chatbot
│   └── utils/        # Utilidades y helpers
├── tests/            # Pruebas unitarias y de integración
├── requirements.txt  # Dependencias del proyecto
├── setup.py          # Instalador del paquete
└── run.py            # Script de ejecución principal
```

---

## ⚡ Instalación rápida

1. **Clona el repositorio:**
   ```sh
   git clone https://github.com/ADRIDEV2024/SuperMarket.AI.git
   cd Chatbot
   ```

2. **Instala las dependencias:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Configura tus variables de entorno:**  
   Renombra `.env.example` a `.env` y añade tu clave de OpenAI y otros parámetros necesarios.

4. **Inicia la aplicación:**
   ```sh
   streamlit run src/gui/main_app.py
   ```

---

## 🛠️ Tecnologías utilizadas

- **Python 3.8+**
- [Streamlit](https://streamlit.io/)
- [OpenAI API](https://openai.com/)
- [MariaDB](https://www.mariadb.org/)
- [PyYAML](https://pyyaml.org/)
- [NLTK](https://www.nltk.org/)

---

## 📚 Documentación

- [Guía de usuario](user_guide.md)
- [Guía de desarrollo](developer_guide.md)

---

## 🤖 Ejemplo de uso

> **Usuario:** ¿Cuánto cuesta la leche de avena?
>
> **Chatbot:** El precio de la leche de avena es 1,75 € en Mercadona y 1,50 € en Lidl. ¿Te gustaría comparar más supermercados?

---

## 💡 Contribuciones

¡Las contribuciones son bienvenidas!  
Por favor, revisa la [guía de desarrollo](developer_guide.md) y CONTRIBUTION.md antes de enviar un pull request o issue, no te cuesta nada realizar un fork a este trabajo y exponer tus ideas al creador😎.

---

## 📄 Licencia

Este proyecto está bajo la licencia GPL 3.0.

---
