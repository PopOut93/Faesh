from marketplace import Marketplace, Product
from ai_personalization import AIPersonalization
from trend_feed import TrendFeed
from avatar_engine import Avatar

class MonetizationAI:
    def __init__(self, marketplace: Marketplace, personalization: AIPersonalization, trend_feed: TrendFeed):
        self.marketplace = marketplace
        self.personalization = personalization
        self.trend_feed = trend_feed

    def suggest_purchase(self, avatar: Avatar):
        personalized = self.personalization.personalize_for_user(avatar)
        trending_feed = self.trend_feed.get_trending_feed()
        suggestions = personalized["recommended"] + [t["recommendations"] for t in trending_feed]
        # Flatten and dedupe
        unique_suggestions = {p.name: p for sublist in suggestions for p in (sublist if isinstance(sublist, list) else [sublist])}
        return list(unique_suggestions.values())
