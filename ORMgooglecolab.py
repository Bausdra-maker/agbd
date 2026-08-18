from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import DeclarativeBase, Session

class Base(DeclarativeBase):
    pass

class Producto(Base):
    __tablename__ = "productos"

    id        = Column(Integer, primary_key=True)
    nombre    = Column(String)
    precio    = Column(Float)
    stock     = Column(Integer)
    categoria = Column(String)

engine = create_engine("sqlite:///:memory:", echo=True)
Base.metadata.create_all(engine)

with Session(engine) as session:
    p1 = Producto(nombre="Teclado", precio=450, stock=15, categoria="Periféricos")
    p2 = Producto(nombre="Mouse", precio=250, stock=30, categoria="Periféricos")
    p3 = Producto(nombre="Monitor", precio=1200, stock=8, categoria="Monitores")
    p4 = Producto(nombre="Pad Mouse", precio=150, stock=50, categoria="Accesorios")
    p5 = Producto(nombre="Auriculares", precio=600, stock=10, categoria="Audio")

    session.add_all([p1, p2, p3, p4, p5])
    session.commit()

with Session(engine) as session:
    baratos = session.query(Producto).filter(Producto.precio < 500).all()

    for p in baratos:
        print(p.nombre, p.precio)