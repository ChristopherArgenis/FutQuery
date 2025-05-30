import pandas as pd

players = pd.read_csv("df_players.csv")

new_columns_requerid = ["short_name", "long_name", "overall", "potential", "value_eur", "wage_eur", "age", "height_cm", "weight_kg",
                    "club_name", "club_position", "club_jersey_number", "nationality_name", "preferred_foot", "pace", "shooting", "passing", "dribbling",
                    "defending", "physic", "skill_dribbling", "skill_curve", "skill_ball_control", "movement_agility", "movement_reactions", "power_shot_power",
                    "power_jumping", "player_face_url", "club_logo_url"]

# Tablas
Jugador = ["long_name", "short_name", "age", "height_cm", "weight_kg", "player_face_url", "club_jersey_number", "preferred_foot"]
posicion = ["club_position"]
Pais = ["nationality_name"]
club = ["club_name", "club_logo_url"]
Finanzas = ["value_eur", "wage_eur"]
metricas = ["overall", "potential", "pace", "shooting", "passing", "dribbling", "defending", "physic"]
habilidades = ["skill_dribbling", "skill_curve", "skill_ball_control", "movement_agility", "movement_reactions", "power_shot_power", "power_jumping"]

# Tablas - DataFrame/Series
Jugador = players[["long_name", "short_name", "age", "height_cm", "weight_kg", "player_face_url", "club_jersey_number", "preferred_foot"]]
posicion = players["club_position"]
Pais = players["nationality_name"]
club = players[["club_name", "club_logo_url"]]
Finanzas = players[["value_eur", "wage_eur"]]
metricas = players[["overall", "potential", "pace", "shooting", "passing", "dribbling", "defending", "physic"]]
habilidades = players[["skill_dribbling", "skill_curve", "skill_ball_control", "movement_agility", "movement_reactions", "power_shot_power", "power_jumping"]]

print(players.isnull().sum())