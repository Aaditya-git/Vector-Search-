from vector_store.qdrant_store import store_documents
from data_processing.markdown_loader import load_and_split_markdown
import os

if __name__ == "__main__":
    md_file_path = r"D:\study-code-repeat\coding\p_hack\faqs_output_total.md"
    
    if not os.path.exists(md_file_path):
        print(f"Error: File not found - {md_file_path}")
        exit(1)

    documents = load_and_split_markdown(md_file_path)

    for doc in documents:
        doc.metadata["source"] = md_file_path
    
    print(f"Loaded {len(documents)} chunks from {md_file_path}")
    

    vector_store = store_documents(documents)
    
    queries = [
        "Does GLI have a library",
        "Does GLI support students with disabilities?",
        "What student organizations exist at GLI?"
    ]
    
    # for query in queries:
    #     print(f"\nQuery: '{query}'")
    #     results = vector_store.similarity_search(query, k=2)
        
    #     for i, doc in enumerate(results):
    #         print(f"\nResult {i+1}:")
    #         print(f"Content: {doc.page_content[:200]}...")
    #         print(f"Source: {doc.metadata['source']}")
    for query in queries:
        print(f"\nQuery: '{query}'")
        results = vector_store.max_marginal_relevance_search(
            query, 
            k=2,
            lambda_mult=0.3 
        )
        
        for i, doc in enumerate(results):
            print(f"\nResult {i+1}:")
            print(f"Content: {doc.page_content[:300]}...")
            print(f"Metadata: {doc.metadata}")