import os
import cohere
import weaviate
from sentence_transformers import SentenceTransformer
import uuid

# Load API keys from environment variables for security
COHERE_API_KEY = os.getenv('COHERE_API_KEY', 'KwrW7VXnrnPlx0MXtoKK3s6cptTfcratretmQsj5')  # Replace with your Cohere API key
WEAVIATE_URL = os.getenv('WEAVIATE_URL', 'https://ebn82fawroqbihprgxepiq.c0.asia-southeast1.gcp.weaviate.cloud')  # Replace with your Weaviate URL
WEAVIATE_API_KEY = os.getenv('WEAVIATE_API_KEY', 'QymsZXqy8zVZ2tKV5IN1qAyMfJEcqyQdVeTg')  # Replace with your Weaviate API key

# Initialize Cohere API client
co = cohere.Client(COHERE_API_KEY)

# Initialize Weaviate client
client = weaviate.Client(url=WEAVIATE_URL, auth_client_secret=weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY))

# Define your Weaviate schema if not already defined
schema = {
    "classes": [{
        "class": "Document",
        "properties": [{
            "name": "text",
            "dataType": ["text"]
        }]
    }]
}

# Create the schema if it doesn't exist
if not client.schema.get().get("classes"):
    client.schema.create(schema)

def embed_text(text):
    """Embed text using the Cohere API."""
    response = co.embed(texts=[text])
    return response.embeddings[0]  # Get the embedding for the first (and only) text

def add_document_to_weaviate(document_id, document_text):
    """Add document chunks to Weaviate."""
    chunk_size = 300
    chunks = [document_text[i:i + chunk_size] for i in range(0, len(document_text), chunk_size)]
    
    for i, chunk in enumerate(chunks):
        embedding = embed_text(chunk)
        
        # Create a valid UUID for each chunk
        chunk_id = str(uuid.uuid4())
        
        client.data_object.create(
            {
                "text": chunk
            },
            "Document",
            uuid=chunk_id,  # Use generated UUID for each chunk
            vector=embedding
        )

def retrieve_relevant_chunks(question, top_k=3):
    """Retrieve the most similar chunks from Weaviate based on the question."""
    query_embedding = embed_text(question)
    
    # Include 'certainty' in the query to get the similarity score
    response = client.query.get("Document", ["text"]).with_near_vector({"vector": query_embedding}).with_limit(top_k).with_additional(['certainty']).do()
    
    return response['data']['Get']['Document']

def generate_answer(question, relevant_chunks):
    """Generate an answer to the question based on relevant document chunks."""
    context = " ".join([chunk['text'] for chunk in relevant_chunks])
    prompt = f"Context: {context}\n\nQuestion: {question}\nAnswer:"
    
    response = co.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=150,
        temperature=0.7
    )
    
    return response.generations[0].text.strip()

def qa_pipeline(document_text, question):
    """Run the QA pipeline: add document, retrieve chunks, generate answer."""
    document_id = "doc1"  # You can make this dynamic based on your input
    add_document_to_weaviate(document_id, document_text)
    relevant_chunks = retrieve_relevant_chunks(question)
    answer = generate_answer(question, relevant_chunks)
    return answer
