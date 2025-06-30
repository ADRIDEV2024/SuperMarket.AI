class DatabaseSchema:

    TABLES = {
        'supermercados': '''
            CREATE TABLE IF NOT EXISTS supermercados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                chain TEXT,
                direccion TEXT,
                city TEXT,
                postal_code TEXT,
                phone TEXT,
                horario_apertura TEXT,
                horario_cierre TEXT,
                tiene_delivery BOOLEAN DEFAULT 0,
                activo BOOLEAN DEFAULT 1
            )
        ''',

        'categorias': '''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                categoria_padre_id INTEGER,
                description TEXT,
                image_url TEXT,
                orden_display INTEGER DEFAULT 0,
                FOREIGN KEY (categoria_padre_id) REFERENCES categorias (id)
            )
        ''',
        
        'productos': '''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                brand TEXT,
                price REAL NOT NULL,
                description TEXT,
                categoria_id INTEGER NOT NULL,
                codigo_barras TEXT UNIQUE,
                measure_unit TEXT,
                contenido_neto REAL,
                ingredientes_principales TEXT,
                image_url TEXT,
                es_ecologico BOOLEAN DEFAULT 0,
                es_sin_gluten BOOLEAN DEFAULT 0,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                activo BOOLEAN DEFAULT 1,
                FOREIGN KEY (categoria_id) REFERENCES categorias (id)
            )
        ''',
        
        'precios': '''
            CREATE TABLE IF NOT EXISTS precios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                market_id INTEGER NOT NULL,
                price REAL NOT NULL,
                price_per_unit REAL NOT NULL,
                en_oferta BOOLEAN DEFAULT 0,
                precio_original REAL,
                descuento_porcentaje REAL,
                stock_disponible INTEGER,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fuente_datos TEXT,
                FOREIGN KEY (producto_id) REFERENCES productos (id),
                FOREIGN KEY (supermercado_id) REFERENCES supermercados (id),
                UNIQUE(producto_id, supermercado_id)
            )
        ''',
        
        'ofertas_especiales': '''
            CREATE TABLE IF NOT EXISTS ofertas_especiales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                tipo_oferta TEXT,
                market_id INTEGER NOT NULL,
                fecha_fin DATE NOT NULL,
                condiciones TEXT,
                activa BOOLEAN DEFAULT 1,
                FOREIGN KEY (supermercado_id) REFERENCES supermercados (id)
            )
        ''',

        'historial_busquedas': '''
            CREATE TABLE IF NOT EXISTS historial_busquedas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                consulta_usuario TEXT NOT NULL,
                intent_detectado TEXT,
                productos_encontrados INTEGER DEFAULT 0,
                respuesta_satisfactoria BOOLEAN,
                tiempo_respuesta REAL,
                fecha_consulta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_usuario TEXT,
                session_id TEXT
            )
        '''
    }

    INDEXES = [
            "CREATE INDEX IF NOT EXISTS idx_productos_nombre ON productos(nombre)",
            "CREATE INDEX IF NOT EXISTS idx_productos_categoria ON productos(categoria_id)",
            "CREATE INDEX IF NOT EXISTS idx_productos_activo ON productos(activo)",
            "CREATE INDEX IF NOT EXISTS idx_precios_producto ON precios(producto_id)",
            "CREATE INDEX IF NOT EXISTS idx_precios_supermercado ON precios(supermercado_id)",
            "CREATE INDEX IF NOT EXISTS idx_precios_fecha ON precios(fecha_actualizacion)",
            "CREATE INDEX IF NOT EXISTS idx_precios_precio ON precios(precio)",
            "CREATE INDEX IF NOT EXISTS idx_ofertas_fechas ON ofertas_especiales(fecha_inicio, fecha_fin)",
            "CREATE INDEX IF NOT EXISTS idx_productos_busqueda ON productos(nombre, marca)",
            "CREATE INDEX IF NOT EXISTS idx_supermercados_activo ON supermercados(activo)"
        ]
