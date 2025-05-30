import pandas as pd
from sqlalchemy.orm import sessionmaker
from crear_db import *

engine = create_engine('sqlite:///fifa2015.db')
Session = sessionmaker(bind=engine)
session = Session()

df = pd.read_csv("df_players.csv").dropna(subset=["club_name", "club_position", "nationality_name", "preferred_foot"])

# Diccionarios para evitar duplicados
club_map, pais_map, pos_map, fin_map = {}, {}, {}, {}

for _, row in df.iterrows():
    # Club
    club_key = row["club_name"]
    if club_key not in club_map:
        club = Club(nombre=row["club_name"], logo_url=row["club_logo_url"])
        session.add(club)
        session.flush()
        club_map[club_key] = club.id
    id_club = club_map[club_key]

    # Pais
    pais_key = row["nationality_name"]
    if pais_key not in pais_map:
        pais = Pais(nombre=pais_key)
        session.add(pais)
        session.flush()
        pais_map[pais_key] = pais.id
    id_pais = pais_map[pais_key]

    # Posición
    pos_key = row["club_position"]
    if pos_key not in pos_map:
        pos = Posicion(posicion=pos_key)
        session.add(pos)
        session.flush()
        pos_map[pos_key] = pos.id
    id_pos = pos_map[pos_key]

    # Finanzas
    fin_key = (row["value_eur"], row["wage_eur"])
    if fin_key not in fin_map:
        fin = Finanzas(valuacion=row["value_eur"], salario_anual=row["wage_eur"])
        session.add(fin)
        session.flush()
        fin_map[fin_key] = fin.id
    id_fin = fin_map[fin_key]

    # Jugador
    jugador = Jugador(
        nombre_completo=row["long_name"], alias=row["short_name"], edad=row["age"],
        altura=row["height_cm"], peso=row["weight_kg"], foto_url=row["player_face_url"],
        pie_preferente=row["preferred_foot"], no_jersey=row["club_jersey_number"]
    )
    session.add(jugador)
    session.flush()

    # j_info
    jinfo = J_Info(
        id_posicion=id_pos, id_club=id_club, id_pais=id_pais, id_finanzas=id_fin, id_jugador=jugador.id
    )
    session.add(jinfo)

    # Metricas
    metricas = Metricas(
        general=row["overall"], potencial=row["potential"], rapidez=row["pace"],
        tiro=row["shooting"], pase=row["passing"], regate=row["dribbling"],
        defensa=row["defending"], fisico=row["physic"]
    )
    session.add(metricas)
    session.flush()

    # Habilidades
    habilidades = Habilidades(
        regate=row["skill_dribbling"], efecto=row["skill_curve"], control_balon=row["skill_ball_control"],
        agilidad=row["movement_agility"], reaccion=row["movement_reactions"],
        poder_tiro=row["power_shot_power"], salto=row["power_jumping"]
    )
    session.add(habilidades)
    session.flush()

    # j_indicador
    jind = J_Indicador(id_jugador=jugador.id, id_metricas=metricas.id, id_habilidades=habilidades.id)
    session.add(jind)

session.commit()
session.close()