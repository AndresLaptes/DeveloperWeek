import pandas as pd
import random as rd
import numpy as np
import re
import ast
import time


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


MAX_NUM_PARTNERS = 4
YEARS = ['1st year', '2nd year', '3rd year', '4th year', 'Masters', 'PhD']
YEAR_TO_INDEX = {year: index for index, year in enumerate(YEARS)}
INVALID_PREFERENCIA = set(["Don't know", "Don't care"])

# Parámetros del algoritmo genético
TAM_POBLACION = 30
NUM_GENERACIONES = 15
PROB_CRUCE = 0.7      # Probabilidad de cruce
PROB_MUTACION = 0.2   # Probabilidad de mutación
PONDERACIONES_TEST = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

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
        self.inicializar_modelo(Participantes)
        
        self.Equipos = Equipos
        self.edad_min = Participantes['age'].min()
        self.id_Usuario = id_Usuario
        self.idParticipantes = Participantes["id"].tolist()
        self.X_Equipos = X_Equipos
        self.edad_max = self.Participantes['age'].max()
        self.Ponderaciones = Ponderaciones
        self.Universidades = set(Participantes["university"])

        self.EquiposValidos = [
            equipo for equipo in self.Equipos 
            if self.id_Usuario not in equipo and len(equipo) >= 1 and len(equipo) < MAX_NUM_PARTNERS
        ]

        try:
            creator.create("FitnessMax", base.Fitness, weights=(1.0,))
            creator.create("Individual", tuple, fitness=creator.FitnessMax)
            
            self.toolbox = base.Toolbox()
            self.configDeap()


        except Exception as e:
            print("Error al procesar el archivo:", e)

    def inicializar_modelo(self, Participantes):
        self.idUsuarios = 

    # Función que crea a un individuo
    def crearIndividuo(self) -> tuple:
        creado_por_usuario = True

        # Crear equipo nuevo con 1-3 miembros aleatorios + usuario objetivos
        otros_usuarios = []
        if len(self.EquiposValidos) != 0:
            otros_usuarios = [
                id for id in self.idParticipantes 
                if id != self.id_Usuario and id not in self.EquiposValidos
            ]
        else: 
            otros_usuarios = self.idParticipantes

        tam_equipo = rd.randint(1, 3)
        team = rd.sample(otros_usuarios, tam_equipo)
        team.append(self.id_Usuario)
        creado_por_usuario = True
    
        return (team, creado_por_usuario)

    # Calcula las puntuaciones normalizadas de la diferencia de edad del Equipo, si los integrantes tienen mucha diferencia el putnaje tendera a 0, 
    # en caso contrario cuanto mas parecidos tengan las edades tendran mas cercano a 1 sera
    def evaluar_Edad(self, team) -> float:
        if len(team) == 1:
            return 0.0

        score = 0
        num_comparaciones = 0

        for i in range(len(team)):
            integrante1 = team[i]
            for j in range(i + 1, len(team)):
                integrante2 = team[j]

                edad1 = self.Participantes.loc[self.Participantes['id'] == integrante1, 'age'].values[0]
                edad2 = self.Participantes.loc[self.Participantes['id'] == integrante2, 'age'].values[0]

                diferencia_edad = abs(edad1 - edad2)

                # score calculado en logaritmo para penalizar diferencias grandes
                score += 1 - (np.log(1 + diferencia_edad) / np.log(self.edad_max - self.edad_min + 1))

                num_comparaciones += 1

        # Devolver el puntaje normalizado 
        return score/num_comparaciones if num_comparaciones > 0 else 1.0

    def evaluar_AñoEscolar(self, team) -> float:
        if len(team) == 1:
            return 0.0

        score = 0
        num_comparaciones = 0

        min_year = 0
        max_year = len(YEARS) - 1

        for i in range(len(team)):
            integrante1 = team[i]
            for j in range(i + 1, len(team)):
                integrante2 = team[j]

                year1 = self.Participantes.loc[self.Participantes['id'] == integrante1, 'year_of_study'].values[0]
                year2 = self.Participantes.loc[self.Participantes['id'] == integrante2, 'year_of_study'].values[0]

                diferencia_year = abs(YEAR_TO_INDEX[year1] - YEAR_TO_INDEX[year2])

                score += 1.0 - (diferencia_year / max_year)

                num_comparaciones += 1

        return score / num_comparaciones if num_comparaciones > 0 else 1.0


    # Calcula las puntuaciones normalizadas de los intereses entre los Participantes
    def evaluar_Intereses(self, team) -> float:
        if len(team) == 1:
            return 0.0

        score = 0
        total_intereses = 0

        for i in range(len(team)):
            integrante1 = team[i]
            for j in range(i + 1, len(team)):
                integrante2 = team[j]

                intereses1 = self.Participantes.loc[self.Participantes['id'] == integrante1, 'interests'].values[0]
                intereses2 = self.Participantes.loc[self.Participantes['id'] == integrante2, 'interests'].values[0]

                intereses1 = set(ast.literal_eval(intereses1))
                intereses2 = set(ast.literal_eval(intereses2))

                test = intereses1.intersection(intereses2)

                if not len(intereses1.intersection(intereses2)) == 0:
                    score += len(intereses1.intersection(intereses2))/len(intereses1.union(intereses2))
            
                total_intereses += 1
            

        # Devolver el puntaje normalizado
        return score / total_intereses if total_intereses > 0 else 1.0

    # Calcula las puntuaciones normalizadas de las Universidades entre los Participantes #la tengo que cambiar
    def evaluar_Universidad(self, team) -> float:
        if len(team) == 1:
            return 1.0
        

        max = ['n', 0]
        for i in range(len(team)):
            uni1 = self.Participantes.loc[self.Participantes['id'] == team[i], 'university'].values[0]
            act = [uni1, 1]
            for j in range(i + 1, len(team)):
                uni2 = self.Participantes.loc[self.Participantes['id'] == team[j], 'university'].values[0]
                if uni1 == uni2:
                    act[1] += 1
            if max[1] < act[1]:
                max = act
        return max[1]/len(team)

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

                preferencia1 = self.Participantes.loc[self.Participantes['id'] == integrante1, 'preferred_role'].values[0]
                preferencia2 = self.Participantes.loc[self.Participantes['id'] == integrante2, 'preferred_role'].values[0]

                if preferencia1 not in INVALID_PREFERENCIA and preferencia2 not in INVALID_PREFERENCIA:
                    if preferencia1 != preferencia2:
                        score += 1
                    normalizar += 1

        return score / normalizar if normalizar > 0 else 1.0


    # Evalua la similitud entre las experiencias cuanto mas diferentes entre ellas son mejor
    def evaluar_Experiencia(self, team) -> float:
        score = 0

        if len(team) == 1:
            return 0.0
    
        normalizar = 0

        for i in range(len(team)):
            integrante1 = team[i]
            for j in range(i + 1, len(team)):
                integrante2 = team[j]

                experiencia1 = self.Participantes.loc[self.Participantes['id'] == integrante1, 'experience_level'].values[0]
                experiencia2 = self.Participantes.loc[self.Participantes['id'] == integrante2, 'experience_level'].values[0]

                if experiencia1 != experiencia2:
                    score += 1
            
                normalizar += 1

        return score/normalizar if normalizar > 0 else 1.0


    # Evaluar la similitud entre hakatones en el equipo, cuantos mas hackatones mejor
    def evaluar_Hackathons(self, team) -> float:
        score = 0

        max_hackathons = self.Participantes['hackathons_done'].max()
    
        for integrante in team:
            hackathons = self.Participantes.loc[self.Participantes['id'] == integrante, 'hackathons_done'].values[0]
            score += hackathons

        return score/ (max_hackathons * len(team))

    def SimilitudTextos(self, embedding1, embedding2) -> float:
        return util.cos_sim(embedding1, embedding2).item()

    def calculate_multiple_scores_with_parallelism(self, pairs):
        with ThreadPoolExecutor() as executor:
            scores = list(executor.map(lambda pair: self.SimilitudTextos(pair[0], pair[1]), pairs))

        return scores

    def evaluar_Textos(self, team, evaluar) -> float:

        if len(team) < 2:
            return 0.0
        
        pairs = []
        for i in range(len(team)):
            integrante1 = team[i]
            for j in range(i + 1, len(team)):
                integrante2 = team[j]

                embedding1 = self.Participantes.loc[self.Participantes['id'] == integrante1, evaluar].values[0]
                embedding2 = self.Participantes.loc[self.Participantes['id'] == integrante2, evaluar].values[0]

                pairs.append((ast.literal_eval(embedding1), ast.literal_eval(embedding2)))

        scores = self.calculate_multiple_scores_with_parallelism(pairs)

        return sum(scores) / len(scores)
    
    # Calcula la interseccion de idiomas entre los participantes del equipo, arreglar aqui
    def evaluar_Idioma(self, team) -> float:
        if len(team) == 1:
            return 0.0  

        idiomas_por_integrante = []
    
        for integrante in team:
            idiomas = self.Participantes.loc[self.Participantes['id'] == integrante, 'preferred_languages']
            if idiomas.notna().any():  
                idiomas = ast.literal_eval(idiomas.values[0])
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
            return 0.0

        tmb = len(team)
        for i in range(len(team)):
            integrante1 = team[i]
            amigos1 = set(ast.literal_eval(self.Participantes.loc[self.Participantes['id'] == integrante1, 'friend_registration'].values[0]))
            for j in range(i + 1, len(team)):
                integrante2 = team[j]
                if integrante2 in amigos1:
                    score += 1          
    
        return score / tmb if tmb > 0 else 1.0
    
    # Calcula cuantos cuanto de bueno es el tamaño del equipo
    def evaluar_PreferedSize(self, team) -> float:
        if len(team) == 1:
            return 0.0

        media = 0
        for integrante in team:
            media += self.Participantes.loc[self.Participantes['id'] == integrante, 'preferred_team_size'].values[0]

        media = media / len(team)
        diff = abs(media - len(team))
        if diff == 0:
            return 1.0
    
        return 1 - min(1, diff / media)

    #Calcula la disponibilidad entre los integrantes del equipo
    def evaluar_Availability(self, team) -> float:
        if len(team) == 1:
            return 0.0

        score = 0
        total_comparaciones = 0

        for i in range(len(team)):
            integrante1 = team[i]
            for j in range(i + 1, len(team)):
                integrante2 = team[j]

                disponibilidad1 = self.Participantes.loc[self.Participantes['id'] == integrante1, 'availability'].values[0]
                disponibilidad2 = self.Participantes.loc[self.Participantes['id'] == integrante2, 'availability'].values[0]

                if disponibilidad1 == disponibilidad2:
                    score += 1

                total_comparaciones += 1

        return score / total_comparaciones if total_comparaciones > 0 else 1.0

    def evaluar_Skills(self, team) -> float:
        if not team:
            return 0
        
        team_skills = []
        for integrante in team:
            skills_data = str(self.Participantes.loc[self.Participantes['id'] == integrante, 'programming_skills'].values[0])
        
            skills_data = skills_data.strip('{}')
        
            if not skills_data:
                continue
            
            pairs = [pair.strip() for pair in skills_data.split(',')]
        
            for pair in pairs:
                skill, level = pair.split(':')
            
                skill = skill.strip().strip('"\'')
                level = int(level.strip().strip('"\''))
            
                team_skills.append((skill, level))
    
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
    
        level_scores = [level / 10 for level in skill_levels.values()]
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
        score += self.evaluar_Textos(team, "ember_obj") * self.Ponderaciones[7]
        score += self.evaluar_Textos(team, "ember_intr") * self.Ponderaciones[8]
        score += self.evaluar_Textos(team, "ember_excitement") * self.Ponderaciones[9]
        score += self.evaluar_Idioma(team) * self.Ponderaciones[10]
        score += self.evaluar_Friend(team) * self.Ponderaciones[11]
        score += self.evaluar_PreferedSize(team) * self.Ponderaciones[12]
        score += self.evaluar_Availability(team) * self.Ponderaciones[13] #se puede mejorar
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

        for i in range(len(equipo) - 1) : 
            if equipo[i] != usuario: 
                team.append(equipo[i])

        score  = (
            self.evaluarEquipoParaUser(usuario, team) * compatibilidadUsuarioEquipo + 
            self.evaluarCompatibilidadEquipo(team) * compatibilidadEquipo
        )

        return score,


    def crossover_teams(self, team1: tuple, team2: tuple) -> tuple:
        
        team1_ids, _ = team1
        team2_ids, _ = team2
    
        team1_without_target = [id for id in team1_ids if id != self.id_Usuario]
        team2_without_target = [id for id in team2_ids if id != self.id_Usuario]
    
        all_members = list(set(team1_without_target + team2_without_target))
    
        if len(all_members) < 2:
            return team1, team2
    
        new_team1 = []
        new_team2 = []
    
        size1 = rd.randint(1, min(3, len(all_members)))
        size2 = rd.randint(1, min(3, len(all_members)))
    
        if all_members:
            new_team1 = rd.sample(all_members, size1)
            remaining_members = [m for m in all_members if m not in new_team1]
            if remaining_members:
                new_team2 = rd.sample(remaining_members, min(size2, len(remaining_members)))
    
        new_team1.append(self.id_Usuario)
        new_team2.append(self.id_Usuario)
    
        return (new_team1, True), (new_team2, True)

    def mutate_team(self, team: tuple) -> tuple:
        team_ids, _ = team
    
        available_users = [
            id for id in self.idParticipantes 
            if id != self.id_Usuario and 
            id not in self.EquiposValidos and 
            id not in team_ids
        ]
    
        if not available_users:
            return team
    
        current_team = [id for id in team_ids if id != self.id_Usuario]
    
        if rd.random() < 0.5 and len(current_team) < 3:
            current_team.append(rd.choice(available_users))
        elif current_team:
            idx_to_replace = rd.randrange(len(current_team))
            current_team[idx_to_replace] = rd.choice(available_users)
    
        current_team.append(self.id_Usuario)
    
        return (current_team, True)

    def select_teams(self, population, k):
        def tournament_selection(tournament_pool):
            if len(tournament_pool) < 3:
                tournament = tournament_pool
            else:
                tournament = rd.sample(tournament_pool, 3)
        
            best_team = None
            best_score = float('-inf')
        
            for team in tournament:
                score = self.evaluarEquipo(team[0])[0]
            
                if score > best_score:
                    best_score = score
                    best_team = team
        
            return best_team
    
        selected = []
        available_teams = population.copy()
    
        for _ in range(k):
            if not available_teams:
                break
            
            selected_team = tournament_selection(available_teams)
            selected.append(selected_team)
        
            if selected_team in available_teams:
                available_teams.remove(selected_team)
    
        return selected

    def configDeap(self):
        # Funcion que crea a un individuo
        self.toolbox.register("individual", tools.initIterate, creator.Individual, self.crearIndividuo)
        # Funcion que crea a la poblacion
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        # Funcion que evalua al equipo, basicamente el calculador del score o fitness
        self.toolbox.register("evaluate", self.evaluarEquipo)
        # Funcion de combinación
        self.toolbox.register("mate", self.crossover_teams)
        # Funcion de mutación
        self.toolbox.register("mutate", self.mutate_team)
        # Funcion de selección
        self.toolbox.register("select", self.select_teams)

    def encontrar_mejores_equipos(self) -> List[tuple]:
        
    
        cache_evaluaciones = {}
    
        def evaluar_con_cache(equipo):
            equipo_tuple = tuple(sorted(equipo[0]))
            if equipo_tuple not in cache_evaluaciones:
                cache_evaluaciones[equipo_tuple] = self.toolbox.evaluate(equipo[0])
            return cache_evaluaciones[equipo_tuple]

        poblacion = []
        used_teams = set()
    
        while len(poblacion) < TAM_POBLACION:
            ind = self.toolbox.individual()
            team_tuple = tuple(sorted(ind[0]))
        
            if team_tuple not in used_teams:
                used_teams.add(team_tuple)
                ind.fitness.values = evaluar_con_cache(ind)
                poblacion.append(ind)

        mejor_equipo = tools.selBest(poblacion, k=1)[0]
        mejor_fitness = mejor_equipo.fitness.values[0]

        mejores_equipos = set()
        umbral_calidad = 0.7  

        generaciones_sin_mejora = 0
        max_generaciones_sin_mejora = 5

        for gen in range(NUM_GENERACIONES):
            if generaciones_sin_mejora >= max_generaciones_sin_mejora:
                break

            descendientes = self.toolbox.select(poblacion, len(poblacion))
            descendientes = list(map(self.toolbox.clone, descendientes))

            for i in range(0, len(descendientes), 2):
                if i + 1 < len(descendientes):
                    if rd.random() < PROB_CRUCE:
                        hijo1, hijo2 = self.toolbox.mate(descendientes[i], descendientes[i+1])
                        descendientes[i] = creator.Individual(hijo1)
                        descendientes[i+1] = creator.Individual(hijo2)
                        descendientes[i].fitness.values = evaluar_con_cache(descendientes[i])
                        descendientes[i+1].fitness.values = evaluar_con_cache(descendientes[i+1])

            for i in range(len(descendientes)):
                if rd.random() < PROB_MUTACION:
                    mutado = self.toolbox.mutate(descendientes[i])
                    descendientes[i] = creator.Individual(mutado)
                    descendientes[i].fitness.values = evaluar_con_cache(descendientes[i])

            mejores_padres = tools.selBest(poblacion, k=5)
            poblacion = descendientes
            poblacion.extend(mejores_padres)
            poblacion = tools.selBest(poblacion, k=TAM_POBLACION)

            mejor_actual = tools.selBest(poblacion, k=1)[0]
            if mejor_actual.fitness.values[0] > mejor_fitness:
                mejor_equipo = mejor_actual
                mejor_fitness = mejor_actual.fitness.values[0]
                generaciones_sin_mejora = 0
            else:
                generaciones_sin_mejora += 1

            for ind in poblacion:
                if ind.fitness.values[0] >= umbral_calidad:
                    equipo_tuple = tuple(sorted(ind[0]))
                    mejores_equipos.add((equipo_tuple, ind[1]))

                if len(mejores_equipos) >= self.X_Equipos * 2:
                    break

        mejores_equipos_lista = list(mejores_equipos)
        mejores_equipos_lista.sort(
            key=lambda x: cache_evaluaciones[tuple(sorted(x[0]))][0],
            reverse=True
        )

        return mejores_equipos_lista[:self.X_Equipos]

    def ejecutar_busqueda_equipos(self):
        mejores_equipos = self.encontrar_mejores_equipos()
    
        print("\nMejores equipos encontrados:")
        for i, (equipo, creado_por_usuario) in enumerate(mejores_equipos, 1):
            fitness = self.toolbox.evaluate(equipo)[0]
            print(f"\nEquipo {i} (Fitness: {fitness:.3f}):")
            for id_miembro in equipo:
                if id_miembro == self.id_Usuario:
                    print(f"- {id_miembro} (Usuario objetivo)")
                else:
                    print(f"- {id_miembro}")
        return mejores_equipos


try:
    start_time = time.time()
    path = get_path_csv("output")
    datos = pd.read_csv(path)
    
    test = TeamFormation([], "2ebad15c-c0ef-4c04-ba98-c5d98403a90c", datos, 5, PONDERACIONES_TEST)
    test.ejecutar_busqueda_equipos()
    end_time = time.time() 
    elapsed_time_ms = (end_time - start_time) * 1000  
    print(f"Tiempo de ejecución: {elapsed_time_ms:.2f} ms")
except Exception as e:
    print("Error al procesar el archivo:", e)