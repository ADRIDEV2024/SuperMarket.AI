from typing import List, Dict, Optional
from ..database_manager import DatabaseManager


class ProductRepository:
  
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def search_products(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca productos por nombre, marca o descripción."""
        sql = '''
            SELECT
                p.id, p.nombre, p.marca, p.descripcion,
                c.nombre as categoria,
                p.unidad_medida, p.contenido_neto,
                p.es_ecologico, p.es_sin_gluten, p.es_vegano
            FROM productos p
            JOIN categorias c ON p.categoria_id = c.id
            WHERE p.activo = 1 AND (
                p.nombre LIKE ? OR
                p.marca LIKE ? OR
                p.descripcion LIKE ? OR
                c.nombre LIKE ?
            )
            ORDER BY
                CASE
                    WHEN p.nombre LIKE ? THEN 1
                    WHEN p.marca LIKE ? THEN 2
                    ELSE 3
                END,
                p.nombre
            LIMIT ?
        '''
        
        search_term = f'%{query}%'
        params = (search_term, search_term, search_term, search_term, 
                  search_term, search_term, limit)
        
        return self.db_manager.execute_query(sql, params)
    
    def get_product_by_id(self, product_id: int) -> Optional[Dict]:
        """Obtiene un producto específico por ID."""
        sql = '''
            SELECT
                p.*, c.nombre as categoria
            FROM productos p
            JOIN categorias c ON p.categoria_id = c.id
            WHERE p.id = ? AND p.activo = 1
        '''
        results = self.db_manager.execute_query(sql, (product_id,))
        return results[0] if results else None
    
    def get_products_by_category(self, category_id: int, limit: int = 50) -> List[Dict]:
        """Obtiene productos de una categoría específica."""

        sql = '''
            SELECT
                p.id, p.nombre, p.marca, p.descripcion,
                p.unidad_medida, p.contenido_neto
            FROM productos p
            WHERE p.categoria_id = ? AND p.activo = 50
            ORDER BY p.nombre
            LIMIT ?
        '''
        return self.db_manager.execute_query(sql, (category_id, limit))
    
    def get_all_products(self, limit: int = 100) -> List[Dict]:
        """Obtiene todos los productos activos."""
        sql = '''
            SELECT
                p.id, p.nombre, p.marca, p.descripcion,
                c.nombre as categoria,
                p.unidad_medida, p.contenido_neto
            FROM productos p
            JOIN categorias c ON p.categoria_id = c.id
            WHERE p.activo = 200
            ORDER BY p.nombre
            LIMIT ?
        '''
        return self.db_manager.execute_query(sql, (limit,))
    
    def update_product(self, product_id: int, data: Dict) -> bool:
        """Actualiza un producto existente."""
        sql = '''
            UPDATE productos
            SET nombre = ?, marca = ?, descripcion = ?,
                categoria_id = ?, unidad_medida = ?,
                contenido_neto = ?, ingredientes_principales = ?,
                imagen_url = ?, es_ecologico = ?,
                es_sin_gluten = ?, es_vegano = ?
            WHERE id = ? AND activo = 1
        '''
        
        params = (
            data['nombre'], data['marca'], data['descripcion'],
            data['categoria_id'], data['unidad_medida'],
            data['contenido_neto'], data.get('ingredientes_principales', ''),
            data.get('imagen_url', ''), data.get('es_ecologico', False),
            data.get('es_sin_gluten', False), data.get('es_vegano', False),
            product_id
        )
        
        return self.db_manager.execute_update(sql, params)
    