from transformers import AutoTokenizer, AutoModel
import torch
from pathlib import Path

def export_model_to_onnx(model_name="sentence-transformers/all-MiniLM-L6-v2", output_path="all-MiniLM-L6-v2.onnx"):
    """
    Exporta un modelo de Hugging Face a formato ONNX compatible para uso en JavaScript o entornos optimizados.
    
    Args:
        model_name (str): Nombre o ruta del modelo preentrenado en Hugging Face.
        output_path (str): Ruta donde se guardará el modelo ONNX.
        
    Returns:
        None
    """
    try:
        # Cargar el modelo y el tokenizer
        print(f"Cargando el modelo: {model_name}")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name)
        
        # Crear un directorio para guardar el modelo si no existe
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generar entrada dummy para la exportación
        dummy_input = tokenizer("This is a dummy input", return_tensors="pt")
        input_names = ["input_ids", "attention_mask"]
        output_names = ["output"]

        # Exportar el modelo a ONNX
        print(f"Exportando el modelo a {output_path}...")
        torch.onnx.export(
            model,                                 # El modelo
            args=tuple(dummy_input.values()),     # Entrada de ejemplo
            f=output_path,                        # Ruta de salida
            input_names=input_names,              # Nombres de entrada
            output_names=output_names,            # Nombres de salida
            dynamic_axes={                        # Dimensiones dinámicas para batch
                "input_ids": {0: "batch_size"}, 
                "attention_mask": {0: "batch_size"}
            },
            opset_version=14,                     # Versión de ONNX
            do_constant_folding=True              # Optimización de constantes
        )
        print(f"Modelo exportado exitosamente a {output_path}")

    except Exception as e:
        print(f"Error al exportar el modelo a ONNX: {e}")

# Llamar a la función
export_model_to_onnx()
