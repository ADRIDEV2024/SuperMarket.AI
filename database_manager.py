import sqlite3
import logging
from contextlib import contextmanager
from typing import Dict, List


class DatabaseManager:
       
    def __init__(self, db_path: str = "data/products_database.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        
    @contextmanager
    def get_connection(self):
        """Context manager para conexiones seguras."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    @contextmanager
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Ejecuta una consulta SELECT y devuelve resultados."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def execute_update(self, query: str, params: tuple = ()) -> bool:
        """Ejecuta INSERT, UPDATE o DELETE."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return True
        except Exception as e:
            self.logger.error(f"Error en execute_update: {e}")
            return False
    
    def execute_batch(self, query: str, params_list: List[tuple]) -> bool:
        """Ejecuta múltiples operaciones en lote."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.executemany(query, params_list)
                conn.commit()
                return True
        except Exception as e:
            self.logger.error(f"Error en execute_batch: {e}")
            return False
    
    def execute_script(self, script: str) -> bool:
        """Ejecuta un script SQL completo."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.executescript(script)
                conn.commit()
                return True
        except Exception as e:
            self.logger.error(f"Error ejecutando script: {e}")
            return False
        
    