from .database_manager import DatabaseManager
from .db_initializer import DatabaseInitializer
from .repositories.product_repository import ProductRepository
from .repositories.price_repository import PriceRepository
from .repositories.market_repository import SupermarketRepository

__all__ = [
    'DatabaseManager',
    'DatabaseInitializer',
    'ProductRepository',
    'PriceRepository',
    'SupermarketRepository'
]

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)    
    db_manager = DatabaseManager()    # Inicializar componentes
    db_initializer = DatabaseInitializer(db_manager)

    if db_initializer.initialize_database():
        print("✅ Base de datos inicializada correctamente")
        
        # Crear repositorios especializados
        product_repo = ProductRepository(db_manager)
        price_repo = PriceRepository(db_manager)
        market_repo = SupermarketRepository(db_manager)
        
        print("✅ Repositorios creados y listos para usar")
        print("\nSistema refactorizado exitosamente:")
        print("- DatabaseManager: Manejo de conexiones")
        print("- ProductRepository: Operaciones con productos")
        print("- PriceRepository: Gestión de precios")
        print("- SupermarketRepository: Información de supermercados")
        print("- DatabaseInitializer: Inicialización de esquemas")
    else:
        print("❌ Error inicializando base de datos")