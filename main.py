import ollama
import sys
from src.impl_retrieval_func import retrieve_chunks as retrieve
from src.impl_vector_db import LANGUAGE_MODEL, add_chunks_to_vector_db, VECTOR_DB
from src.loading_datasets import dataset

print("Initializing vector database...")
# Populate vector DB from dataset
for i, chunk in enumerate(dataset):
    add_chunks_to_vector_db(chunk.strip())
    if (i + 1) % 10 == 0 or (i + 1) == len(dataset):
        print(f"Progress: {i+1}/{len(dataset)} chunks added.")

print("\n=== RAG System Initialized ===")

while True:
    print("\n" + "=" * 40)
    print("Select an option:")
    print("1. Ask the Chatbot (RAG)")
    print("2. Search Vector Database (Direct)")
    print("3. View Database Statistics")
    print("4. Exit")
    print("=" * 40)
    
    choice = input("Enter choice (1-4): ").strip()
    
    match choice:
        case "1":
            input_query = input('\nAsk me a question: ').strip()
            if not input_query:
                print("Query cannot be empty.")
                continue
                
            print('\nRetrieving context from database...')
            retrieved_knowledge = retrieve(input_query, top_n=3)
            
            print('\nRetrieved knowledge:')
            for chunk, similarity in retrieved_knowledge:
                print(f' - (similarity: {similarity:.2f}) {chunk}')
            
            instruction_prompt = f'''You are a helpful chatbot.
Use only the following pieces of context to answer the question. If the answer is not found in the context, say "I cannot answer this based on the provided files." Don't make up any new information:
{'\n'.join([f' - {chunk}' for chunk, similarity in retrieved_knowledge])}
'''
            
            print('\nGenerating Chatbot response...')
            try:
                stream = ollama.chat(
                    model=LANGUAGE_MODEL,
                    messages=[
                        {'role': 'system', 'content': instruction_prompt},
                        {'role': 'user', 'content': input_query},
                    ],
                    stream=True,
                )
                for chunk in stream:
                    print(chunk['message']['content'], end='', flush=True)
                print()
            except Exception as e:
                print(f"Error generating response: {e}")
                
        case "2":
            search_query = input('\nEnter search terms: ').strip()
            if not search_query:
                print("Search query cannot be empty.")
                continue
                
            print('\nQuerying vector database...')
            retrieved_knowledge = retrieve(search_query, top_n=5)
            
            print('\nTop matching chunks:')
            for i, (chunk, similarity) in enumerate(retrieved_knowledge):
                print(f' {i+1}. (similarity: {similarity:.2f}) {chunk}')
                
        case "3":
            print('\n--- Database Stats ---')
            print(f'Total Chunks Indexed: {len(VECTOR_DB)}')
            print(f'LLM Model: {LANGUAGE_MODEL}')
            
        case "4":
            print('\nExiting RAG system. Goodbye!')
            sys.exit(0)
            
        case _:
            print('\nInvalid option. Please enter a number between 1 and 4.')