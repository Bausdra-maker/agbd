from sqlalchemy import Column, Integer, String, Float, Boolean, create_engine, and_, or_
from sqlalchemy.orm import DeclarativeBase, Session

class Base(DeclarativeBase):
    pass

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=True)  # Se cambió a True
    categoria = Column(String, nullable=True)  # Se cambió a True para el ejercicio 12
    precio = Column(Float, nullable=True)  # Se cambió a True para el ejercicio 12
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

    print("\n   4) Productos con precio > 10000 (Mayor a menor)   ")
    caros = session.query(Producto).filter(Producto.precio > 10000).order_by(Producto.precio.desc()).all()
    for p in caros:
        print(p.nombre, p.precio)

    print("\n 5) Productos con stock <= 12 y activos  ")
    bajo_stock_activos = session.query(Producto).filter(Producto.stock <= 12, Producto.activo == True).all()
    for p in bajo_stock_activos:
        print(p.nombre, p.stock, p.activo)

    print("\n  6) Precio entre 5000 y 20000 (con and_)  ")
    en_rango = session.query(Producto).filter(
           and_(Producto.precio >= 5000, Producto.precio <= 20000)
    ).all()
    for p in en_rango:
        print(p.nombre, p.precio)

    print("\n 7) Producto mas caro de toda la tabla   ")
    mas_caro = session.query(Producto).order_by(Producto.precio.desc()).first()
    if mas_caro:
        print(mas_caro.nombre, mas_caro.precio)

    print("\n  8) Productos inactivos   ")
    inactivos = session.query(Producto).filter(Producto.activo == False).all()
    for p in inactivos:
        print(p.nombre, p.activo)

    print("\n  9) Categoria 'audio' o 'componentes' (con or_)  ")
    audio_o_componentes = session.query(Producto).filter(
        or_(Producto.categoria == "audio", Producto.categoria == "componentes")
    ).all()
    for p in audio_o_componentes:
        print(p.nombre, p.categoria)

    print("\n  10) Productos cuyo nombre contiene la letra 'a'  ")
    con_letra_a = session.query(Producto).filter(Producto.nombre.contains("a")).all()
    for p in con_letra_a:
        print(p.nombre)
    print(f"Total de productos encontrados: {len(con_letra_a)}")

    print("\n  11) Productos cuyo nombre empieza con 'M'  ")
    empieza_m = session.query(Producto).filter(Producto.nombre.startswith("M")).all()
    for p in empieza_m:
        print(p.nombre)

    print("\n  12) Agregar producto sin categoria ni precio y filtrar por NULL  ")
    nuevo_producto = Producto(nombre="Producto Borrador", categoria=None, precio=None, stock=5)
    session.add(nuevo_producto)
    session.commit()

    categoria_null = session.query(Producto).filter(Producto.categoria == None).all()
    for p in categoria_null:
        print(f"Producto con categoria NULL: {p.nombre}")

    precio_null = session.query(Producto).filter(Producto.precio == None).all()
    for p in precio_null:
        print(f"Producto con precio NULL: {p.nombre}")


    # ¿Que pasa si filtran por precio == None? ¿Aparece el mismo producto?
    # Sí, aparece exactamente el mismo producto ("Producto Borrador"),
    # ya que a ese registro en particular le asignamos el valor None (SQL NULL) 
    # tanto en la columna 'categoria' como en la columna 'precio'.

    print("\n  13) Buscar Hub USB-C por id, actualizar stock y activo  ")
    # Buscamos por id (en los datos iniciales, el Hub USB-C tiene ID 9)
    hub = session.get(Producto, 9)
    if hub:
        hub.stock = 20
        hub.activo = True
        session.commit()

    # Verificación
    hub_verificado = session.get(Producto, 9)
    print(f"Hub actualizado -> ID: {hub_verificado.id}, Nombre: {hub_verificado.nombre}, Stock: {hub_verificado.stock}, Activo: {hub_verificado.activo}")

    print("\n  14) Aumento del 10% a la categoria 'perifericos'  ")
    perifericos = session.query(Producto).filter(Producto.categoria == "perifericos").all()
    for p in perifericos:
        p.precio = p.precio * 1.10
    session.commit()

    teclado = session.query(Producto).filter(Producto.nombre == "Teclado mecanico").first()
    print(f"Precio del Teclado mecanico tras el aumento: ${teclado.precio:.2f}")


    # ¿Cuanto cuesta el Teclado mecanico despues del aumento?
    # Respuesta: Cuesta $9350.0 (Precio original: $8500.0 + 10% de aumento).

    print("\n  15) Eliminar Cable HDMI de la base de datos  ")
    # Cable HDMI tiene id=10 en el principio
    hdmi = session.get(Producto, 10)
    if hdmi:
        session.delete(hdmi)
        session.commit()

    total_productos = session.query(Producto).count()
    print(f"Total de productos en la base de datos: {total_productos}")
    # Nota: Quedan 10 productos (10 iniciales + 1 del Ej 12 - 1 eliminado = 10 productos).

    print("\n  16) Eliminar productos con precio < 2000 o inactivos  ")
    # Nota: Se debe validar 'precio != None' para evitar errores de comparación
    a_eliminar = session.query(Producto).filter(
        or_(
            and_(Producto.precio < 2000, Producto.precio != None),
            Producto.activo == False
        )
    ).all()

    cantidad_borrados = len(a_eliminar)
    for p in a_eliminar:
        session.delete(p)
    session.commit()

    print(f"Cantidad de productos borrados: {cantidad_borrados}")


    # ¿Cuantos borraron?
    # Respuesta: Se borraron 0 productos en este punto. El motivo es que:
    # 1. El 'Cable HDMI' (que costaba 1800 < 2000) ya fue eliminado en el Ejercicio 15.
    # 2. El 'Hub USB-C' (que estaba inactivo) fue activado previamente en el Ejercicio 13.
    # Por lo tanto, no quedan registros en la base de datos que cumplan estas condiciones.

    print("\n  --- SI TERMINARON (EXTRA) ---  ")

    print("\n  a) Productos cuyo nombre contiene la palabra 'USB'  ")
    con_usb = session.query(Producto).filter(Producto.nombre.contains("USB")).all()
    for p in con_usb:
        print(p.nombre)

    print("\n  b) Productos ordenados por categoria y precio de menor a mayor  ")
    ordenados = session.query(Producto).order_by(Producto.categoria.asc(), Producto.precio.asc()).all()
    for p in ordenados:
        print(f"Categoria: {p.categoria} | Nombre: {p.nombre} | Precio: ${p.precio}")

    print("\n  c) Conteo de productos activos e inactivos (queries separadas)  ")
    activos_count = session.query(Producto).filter(Producto.activo == True).count()
    inactivos_count = session.query(Producto).filter(Producto.activo == False).count()
    print(f"Productos activos: {activos_count}")
    print(f"Productos inactivos: {inactivos_count}")