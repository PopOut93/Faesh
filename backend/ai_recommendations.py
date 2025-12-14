from marketplace import Marketplace, Product

class AIRecommendations:
    def __init__(self, marketplace: Marketplace):
        self.marketplace = marketplace

    def recommend_for_user(self, user_id: int, top_n: int = 5):
        # Placeholder: In real AI, use user data and preferences
        recommended = self.marketplace.products[-top_n:]
        return [f"Recommended for user {user_id}: {p.brand} {p.name}" for p in recommended]
