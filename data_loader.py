import csv
import json
import sqlite3
from typing import List, Dict, Any, Optional


class DataLoader:
    """
    Clase para cargar datos de productos, precios y promociones desde diferentes fuentes.
    """

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path

    def load_from_csv(self, file_path: str) -> List[Dict[str, Any]]:
        
        data = []
        try:
            with open(file_path, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    data.append(row)
        except Exception as e:
            print(f"Error al cargar CSV: {e}")
        return data

    def load_from_json(self, file_path: str) -> List[Dict[str, Any]]:
      
        try:
            with open(file_path, mode='r', encoding='utf-8') as jsonfile:
                data = json.load(jsonfile)
            if isinstance(data, dict):
                data = [data]
            return data
        except Exception as e:
            print(f"Error al cargar JSON: {e}")
            return []

    def load_from_db(self, query: str) -> List[Dict[str, Any]]:
      
        if not self.db_path:
            print("No se ha especificado la ruta de la base de datos.")
            return []
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            conn.close()
            return results
        except Exception as e:
            print(f"Error al cargar desde la base de datos: {e}")
            return []


if __name__ == "__main__":
    loader = DataLoader(db_path="products_database.db")
    products_csv = loader.load_from_csv("productos.csv")
    products_json = loader.load_from_json("productos.json")
    products_db = loader.load_from_db("SELECT * FROM productos")
    print("Productos desde CSV:", products_csv)
    print("Productos desde JSON:", products_json)
    print("Productos desde DB:", products_db)

    