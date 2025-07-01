# Guía de Desarrollo para Supermarket.AI Assistant 🤖🛒

Esta guía está orientada a desarrolladores que deseen entender, personalizar y extender **Supermarket.AI Assistant**. Aquí encontrarás información sobre la arquitectura, configuración, personalización y ejemplos de uso para sacarle el máximo partido al chatbot.

## Índice

1. [Introducción](#introducción)
2. [Requisitos previos](#requisitos-previos)
3. [Estructura del proyecto](#estructura-del-proyecto)
4. [Configuración inicial](#configuración-inicial)
5. [Personalización del chatbot](#personalización-del-chatbot)
6. [Extensión de funcionalidades](#extensión-de-funcionalidades)
7. [Ejemplos de uso y pruebas](#ejemplos-de-uso-y-pruebas)
8. [Buenas prácticas](#buenas-prácticas)
9. [Recursos adicionales](#recursos-adicionales)

---

## Introducción

Supermarket.AI Assistant es un chatbot modular y extensible, pensado para ayudar a los usuarios a encontrar productos, comparar precios y recibir recomendaciones en supermercados. Está construido en Python, utiliza [Streamlit](https://streamlit.io/) para la interfaz y la API de OpenAI para la IA conversacional.

---

## Requisitos previos

- **Python 3.8+**
- Acceso a una clave de API de OpenAI
- Conocimientos básicos de Python y manejo de entornos virtuales

---

## Estructura del proyecto

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

## Configuración inicial

1. **Clona el repositorio:**
   ```sh
   git clone https://github.com/ADRIDEV2024/SuperMarket.AI.git
   cd Chatbot
   ```

2. **Instala las dependencias:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Configura las variables de entorno:**
   - Renombra `.env.example` a `.env`.
   - Añade tu clave de OpenAI y otros parámetros necesarios.

4. **Configura la aplicación:**
   - Edita [`config/app_config.yaml`](../config/config/app_config.yaml) para ajustar parámetros como idioma, tema, bases de datos, modelo de IA, etc.
   - Ejemplo de parámetros personalizables:
     ```yaml
     gui:
       theme: dark
       language: es
       enable_notifications: true
     openai:
       model: gpt-4
       temperature: 0.7
     ```

5. **Inicia la aplicación:**
   ```sh
   streamlit run src/gui/main_app.py
   ```

---
