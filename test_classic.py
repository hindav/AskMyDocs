try:
    from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
    print("Import langchain_classic.chains success")
except ImportError as e:
    print(f"Import langchain_classic.chains failed: {e}")
