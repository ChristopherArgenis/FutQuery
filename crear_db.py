import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Tablas
class Posicion(Base):
    __tablename__ = 'posicion'
    id = Column(Integer, primary_key=True)
    posicion = Column(String)

class Club(Base):
    __tablename__ = 'club'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    logo_url = Column(Text)

class Pais(Base):
    __tablename__ = 'pais'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)

class Finanzas(Base):
    __tablename__ = 'finanzas'
    id = Column(Integer, primary_key=True)
    valuacion = Column(Integer)
    salario_anual = Column(Integer)

class Metricas(Base):
    __tablename__ = 'metricas'
    id = Column(Integer, primary_key=True)
    general = Column(Integer)
    potencial = Column(Integer)
    rapidez = Column(Integer)
    tiro = Column(Integer)
    pase = Column(Integer)
    regate = Column(Integer)
    defensa = Column(Integer)
    fisico = Column(Integer)

class Habilidades(Base):
    __tablename__ = 'habilidades'
    id = Column(Integer, primary_key=True)
    regate = Column(Integer)
    efecto = Column(Integer)
    control_balon = Column(Integer)
    agilidad = Column(Integer)
    reaccion = Column(Integer)
    poder_tiro = Column(Integer)
    salto = Column(Integer)

class Jugador(Base):
    __tablename__ = 'jugador'
    id = Column(Integer, primary_key=True)
    nombre_completo = Column(Text)
    alias = Column(String)
    edad = Column(Integer)
    altura = Column(Integer)
    peso = Column(Integer)
    foto_url = Column(Text)
    pie_preferente = Column(String)
    no_jersey = Column(Integer)

class J_Info(Base):
    __tablename__ = 'j_info'
    id = Column(Integer, primary_key=True)
    id_posicion = Column(Integer, ForeignKey('posicion.id'))
    id_club = Column(Integer, ForeignKey('club.id'))
    id_pais = Column(Integer, ForeignKey('pais.id'))
    id_finanzas = Column(Integer, ForeignKey('finanzas.id'))
    id_jugador = Column(Integer, ForeignKey('jugador.id'))

class J_Indicador(Base):
    __tablename__ = 'j_indicador'
    id = Column(Integer, primary_key=True)
    id_jugador = Column(Integer, ForeignKey('jugador.id'))
    id_metricas = Column(Integer, ForeignKey('metricas.id'))
    id_habilidades = Column(Integer, ForeignKey('habilidades.id'))

# Crear base de datos SQLite
engine = create_engine('sqlite:///fifa2015.db')
Base.metadata.create_all(engine)