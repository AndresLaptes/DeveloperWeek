from sentence_transformers import SentenceTransformer, util


def SimilitudTextos(text1, text2) -> float:
    model = SentenceTransformer("all-MiniLM-L6-v2") #tengo que ver versiones

    similarity_score = util.cos_sim(embedding1, embedding2).item()

    # Escalar el puntaje para penalizar diferencias significativas
    # Un rango sugerido es [-1, 1], donde -1 es totalmente opuesto y 1 es idéntico.
    if similarity_score > 0.8:
        return similarity_score  # Objetivos muy similares
    elif similarity_score > 0:
        return similarity_score - 0.2  # Algo diferentes, pequeña penalización
    else:
        return similarity_score - 0.5 # Bastante diferente gran penalizacion

try :
    text1 = ""
    text2 = ""

    similitud = SimilitudTextos(text1, text2)
    print("La similitud entre los dos textos es: ", similitud)

except Exception as e:
    print("A dado el siguiente error", e)