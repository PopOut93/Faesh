from social_stories import SocialStories
from outfit_microtune import OutfitMicrotune
from avatar_engine import Avatar

class TrendFeed:
    def __init__(self, social_stories: SocialStories, microtune: OutfitMicrotune):
        self.social_stories = social_stories
        self.microtune = microtune
        self.trending_outfits = []

    def update_trends(self, avatars: list[Avatar]):
        for avatar in avatars:
            score_info = self.microtune.tune_and_score(avatar)
            if score_info["score"]["score"] > 50:  # placeholder threshold
                self.trending_outfits.append({
                    "avatar_id": avatar.user_id,
                    "recommendations": score_info["recommendations"]
                })
        return self.trending_outfits

    def get_trending_feed(self, limit: int = 10):
        return self.trending_outfits[-limit:]
