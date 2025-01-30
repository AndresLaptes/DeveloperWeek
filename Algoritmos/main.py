import pandas as pd
import random as rd
import numpy as np
import re


from deap import base, creator, tools, algorithms
from pathlib import Path
from typing import List, Dict

from sentence_transformers import SentenceTransformer, util
from concurrent.futures import ThreadPoolExecutor


def get_path_csv(filename):
    if not filename.endswith('.csv'):
        filename = f"{filename}.csv"
    
    current_dir = Path(__file__).parent
    csv_dir = current_dir / 'DataSets'
    file_path = csv_dir / filename

    if not file_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {filename}")
    
    return file_path


PonderacionesTest = {1,1,1,1,2,3,2,1,3,1,4,1,1,1,2,3,5,2,1}

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


MAX_NUM_PARTNERS = 4
YEARS = ['1st year', '2nd year', '3rd year', '4th year', 'Masters', 'PhD']
YEAR_TO_INDEX = {year: index for index, year in enumerate(YEARS)}
INVALID_PREFERENCIA = set(["Don't know", "Don't care"])


class TeamFormation:
    # Equipos -> todos los equipos disponibles, 1 equipo es una lista de los id de los participantes (lsit(list(String)))
    # id_Usuario -> el usuario que busca equipo
    # X_Equipos -> el número de equipos que hay que buscar
    # Participantes -> los participantes del evento, la BD de usuarios con su info
    # Ponderaciones -> dado es una lista de valores de 18 posiciones. Representa lo siguiente
    # son los atributos de un participante (los importantes mirar excel) que si el valor es positivo se prioriza maximizar
    # en caso contrario si es negativo se minimizara, cuando mayor sean en cada caso los numeros tanto positivos
    # o negativos mayor prioridad tendran
    def __init__(self, Equipos, id_Usuario, Participantes, X_Equipos, Ponderaciones):
        self.Equipos = Equipos
        self.id_Usuario = id_Usuario
        self.idParticipantes = Participantes["ID"].astype(str)
        self.idParticipantes = Participantes
        self.X_Equipos = X_Equipos
        self.Ponderaciones = Ponderaciones
        self.Universidades = set(Participantes["University"])

        self.EquiposValidos = [
            equipo for equipo in self.Equipos 
            if self.id_Usuario not in equipo and len(equipo) >= 1 and len(equipo) < MAX_NUM_PARTNERS
        ]

        try:
            path = get_path_csv("Data")
            datos = pd.read_csv(path)
    
            teams = generateRandomTeams(datos)
    
            creator.create("FitnessMax", base.Fitness, weights=(1.0,))
            creator.create("Individual", tuple, fitness=creator.FitnessMax)
            
            self.toolbox = base.Toolbox()
            self.configDeap()


        except Exception as e:
            print("Error al procesar el archivo:", e)

    # Función que crea a un individuo
    def crearIndividuo(self) -> tuple:
        creado_por_usuario = True

        # Crear equipo nuevo con 1-3 miembros aleatorios + usuario objetivos
        otros_usuarios = [
            id for id in self.idParticipantes 
            if id != self.id_Usuario and id not in self.EquiposValidos
        ]

        tam_equipo = rd.randint(1, 3)
        team = rd.sample(otros_usuarios, tam_equipo)
        team.append(self.id_Usuario)
        creado_por_usuario = True
    
        return (team, creado_por_usuario)

    # Calcula las puntuaciones normalizadas de la diferencia de edad del Equipo, si los integrantes tienen mucha diferencia el putnaje tendera a 0, 
    # en caso contrario cuanto mas parecidos tengan las edades tendran mas cercano a 1 sera
    def evaluar_Edad(self, team) -> float:
        if len(team) == 1:
            return 1.0

        score = 0
        num_comparaciones = 0

        edad_min = self.Participantes['Age'].min()
        edad_max = self.Participantes['Age'].max()

        for i in range(len(team)):
            integrante1 = team[i]
            for j in range(i + 1, len(team)):
                integrante2 = team[j]

                edad1 = self.Participantes.loc[self.Participantes['ID'] == integrante1, 'Age'].values[0]
                edad2 = self.Participantes.loc[self.Participantes['ID'] == integrante2, 'Age'].values[0]

                diferencia_edad = abs(edad1 - edad2)

                # score calculado en logaritmo para penalizar diferencias grandes
                score += 1 - (np.log(1 + diferencia_edad) / np.log(edad_max - edad_min + 1))

                num_comparaciones += 1

        # Devolver el puntaje normalizado 
        return score/num_comparaciones if num_comparaciones > 0 else 1.0

    def evaluar_AñoEscolar(self, team) -> float:
        if len(team) == 1:
            return 1.0

        score = 0
        num_comparaciones = 0

        min_year = 0
        max_year = len(YEARS) - 1

        for i in range(len(team)):
            integrante1 = team[i]
            for j in range(i + 1, len(team)):
                integrante2 = team[j]

                year1 = self.Participantes.loc[self.Participantes['ID'] == integrante1, 'Year'].values[0]
                year2 = self.Participantes.loc[self.Participantes['ID'] == integrante2, 'Year'].values[0]

                diferencia_year = abs(YEAR_TO_INDEX[year1] - YEAR_TO_INDEX[year2])

                score += 1.0 - (diferencia_year / max_year)

                num_comparaciones += 1

        return score / num_comparaciones if num_comparaciones > 0 else 1.0


    # Calcula las puntuaciones normalizadas de los intereses entre los Participantes
    def evaluar_Intereses(self, team) -> float:
        if len(team) == 1:
            return 1.0

        score = 0
        total_intereses = 0

        for i in range(len(team)):
            integrante1 = team[i]
            for j in range(i + 1, len(team)):
                integrante2 = team[j]

                intereses1 = self.Participantes.loc[self.Participantes['ID'] == integrante1['ID'], 'Interests'].values[0]
                intereses2 = self.Participantes.loc[self.Participantes['ID'] == integrante2['ID'], 'Interests'].values[0]

                intereses1 = set(intereses1.split(", "))
                intereses2 = set(intereses2.split(", "))

                if not len(intereses1.union(intereses2)) == 0:
                    score += len(intereses1.intersection(intereses2))/len(intereses1.union(intereses2))
            
                total_intereses += 1
            

        # Devolver el puntaje normalizado
        return score / total_intereses if total_intereses > 0 else 1.0

    # Calcula las puntuaciones normalizadas de las Universidades entre los Participantes
    def evaluar_Universidad(self, team) -> float:
        if len(team) == 1:
            return 1.0
        
        score = 0
        for part in team:
            uni = self.Participantes.loc[self.Participantes['ID'] == part, 'University'].values[0]
            if uni in self.Universidades:
                score += 1

        return score/len(team)

    # Calcula las puntuaciones normalizadas de las preferencias entre los participantes
    def evaluar_Preferencia(self, team) -> float:
        score = 0

        if len(team) == 1:
            return 1.0
    
        normalizar = 0

        for i in range(len(team)):
            integrante1 = team[i]
            for j in range(i + 1, len(team)):
                integrante2 = team[j]

                preferencia1 = self.Participantes.loc[self.Participantes['ID'] == integrante1['ID'], 'Preferred Role'].values[0]
                preferencia2 = self.Participantes.loc[self.Participantes['ID'] == integrante2['ID'], 'Preferred Role'].values[0]

                if preferencia1 not in INVALID_PREFERENCIA and preferencia2 not in INVALID_PREFERENCIA:
                    if preferencia1 != preferencia2:
                        score += 1
                    normalizar += 1

        return score / normalizar if normalizar > 0 else 1.0


    # Evalua la similitud entre las experiencias cuanto mas diferentes entre ellas son mejor
    def evaluar_Experiencia(self, team) -> float:
        score = 0

        if len(team) == 1:
            return 1.0
    
        normalizar = 0

        for i in range(len(team)):
            integrante1 = team[i]
            for j in range(i + 1, len(team)):
                integrante2 = team[j]

                experiencia1 = self.Participantes.loc[self.Participantes['ID'] == integrante1['ID'], 'Experience Level'].values[0]
                experiencia2 = self.Participantes.loc[self.Participantes['ID'] == integrante2['ID'], 'Experience Level'].values[0]

                if experiencia1 != experiencia2:
                    score += 1
            
                normalizar += 1

        return score/normalizar if normalizar > 0 else 1.0


    # Evaluar la similitud entre hakatones en el equipo, cuantos mas hackatones mejor
    def evaluar_Hackathons(self, team) -> float:
        score = 0

        max_hackathons = self.Participantes['Hackathons Done'].max()
    
        for integrante in team:
            hackathons = self.Participantes.loc[self.Particiantes['ID'] == integrante['ID'], 'Hackathons Done'].values[0]
            score += hackathons

        return score/ (max_hackathons * len(team))

    def SimilitudTextos(self, embedding1, embedding2) -> float:
        return util.cos_sim(embedding1, embedding2).item()

    def calculate_multiple_scores_with_parallelism(pairs):
        with ThreadPoolExecutor() as executor:
            scores = list(executor.map(lambda pair: (pair[0], pair[1]), pairs))

        return scores

    def evaluar_Textos(self, team, evaluar) -> float:

        if len(team) < 2:
            return 1.0
        
        pairs = []
        for i in range(len(team)):
            integrante1 = team[i]
            for j in range(i + 1, len(team)):
                integrante2 = team[j]

                embedding1 = integrante1[evaluar]
                embedding2 = integrante2[evaluar]

                pairs.append((embedding1, embedding2))

        scores = self.calculate_multiple_scores_with_parallelism(pairs)

        return sum(scores) / len(scores)
    
    # Calcula la interseccion de idiomas entre los participantes del equipo
    def evaluar_Idioma(self, team) -> float:
        if len(team) == 1:
            return 1.0  

        idiomas_por_integrante = []
    
        for integrante in team:
            idiomas = self.Participantes.loc[self.Participantes['ID'] == integrante['ID'], 'Preferred Languages']
            if idiomas.notna().any():  
                idiomas = idiomas.values[0].split(", ")
                idiomas_por_integrante.append(set(idiomas)) 

        if not idiomas_por_integrante:  
            return 0.0


        idioma_comun = set.intersection(*idiomas_por_integrante) if idiomas_por_integrante else set()

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
    
     
    # Calcula cuantos miebros del equipo son amigos
    def evaluar_Friend(self, team) -> float:
        score = 0

        if len(team) == 1:
            return 1.0

        tmb = len(team)
        for i in range(len(team)):
            integrante1 = team[i]
            amigos1 = set(self.Participantes.loc[self.Participantes['ID'] == integrante1['ID'], 'Friend Registration'].values[0].split(", "))
            for j in range(i + 1, len(team)):
                integrante2 = team[j]
                if integrante2['ID'] in amigos1:
                    score += 1          
    
        return score / tmb if tmb > 0 else 1.0
    
    # Calcula cuantos cuanto de bueno es el tamaño del equipo
    def evaluar_PreferedSize(self, team) -> float:
        if len(team) == 1:
            return 1.0

        media = 0
        for integrante in team:
            media += self.Participantes.loc[self.Participantes['ID'] == integrante['ID'], 'Preferred Team Size'].values[0]

        media = media / len(team)
        diff = abs(media - len(team))
        if diff == 0:
            return 1.0
    
        return 1 - min(1, diff / media)

    #Calcula la disponibilidad entre los integrantes del equipo
    def evaluar_Availability(self, team) -> float:
        if len(team) == 1:
            return 1.0

        score = 0
        total_comparaciones = 0

        for i in range(len(team)):
            integrante1 = team[i]
            for j in range(i + 1, len(team)):
                integrante2 = team[j]

                disponibilidad1 = self.Participantes.loc[self.Participantes['ID'] == integrante1['ID'], 'Availability'].values[0]
                disponibilidad2 = self.Participantes.loc[self.Participantes['ID'] == integrante2['ID'], 'Availability'].values[0]

                if disponibilidad1 == disponibilidad2:
                    score += 1

                total_comparaciones += 1

        return score / total_comparaciones if total_comparaciones > 0 else 1.0

    def evaluar_Skills(self, team) -> float:
        team_skills = []
        for integrante in team:
            data = str(self.Participante.loc[self.Participante['ID'] == integrante['ID'], 'Programming Skills'].values[0])
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

    # Calcula la compatibilidad que tiene los integrates del equipo entre si sin tener encuenta el 
    # usuario objetivo
    def evaluarCompatibilidadEquipo(self, team) -> float:
        score = 0
        
        score += self.evaluar_Edad(team) * self.Ponderaciones[0]
        score += self.evaluar_AñoEscolar(team) * self.Ponderaciones[1]
        score += self.evaluar_Universidad(team) * self.Ponderaciones[2]
        score += self.evaluar_Intereses(team) * self.Ponderaciones[3]
        score += self.evaluar_Preferencia(team) * self.Ponderaciones[4]
        score += self.evaluar_Experiencia(team) * self.Ponderaciones[5]
        score += self.evaluar_Hackathons(team) * self.Ponderaciones[6]
        score += self.evaluar_Textos(team, 'ember_obj') * self.Ponderaciones[7]
        score += self.evaluar_Textos(team, 'ember_intr') * self.Ponderaciones[8]
        score += self.evaluar_Textos(team, 'ember_excitement') * self.Ponderaciones[9]
        score += self.evaluar_Idioma(team) * self.Ponderaciones[10]
        score += self.evaluar_Friend(team) * self.Ponderaciones[11]
        score += self.evaluar_PreferedSize(team) * self.Ponderaciones[12]
        score += self.evaluar_Availability(team) * self.Ponderaciones[13]
        score += self.evaluar_Skills(team) * self.Ponderaciones[14]
        
        return score

    # Calcula la compatibilidad entre el equipo y nuestro usuario
    def evaluarEquipoParaUser(self, usuario, team) -> float:
        score = 0

        team.append(usuario)
        score = self.evaluarCompatibilidadEquipo(team)

        return score

    # Tengo que ver todavia como evalua si el equipo es el adecuado, tendre que crear funciones para el calculo
    # Necesito el vector de Preferencias (Exel), ver lo importante o no
    def evaluarEquipo(self, equipo: tuple) -> tuple:
        usuario = self.id_Usuario
        team = list()

        compatibilidadUsuarioEquipo = 0.7
        compatibilidadEquipo = 0.3

        for i in len(equipo) - 1 : 
            if equipo[i] != usuario: 
                team.append(equipo[i])

        score  = (
            self.evaluarEquipoParaUser(usuario, team) * compatibilidadUsuarioEquipo + 
            self.evaluarCompatibilidadEquipo(team) * compatibilidadEquipo
        )

        return score,


    def configDeap(self):
        # Funcion que crea a un individuo
        self.toolbox.register("individual", tools.initIterate, creator.Individual, self.crearIndividuo())
        # Funcion que crea a la poblacion
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        # Funcion que evalua al equipo, basicamente el calculador del score o fitness
        self.toolbox.register("evaluate", self.evaluarEquipo(self.Equipos))
