from trend_feed import TrendFeed
from ai_personalization import AIPersonalization
from avatar_engine import Avatar

class TrendScoring:
    def __init__(self, trend_feed: TrendFeed, personalization: AIPersonalization):
        self.trend_feed = trend_feed
        self.personalization = personalization

    def compute_trend_score(self, avatar: Avatar):
        trending_feed = self.trend_feed.get_trending_feed()
        personalized = self.personalization.personalize_for_user(avatar)
        # Placeholder scoring logic
        score = len(trending_feed) * 10 + len(personalized["recommended"]) * 5
        return {
            "avatar_id": avatar.user_id,
            "trend_score": score,
            "personalized_recommendations": personalized
        }
