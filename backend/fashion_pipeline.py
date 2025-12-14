from avatar_engine import Avatar
from outfit_engine import OutfitEngine
from ai_recommendations import AIRecommendations
from outfit_microtune import OutfitMicrotune
from trend_feed import TrendFeed
from ai_personalization import AIPersonalization
from marketplace import Marketplace

class FashionPipeline:
    def __init__(self, avatar_engine, outfit_engine, marketplace: Marketplace):
        self.avatar_engine = avatar_engine
        self.outfit_engine = outfit_engine
        self.marketplace = marketplace
        self.ai_rec = AIRecommendations(marketplace)
        self.microtune = OutfitMicrotune(outfit_engine, self.ai_rec)
        self.social_trend = None
        self.personalization = None

    def attach_trend_feed(self, trend_feed: TrendFeed):
        self.social_trend = trend_feed
        self.personalization = AIPersonalization(self.marketplace, self.ai_rec, trend_feed)

    def process_user(self, avatar: Avatar):
        # Step 1: Align outfit and score
        micro_results = self.microtune.tune_and_score(avatar)

        # Step 2: Update trend feed
        if self.social_trend:
            self.social_trend.update_trends([avatar])

        # Step 3: Generate personalized recommendations
        if self.personalization:
            personalized = self.personalization.personalize_for_user(avatar)
        else:
            personalized = {}

        return {
            "micro_results": micro_results,
            "personalized": personalized
        }
