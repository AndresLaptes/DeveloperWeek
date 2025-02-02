Algoritmo de Formación de Equipos usando Algoritmos Genéticos
Este repositorio contiene una implementación en Python de un algoritmo genético diseñado para formar equipos óptimos basados en factores de compatibilidad como edad, intereses, habilidades técnicas y más. Utiliza el framework DEAP para algoritmos evolutivos y SentenceTransformers para comparar similitudes textuales.

Requisitos Previos
Python 3.7+

Paquetes necesarios:

pandas

numpy

deap

sentence-transformers

Instalación
Clona el repositorio:

bash
Copy
git clone https://github.com/tuusuario/formacion-equipos-genetico.git
cd formacion-equipos-genetico
Instala las dependencias:

bash
Copy
pip install pandas numpy deap sentence-transformers
Preparación de Datos
Prepara un archivo CSV con los datos de los participantes. Debe incluir estas columnas (ejemplo en DataSets/output.csv):

id: Identificador único

age: Edad del participante

university: Universidad

year_of_study: Año de estudio

interests: Intereses (lista como string)

preferred_role: Rol preferido

experience_level: Nivel de experiencia

hackathons_done: Número de hackatones completados

preferred_languages: Idiomas preferidos (lista como string)

friend_registration: Amigos registrados (lista de IDs)

preferred_team_size: Tamaño de equipo preferido

availability: Disponibilidad

programming_skills: Habilidades de programación (diccionario como string)

Columnas de embeddings textuales (ember_obj, ember_intr, ember_excitement)

Coloca tu CSV en el directorio DataSets.

Uso
Modifica el bloque principal del script:

python
Copy
try:
    start_time = time.time()
    path = get_path_csv("tu_archivo")  # Cambia al nombre de tu CSV
    datos = pd.read_csv(path)
    
    # Parámetros: (equipos_existentes, usuario_objetivo, datos, num_equipos, ponderaciones)
    config = TeamFormation(
        equipos_existentes=[], 
        id_Usuario="2ebad15c-c0ef-4c04-a98-c5d98403a90c",
        Participantes=datos,
        X_Equipos=5,
        Ponderaciones=PONDERACIONES_TEST
    )
    config.ejecutar_busqueda_equipos()
    
    end_time = time.time()
    print(f"Tiempo de ejecución: {(end_time - start_time)*1000:.2f} ms")
except Exception as e:
    print("Error:", e)
Parámetros Clave
El constructor TeamFormation recibe:

python
Copy
TeamFormation(equipos_existentes, id_Usuario, Participantes, X_Equipos, Ponderaciones)
equipos_existentes: Lista de equipos preexistentes

id_Usuario: ID del usuario para quien se forman equipos

Participantes: DataFrame con datos de participantes

X_Equipos: Número de equipos óptimos a generar

Ponderaciones: Lista de 15 pesos para factores de compatibilidad:

Similitud de edad

Similitud académica

Compatibilidad universitaria

Intereses comunes

Compatibilidad de roles

Diversidad de experiencia

Experiencia en hackatones

Similitud de objetivos (embeddings)

Similitud de declaración de intereses

Similitud de declaración de motivación

Compatibilidad de idiomas

Conexiones de amistad

Tamaño de equipo preferido

Solapamiento de disponibilidad

Complementariedad de habilidades

Ejemplo de Salida
Copy
Mejores equipos encontrados:

Equipo 1 (Fitness: 0.872):
- 2ebad15c-c0ef-4c04-a98-c5d98403a90c (Usuario objetivo)
- 550e8400-e29b-41d4-a716-446655440000
- 6ba7b810-9dad-11d1-80b4-00c04fd430c8

Equipo 2 (Fitness: 0.845):
- 2ebad15c-c0ef-4c04-a98-c5d98403a90c (Usuario objetivo)
- 6ba7b810-9dad-11d1-80b4-00c04fd430c9

Tiempo de ejecución: 4523.64 ms
Personalización
Ajustar Ponderaciones:

python
Copy
PONDERACIONES_TEST = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]  # Todos los factores con igual peso
Parámetros del Algoritmo:

python
Copy
TAM_POBLACION = 30      # Tamaño de la población
NUM_GENERACIONES = 15   # Número de generaciones
PROB_CRUCE = 0.7        # Probabilidad de cruce
PROB_MUTACION = 0.2     # Probabilidad de mutación
Tamaño de Equipo:

python
Copy
MAX_NUM_PARTNERS = 4    # Máximo de miembros por equipo (incluyendo al usuario)
Notas Importantes
Utiliza caché para evaluaciones repetidas

Compara embeddings textuales con similitud coseno

Procesamiento paralelo para comparaciones textuales

El tiempo de ejecución aumenta con el tamaño del dataset

Los embeddings textuales deben generarse previamente

Para dudas o problemas, abre un issue en el repositorio.