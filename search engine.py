# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 05:33:22 2023

@author: micha
"""

import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import defaultdict
import string

# Ensure you have these NLTK resources downloaded in your environment:
# nltk.download('punkt')
# nltk.download('stopwords')

class SearchEngine:
    def __init__(self, documents):
        self.documents = documents
        self.inverted_index = defaultdict(set)
        self.build_index()

    def build_index(self):
        """Build an inverted index from the documents."""
        for doc_id, doc in enumerate(self.documents):
            # Tokenize and remove punctuation
            tokens = word_tokenize(doc.lower())
            # Remove stopwords and punctuation
            tokens = [word for word in tokens if word not in stopwords.words('english') and word not in string.punctuation]
            # Add tokens to the inverted index
            for token in tokens:
                self.inverted_index[token].add(doc_id)

    def search(self, query):
        """Search for a query in the documents, return matching document IDs."""
        # Process the query
        query_tokens = word_tokenize(query.lower())
        query_tokens = [word for word in query_tokens if word not in stopwords.words('english') and word not in string.punctuation]

        # Find document IDs containing all query tokens
        if not query_tokens:
            return []

        # Start with the set of documents containing the first token
        result = self.inverted_index[query_tokens[0]]

        # Intersect with sets of documents containing other tokens
        for token in query_tokens[1:]:
            result = result.intersection(self.inverted_index[token])

        return list(result)

# Sample documents
documents = [
    "The quick brown fox jumps over the lazy dog",
    "Never jump over a lazy dog quickly",
    "Bright vixens jump; dozy fowl quack",
    "Quick wafting zephyrs vex bold Jim"
]

# Create a search engine instance with sample documents
engine = SearchEngine(documents)

# Sample search
search_results = engine.search("quick dog")
print(search_results)
