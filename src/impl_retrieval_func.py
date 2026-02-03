import ollama
from .impl_vector_db import VECTOR_DB, EMBEDDING_MODEL


def cosine_similarity(query_embedding, chunk_embedding):
    dot_product=sum([a*b for a,b in zip(query_embedding, chunk_embedding)])
    norm_query_embedding=sum([a**2 for a in query_embedding])**0.5
    norm_chunk_embedding=sum([b**2 for b in chunk_embedding])**0.5
    return dot_product / (norm_query_embedding * norm_chunk_embedding)


def retrieve_chunks(query, top_n=3):
    query_embedding=ollama.embed(model=EMBEDDING_MODEL, input=query)['embeddings'][0]
    
    similarities = []
    for embedding, chunk in VECTOR_DB:
        similarity = cosine_similarity(query_embedding, embedding)
        similarities.append((chunk, similarity))

    similarities.sort(key=lambda x: x[1], reverse=True)

    return similarities[:top_n]