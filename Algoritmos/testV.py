from pathlib import Path
import numpy as np
import time
import orjson
import math
import random as rd
from deap import base, creator, tools, algorithms

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
    def __init__(self, Equipos, id_Usuario, Participantes, X_Equipos, Ponderaciones):
        self.Inicializacion(Equipos, id_Usuario, Participantes, X_Equipos, Ponderaciones)
        try:
            creator.create("FitnessMax", base.Fitness, weights=(1.0,))
            creator.create("Individual", tuple, fitness=creator.FitnessMax)
            
            self.toolbox = base.Toolbox()
            self.configDeap()


        except Exception as e:
            print("Error al procesar el archivo:", e)

    def Inicializacion(self, Equipos, id_Usuario, Participantes, X_Equipos, Ponderaciones):
        self.Equipos = np.array(Equipos, dtype=object)
        self.id_Usuario = id_Usuario


        self.data = {p["id"]: p for p in Participantes}
        self.num_Equipos = X_Equipos
        self.Ponderaciones = np.array(Ponderaciones, dtype=float)

        self.idParticipantes = []
        self.edad_min = float('-inf')
        self.edad_max = float('inf')

        for participante in self.data.values():
            self.idParticipantes.append(participante["id"])
            
            edad_act = participante["age"]
            if self.edad_min < edad_act :
                self.edad_min = edad_act 
            if self.edad_max > edad_act : 
                self.edad_max = edad_act 

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

    def evaluarEquipoParaUser(self, usuario, team) -> float:
        score = 0

        team.append(usuario)
        score = self.evaluarCompatibilidadEquipo(team)

        return score

    def evaluarCompatibilidadEquipo(self, team) -> float:
        score = 0
        info = [self.get_participant_info(id) for id in team]

        score += self.evaluar_Edad(info) * self.Ponderaciones[0]
        score += self.evaluar_AñoEscolar(info) * self.Ponderaciones[1]
        score += self.evaluar_Universidad(info) * self.Ponderaciones[2]
        score += self.evaluar_Intereses(info) * self.Ponderaciones[3]
        score += self.evaluar_Preferencia(info) * self.Ponderaciones[4]
        score += self.evaluar_Experiencia(info) * self.Ponderaciones[5]
        score += self.evaluar_Hackathons(info) * self.Ponderaciones[6]
        score += self.evaluar_Textos(info, "ember_obj") * self.Ponderaciones[7]
        score += self.evaluar_Textos(info, "ember_intr") * self.Ponderaciones[8]
        score += self.evaluar_Textos(info, "ember_excitement") * self.Ponderaciones[9]
        score += self.evaluar_Idioma(info) * self.Ponderaciones[10]
        score += self.evaluar_Friend(info) * self.Ponderaciones[11]
        score += self.evaluar_PreferedSize(info) * self.Ponderaciones[12]
        score += self.evaluar_Availability(info) * self.Ponderaciones[13] 
        score += self.evaluar_Skills(info) * self.Ponderaciones[14]
        
        return score

    def get_participant_info(self, id):
        return self.data.get(id, None)

    def get_column_value(self, participant_info, column):
        if participant_info is None:
            return None
        return participant_info.get(column, None)

def get_path(filename: str, tipo: str) -> str:
    if not filename.endswith(tipo):
        filename = f"{filename}.{tipo}"
    
    current_dir = Path(__file__).parent
    csv_dir = current_dir / 'DataSets'
    file_path = csv_dir / filename

    if not file_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {filename}")
    
    return file_path

path = get_path("output", "json")

if __name__ == "__main__":
    try:
        start_time = time.time()
                
        with open(path, "rb") as f:
            datos = orjson.loads(f.read())

        end_time = time.time()
        elapsed_time_ms = (end_time - start_time) * 1000  
        print(f"Tiempo de ejecución (cargar JSON): {elapsed_time_ms:.2f} ms")
        
        start_time = time.time()
        data = TeamFormation([], "2ebad15c-c0ef-4c04-ba98-c5d98403a90c", datos, 5, PONDERACIONES_TEST)

        end_time = time.time()
        elapsed_time_ms = (end_time - start_time) * 1000  
        print(f"Tiempo de ejecución (inicialización de datos): {elapsed_time_ms:.2f} ms")

        start_time = time.time()
        info = data.get_column_value(data.get_participant_info("2ebad15c-c0ef-4c04-ba98-c5d98403a90c"), "id")
        print(info)
        end_time = time.time()
        elapsed_time_ms = (end_time - start_time) * 1000  
        print(f"Tiempo de ejecución (get_Datos): {elapsed_time_ms:.2f} ms")

    except Exception as e:
        print(f"Error: {str(e)}")

