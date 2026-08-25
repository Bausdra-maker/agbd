from sqlalchemy import Column, Integer, String, Float, Boolean, create_engine, and_, or_
from sqlalchemy.orm import DeclarativeBase, Session

class Base(DeclarativeBase):
    pass

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    activo = Column(Boolean, default=True)

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)

productos_iniciales = [
    Producto(nombre="Teclado mecanico", categoria="perifericos", precio=8500.0, stock=15),
    Producto(nombre="Mouse inalambrico", categoria="perifericos", precio=4200.0, stock=30),
    Producto(nombre="Monitor 24 pulgadas", categoria="monitores", precio=62000.0, stock=8),
    Producto(nombre="Auriculares bluetooth", categoria="audio", precio=12300.0, stock=20),
    Producto(nombre="Webcam Full HD", categoria="perifericos", precio=9800.0, stock=12),
    Producto(nombre="SSD 1TB", categoria="almacenamiento", precio=18500.0, stock=25),
    Producto(nombre="RAM 16GB", categoria="componentes", precio=15600.0, stock=18),
    Producto(nombre="Mousepad XL", categoria="perifericos", precio=2100.0, stock=40),
    Producto(nombre="Hub USB-C", categoria="accesorios", precio=5400.0, stock=6, activo=False),
    Producto(nombre="Cable HDMI", categoria="accesorios", precio=1800.0, stock=50),
]

with Session(engine) as session:
    session.add_all(productos_iniciales)
    session.commit()

with Session(engine) as session:

    print("  3) Productos de la categoria 'perifericos'   ")
    perifericos = session.query(Producto).filter(Producto.categoria == "perifericos").all()
    
    for p in perifericos:
        print(p.nombre, p.precio)

    print("   4) Productos con precio > 10000 (Mayor a menor)   ")
    caros = session.query(Producto).filter(Producto.precio > 10000).order_by(Producto.precio.desc()).all()
    
    for p in caros:
        print(p.nombre, p.precio)

    print(" 5) Productos con stock <= 12 y activos  ")
    bajo_stock_activos = session.query(Producto).filter(Producto.stock <= 12, Producto.activo == True).all()
    
    for p in bajo_stock_activos:
        print(p.nombre, p.stock, p.activo)

    print("  6) Precio entre 5000 y 20000 (con and_)  ")
    en_rango = session.query(Producto).filter(
           and_(Producto.precio >= 5000, Producto.precio <= 20000)
    ).all()
   
    for p in en_rango:
        print(p.nombre, p.precio)

    print(" 7) Producto mas caro de toda la tabla   ")
    mas_caro = session.query(Producto).order_by(Producto.precio.desc()).first()
    if mas_caro:
        print(mas_caro.nombre, mas_caro.precio)

    print("  8) Productos inactivos   ")
    inactivos = session.query(Producto).filter(Producto.activo == False).all()
    for p in inactivos:
        print(p.nombre, p.activo)

    print("  9) Categoria 'audio' o 'componentes' (con or_)  ")
    audio_o_componentes = session.query(Producto).filter(
        or_(Producto.categoria == "audio", Producto.categoria == "componentes")
    ).all()
    
    for p in audio_o_componentes:
        print(p.nombre, p.categoria)

    print("  10) Productos cuyo nombre contiene la letra 'a'  ")
    con_letra_a = session.query(Producto).filter(Producto.nombre.contains("a")).all()
    
    for p in con_letra_a:
        print(p.nombre)
        
    print(f"Total de productos encontrados: {len(con_letra_a)}")