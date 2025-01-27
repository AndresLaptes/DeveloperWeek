import pandas as pd
import random as rd
from deap import base, creator, tools, algorithms
from pathlib import Path
from typing import List, Dict



def get_path_csv(filename):
    if not filename.endswith('.csv'):
        filename = f"{filename}.csv"
    
    current_dir = Path(__file__).parent
    csv_dir = current_dir / 'DataSets'
    file_path = csv_dir / filename

    if not file_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {filename}")
    
    return file_path


Ponderaciones = {1,1,1,1,2,3,2,1,3,1,4,1,1,1,2,3,5,2,1}

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

class TeamFormation:
    # Equipos -> todos los equipos disponibles, 1 equipo es una lista de los id de los participantes (lsit(list(String)))
    # id_Usuario -> el usuario que busca equipo
    # X_Equipos -> el número de equipos que hay que buscar
    # Participantes -> los participantes del evento, la BD de usuarios con su info
    def __init__(self, Equipos, id_Usuario, Participantes, X_Equipos):
        self.teams = teams
        self.Equipos = Equipos
        self.id_Usuario = id_Usuario
        self.idParticipantes = Participantes["ID"].astype(str)
        self.X_Equipos = X_Equipos

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


    def crearIndividuo(self) -> tuple:
        creado_por_usuario = False

        # 10% de probabilidad de crear un equipo nuevo
        if rd.random() < 0.1:
            # Crear equipo nuevo con 1-3 miembros aleatorios + usuario objetivo
            otros_usuarios = [
                id for id in self.idParticipantes 
                if id != self.id_Usuario
            ]
            tam_equipo = rd.randint(1, 3)
            team = rd.sample(otros_usuarios, tam_equipo)
            team.append(self.id_Usuario)
            creado_por_usuario = True
            return (team, creado_por_usuario)
    
        equipos_validos = [
            equipo for equipo in self.Equipos 
            if self.id_Usuario not in equipo and len(equipo) >= 1 and len(equipo) < MAX_NUM_PARTNERS
        ] 
    
        # Si no he encontrado ningun equipo valido devuelvo el Usuario que crea su propio equipo y esta el solo
        if not equipos_validos:
            creado_por_usuario = True
            return ([self.id_Usuario], creado_por_usuario)
    
        equipo_elegido = rd.choice(equipos_validos)
        team = list(equipo_elegido)
        team.append(self.id_Usuario)
    
        return (team, creado_por_usuario)
    

    # Tengo que ver todavia como evalua si el equipo es el adecuado, tendre que crear funciones para el calculo
    # Necesito el vector de Preferencias (Exel), ver lo importante o no
    def evaluarEquipo(self, equipo: tuple) -> tuple:
        

        score  = (

        )

        return score,


    def configDeap(self):
        # Funcion que crea a un individuo
        self.toolbox.register("individual", tools.initIterate, creator.Individual, self.crearIndividuo)
        # Funcion que crea a la poblacion
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        # Funcion que evalua al equipo, basicamente el calculador del score o fitness
        self.toolbox.register("evaluate", self.evaluarEquipo)
