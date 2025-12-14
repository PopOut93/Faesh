from outfit_microtune import OutfitMicrotune
from search_refine import SearchRefine
from ai_recommendations import AIRecommendations

class AIMicroTune:
    def __init__(self, microtune: OutfitMicrotune, search_refine: SearchRefine, ai_rec: AIRecommendations):
        self.microtune = microtune
        self.search_refine = search_refine
        self.ai_rec = ai_rec

    def fine_tune_outfit(self, user_id: int, avatar, query: str):
        # Step 1: Tune outfit
        micro_results = self.microtune.tune_and_score(avatar)

        # Step 2: Refine search results
        search_results = self.search_refine.search(query, user_id)

        # Step 3: Combine with AI recommendations
        recommendations = self.ai_rec.recommend_for_user(user_id, top_n=3)

        return {
            "micro_results": micro_results,
            "search_results": search_results,
            "recommendations": recommendations
        }
