try:
    from langchain.chains import create_history_aware_retriever, create_retrieval_chain
    print("langchain.chains import success")
except ImportError as e:
    print(f"langchain.chains import failed: {e}")

try:
    from langchain_community.vectorstores import FAISS
    print("langchain_community.vectorstores import success")
except ImportError as e:
    print(f"langchain_community.vectorstores import failed: {e}")
