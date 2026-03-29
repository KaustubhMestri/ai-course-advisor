import chromadb
from sentence_transformers import SentenceTransformer
import os

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.PersistentClient(path="./chroma_db")

try:
    chroma_client.delete_collection("course_catalog")
except:
    pass
collection = chroma_client.create_collection("course_catalog")

def ingest_file(filepath: str):
    print(f"\n📥 Ingesting: {filepath}")
    
    with open(filepath, 'r') as f:
        text = f.read()
    
    # Chunk by double newline
    chunks = [c.strip() for c in text.split('\n\n') if c.strip()]
    
    for i, chunk in enumerate(chunks):
        chunk_id = f"{os.path.basename(filepath)}_{i}"
        embedding = embedding_model.encode(chunk).tolist()
        
        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[{
                "chunk_id": chunk_id,
                "source_url": f"data/catalog/{os.path.basename(filepath)}",
                "section": os.path.basename(filepath).replace('.txt', '')
            }],
            ids=[chunk_id]
        )
    
    print(f"   ✅ {len(chunks)} chunks stored")

def main():
    data_dir = "data/catalog"
    print("🚀 Starting ingestion...\n")
    
    for filename in os.listdir(data_dir):
        if filename.endswith('.txt'):
            ingest_file(os.path.join(data_dir, filename))
    
    print(f"\n✅ Done! Total chunks: {collection.count()}")

if __name__ == "__main__":
    main()