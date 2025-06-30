import logging
from .database_manager import DatabaseManager
from .database_schema import DatabaseSchema


class DatabaseInitializer:

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.logger = logging.getLogger(__name__)
    
    def initialize_database(self) -> bool:

        try:

            for table_name, table_sql in DatabaseSchema.TABLES.items():
                if not self.db_manager.execute_update(table_sql):
                    self.logger.error(f"Error creando tabla {table_name}")
                    return False
            
            for index_sql in DatabaseSchema.INDEXES:
                if not self.db_manager.execute_update(index_sql):
                    self.logger.warning(f"Error creando índice: {index_sql}")
            
            self.logger.info("Base de datos inicializada correctamente")
            return True
            
        except Exception as e:
            self.logger.error(f"Error inicializando base de datos: {e}")
            return False
