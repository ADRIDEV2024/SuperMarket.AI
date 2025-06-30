import os
from utils.config import OPENAI_API_KEY, BOT_NAME, DEFAULT_SYSTEM_PROMPT
from api.openai_client import OpenAIClient
from data_proc.data_loader import DataLoader
from data_proc.database_manager import DatabaseManager
from data_proc.db_initializer import DatabaseInitializer
from .chatbot_engine import ChatbotEngine
from gui.main_app import run_app

def main():
    # Load configuration
    api_key = os.getenv("OPENAI_API_KEY", OPENAI_API_KEY)
    bot_name = BOT_NAME
    system_prompt = DEFAULT_SYSTEM_PROMPT

    # Initialize OpenAI client
    openai_client = OpenAIClient(api_key=api_key, system_prompt=system_prompt)

    # Load product data and initialize database
    product_data = DataLoader()
    db_manager = DatabaseManager()
    db_manager = DatabaseInitializer(db_manager)
    if not db_manager.initialize_database():
        print("❌ Error initializing database")
        return 
    # Initialize chatbot engine
    chatbot = ChatbotEngine(
        openai_client=openai_client,
        product_data=product_data,
        bot_name=bot_name,
        system_prompt=system_prompt
    )

    # Launch GUI application
    run_app()


if __name__ == "__main__":  
    main()
