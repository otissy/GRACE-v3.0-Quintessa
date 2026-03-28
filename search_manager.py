import re
from duckduckgo_search import DDGS
from langchain_community.document_loaders import WebBaseLoader

class SearchManager:
    def __init__(self, max_results=3):
        self.ddgs = DDGS()
        self.max_results = max_results

    def search(self, query):
        """Perform DuckDuckGo search and return summaries."""
        # Prepend 'Google ' to queries as requested for 'grounding' style
        grounding_query = f"Google {query}"
        print(f"Searching: {grounding_query}...")
        
        results = []
        with self.ddgs as ddgs:
            for r in ddgs.text(grounding_query, max_results=self.max_results):
                results.append(f"Source: {r['href']}\nTitle: {r['title']}\nSnippet: {r['body']}\n")
        return results

    def load_url(self, url):
        """Load and parse content from a specific URL."""
        print(f"Loading page: {url}...")
        loader = WebBaseLoader(url)
        # Using lxml or html.parser as configured in the env correctly
        docs = loader.load()
        # Return truncated content for brevity
        return [doc.page_content[:2000] for doc in docs]

    def extract_urls(self, text):
        """Simple URL extraction from text."""
        return re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)

if __name__ == "__main__":
    sm = SearchManager()
    print(sm.search("Who is the 23 year old Quintessa?"))
    # Load example
    # print(sm.load_url("https://example.com"))
