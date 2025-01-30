import pandas as pd
import random as rd
import numpy as np
import re
from collections import defaultdict
from pathlib import Path

YEARS = ['1st year', '2nd year', '3rd year', '4th year', 'Masters', 'PhD']
YEAR_TO_INDEX = {year: index for index, year in enumerate(YEARS)}

def get_path_csv(filename):
    if not filename.endswith('.csv'):
        filename = f"{filename}.csv"
    
    current_dir = Path(__file__).parent.parent
    csv_dir = current_dir / 'DataSets'
    file_path = csv_dir / filename

    if not file_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {filename}, en {file_path}")
    
    return file_path

def generateRandomTeams(datos):
    num = rd.randint(1, 20)
    teams = []

    Used = set()
    for i in range(num):
        team = []
        num_eq = rd.randint(1, 4)
        for j in range(num_eq):
            pos = rd.randint(0, len(datos) - 1)
            if pos not in Used:
                team.append(datos.iloc[pos])
                Used.add(pos)
        teams.append(team)

    return teams

def evaluar_Edad(team, datos) -> float:
    if len(team) == 1:
        return 1.0

    score = 0
    num_comparaciones = 1

    edad_min = datos['Age'].min()
    edad_max = datos['Age'].max()

    # Iterar sobre pares únicos de integrantes
    for i in range(len(team)):
        for j in range(i + 1, len(team)):
            integrante1 = team[i]
            integrante2 = team[j]

            edad1 = datos.loc[datos['ID'] == integrante1['ID'], 'Age'].values[0]
            edad2 = datos.loc[datos['ID'] == integrante2['ID'], 'Age'].values[0]

            diferencia_edad = abs(edad1 - edad2)
            
            score += 1 - (np.log(1 + diferencia_edad) / np.log(edad_max - edad_min + 1))

            num_comparaciones += 1

    # Devolver el puntaje normalizado (si quieres promediar por el número de comparaciones)
    return score/num_comparaciones

def evaluar_AñoEscolar(team, datos) -> float:
        if len(team) == 1:
            return 1.0

        score = 0
        num_comparaciones = 0

        min_year = 0
        max_year = len(YEARS) - 1

        for i in range(len(team)):
            for j in range(i + 1, len(team)):
                integrante1 = team[i]
                integrante2 = team[j]

                year1 = datos.loc[datos['ID'] == integrante1['ID'], 'Year of Study'].values[0]
                year2 = datos.loc[datos['ID'] == integrante2['ID'], 'Year of Study'].values[0]

                diferencia_year = abs(YEAR_TO_INDEX[year1] - YEAR_TO_INDEX[year2])

                score += 1.0 - (diferencia_year / max_year)

                num_comparaciones += 1

        # Devolver el puntaje normalizado
        return score / num_comparaciones if num_comparaciones > 0 else 1.0

def evaluar_Intereses(team, datos) -> float:
    if len(team) == 1:
        return 1.0

    score = 0
    total_intereses = 0

    for i in range(len(team)):
        integrante1 = team[i]
        for j in range(i + 1, len(team)):
            integrante2 = team[j]

            intereses1 = datos.loc[datos['ID'] == integrante1['ID'], 'Interests'].values[0]
            intereses2 = datos.loc[datos['ID'] == integrante2['ID'], 'Interests'].values[0]

            intereses1 = set(intereses1.split(", "))
            intereses2 = set(intereses2.split(", "))

            if not len(intereses1.union(intereses2)) == 0:
                score += len(intereses1.intersection(intereses2))/len(intereses1.union(intereses2))
            
            total_intereses += 1
            

    # Devolver el puntaje normalizado
    return score / total_intereses if total_intereses > 0 else 1.0


INVALID_PREFERENCIA = set(["Don't know", "Don't care"])

def evaluar_Preferencia(team, datos) -> float:
    score = 0

    if len(team) == 1:
        return 1.0
    
    normalizar = 0

    for i in range(len(team)):
        integrante1 = team[i]
        for j in range(i + 1, len(team)):
            integrante2 = team[j]

            preferencia1 = datos.loc[datos['ID'] == integrante1['ID'], 'Preferred Role'].values[0]
            preferencia2 = datos.loc[datos['ID'] == integrante2['ID'], 'Preferred Role'].values[0]

            if preferencia1 not in INVALID_PREFERENCIA and preferencia2 not in INVALID_PREFERENCIA:
                if preferencia1 != preferencia2:
                    score += 1
                normalizar += 1

    return score / normalizar if normalizar > 0 else 1.0

def evaluar_Experiencia(team, datos) -> float:
    score = 0

    if len(team) == 1:
        return 1.0
    
    normalizar = 0

    for i in range(len(team)):
        integrante1 = team[i]
        for j in range(i + 1, len(team)):
            integrante2 = team[j]

            experiencia1 = datos.loc[datos['ID'] == integrante1['ID'], 'Experience Level'].values[0]
            experiencia2 = datos.loc[datos['ID'] == integrante2['ID'], 'Experience Level'].values[0]

            if experiencia1 != experiencia2:
                score += 1
            
            normalizar += 1

    return score/normalizar

def evaluar_Hackathons(team, datos) -> float:
    score = 0

    max_hackathons = datos['Hackathons Done'].max()
    
    for integrante in team:
        hackathons = datos.loc[datos['ID'] == integrante['ID'], 'Hackathons Done'].values[0]
        score += hackathons

    return score/ (max_hackathons * len(team))

def evaluar_Idioma(team, datos) -> float:
    if len(team) == 1:
        return 1.0  # Si hay solo un integrante, el puntaje es 1.0

    idiomas_por_integrante = []
    
    for integrante in team:
        idiomas = datos.loc[datos['ID'] == integrante['ID'], 'Preferred Languages']
        if idiomas.notna().any():  # Verificar si hay datos
            idiomas = idiomas.values[0].split(", ")
            idiomas_por_integrante.append(set(idiomas))  # Extraer correctamente el conjunto

    if not idiomas_por_integrante:  # Si la lista está vacía, devolver 0
        return 0.0

    # Intersección de idiomas entre todos los integrantes
    idioma_comun = set.intersection(*idiomas_por_integrante) if idiomas_por_integrante else set()

    # Determinar el puntaje basado en cuántos integrantes comparten idioma
    num_con_idioma_comun = sum(1 for idiomas in idiomas_por_integrante if idioma_comun & idiomas)

    if num_con_idioma_comun == len(team):  
        return 1.0
    elif num_con_idioma_comun == len(team) - 1:
        return 0.75
    elif num_con_idioma_comun == len(team) - 2:
        return 0.5
    elif num_con_idioma_comun == len(team) - 3:
        return 0.25
    else:
        return 0.0

def evaluar_Friend(team, datos) -> float:
    score = 0

    if len(team) == 1:
        return 1.0

    tmb = len(team)
    for i in range(len(team)):
        integrante1 = team[i]
        amigos1 = set(datos.loc[datos['ID'] == integrante1['ID'], 'Friend Registration'].values[0].split(", "))
        for j in range(i + 1, len(team)):
            integrante2 = team[j]
            if integrante2['ID'] in amigos1:
                score += 1          
    
    return score / tmb if tmb > 0 else 1.0

def evaluar_PreferedSize(team, datos) -> float:
    if len(team) == 1:
        return 1.0

    media = 0
    for integrante in team:
        media += datos.loc[datos['ID'] == integrante['ID'], 'Preferred Team Size'].values[0]

    media = media / len(team)
    diff = abs(media - len(team))
    if diff == 0:
        return 1.0
    
    return 1 - min(1, diff / media)

def evaluar_Availability(team, datos) -> float:
    if len(team) == 1:
        return 1.0

    score = 0
    total_comparaciones = 0

    for i in range(len(team)):
        integrante1 = team[i]
        for j in range(i + 1, len(team)):
            integrante2 = team[j]

            disponibilidad1 = datos.loc[datos['ID'] == integrante1['ID'], 'Availability'].values[0]
            disponibilidad2 = datos.loc[datos['ID'] == integrante2['ID'], 'Availability'].values[0]

            if disponibilidad1 == disponibilidad2:
                score += 1

            total_comparaciones += 1

    return score / total_comparaciones if total_comparaciones > 0 else 1.0

def evaluar_Skills(team, datos) -> float:
    team_skills = []
    for integrante in team:
        data = str(datos.loc[datos['ID'] == integrante['ID'], 'Programming Skills'].values[0])
        pares = re.findall(r'([^:,]+): (\d+)', data)
        skills = [(habilidad.strip(), int(nivel)) for habilidad, nivel in pares]
        team_skills.extend(skills)
    
    if not team_skills:
        return 0
    
    skill_counts = {}
    skill_levels = {}
    for skill, level in team_skills:
        skill_counts[skill] = skill_counts.get(skill, 0) + 1
        skill_levels[skill] = max(skill_levels.get(skill, 0), level)
    
    total_skills = len(team_skills)
    unique_skills = len(skill_counts)
    diversity_score = unique_skills / total_skills 
    
    level_scores = []
    for skill, level in skill_levels.items():
        level_score = level / 10 
        level_scores.append(level_score)
    
    avg_level_score = sum(level_scores) / len(level_scores) if level_scores else 0
    
    final_score = (diversity_score * 0.6) + (avg_level_score * 0.4)
    
    return round(final_score, 2)

try:
    datos = pd.read_csv(get_path_csv("Data"))
    temas = generateRandomTeams(datos)

    for i in range(len(temas)):
        for j in range(len(temas[i])):
            print(f"Edad de {temas[i][j]['Name']}: {temas[i][j]['Age']}")
            print(f"Año escolar: {temas[i][j]['Year of Study']}")
            print(f"Interese: {temas[i][j]['Interests']}")
            print(f"Preferencia: {temas[i][j]['Preferred Role']}")
            print(f"Experiencia: {temas[i][j]['Experience Level']}")
            print(f"Hackathons: {temas[i][j]['Hackathons Done']}")
            print(f"Idioma: {temas[i][j]['Preferred Languages']}")
            print(f"Amigos: {temas[i][j]["Friend Registration"]}")
            print(f"Prefered Size: {temas[i][j]["Preferred Team Size"]}")
            print(f"Disponibilidad: {temas[i][j]["Availability"]}")
            print(f"Skills: {temas[i][j]["Programming Skills"]}")
        print(f"Score Edad: {evaluar_Edad(temas[i], datos)}")
        print(f"Score Año: {evaluar_AñoEscolar(temas[i], datos)}")
        print(f"Score Intereses: {evaluar_Intereses(temas[i], datos)}")
        print(f"Score Preferencia: {evaluar_Preferencia(temas[i], datos)}")
        print(f"Score Experiencia: {evaluar_Experiencia(temas[i], datos)}")
        print(f"Score Hackathons: {evaluar_Hackathons(temas[i], datos)}")
        print(f"Score Idioma: {evaluar_Idioma(temas[i], datos)}")
        print(f"Score Friend: {evaluar_Friend(temas[i], datos)}")
        print(f"Score Prefered Size: {evaluar_PreferedSize(temas[i], datos)}")
        print(f"Score Availability: {evaluar_Availability(temas[i], datos)}")
        print(f"Score Skills: {evaluar_Skills(temas[i], datos)}\n")
    
    print("\n")

    preferencias = set(datos["Programming Skills"])
    
    


except Exception as e:
    print("Error al procesar el archivo:", e)