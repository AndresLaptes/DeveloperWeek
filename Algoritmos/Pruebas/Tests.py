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

                score += 1 - (np.log(1 + diferencia_year) / np.log(max_year - min_year + 1))

                num_comparaciones += 1

        # Devolver el puntaje normalizado
        return score / num_comparaciones

try:
    datos = pd.read_csv(get_path_csv("Data"))
    temas = generateRandomTeams(datos)

    for i in range(len(temas)):
        for j in range(len(temas[i])):
            print(f"Edad de {temas[i][j]['Name']}: {temas[i][j]['Age']}, ")
            print(f"año escolar: {temas[i][j]['Year of Study']}")
        print(f"Score Edad: {evaluar_Edad(temas[i], datos)}")
        print(f"Score Año: {evaluar_AñoEscolar(temas[i], datos)}\n")
    
    print("\n")


    print(set(datos['University']))


except Exception as e:
    print("Error al procesar el archivo:", e)