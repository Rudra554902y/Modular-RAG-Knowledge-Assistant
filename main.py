from src.search import RAGSearch

def main():
    rag_search = RAGSearch()
    while True:
        query = input("Enter your query: ").strip()
        if not query:
            break
        print()
        summary = rag_search.search_and_summarize(query=query,top_k=3)+"\n"
        print("Summary:\n\n",summary)


if __name__ == "__main__":
    main()
