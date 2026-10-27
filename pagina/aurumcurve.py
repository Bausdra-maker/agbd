from sqlalchemy import Column, Float, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Configuración de la conexión a MySQL
DATABASE_URL = "mysql+pymysql://aurum:ac123456@10.9.120.5:3306/Aurum-Curve"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# --- 1. MODELOS DE LA DISTRIBUIDORA E-COMMERCE ---


class Categoria(Base):
  __tablename__ = "categorias"

  id = Column(Integer, primary_key=True, autoincrement=True)
  nombre = Column(String(100), nullable=False)
  slug = Column(String(100), unique=True, nullable=False)


class Proveedor(Base):
  __tablename__ = "proveedores"

  id = Column(Integer, primary_key=True, autoincrement=True)
  nombre = Column(String(100), nullable=False)
  contacto = Column(String(50))
  telefono = Column(String(20))


class Producto(Base):
  __tablename__ = "productos"

  id = Column(Integer, primary_key=True, autoincrement=True)
  nombre = Column(String(100), nullable=False)
  categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
  talle = Column(String(10), nullable=False)
  color = Column(String(30), nullable=False)
  precio_mayorista = Column(Float, nullable=False)
  stock = Column(Integer, nullable=False)

  categoria = relationship("Categoria")


class Cliente(Base):
  __tablename__ = "clientes"

  id = Column(Integer, primary_key=True, autoincrement=True)
  razon_social = Column(String(150), nullable=False)
  cuil = Column(String(20), unique=True)
  email = Column(String(100))


class Pedido(Base):
  __tablename__ = "pedidos"

  id = Column(Integer, primary_key=True, autoincrement=True)
  cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
  fecha = Column(String(20), nullable=False)
  estado = Column(String(30), default="Pendiente")
  total = Column(Float, nullable=False)

  cliente = relationship("Cliente")


# Creación de tablas en phpMyAdmin
Base.metadata.create_all(bind=engine)


# --- 2. FUNCIONES DE BACKEND ---


def obtener_resumen_catalogo():
  db = SessionLocal()
  try:
    productos = db.query(Producto).all()
    return [
        {
            "id": p.id,
            "articulo": p.nombre,
            "categoria": p.categoria.nombre if p.categoria else "Sin categoría",
            "talle": p.talle,
            "color": p.color,
            "precio": p.precio_mayorista,
            "stock": p.stock,
        }
        for p in productos
    ]
  finally:
    db.close()


def obtener_lista_clientes():
  db = SessionLocal()
  try:
    clientes = db.query(Cliente).all()
    return [
        {
            "id": c.id,
            "razon_social": c.razon_social,
            "cuil": c.cuil,
            "email": c.email,
        }
        for c in clientes
    ]
  finally:
    db.close()


# --- 3. INSERCIÓN DE DATOS MASIVOS (10 CATEGORÍAS Y PRODUCTOS) ---

if __name__ == "__main__":
  db = SessionLocal()

  if db.query(Producto).count() == 0:
    print("Inicializando base de datos completa para la distribuidora...")

    # 1. Las 10 Categorías principales de e-commerce
    cat_destacados = Categoria(nombre="Destacados", slug="destacados")
    cat_hombre = Categoria(nombre="Hombre", slug="hombre")
    cat_mujer = Categoria(nombre="Mujer", slug="mujer")
    cat_nino = Categoria(nombre="Niño/a", slug="nino-a")
    cat_accesorios = Categoria(nombre="Accesorios", slug="accesorios")
    cat_deportes = Categoria(nombre="Deportes", slug="deportes")
    cat_calzado = Categoria(nombre="Calzado", slug="calzado")
    cat_abrigos = Categoria(nombre="Abrigos", slug="abrigos")
    cat_ropa_interior = Categoria(nombre="Ropa Interior", slug="ropa-interior")
    cat_pantalones = Categoria(
        nombre="Pantalones y Jeans", slug="pantalones-y-jeans"
    )

    db.add_all([
        cat_destacados,
        cat_hombre,
        cat_mujer,
        cat_nino,
        cat_accesorios,
        cat_deportes,
        cat_calzado,
        cat_abrigos,
        cat_ropa_interior,
        cat_pantalones,
    ])
    db.commit()

    # 2. Proveedores (4 proveedores distintos)
    prov1 = Proveedor(
        nombre="Textil Sur S.A.", contacto="Carlos Gomez", telefono="1144556677"
    )
    prov2 = Proveedor(
        nombre="Confecciones Moda SRL",
        contacto="Ana Ruiz",
        telefono="1122334455",
    )
    prov3 = Proveedor(
        nombre="Importadora Textil Global",
        contacto="Marcos Perez",
        telefono="1199887766",
    )
    prov4 = Proveedor(
        nombre="Indumentaria Deportiva Pro",
        contacto="Lucia Benitez",
        telefono="1155443322",
    )
    db.add_all([prov1, prov2, prov3, prov4])
    db.commit()

    # 3. Clientes (incluyendo tu registro personal)
    cli1 = Cliente(
        razon_social="Boutique Estilo Urbano",
        cuil="20-35678912-4",
        email="contacto@estilourbano.com",
    )
    cli2 = Cliente(
        razon_social="Indumentaria Casual Shop",
        cuil="27-28912345-9",
        email="ventas@casualshop.com",
    )
    cli3 = Cliente(
        razon_social="Tienda Multimarca Norte",
        cuil="20-32456789-1",
        email="compras@nortemultimarca.com",
    )
    cli4 = Cliente(
        razon_social="Local Outlet Palermo",
        cuil="27-38112233-8",
        email="outletpalermo@gmail.com",
    )
    cli_bautista = Cliente(
        razon_social="Bautista Daniel La Roca Velez Lopez",
        cuil="20-49091002-3",
        email="bautistadaniellarocavelezlopez@gmail.com",
    )
    db.add_all([cli1, cli2, cli3, cli4, cli_bautista])
    db.commit()

    # 4. Catálogo masivo con productos para las 10 categorías
    prods = [
        # --- DESTACADOS ---
        Producto(
            nombre="Campera Puffer Impermeable",
            categoria=cat_destacados,
            talle="M",
            color="Verde Militar",
            precio_mayorista=45000.00,
            stock=15,
        ),
        Producto(
            nombre="Buzo Oversize Edición Limitada",
            categoria=cat_destacados,
            talle="L",
            color="Negro",
            precio_mayorista=28000.00,
            stock=25,
        ),
        Producto(
            nombre="Remera Estampada Premium",
            categoria=cat_destacados,
            talle="S",
            color="Blanco",
            precio_mayorista=9500.00,
            stock=40,
        ),
        Producto(
            nombre="Jean Mom Fit Premium",
            categoria=cat_destacados,
            talle="38",
            color="Celeste",
            precio_mayorista=22000.00,
            stock=30,
        ),
        Producto(
            nombre="Blazer Sastrero Urbano",
            categoria=cat_destacados,
            talle="M",
            color="Beige",
            precio_mayorista=38000.00,
            stock=12,
        ),
        Producto(
            nombre="Gorra Trucker Exclusiva",
            categoria=cat_destacados,
            talle="Único",
            color="Negro",
            precio_mayorista=6000.00,
            stock=50,
        ),
        Producto(
            nombre="Zapatillas Urbanas Core",
            categoria=cat_destacados,
            talle="41",
            color="Blanco/Gris",
            precio_mayorista=42000.00,
            stock=18,
        ),
        # --- HOMBRE ---
        Producto(
            nombre="Remera Básica Algodón Peinado",
            categoria=cat_hombre,
            talle="L",
            color="Negro",
            precio_mayorista=7500.00,
            stock=80,
        ),
        Producto(
            nombre="Camisa Casual Slim Fit",
            categoria=cat_hombre,
            talle="M",
            color="Azul Francia",
            precio_mayorista=19000.00,
            stock=35,
        ),
        Producto(
            nombre="Buzo Hoodie con Canguro",
            categoria=cat_hombre,
            talle="XL",
            color="Gris Melange",
            precio_mayorista=24000.00,
            stock=30,
        ),
        Producto(
            nombre="Pantalón Jogger Rústico",
            categoria=cat_hombre,
            talle="M",
            color="Negro",
            precio_mayorista=16000.00,
            stock=45,
        ),
        Producto(
            nombre="Campera Denim clásica",
            categoria=cat_hombre,
            talle="L",
            color="Azul Oscuro",
            precio_mayorista=31000.00,
            stock=20,
        ),
        Producto(
            nombre="Bermuda Gabardina",
            categoria=cat_hombre,
            talle="40",
            color="Beige",
            precio_mayorista=14500.00,
            stock=25,
        ),
        Producto(
            nombre="Remera Manga Larga Básica",
            categoria=cat_hombre,
            talle="M",
            color="Gris Oscuro",
            precio_mayorista=8900.00,
            stock=40,
        ),
        # --- MUJER ---
        Producto(
            nombre="Vestido Midi Estampado",
            categoria=cat_mujer,
            talle="S",
            color="Floral Rojo",
            precio_mayorista=16500.00,
            stock=40,
        ),
        Producto(
            nombre="Top Deportivo Seamless",
            categoria=cat_mujer,
            talle="M",
            color="Rosa Pastel",
            precio_mayorista=7200.00,
            stock=50,
        ),
        Producto(
            nombre="Blusa Satinada Elegante",
            categoria=cat_mujer,
            talle="S",
            color="Blanco",
            precio_mayorista=14000.00,
            stock=30,
        ),
        Producto(
            nombre="Cardigan Tejido Fino",
            categoria=cat_mujer,
            talle="M",
            color="Lila",
            precio_mayorista=18500.00,
            stock=25,
        ),
        Producto(
            nombre="Short de Jeans Tiro Alto",
            categoria=cat_mujer,
            talle="36",
            color="Celeste Deslavado",
            precio_mayorista=12500.00,
            stock=35,
        ),
        Producto(
            nombre="Campera Bomber Satinada",
            categoria=cat_mujer,
            talle="S",
            color="Negro",
            precio_mayorista=29000.00,
            stock=20,
        ),
        Producto(
            nombre="Body de Algodón y Lycra",
            categoria=cat_mujer,
            talle="M",
            color="Nude",
            precio_mayorista=9800.00,
            stock=45,
        ),
        # --- NIÑO/A ---
        Producto(
            nombre="Remerita Infantil Dinosaurios",
            categoria=cat_nino,
            talle="6",
            color="Amarillo",
            precio_mayorista=5000.00,
            stock=70,
        ),
        Producto(
            nombre="Conjunto Moletón Kids",
            categoria=cat_nino,
            talle="8",
            color="Celeste",
            precio_mayorista=12000.00,
            stock=25,
        ),
        Producto(
            nombre="Vestidito Floral Niña",
            categoria=cat_nino,
            talle="4",
            color="Rosa",
            precio_mayorista=9500.00,
            stock=30,
        ),
        Producto(
            nombre="Buzo Canguro Infantil",
            categoria=cat_nino,
            talle="10",
            color="Rojo",
            precio_mayorista=11000.00,
            stock=20,
        ),
        Producto(
            nombre="Pantalón Jogging Kids",
            categoria=cat_nino,
            talle="6",
            color="Gris",
            precio_mayorista=7800.00,
            stock=35,
        ),
        Producto(
            nombre="Campera Impermeable Infantil",
            categoria=cat_nino,
            talle="8",
            color="Azul",
            precio_mayorista=19500.00,
            stock=15,
        ),
        # --- ACCESORIOS ---
        Producto(
            nombre="Gorra Curve Trucker",
            categoria=cat_accesorios,
            talle="Único",
            color="Negro/Blanco",
            precio_mayorista=4500.00,
            stock=90,
        ),
        Producto(
            nombre="Cinto de Cuero PU",
            categoria=cat_accesorios,
            talle="L",
            color="Marrón",
            precio_mayorista=6000.00,
            stock=40,
        ),
        Producto(
            nombre="Mochila Urbana Antirrobo",
            categoria=cat_accesorios,
            talle="Único",
            color="Gris",
            precio_mayorista=25000.00,
            stock=20,
        ),
        Producto(
            nombre="Bufanda tejida de invierno",
            categoria=cat_accesorios,
            talle="Único",
            color="Bordo",
            precio_mayorista=5500.00,
            stock=35,
        ),
        Producto(
            nombre="Lentes de Sol UV400",
            categoria=cat_accesorios,
            talle="Único",
            color="Negro",
            precio_mayorista=8000.00,
            stock=30,
        ),
        Producto(
            nombre="Riñonera Deportiva Impermeable",
            categoria=cat_accesorios,
            talle="Único",
            color="Azul",
            precio_mayorista=7000.00,
            stock=45,
        ),
        # --- DEPORTES ---
        Producto(
            nombre="Calzas Deportivas Lycra Pro",
            categoria=cat_deportes,
            talle="S",
            color="Negro",
            precio_mayorista=14000.00,
            stock=55,
        ),
        Producto(
            nombre="Remera Térmica Running",
            categoria=cat_deportes,
            talle="L",
            color="Azul Francia",
            precio_mayorista=11000.00,
            stock=35,
        ),
        Producto(
            nombre="Short de Entrenamiento Dry Fit",
            categoria=cat_deportes,
            talle="M",
            color="Gris",
            precio_mayorista=9200.00,
            stock=50,
        ),
        Producto(
            nombre="Campera Windbreaker Deportiva",
            categoria=cat_deportes,
            talle="L",
            color="Negro/Verde",
            precio_mayorista=27000.00,
            stock=18,
        ),
        Producto(
            nombre="Top Deportivo Alto Impacto",
            categoria=cat_deportes,
            talle="S",
            color="Blanco",
            precio_mayorista=10500.00,
            stock=30,
        ),
        Producto(
            nombre="Botella Deportiva Térmica",
            categoria=cat_deportes,
            talle="Único",
            color="Acero",
            precio_mayorista=8500.00,
            stock=40,
        ),
        # --- CALZADO ---
        Producto(
            nombre="Zapatillas Urbanas Classic",
            categoria=cat_calzado,
            talle="40",
            color="Blanco",
            precio_mayorista=35000.00,
            stock=25,
        ),
        Producto(
            nombre="Botinetas de Eco-Cuero",
            categoria=cat_calzado,
            talle="38",
            color="Negro",
            precio_mayorista=41000.00,
            stock=15,
        ),
        Producto(
            nombre="Zapatillas de Running Performance",
            categoria=cat_calzado,
            talle="42",
            color="Azul/Naranja",
            precio_mayorista=48000.00,
            stock=20,
        ),
        Producto(
            nombre="Sandalias de Verano Anátomicas",
            categoria=cat_calzado,
            talle="37",
            color="Camel",
            precio_mayorista=21000.00,
            stock=30,
        ),
        Producto(
            nombre="Borcegos de Cuero Sintético",
            categoria=cat_calzado,
            talle="39",
            color="Negro",
            precio_mayorista=46000.00,
            stock=12,
        ),
        Producto(
            nombre="Ojotas de Goma Livianas",
            categoria=cat_calzado,
            talle="41",
            color="Azul Marino",
            precio_mayorista=6500.00,
            stock=60,
        ),
        # --- ABRIGOS ---
        Producto(
            nombre="Trench Coat Clásico",
            categoria=cat_abrigos,
            talle="M",
            color="Beige",
            precio_mayorista=49000.00,
            stock=10,
        ),
        Producto(
            nombre="Saco de Paño Elegante",
            categoria=cat_abrigos,
            talle="L",
            color="Negro",
            precio_mayorista=52000.00,
            stock=8,
        ),
        Producto(
            nombre="Chaleco Acolchado Capitone",
            categoria=cat_abrigos,
            talle="M",
            color="Azul Oscuro",
            precio_mayorista=26000.00,
            stock=22,
        ),
        Producto(
            nombre="Poncho Tejido Rústico",
            categoria=cat_abrigos,
            talle="Único",
            color="Gris Melange",
            precio_mayorista=21000.00,
            stock=15,
        ),
        Producto(
            nombre="Campera de Cuerina Rockera",
            categoria=cat_abrigos,
            talle="S",
            color="Negro",
            precio_mayorista=39000.00,
            stock=14,
        ),
        Producto(
            nombre="Cardigan Largo de Lana",
            categoria=cat_abrigos,
            talle="L",
            color="Marrón Claro",
            precio_mayorista=24000.00,
            stock=18,
        ),
        # --- ROPA INTERIOR ---
        Producto(
            nombre="Pack x3 Boxers de Algodón",
            categoria=cat_ropa_interior,
            talle="L",
            color="Surtidos",
            precio_mayorista=11000.00,
            stock=50,
        ),
        Producto(
            nombre="Pack x3 Bombachas Vedettina",
            categoria=cat_ropa_interior,
            talle="M",
            color="Surtidos",
            precio_mayorista=7500.00,
            stock=60,
        ),
        Producto(
            nombre="Conjunto de Encaje y Microfibra",
            categoria=cat_ropa_interior,
            talle="85",
            color="Rojo",
            precio_mayorista=12500.00,
            stock=30,
        ),
        Producto(
            nombre="Medias Invisibles Pack x3",
            categoria=cat_ropa_interior,
            talle="Único",
            color="Blanco/Negro",
            precio_mayorista=3500.00,
            stock=100,
        ),
        Producto(
            nombre="Camisilla de Algodón Masculina",
            categoria=cat_ropa_interior,
            talle="M",
            color="Blanco",
            precio_mayorista=5000.00,
            stock=45,
        ),
        Producto(
            nombre="Bóxer Deportivo Ajustado",
            categoria=cat_ropa_interior,
            talle="L",
            color="Gris",
            precio_mayorista=4800.00,
            stock=55,
        ),
        # --- PANTALONES Y JEANS ---
        Producto(
            nombre="Jean Slim Fit Clásico",
            categoria=cat_pantalones,
            talle="42",
            color="Azul Oscuro",
            precio_mayorista=18000.00,
            stock=45,
        ),
        Producto(
            nombre="Pantalón Wide Leg Sastrero",
            categoria=cat_pantalones,
            talle="38",
            color="Negro",
            precio_mayorista=20500.00,
            stock=35,
        ),
        Producto(
            nombre="Pantalón Cargo Urbano",
            categoria=cat_pantalones,
            talle="40",
            color="Verde Oliva",
            precio_mayorista=23000.00,
            stock=28,
        ),
        Producto(
            nombre="Jean Flare Tiro Alto",
            categoria=cat_pantalones,
            talle="36",
            color="Azul Clásico",
            precio_mayorista=19500.00,
            stock=30,
        ),
        Producto(
            nombre="Pantalón Chino Gabardina",
            categoria=cat_pantalones,
            talle="42",
            color="Beige",
            precio_mayorista=17500.00,
            stock=40,
        ),
        Producto(
            nombre="Jogging de Algodón Frizado",
            categoria=cat_pantalones,
            talle="L",
            color="Gris Melange",
            precio_mayorista=15000.00,
            stock=50,
        ),
    ]

    db.add_all(prods)
    db.commit()

    # 5. Pedidos iniciales
    ped1 = Pedido(
        cliente_id=cli1.id,
        fecha="2026-06-01",
        estado="Despachado",
        total=52500.00,
    )
    ped2 = Pedido(
        cliente_id=cli_bautista.id,
        fecha="2026-06-06",
        estado="Pendiente",
        total=39000.00,
    )
    db.add_all([ped1, ped2])
    db.commit()
    print("¡Base de datos poblada masivamente con éxito!")

  db.close()

  # --- MOSTRAR RESULTADOS EN CONSOLA ---
  print("\n--- LISTA DE CLIENTES ---")
  for cli in obtener_lista_clientes():
    print(cli)

  catalogo = obtener_resumen_catalogo()
  print(f"\n--- TOTAL DE PRODUCTOS EN STOCK: {len(catalogo)} ---")
  print("¡Catálogo completo y listo para el e-commerce!")