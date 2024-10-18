import weaviate
import uuid
from transformers import pipeline

# Initialize Weaviate client
WEAVIATE_URL = "https://ebn82fawroqbihprgxepiq.c0.asia-southeast1.gcp.weaviate.cloud" 
WEAVIATE_API_KEY = "QymsZXqy8zVZ2tKV5IN1qAyMfJEcqyQdVeTg"

client = weaviate.Client(url=WEAVIATE_URL, auth_client_secret=weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY))

# Define the embedding model
embedder = pipeline("feature-extraction", model="distilbert-base-uncased")

# Function to embed text
def embed_text(text):
    embeddings = embedder(text)
    return embeddings[0][0]  # Return the first layer of the embeddings

# Define the schema for Weaviate
schema = {
    "classes": [{
        "class": "Document",
        "properties": [{
            "name": "text",
            "dataType": ["text"]
        }],
        "vectorizer": "none",  # Use your own vectors, not Weaviate's internal vectorizer
        "vectorIndexType": "hnsw",
        "vectorIndexConfig": {
            "efConstruction": 128,
            "M": 16,
            "distance": "cosine"
        },
        "moduleConfig": {
            "text2vec-huggingface": {
                "model": "distilbert-base-uncased",
                "vectorDimension": 768  # Set to the correct dimension
            }
        }
    }]
}

# Create or update Weaviate schema
def create_schema():
    # Check if the class already exists
    existing_classes = client.schema.get().get("classes")
    class_exists = any(cls["class"] == "Document" for cls in existing_classes)

    if class_exists:
        print("Deleting existing class 'Document'...")
        client.schema.delete_class("Document")  # Delete existing class if it exists

    print("Creating new schema for 'Document' class...")
    client.schema.create(schema)  # Create the updated schema
    print("Schema created successfully.")

# Function to add document to Weaviate
def add_document_to_weaviate(document_text):
    """Add document to Weaviate."""
    # Generate a new UUID
    document_id = str(uuid.uuid4())  # Generate a valid UUID
    # Embed the document text
    embedding = embed_text(document_text)

    # Create the document in Weaviate
    client.data_object.create(
        {
            "text": document_text,
            "_additional": {
                "vector": embedding  # Pass the embedding as part of the object
            }
        },
        class_name="Document",
        uuid=document_id  # Use the generated UUID
    )
    print(f"Document '{document_id}' added to Weaviate.")

# Main function
if __name__ == "__main__":
    create_schema()  # Create or update the schema

    # Example: Add a document
    document_text = "This is an example document text."
    add_document_to_weaviate(document_text)
