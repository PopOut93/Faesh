from marketplace import Marketplace, Product
from ai_recommendations import AIRecommendations
from trend_feed import TrendFeed
from avatar_engine import Avatar

class AIPersonalization:
    def __init__(self, marketplace: Marketplace, ai_rec: AIRecommendations, trend_feed: TrendFeed):
        self.marketplace = marketplace
        self.ai_rec = ai_rec
        self.trend_feed = trend_feed

    def personalize_for_user(self, avatar: Avatar):
        recommended = self.ai_rec.recommend_for_user(avatar.user_id, top_n=5)
        trending = self.trend_feed.get_trending_feed(limit=5)
        return {
            "recommended": recommended,
            "trending": trending
        }
