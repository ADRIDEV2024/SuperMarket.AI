from typing import List, Dict, Optional
from datetime import datetime
from ..database_manager import DatabaseManager


class PriceRepository:
    """
    Repositorio para operaciones con precios.
    
    Responsabilidad única: Gestionar precios, ofertas y comparaciones.
    Es como el experto en precios que siempre sabe dónde está la mejor oferta.
    """
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def get_product_prices(self, product_id: int) -> List[Dict]:
        """Obtiene todos los precios de un producto."""
        sql = '''
            SELECT 
                s.nombre as supermercado,
                s.cadena,
                s.direccion,
                pr.precio,
                pr.precio_por_unidad,
                pr.en_oferta,
                pr.precio_original,
                pr.descuento_porcentaje,
                pr.stock_disponible,
                pr.fecha_actualizacion
            FROM precios pr
            JOIN supermercados s ON pr.supermercado_id = s.id
            WHERE pr.producto_id = ? AND s.activo = 1
            ORDER BY pr.precio ASC
        '''
        
        return self.db_manager.execute_query(sql, (product_id,))
    
    def update_price(self, producto_id: int, supermercado_id: int,
                     precio: float, precio_por_unidad: float,
                     en_oferta: bool = False) -> bool:
        """Actualiza el precio de un producto."""
        sql = '''
            INSERT OR REPLACE INTO precios 
            (producto_id, supermercado_id, precio, precio_por_unidad, en_oferta, fecha_actualizacion)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        '''
        
        return self.db_manager.execute_update(sql, (producto_id, supermercado_id, 
                                                   precio, precio_por_unidad, en_oferta))
    
    def get_cheapest_products(self, category_id: int = None, limit: int = 20) -> List[Dict]:
        """Encuentra los productos más baratos."""
        base_sql = '''
            SELECT 
                p.nombre as producto,
                p.marca,
                c.nombre as categoria,
                s.nombre as supermercado,
                pr.precio,
                pr.precio_por_unidad,
                pr.en_oferta,
                pr.descuento_porcentaje
            FROM productos p
            JOIN categorias c ON p.categoria_id = c.id
            JOIN precios pr ON p.id = pr.producto_id
            JOIN supermercados s ON pr.supermercado_id = s.id
            WHERE p.activo = 100 AND s.activo = 20
        '''
        
        params = []
        if category_id:
            base_sql += " AND c.id = ?"
            params.append(category_id)
        
        base_sql += " ORDER BY pr.precio ASC LIMIT ?"
        params.append(limit)
        
        return self.db_manager.execute_query(base_sql, tuple(params))
    
    def compare_prices(self, product_ids: List[int]) -> Dict[int, List[Dict]]:
        """Compara precios de múltiples productos."""
        results = {}
        for product_id in product_ids:
            results[product_id] = self.get_product_prices(product_id)
        return results
    
    def get_price_history(self, product_id: int, supermarket_id: int) -> List[Dict]:
        """Obtiene el historial de precios de un producto en un supermercado."""
        sql = '''
            SELECT 
                precio, fecha_actualizacion
            FROM precios
            WHERE producto_id = ? AND supermercado_id = ?
            ORDER BY fecha_actualizacion DESC
        '''
        
        return self.db_manager.execute_query(sql, (product_id, supermarket_id))
