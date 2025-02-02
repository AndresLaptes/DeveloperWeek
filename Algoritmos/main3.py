import pandas as pd
import numpy as np
import random as rd
from deap import base, creator, tools, algorithms
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor  # Cambiado a ThreadPool
from pathlib import Path
import ast
import time

MAX_NUM_PARTNERS = 4
YEARS = ['1st year', '2nd year', '3rd year', '4th year', 'Masters', 'PhD']
YEAR_INDEX = {year: idx for idx, year in enumerate(YEARS)}
TAM_POBLACION = 30
NUM_GENERACIONES = 15
PROB_CRUCE = 0.7
PROB_MUTACION = 0.2
PONDERACIONES_TEST = [1]*15

class TeamEvaluator:
    def __init__(self, participantes):
        self._prepare_data(participantes)
        
    def _prepare_data(self, df):
        """Preprocesamiento optimizado sin objetos no serializables"""
        self.id_to_idx = {id: idx for idx, id in enumerate(df['id'])}
        self.ages = df['age'].values
        self.years = np.array([YEAR_INDEX[y] for y in df['year_of_study']])
        self.universities = df['university'].values
        self.interests = [ast.literal_eval(x) for x in df['interests']]
        self.roles = df['preferred_role'].values
        self.experience = df['experience_level'].values
        self.hackathons = df['hackathons_done'].values
        self.languages = [ast.literal_eval(x) for x in df['preferred_languages']]
        self.friends = [ast.literal_eval(x) for x in df['friend_registration']]
        self.team_sizes = df['preferred_team_size'].values
        self.availability = df['availability'].values
        self.skills = [self._parse_skills(x) for x in df['programming_skills']]
        self.max_hackathons = np.max(self.hackathons)
        self.edad_range = np.ptp(self.ages) + 1
        
        # Embeddings preprocesados como numpy arrays
        self.embeddings = {
            'ember_obj': np.array([ast.literal_eval(x) for x in df['ember_obj']], dtype=np.float32),
            'ember_intr': np.array([ast.literal_eval(x) for x in df['ember_intr']], dtype=np.float32),
            'ember_excitement': np.array([ast.literal_eval(x) for x in df['ember_excitement']], dtype=np.float32)
        }

    def _parse_skills(self, skill_str):
        return dict(
            (k.strip().strip('"\''), int(v.strip().strip('"\''))) 
            for k, v in (pair.split(':', 1) for pair in skill_str.strip('{}').split(','))
        )

class ParallelTeamFormation:
    def __init__(self, equipos, user_id, participantes, x_equipos, ponderaciones):
        self.evaluator = TeamEvaluator(participantes)
        self.user_id = user_id
        self.user_idx = self.evaluator.id_to_idx[user_id]
        self.x_equipos = x_equipos
        self.ponderaciones = np.array(ponderaciones)
        
        self._setup_evolution()
        
    def _setup_evolution(self):
        """Configuración del algoritmo genético"""
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)
        
        self.toolbox = base.Toolbox()
        self.toolbox.register("individual", self._gen_individual)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("evaluate", self._evaluate)
        self.toolbox.register("mate", self._crossover)
        self.toolbox.register("mutate", self._mutate)
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        
        # Usar ThreadPoolExecutor en lugar de ProcessPool
        self.executor = ThreadPoolExecutor()
        self.toolbox.register("map", self.executor.map)

    def _gen_individual(self):
        """Genera un individuo válido"""
        available = [
            idx for idx in self.evaluator.id_to_idx.values() 
            if idx != self.user_idx
        ]
        team_size = rd.randint(1, 3)
        return creator.Individual(
            [self.user_idx] + rd.sample(available, team_size)
        )

    def _evaluate(self, individual):
        """Función de evaluación optimizada y serializable"""
        team = np.unique(individual)
        if len(team) < 2:
            return (0.0,)
        
        scores = np.zeros(15)
        ev = self.evaluator
        
        # Edad
        ages = ev.ages[team]
        age_diff = np.mean(np.abs(ages[:, None] - ages[None, :]))
        scores[0] = 1 - np.log(1 + age_diff) / np.log(ev.edad_range)
        
        # Año escolar
        years = ev.years[team]
        year_diff = np.mean(np.abs(years[:, None] - years[None, :]))
        scores[1] = 1 - year_diff / (len(YEARS) - 1)
        
        # Universidad
        unis, counts = np.unique(ev.universities[team], return_counts=True)
        scores[2] = counts.max() / len(team)
        
        # Intereses
        intersect = sum(len(set(ev.interests[i]) & set(ev.interests[j])) 
                       for i in team for j in team if i < j)
        union = sum(len(set(ev.interests[i]) | set(ev.interests[j])) 
                   for i in team for j in team if i < j)
        scores[3] = intersect / union if union > 0 else 0
        
        # Preferencia roles
        valid_roles = ev.roles[team][ev.roles[team] != "Don't know"]
        scores[4] = (valid_roles[:, None] != valid_roles[None, :]).mean() if len(valid_roles) > 1 else 0
        
        # Experiencia
        exp = ev.experience[team]
        scores[5] = (exp[:, None] != exp[None, :]).mean()
        
        # Hackathones
        scores[6] = ev.hackathons[team].mean() / ev.max_hackathons
        
        # Embeddings (usando producto punto vectorizado)
        for i, emb_type in enumerate(['ember_obj', 'ember_intr', 'ember_excitement'], 7):
            embs = ev.embeddings[emb_type][team]
            scores[i] = np.dot(embs, embs.T).mean()
        
        return (np.dot(scores, self.ponderaciones),)

    def _crossover(self, ind1, ind2):
        """Operador de cruce optimizado"""
        combined = list(set(ind1) | set(ind2))
        np.random.shuffle(combined)
        split = np.random.randint(1, len(combined))
        return (
            creator.Individual(combined[:split]),
            creator.Individual(combined[split:])
        )

    def _mutate(self, individual):
        """Operador de mutación optimizado"""
        team = list(individual)
        possible = [idx for idx in self.evaluator.id_to_idx.values() 
                   if idx != self.user_idx and idx not in team]
        
        if possible:
            if rd.random() < 0.5 and len(team) < MAX_NUM_PARTNERS:
                team.insert(rd.randint(0, len(team)), rd.choice(possible))
            else:
                team[rd.randint(0, len(team)-1)] = rd.choice(possible)
        
        return creator.Individual(team)

    def find_teams(self):
        """Ejecuta la búsqueda de equipos"""
        pop = self.toolbox.population(n=TAM_POBLACION)
        hof = tools.HallOfFame(self.x_equipos)
        stats = tools.Statistics(lambda ind: ind.fitness.values[0])
        stats.register("avg", np.mean)
        stats.register("min", np.min)
        stats.register("max", np.max)
        
        algorithms.eaSimple(
            pop, self.toolbox, cxpb=PROB_CRUCE, mutpb=PROB_MUTACION,
            ngen=NUM_GENERACIONES, stats=stats, halloffame=hof, verbose=True
        )
        
        # Convertir índices a IDs
        id_map = {v: k for k, v in self.evaluator.id_to_idx.items()}
        return [
            [id_map[idx] for idx in ind if idx != self.user_idx]
            for ind in hof
        ]

# Uso del sistema
if __name__ == "__main__":
    try:
        start_time = time.time()
        path = Path(__file__).parent / 'DataSets' / 'output.csv'
        data = pd.read_csv(path)
        
        tf = ParallelTeamFormation([], "2ebad15c-c0ef-4c04-ba98-c5d98403a90c", data, 5, PONDERACIONES_TEST)
        mejores_equipos = tf.find_teams()
        
        print("\nMejores equipos encontrados:")
        for i, equipo in enumerate(mejores_equipos, 1):
            print(f"\nEquipo {i}:")
            for member in equipo:
                print(f"- {member}")
        
        print(f"\nTiempo total: {time.time()-start_time:.2f} segundos")
    except Exception as e:
        print(f"Error: {str(e)}")