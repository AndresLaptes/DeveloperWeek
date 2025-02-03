from pathlib import Path
import pandas as pd
import dask.dataframe as dd
import random as rd
import numpy as np
import time


def get_path(filename : str, tipo : str) -> str:
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
        
        datos = dd.read_json(path)
        end_time = time.time() 

        elapsed_time_ms = (end_time - start_time) * 1000  
        print(f"Tiempo de ejecución: {elapsed_time_ms:.2f} ms")

    except Exception as e:
        print(f"Error: {str(e)}")