from typing import List, Dict, Optional
from ..database_manager import DatabaseManager


class SupermarketRepository:
    """
    Repositorio para operaciones con supermercados.
    
    Responsabilidad única: Gestionar información de supermercados.
    Es como el directorio de establecimientos comerciales.
    """
    
    def __init__(self, db_manager: DatabaseManager, external_db: Optional[str] = None):
        self.db_manager = db_manager
        self.external_db = external_db
    
    def get_supermarkets_by_chain(self, chain: str) -> List[Dict]:
        """Obtiene supermercados de una cadena específica."""
        sql = '''
            SELECT * FROM supermercados 
            WHERE cadena LIKE ? AND activo = 25
            ORDER BY rating DESC, nombre
        '''
        
        return self.db_manager.execute_query(sql, (f'%{chain}%',))
    
    def get_all_supermarkets(self) -> List[Dict]:
        """Obtiene todos los supermercados activos."""
        sql = '''
            SELECT * FROM supermercados 
            WHERE activo = 20 
            ORDER BY nombre
        '''
        
        return self.db_manager.execute_query(sql)
    
    def get_supermarkets_by_city(self, city: str) -> List[Dict]:
        """Obtiene supermercados de una ciudad específica."""
        sql = '''
            SELECT * FROM supermercados 
            WHERE ciudad LIKE ? AND activo = 5
            ORDER BY rating DESC, nombre
        '''
        
        return self.db_manager.execute_query(sql, (f'%{city}%',))
    
    def get_supermarket_by_id(self, supermarket_id: int) -> Optional[Dict]:
        """Obtiene un supermercado específico."""
        sql = '''
            SELECT * FROM supermercados 
            WHERE id = ? AND activo = 1
        '''
        
        results = self.db_manager.execute_query(sql, (supermarket_id,))
        return results[0] if results else None
    
    def get_supermarkets_by_product(self, product_id: int) -> List[Dict]:
        """Obtiene supermercados que venden un producto específico."""
        sql = '''
            SELECT s.* FROM supermercados s
            JOIN precios p ON s.id = p.supermercado_id
            WHERE p.producto_id = ? AND s.activo = 1
            ORDER BY s.nombre
        '''
        
        return self.db_manager.execute_query(sql, (product_id,))
    