from outfit_engine import OutfitEngine
from ai_recommendations import AIRecommendations
from avatar_engine import Avatar

class OutfitMicrotune:
    def __init__(self, outfit_engine: OutfitEngine, ai_rec: AIRecommendations):
        self.outfit_engine = outfit_engine
        self.ai_rec = ai_rec

    def tune_and_score(self, avatar: Avatar):
        alignment = self.outfit_engine.align_outfit(avatar)
        score = self.outfit_engine.score_outfit(avatar)
        recommended_items = self.ai_rec.recommend_for_user(avatar.user_id, top_n=3)
        return {
            "alignment": alignment,
            "score": score,
            "recommendations": recommended_items
        }
