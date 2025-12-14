from marketplace import Marketplace, Product
from ai_recommendations import AIRecommendations

class SearchRefine:
    def __init__(self, marketplace: Marketplace, ai_rec: AIRecommendations):
        self.marketplace = marketplace
        self.ai_rec = ai_rec

    def search(self, query: str, user_id: int, top_n: int = 5):
        # Placeholder: real AI would use embeddings and micro-tuning
        results = [p for p in self.marketplace.products if query.lower() in p.name.lower()]
        recommendations = self.ai_rec.recommend_for_user(user_id, top_n=top_n)
        return {
            "search_results": results[:top_n],
            "recommendations": recommendations
        }
