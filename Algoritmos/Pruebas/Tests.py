import pandas as pd
import random as rd
import numpy as np
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

try:
    datos = pd.read_csv(get_path_csv("Data"))
    temas = generateRandomTeams(datos)

    for i in range(len(temas)):
        for j in range(len(temas[i])):
            print(f"Edad de {temas[i][j]['Name']}: {temas[i][j]['Age']}, ")
            print(f"año escolar: {temas[i][j]['Year of Study']}, ")
            print(f"interese: {temas[i][j]['Interests']}")
            print(f"preferencia: {temas[i][j]['Preferred Role']}")
            print(f"experiencia: {temas[i][j]['Experience Level']}")
            print(f"Hackathons: {temas[i][j]['Hackathons Done']}")
        print(f"Score Edad: {evaluar_Edad(temas[i], datos)}")
        print(f"Score Año: {evaluar_AñoEscolar(temas[i], datos)}")
        print(f"Score Intereses: {evaluar_Intereses(temas[i], datos)}")
        print(f"Score Preferencia: {evaluar_Preferencia(temas[i], datos)}")
        print(f"Score Experiencia: {evaluar_Experiencia(temas[i], datos)}")
        print(f"Score Hackathons: {evaluar_Hackathons(temas[i], datos)}\n")
    
    print("\n")

    preferencias = set(datos["Hackathons Done"])
    print(preferencias)
    


except Exception as e:
    print("Error al procesar el archivo:", e)