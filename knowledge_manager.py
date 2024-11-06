# knowledge_manager.py

import json
from context_manager import get_context, update_context
from utility_functions import load_from_json, save_to_json
from fuzzywuzzy import process  # Assuming you have the fuzzywuzzy library installed
from functools import lru_cache  # For caching

class KnowledgeManager:
    def __init__(self, knowledge_file_path="knowledge_base.json"):
        self.knowledge_base = load_from_json(knowledge_file_path) or {}
        self.knowledge_file_path = knowledge_file_path

    # ---- 1. Hierarchical Knowledge Storage and Retrieval ----
    def get_knowledge(self, topic, subtopic=None):
        """
        Retrieves knowledge on a topic or subtopic.
        Args:
            topic (str): The main topic to look up.
            subtopic (str): Optional, the specific subtopic within the main topic.
        Returns:
            dict or str: Information related to the topic or subtopic, or a default message.
        """
        if subtopic:
            return self.knowledge_base.get(topic, {}).get(subtopic, "No information available on this subtopic.")
        return self.knowledge_base.get(topic, "No information available on this topic.")

    # ---- 2. Updating Knowledge with Hierarchies ----
    def add_or_update_knowledge(self, topic, content, subtopic=None):
        """
        Adds or updates information on a topic or subtopic.
        Args:
            topic (str): The main topic.
            content (str): The information to store.
            subtopic (str): Optional, the specific subtopic within the main topic.
        """
        if subtopic:
            if topic not in self.knowledge_base:
                self.knowledge_base[topic] = {}
            self.knowledge_base[topic][subtopic] = content
        else:
            self.knowledge_base[topic] = content
        self._save_knowledge_base()

    # ---- 3. Caching for Frequently Accessed Knowledge ----
    @lru_cache(maxsize=100)
    def cached_get_knowledge(self, topic, subtopic=None):
        """
        Cached version of get_knowledge for frequently accessed items.
        """
        return self.get_knowledge(topic, subtopic)

    # ---- 4. Fuzzy Matching for Enhanced Searching ----
    def fuzzy_search(self, query, threshold=80):
        """
        Searches for the closest matching topic in the knowledge base.
        Args:
            query (str): The search query.
            threshold (int): The match score threshold for fuzzy matching.
        Returns:
            str: The most relevant topic or a default message.
        """
        topics = list(self.knowledge_base.keys())
        closest_match, score = process.extractOne(query, topics)
        if score >= threshold:
            return self.get_knowledge(closest_match)
        return "No closely matching topic found."

    # ---- 5. Context-Based Recommendations ----
    def suggest_related_topics(self, context_topic, limit=3):
        """
        Suggests topics related to the current topic or context.
        Args:
            context_topic (str): The current topic to suggest from.
            limit (int): The number of suggestions to provide.
        Returns:
            list of str: Suggested related topics.
        """
        # Assuming context_topic has some related entries in knowledge_base, if not, adjust as needed
        related_topics = [key for key in self.knowledge_base if context_topic.lower() in key.lower()]
        return related_topics[:limit] if related_topics else ["No related topics found."]

    # ---- 6. Advanced Query Parsing (Basic NLP) ----
    def query_knowledge(self, query):
        """
        Interprets and answers a knowledge-based query.
        Args:
            query (str): The search query.
        Returns:
            str: The response based on the query.
        """
        # Basic NLP tokenization and keyword detection
        words = query.lower().split()
        if "define" in words or "what is" in words:
            topic = words[-1]  # Naive approach, assumes last word is the topic
            return self.fuzzy_search(topic)
        return "I'm not sure how to interpret that query."

    # ---- Helper Methods ----
    def _save_knowledge_base(self):
        """
        Saves the knowledge base to file.
        """
        save_to_json(self.knowledge_file_path, self.knowledge_base)
    
    def clear_cache(self):
        """
        Clears the cached knowledge retrieval.
        """
        self.cached_get_knowledge.cache_clear()