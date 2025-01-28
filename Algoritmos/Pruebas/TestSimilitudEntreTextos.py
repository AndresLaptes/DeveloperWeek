import time
from sentence_transformers import SentenceTransformer, util
from concurrent.futures import ThreadPoolExecutor   

model = SentenceTransformer("paraphrase-MiniLM-L3-v2")

def SimilitudTextos(embedding1, embedding2) -> float:
    return util.cos_sim(embedding1, embedding2).item()

def calculate_multiple_scores_with_parallelism(pairs):

    with ThreadPoolExecutor() as executor:
        scores = list(executor.map(lambda pair: SimilitudTextos(pair[0], pair[1]), pairs))

    return scores


pairs = [
    # Textos con alta similitud
    (
        "I'm thrilled to join this datathon! My goal is to learn, meet amazing people, and have a great time.",
        "I’m super excited to be part of this datathon! My objective is to have fun, make new friends, and learn as much as I can."
    ),
    # Textos con baja similitud
    (
        "My main objective for this datathon is to win. I want to focus all my energy on creating an innovative project.",
        "I’m attending this datathon to have a fun time and relax. For me, it’s all about making connections and enjoying the vibe."
    ),
    # Textos completamente diferentes
    (
        "I love programming in Python and building machine learning models.",
        "Today is a sunny day, and I want to go for a walk in the park."
    )
]

embending = [
    (model.encode(pairs[0][0], convert_to_tensor=True), model.encode(pairs[0][1], convert_to_tensor=True)), 
    (model.encode(pairs[1][0], convert_to_tensor=True), model.encode(pairs[1][1], convert_to_tensor=True)), 
    (model.encode(pairs[2][0], convert_to_tensor=True), model.encode(pairs[2][1], convert_to_tensor=True))
]

try :
    start_time = time.time()
    
    scores = calculate_multiple_scores_with_parallelism(embending)
    print(f"\nSimilarity Scores for All Pairs: {scores}")

    end_time = time.time() 
    elapsed_time_ms = (end_time - start_time) * 1000  
    print(f"Tiempo de ejecución: {elapsed_time_ms:.2f} ms")

except Exception as e:
    print("A dado el siguiente error", e)