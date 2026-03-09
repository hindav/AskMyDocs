try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    print("Import successful")
except ImportError as e:
    print(f"Import failed: {e}")
    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        print("Import successful from langchain_text_splitters")
    except ImportError as e2:
        print(f"Import failed from langchain_text_splitters: {e2}")
