# response_middleware.py
import json

class ResponseMiddleware:
    def __init__(self, knowledge_file="knowledge.json"):
        self.knowledge_file = knowledge_file
        self.knowledge = self.load_knowledge()

    def load_knowledge(self):
        try:
            with open(self.knowledge_file, 'r') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError):
            return {}

    def save_knowledge(self):
        with open(self.knowledge_file, 'w') as f:
            json.dump(self.knowledge, f, ensure_ascii=False, indent=4)

    def get_fallback_response(self, user_input):
        if user_input in self.knowledge:
            return self.knowledge[user_input]
        else:
            return "I'm not sure how to respond. Could you teach me?"

    def learn_response(self, user_input, user_feedback):
        # Store user feedback as a response to this input
        self.knowledge[user_input] = user_feedback
        self.save_knowledge()

    def process_feedback(self, user_input, feedback):
        if feedback.get("user_reaction") == "positive":
            # Reinforce the response for similar future queries
            if user_input in self.knowledge:
                self.knowledge[user_input]["strength"] += 1
            else:
                self.learn_response(user_input, feedback.get("suggestion"))
            self.save_knowledge()

response_middleware = ResponseMiddleware()