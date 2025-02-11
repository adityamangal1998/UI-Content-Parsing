from sentence_transformers import CrossEncoder, SentenceTransformer
import chromadb
import config

# Initialize ChromaDB client and collection
chroma_client = chromadb.PersistentClient(path=config.CHROMA_DB_PATH)
collection = chroma_client.get_or_create_collection(config.CHROMA_COLLECTION_NAME)

# Load cross-encoder for re-ranking
cross_encoder = CrossEncoder(config.CROSS_ENCODER_MODEL)
embedding_model = SentenceTransformer(config.EMBEDDING_MODEL)

def chunk_text(text, chunk_size=500, overlap=50):
    """Splits text into overlapping chunks to improve retrieval."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def store_in_vectordb(url, content):
    """Stores scraped content as chunks in ChromaDB with metadata."""
    chunks = chunk_text(content)
    for i, chunk in enumerate(chunks):
        embedding = embedding_model.encode(chunk).tolist()
        doc_id = f"{url}_chunk_{i}"  # Unique ID for each chunk
        metadata = {"url": url}  # Store URL in metadata to enable filtering
        collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[metadata]
        )
    print(f"Stored {len(chunks)} chunks from {url} in VectorDB")

def query_vectordb(query, urls, top_k=5, threshold=0.05):
    """Queries the vector database, filters by URLs if provided, then re-ranks results with thresholding."""
    print(f"urls : {urls}")
    print(f"Total documents in collection: {collection.count()}")

    query_embedding = embedding_model.encode(query).tolist()
    metadata_key = "url"
    filter_condition = None
    if urls:
        if isinstance(urls, str):
            urls = [urls]  # Ensure urls is a list
        filter_condition = {metadata_key: {"$in": urls}}  # Metadata filtering

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where=filter_condition
    )

    if not results['documents'][0]:
        print("No results found. Trying without filter...")
        return ""

    # Extract documents and scores for re-ranking
    doc_texts = results["documents"][0]
    doc_scores = results["distances"][0]  # Lower is better in ChromaDB (cosine similarity)

    # Pair query with each document for cross-encoder ranking
    pairs = [(query, doc) for doc in doc_texts]

    # Re-rank using cross-encoder
    rerank_scores = cross_encoder.predict(pairs)

    # Sort documents based on re-rank scores (higher is better for cross-encoder)
    reranked_results = sorted(zip(doc_texts, rerank_scores), key=lambda x: x[1], reverse=True)

    # Get the highest-ranked document and its score
    best_doc, best_score = reranked_results[0]

    # Apply thresholding
    if abs(best_score) < threshold:
        print(f"No document meets the threshold ({threshold}). Returning empty result.")
        return ""

    return best_doc