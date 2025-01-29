from transformers import AutoTokenizer, AutoModel
import torch
import sys
import json

# Load the tokenizer and model for sentence embedding
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

def run_model(input_text):
    # Tokenize the input text
    inputs = tokenizer(input_text, return_tensors='pt', truncation=True, padding=True)
    
    # Forward pass through the model
    with torch.no_grad():
        outputs = model(**inputs)

    # Get the embeddings (the last hidden state)
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().tolist()  # Mean pooling to get a single vector
    return embeddings  # You can use the embeddings as needed

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Error: Please provide the input text.")
        sys.exit(1)

    input_text = sys.argv[1]  # Get input text as command-line argument
    
    result = run_model(input_text)  # Run the model
    print(json.dumps({"result": result}))  # Output the result as a JSON
